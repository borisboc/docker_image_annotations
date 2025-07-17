import fiftyone as fo
import tempfile
from pathlib import Path
import sys
import py7zr
import shutil
import argparse


def export_fiftyone_dataset(
    dataset_name: str, rel_dir: str = None, export_dir: Path = None
):

    if export_dir is None:
        export_dir = (
            Path(tempfile.gettempdir())
            .joinpath("fiftyone_exports")
            .joinpath(dataset_name)
        )

    if export_dir.exists():
        raise Exception(
            f"{export_dir} already exist ! Please remove it if you want to execute this script"
        )

    print("Exporting dataset to folder ", export_dir)

    archive_fp = export_dir.parent.joinpath(export_dir.name + ".7z")

    if archive_fp.exists():
        raise Exception(
            f"{archive_fp} already exist ! Please remove it if you want to execute this script"
        )

    dataset = fo.load_dataset(dataset_name)

    # Export the dataset without copying the media files
    dataset.export(
        export_dir=str(export_dir),
        dataset_type=fo.types.FiftyOneDataset,
        export_media=False,
        rel_dir=rel_dir,
    )

    print("Compressing folder to file ", archive_fp)

    with py7zr.SevenZipFile(archive_fp, "w") as z:
        z.writeall(export_dir, arcname=archive_fp.stem)

    print("Deleting (uncompressed) folder ", export_dir)

    shutil.rmtree(export_dir, True)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Export a fiftyone dataset to a folder, using the fiftyone formats (see o.types.FiftyOneDataset)"
    )
    parser.add_argument(
        "dataset_name",
        type=str,
        help="The name of the dataset to export",
    )
    parser.add_argument(
        "-r",
        "--rel-dir",
        type=str,
        default=None,
        help="The relative path to folder containing the images. See FiftyOneDataset export documentation.",
    )
    parser.add_argument(
        "-e",
        "--export-dir",
        type=Path,
        default=None,
        help="The path where to export the dataset. If none, then using TempDir/fiftyone_exports",
    )
    args = parser.parse_args()

    export_fiftyone_dataset(args.dataset_name, args.rel_dir, args.export_dir)
