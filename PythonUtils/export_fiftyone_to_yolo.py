import fiftyone as fo
from fiftyone import ViewField as F
from pathlib import Path
from typing import Optional


def export_fiftyone_dataset_to_yolov5(
    dataset_name: str,
    label_field: str,
    splits: Optional[list[str]] = None,
    export_dir: Path = None,
    export_media: str = "symlink",
    classes: Optional[list[str]] = None,
):

    if export_dir is None:
        export_dir = (
            Path(tempfile.gettempdir())
            .joinpath("fiftyone_exports_yolov5")
            .joinpath(dataset_name)
        )

    if export_dir.exists():
        raise Exception(
            f"{export_dir} already exist ! Please remove it if you want to execute this script"
        )

    print(
        f"Exporting dataset {dataset_name} with splits {splits} as YOLO format into to folder {export_dir}"
    )

    dataset = fo.load_dataset(dataset_name)

    if not dataset.has_sample_field(label_field):
        raise Exception(
            f"Error : dataset {dataset_name} does not have label_field {label_field}"
        )

    field = dataset.get_field(label_field)
    dt = field.document_type
    if dt is fo.core.labels.Detections:
        subfield_name = "detections"
    elif dt is fo.core.labels.Polylines:
        subfield_name = "polylines"
    else:
        raise Exception(
            f"Error : export to YoloV5 only works for Detections and Polylines, but label_field {label_field} is {dt}"
        )

    if classes is None:
        classes = dataset.distinct(F(f"{label_field}.{subfield_name}.label"))

    if splits and len(splits) > 0:
        # Export the splits
        for split in splits:

            split_view = dataset.match_tags(split)

            split_view.export(
                export_dir=str(export_dir.absolute()),
                dataset_type=fo.types.YOLOv5Dataset,
                label_field=label_field,
                split=split,
                export_media=export_media,
                classes=classes,
            )
    else:
        # Export the dataset (without split)
        dataset.export(
            export_dir=str(export_dir.absolute()),
            dataset_type=fo.types.YOLOv5Dataset,
            label_field=label_field,
            export_media=export_media,
            classes=classes,
        )


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(
        description="Export and convert a fiftyone dataset into a YOLOV5 dataset (see fiftyone.types.YOLOv5Dataset)"
    )
    parser.add_argument(
        "dataset_name",
        type=str,
        help="The name of the dataset to export and convert",
    )
    parser.add_argument(
        "label_field",
        type=str,
        help="The name of the label field (e.g. detection annotations) that will be exported",
    )
    parser.add_argument(
        "-e",
        "--export-dir",
        type=Path,
        default=None,
        help="The path where to export the dataset. If none, then using TempDir/fiftyone_exports_yolov5",
    )
    parser.add_argument(
        "-s",
        "--splits",
        type=str,
        nargs="+",
        default=[],
        help="The names of the splits to be exported, if specified. Split name must be a sample tag.",
    )
    parser.add_argument(
        "-em",
        "--export-media",
        default="symlink",
        choices=[True, False, "move", "symlink", "manifest"],
        help="controls how to export the raw media.",
    )
    args = parser.parse_args()

    export_fiftyone_dataset_to_yolov5(
        dataset_name=args.dataset_name,
        label_field=args.label_field,
        splits=args.splits,
        export_dir=args.export_dir,
    )
