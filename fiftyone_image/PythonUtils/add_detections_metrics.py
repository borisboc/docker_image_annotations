import fiftyone as fo
from fiftyone import ViewField as F
import argparse


def parse_args():
    parser = argparse.ArgumentParser(
        description="""Computes and add bounding boxes metrics (such as width, height, positions/distances) in relative or absolute (pixel) values/coordinates."""
    )
    parser.add_argument(
        help="Name of the dataset",
        type=str,
        default="MY_DATASET_NAME",
        dest="dataset_name",
    )
    parser.add_argument(
        help="Name of the field of the detections",
        type=str,
        default="MY_DETECTION_FIELD_NAME",
        dest="detection_field_name",
    )
    parser.add_argument(
        "-no-rel",
        "--no-relative-values",
        action="store_false",
        dest="relative_values",
        default=True,
        help="relative values/coordinates will NOT be computed",
    )
    parser.add_argument(
        "-no-px",
        "--no-px-values",
        action="store_false",
        dest="px_values",
        default=True,
        help="absolute (pixel) values/coordinates will NOT be computed",
    )

    args = parser.parse_args()
    return args


def _compute_add_bbox_metrics(
    dataset: fo.core.dataset.Dataset,
    view: fo.core.view.DatasetView,
    detection_field_name: str,
    width_scale: list[float, fo.ViewField],
    height_scale: list[float, fo.ViewField],
    additionnal_metric_name: str,
    additionnal_info_name: str,
    field_type: list[fo.FloatField, fo.IntField],
):
    """Compute the metrics based on bounding_box and width/height (if available)
    REMARK : this is currently slow on very large datasets (e.g. 100 000 samples). BB20250801

    Args:
        dataset (fo.core.dataset.Dataset): full dataset
        view (fo.core.view.DatasetView): view with the samples
        detection_field_name (str): the name of the field with the detections
        width_scale (list[float, fo.ViewField]): either pass 1.0 (for relative metrics) or pass F("$metadata.width") (for absolute / px metrics)")
        height_scale (list[float, fo.ViewField]): either pass 1.0 (for relative metrics) or pass F("$metadata.height") (for absolute / px metrics)")
        additionnal_metric_name (str): will be added on the metric name (e.g. "bbox_height" + additionnal_metric_name). You may pass "_rel" or "_px".
        additionnal_info_name (str): will be added on the field info. You may pass "Relative bounding box " or "Absolute (in pixels) bounding box ".
        field_type (list[fo.FloatField, fo.IntField]): either fo.FloatField for relative metrics, or fo.IntField for absolute (pixel) metrics.
    """

    bbox_width = view.values(
        F(f"{detection_field_name}.detections.bounding_box")[2] * width_scale
    )
    bbox_center_col = view.values(
        (
            F(f"{detection_field_name}.detections.bounding_box")[0]
            + F(f"{detection_field_name}.detections.bounding_box")[2] * 0.5
        )
        * width_scale
    )

    # useful to check if bounding box is touching / very close to left border of image
    bbox_dist_left = view.values(
        F(f"{detection_field_name}.detections.bounding_box")[0] * width_scale
    )

    # useful to check if bounding box is touching / very close to right border of image
    bbox_dist_right = view.values(
        width_scale
        * (
            1.0
            - (
                F(f"{detection_field_name}.detections.bounding_box")[0]
                + F(f"{detection_field_name}.detections.bounding_box")[2]
            )
        )
    )

    bbox_height = view.values(
        F(f"{detection_field_name}.detections.bounding_box")[3] * height_scale
    )
    bbox_center_row = view.values(
        (
            F(f"{detection_field_name}.detections.bounding_box")[1]
            + F(f"{detection_field_name}.detections.bounding_box")[3] * 0.5
        )
        * height_scale
    )

    # useful to check if bounding box is touching / very close to top border of image
    bbox_dist_top = view.values(
        F(f"{detection_field_name}.detections.bounding_box")[1] * height_scale
    )

    # useful to check if bounding box is touching / very close to bottom border of image
    bbox_dist_bottom = view.values(
        height_scale
        * (
            1.0
            - (
                F(f"{detection_field_name}.detections.bounding_box")[1]
                + F(f"{detection_field_name}.detections.bounding_box")[3]
            )
        )
    )

    bbox_area = view.values(
        F(f"{detection_field_name}.detections.bounding_box")[2]
        * F(f"{detection_field_name}.detections.bounding_box")[3]
        * width_scale
        * height_scale
    )

    bbox_height_str = "bbox_height" + additionnal_metric_name
    bbox_width_str = "bbox_width" + additionnal_metric_name
    bbox_area_str = "bbox_area" + additionnal_metric_name
    bbox_center_row_str = "bbox_center_row" + additionnal_metric_name
    bbox_center_col_str = "bbox_center_col" + additionnal_metric_name
    bbox_dist_top_str = "bbox_dist_top" + additionnal_metric_name
    bbox_dist_left_str = "bbox_dist_left" + additionnal_metric_name
    bbox_dist_bottom_str = "bbox_dist_bottom" + additionnal_metric_name
    bbox_dist_right_str = "bbox_dist_right" + additionnal_metric_name

    bbox_names = [
        bbox_height_str,
        bbox_width_str,
        bbox_area_str,
        bbox_center_row_str,
        bbox_center_col_str,
        bbox_dist_top_str,
        bbox_dist_left_str,
        bbox_dist_bottom_str,
        bbox_dist_right_str,
    ]

    bbox_infos = [
        additionnal_info_name + i
        for i in [
            "height",
            "width",
            "area",
            "center row",
            "center column",
            "distance with top border of image",
            "distance with left border of image",
            "distance with bottom border of image",
            "distance with right border of image",
        ]
    ]

    values = [
        bbox_height,
        bbox_width,
        bbox_area,
        bbox_center_row,
        bbox_center_col,
        bbox_dist_top,
        bbox_dist_left,
        bbox_dist_bottom,
        bbox_dist_right,
    ]
    for n, i, v in zip(bbox_names, bbox_infos, values):
        full_field_name = f"{detection_field_name}.detections.{n}"
        dataset.add_sample_field(
            full_field_name,
            field_type,
            description=i,
        )
        view.set_values(full_field_name, v)

    view.save()


