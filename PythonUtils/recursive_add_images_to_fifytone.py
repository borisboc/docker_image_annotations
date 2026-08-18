import argparse
from pathlib import Path

import fiftyone as fo

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""Add images to fiftyone dataset. It supports glob patterns.
        This is an alternative to function `from_images_patt` does not perform a fully recursive (with subfolders),
        even with patterns such as `/home/local_images/MySubfolder/**/*.png`""",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "dataset_name",
        type=str,
        help="The name of the FiftyOne dataset",
    )
    parser.add_argument(
        "folder",
        type=Path,
        help="Trunk folder of the images to be added",
    )
    parser.add_argument(
        "glob_pat",
        type=str,
        help="Glob pattern to find the images. For instance '/**/*.png'",
    )

    args = parser.parse_args()

    folder: Path = args.folder

    image_files_str = [str(p) for p in list(folder.rglob(args.glob_pat))]
    print(f"Found {len(image_files_str)} image file paths")

    if len(image_files_str) > 0:
        if not fo.dataset_exists(args.dataset_name):
            dataset = fo.Dataset.from_images(
                image_files_str, name=args.dataset_name, persistent=True, progress=True
            )
        else:
            dataset = fo.load_dataset(args.dataset_name)
            dataset.persistent = True
            samples = [fo.Sample(filepath=f) for f in image_files_str]
            dataset.add_samples(samples, progress=True)
