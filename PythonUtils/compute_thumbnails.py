import fiftyone as fo
import fiftyone.utils.image as foui
from fiftyone import ViewField as F
from pathlib import Path
import argparse


def compute_thumbnails(
    dataset_name: str,
    output_dir_for_thumbnails: Path,
    rel_dir: str = None,
    skip_if_has_thumbnail: bool = True,
    size=(-1, 128),
    ext=".jpg",
    num_workers=None,
    progress=True,
):
    # source : https://voxel51.com/blog/fiftyone-computer-vision-tips-and-tricks-may-19-2023#f3156044d03a

    dataset = fo.load_dataset(dataset_name)

    if skip_if_has_thumbnail:
        subds = dataset.match(~F("thumbnail_path"))
    else:
        subds = dataset

    print(
        f"About to generate {len(subds)} thumbnails to folder {output_dir_for_thumbnails}"
    )

    foui.transform_images(
        subds,
        size=size,
        output_field="thumbnail_path",
        output_dir=output_dir_for_thumbnails,
        rel_dir=rel_dir,
        ext=ext,
        num_workers=num_workers,
        progress=progress,
    )

    # Modify the dataset's App config
    subds.app_config.media_fields = ["filepath", "thumbnail_path"]
    subds.app_config.grid_media_field = "thumbnail_path"
    subds.save()  # must save after edits

    print(f"Generated {len(subds)} thumbnails to folder {output_dir_for_thumbnails}")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Precompute thumbnails of the images of a dataset. And save thumbnails to an output directory. "
        "Take care of rel-dir if you want the same sub-folder architecture inside the output directory"
    )
    parser.add_argument(
        "dataset_name",
        type=str,
        help="The name of the dataset to import",
    )
    parser.add_argument(
        "output_dir_for_thumbnails",
        type=Path,
        help="The path where the thumbnails will be saved to",
    )
    parser.add_argument(
        "-r",
        "--rel-dir",
        type=str,
        default=None,
        help="The relative path to folder containing the images. See FiftyOneDataset import documentation.",
    )
    parser.add_argument(
        "--skip-already",
        action="store_true",
        help="True : select samples which DON'T have 'thumbnail_path' attribute.",
    )
    parser.add_argument(
        "--no-skip-already",
        dest="skip_already",
        action="store_false",
        help="All samples will be processed (and 'thumbnail_path' will be overwritten)",
    )
    parser.set_defaults(skip_already=True)
    parser.add_argument(
        "--size",
        type=int,
        nargs="+",
        default=(-1, 128),
        help="Size of the thumbnail. Put -1 to one dimension if you want to keep ratio",
    )
    parser.add_argument(
        "--ext",
        type=str,
        default=".jpg",
        help="Extension / file format of the thumbnail.",
    )
    parser.add_argument(
        "--num-workers",
        type=int,
        default=None,
        help="A suggested number of worker processes to use.",
    )
    parser.add_argument(
        "--progress",
        type=bool,
        default=True,
        help=" whether to render a progress bar (True/False).",
    )

    args = parser.parse_args()

    compute_thumbnails(
        args.dataset_name,
        args.output_dir_for_thumbnails,
        args.rel_dir,
        args.skip_already,
        args.size,
        args.ext,
        args.num_workers,
        args.progress,
    )