def add_detections_AABB_metrics(
    dataset: fo.core.dataset.Dataset,
    view: fo.core.view.DatasetView,
    detection_field_name: str,
    add_relative_metrics: bool = True,
    add_px_metrics: bool = True,
):
    """Add the number of detections (in "num_detections") per samples. And compute the bounding boxes metrics

    Args:
        dataset (fo.core.dataset.Dataset): full dataset
        view (fo.core.view.DatasetView): view with the samples
        detection_field_name (str): the name of the field with the detections
        add_relative_metrics (bool, optional): If true relative bbox metrics (in float) will be computed. Defaults to True.
        add_px_metrics (bool, optional): If true absolute (pixel) bbox metrics (in int) will be computed. Defaults to True.
    """

    # Adding the number of detections, for each samples
    num_detections_str = "num_detections"

    field_num_detections = f"{detection_field_name}.{num_detections_str}"

    if not dataset.has_sample_field(field_num_detections):
        dataset.add_sample_field(
            field_num_detections,
            fo.IntField,
            description="Number of detections in the sample",
        )
        dataset.save()

    num_detects = view.values(F(f"{detection_field_name}.detections").length())

    view.set_values(field_num_detections, num_detects)

    if add_relative_metrics:
        _compute_add_bbox_metrics(
            dataset,
            view,
            detection_field_name,
            1.0,
            1.0,
            "_rel",
            "Relative bounding box ",
            fo.FloatField,
        )

    if add_px_metrics:
        _compute_add_bbox_metrics(
            dataset,
            view,
            detection_field_name,
            F("$metadata.width"),
            F("$metadata.height"),
            "_px",
            "Absolute (in pixels) bounding box ",
            fo.IntField,
        )


if __name__ == "__main__":
    args = parse_args()
    dataset_name = args.dataset_name
    detection_field_name = args.detection_field_name
    add_relative_metrics = args.relative_values
    add_px_metrics = args.px_values

    print(
        f"Computing AABB metrics on detections {detection_field_name} of dataset {dataset_name}"
    )

    dataset = fo.load_dataset(dataset_name)
    view = dataset.match(F(detection_field_name))

    add_detections_AABB_metrics(
        dataset, view, detection_field_name, add_relative_metrics, add_px_metrics
    )
