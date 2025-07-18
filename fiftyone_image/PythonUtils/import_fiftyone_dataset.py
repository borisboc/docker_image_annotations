import fiftyone as fo
import tempfile
from pathlib import Path
import sys
import py7zr
import shutil
import argparse


def import_fiftyone_dataset(
    dataset_name: str,
    dataset_dir_or_7z: Path,
    rel_dir: str = None,
):

    if not dataset_dir_or_7z.exists():
        raise Exception(f"{dataset_dir_or_7z} does not exist !")

    if dataset_dir_or_7z.is_file():
        print(f"Extracting archive {dataset_dir_or_7z}")
        with py7zr.SevenZipFile(dataset_dir_or_7z, "r") as zip:
            dir_name = zip.files.files_list[0]["filename"]
            dataset_dir = dataset_dir_or_7z.parent.joinpath(dir_name)
            if dataset_dir.exists():
                raise Exception(
                    f"Extraction target dir {dataset_dir} already exists (you may remove it first) !"
                )
            zip.extractall(path=dataset_dir_or_7z.parent)
    else:
        dataset_dir = dataset_dir_or_7z

    print("Importing dataset from folder ", dataset_dir)

    # Import dataset, prepending `rel_dir` to each media path
    dataset = fo.Dataset.from_dir(
        dataset_dir=dataset_dir,
        dataset_type=fo.types.FiftyOneDataset,
        rel_dir=rel_dir,
        name=dataset_name,
    )


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Import a fiftyone dataset to from a folder or 7z archive, using the fiftyone formats (see o.types.FiftyOneDataset)"
    )
    parser.add_argument(
        "dataset_name",
        type=str,
        help="The name of the dataset to import",
    )
    parser.add_argument(
        "dataset_dir_or_7z",
        type=Path,
        help="The path to the folder or 7z archive to be imported",
    )
    parser.add_argument(
        "-r",
        "--rel-dir",
        type=str,
        default=None,
        help="The relative path to folder containing the images. See FiftyOneDataset import documentation.",
    )

    args = parser.parse_args()

    import_fiftyone_dataset(args.dataset_name, args.dataset_dir_or_7z, args.rel_dir)
