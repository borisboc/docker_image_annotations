#!/usr/bin/env python3
# config_manager.py
import argparse
import subprocess
import os
from pathlib import Path
import re

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
        matches = re.findall(r'profiles:\s*\[([^\]]+)\]', content)
        for match in matches:
            for profile in match.split(','):
                profiles.add(profile.strip().strip('"\''))
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
            subprocess.run(["docker", "container", "rm", container], 
                          capture_output=True, check=False)
            print(f"Container {container} removed (if it existed)")
        except Exception as e:
            print(f"Warning: Could not remove container {container}: {e}")

def run_configuration(profile, compose_file, project_name, extra_env=None, extra_args=None):
    """
    Run the specified configuration
    
    Args:
        profile (str): Profile to use (cpu or gpu)
        compose_file (str): Docker-compose file to use
        project_name (str): Docker project name
        extra_env (dict): Additional environment variables
        extra_args (list): Additional arguments to append to the docker compose command
    """
    # Containers to clean up before starting
    containers_to_clean = [
        "img-annotations-sa2-label-studio",
        "img-annotations-fiftyone",
        "img-annotations-label-studio",
        "img-annotations-mongodb"
    ]
    
    print(f"Cleaning up containers...")
    cleanup_containers(containers_to_clean)
    
    # Set environment variables
    env = os.environ.copy()
    if extra_env:
        env.update(extra_env)
    
    # Set the build profile environment variable
    env['IMG_ANNOTATIONS_BUILD_PROFILE'] = profile
    
    # Build docker compose command
    cmd = [
        'docker', 'compose',
        '-f', compose_file,
        '--profile', profile,
        '-p', project_name,
        'up'
    ]
    
    # Add extra arguments if provided
    if extra_args:
        cmd.extend(extra_args)
    
    print(f"Starting with profile '{profile}' using {compose_file}")
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
    parser = argparse.ArgumentParser(description="Docker Configuration Manager")
    
    # Profile selection
    parser.add_argument('--profile', '-p', 
                       choices=['cpu', 'gpu'], 
                       default='cpu',
                       help='Profile to use (cpu or gpu)')
    
    # Compose file selection
    parser.add_argument('--compose-file', '-f',
                       default='compose_local_files.yaml',
                       help='Docker-compose file to use')
    
    # Project name
    parser.add_argument('--project', '-n',
                       default='image_annotations',
                       help='Docker project name')
    
    # List available profiles
    parser.add_argument('--list-profiles', '-l',
                       action='store_true',
                       help='List available profiles in the compose file')
    
    # Additional environment variables
    parser.add_argument('--env-var', '-e',
                       action='append',
                       metavar='KEY=VALUE',
                       help='Additional environment variables')
    
    # Additional docker compose arguments
    parser.add_argument('--extra-args', '-a',
                       nargs=argparse.REMAINDER,
                       help='Additional arguments to pass to docker compose (everything after -- will be passed through)')
    
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
            if '=' in env_var:
                key, value = env_var.split('=', 1)
                extra_env[key] = value
    
    # Get extra arguments
    extra_args = args.extra_args if args.extra_args else []
    
    # Run the selected configuration
    run_configuration(args.profile, args.compose_file, args.project, extra_env, extra_args)

if __name__ == '__main__':
    main()
