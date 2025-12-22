#!/usr/bin/env python3
# config_manager.py
import argparse
import subprocess
import os
from pathlib import Path
import re
from typing import Optional


def get_available_profiles(compose_file):
    """
    Extract available profiles from the compose file

    Args:
        compose_file (str): Path to the docker-compose file

    Returns:
        list: List of available profiles
    """
    profiles = set()
    try:
        content = Path(compose_file).read_text()
        # Find profiles in the compose file
        matches = re.findall(r"profiles:\s*\[([^\]]+)\]", content)
        for match in matches:
            for profile in match.split(","):
                profiles.add(profile.strip().strip("\"'"))
    except Exception as e:
        print(f"Warning: Could not read profiles from {compose_file}: {e}")
    return list(profiles)


def cleanup_containers(container_names):
    """
    Remove existing containers

    Args:
        container_names (list): List of container names to remove
    """
    for container in container_names:
        try:
            subprocess.run(
                ["docker", "container", "rm", container],
                capture_output=True,
                check=False,
            )
            print(f"Container {container} removed (if it existed)")
        except Exception as e:
            print(f"Warning: Could not remove container {container}: {e}")


def run_configuration(
    profile: list[str],
    build_profile: str,
    compose_file: str,
    project_name: str,
    extra_env: Optional[dict] = None,
    extra_args: Optional[list] = None,
):
    """
    Run the specified configuration

    Args:
        profile (list[str]): Profile to use (cpu or gpu)
        build_profile (str): The build profile (either cpu or gpu) passed for building containers (fiftyone in particular)
        compose_file (str): Docker-compose file to use
        project_name (str): Docker project name
        extra_env (dict): Additional environment variables
        extra_args (list): Additional arguments to append to the docker compose command
    """
    # Containers to clean up before starting
    containers_to_clean = [
        "img-ann-sa2-label-studio",
        "img-ann-fiftyone",
        "img-ann-label-studio",
        "img-ann-mongodb",
    ]

    print(f"Cleaning up containers...")
    cleanup_containers(containers_to_clean)

    # Set environment variables
    env = os.environ.copy()
    if extra_env:
        env.update(extra_env)

    # Set the build profile environment variable
    print(f"Using build profile : {build_profile}")
    env["IMG_ANNOTATIONS_BUILD_PROFILE"] = build_profile

    if type(profile) is list:
        profiles_list = []
        for prf in profile:
            # creating a list looking like --profile gpu --profile mongodb  etc.
            profiles_list += ["--profile", prf]
    else:
        profiles_list = ["--profile", profile]

    # Build docker compose command
    cmd = (
        [
            "docker",
            "compose",
            "-f",
            compose_file,
        ]
        + profiles_list
        + [
            "-p",
            project_name,
            "up",
        ]
    )

    # Add extra arguments if provided
    if extra_args:
        cmd.extend(extra_args)

    print(f"Starting with profile(s) '{profile}' using {compose_file}")
    print(f"Command: {' '.join(cmd)}")

    try:
        # Run the docker compose command
        subprocess.run(cmd, env=env)
    except KeyboardInterrupt:
        print("\nStop requested by user")
    except Exception as e:
        print(f"Error during startup: {e}")


def main():
    """Main function to parse arguments and run configuration"""
    parser = argparse.ArgumentParser(
        description="Docker Configuration Manager",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    # Profile selection
    parser.add_argument(
        "--profile",
        "-p",
        choices=[
            "cpu",
            "gpu",
            "mongodb",
            "cpu-fiftyone",
            "gpu-fiftyone",
            "cpu-sa2-label-studio",
            "gpu-sa2-label-studio",
            "label-studio",
        ],
        default=["cpu"],
        nargs="+",
        help="Profile(s) to use (cpu, gpu, etc.). It is a list : you can concatenate several profile to create your own custom network of containers",
    )
    parser.add_argument(
        "--build-profile",
        "-bp",
        choices=["cpu", "gpu"],
        default=None,
        type=Optional[str],
        help="The build profile : cpu or gpu. If None, then it will be infered from the string(s) inside --profile argument",
    )

    # Compose file selection
    parser.add_argument(
        "--compose-file",
        "-f",
        default="compose_local_files.yaml",
        help="Docker-compose file to use",
    )

    # Project name
    parser.add_argument(
        "--project", "-n", default="img-ann", help="Docker project name"
    )

    # List available profiles
    parser.add_argument(
        "--list-profiles",
        "-l",
        action="store_true",
        help="List available profiles in the compose file",
    )

    # Additional environment variables
    parser.add_argument(
        "--env-var",
        "-e",
        action="append",
        metavar="KEY=VALUE",
        help="Additional environment variables",
    )

    # Additional docker compose arguments
    parser.add_argument(
        "--extra-args",
        "-a",
        nargs=argparse.REMAINDER,
        help="Additional arguments to pass to docker compose (everything after -- will be passed through)",
    )

    args = parser.parse_args()

    # List profiles if requested
    if args.list_profiles:
        profiles = get_available_profiles(args.compose_file)
        print("Available profiles:")
        for profile in profiles:
            print(f"  - {profile}")
        return

    # Parse additional environment variables
    extra_env = {}
    if args.env_var:
        for env_var in args.env_var:
            if "=" in env_var:
                key, value = env_var.split("=", 1)
                extra_env[key] = value

    # Get extra arguments
    extra_args = args.extra_args if args.extra_args else []

    # Run the selected configuration
    if args.build_profile:
        build_profile = args.build_profile
    else:
        if "gpu" in args.profile or "gpu-fiftyone" in args.profile:
            build_profile = "gpu"
        else:
            build_profile = "cpu"

    run_configuration(
        args.profile,
        build_profile,
        args.compose_file,
        args.project,
        extra_env,
        extra_args,
    )


if __name__ == "__main__":
    main()
