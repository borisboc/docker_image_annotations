from label_studio_sdk.client import LabelStudio
from label_studio_sdk.label_interface.objects import PredictionValue
from label_studio_sdk.converter.brush import decode_rle
import uuid
import cv2
import numpy as np


def mask_to_polygons_xy_percent(mask, img_width, img_height):
    contours, hierachy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_L1)
    polygons_xy = []
    img_width = 1.0 * img_width
    img_height = 1.0 * img_height

    for obj in contours:
        coords = []

        for point in obj:

            coords.append(
                [
                    float(point[0][0]) * 100.0 / img_width,
                    float(point[0][1]) * 100.0 / img_height,
                ]
            )

        polygons_xy.append(coords)
    return polygons_xy


def brush_annotation_to_polygon_prediction(
    ls: LabelStudio, task_id, annotation, prediction_from_name
):
    items = []
    for result in annotation["result"]:
        if result["type"] == "brushlabels":
            rle = None
            if "rle" in result:
                rle = result["rle"]
                label = result["brushlabels"]
            elif "value" in result:
                val = result["value"]
                if "rle" in val:
                    rle = val["rle"]
                    label = val["brushlabels"]
            if rle is None:
                continue

            image_rotation = result["image_rotation"]
            if image_rotation != 0:
                raise Exception("Rotation !=0 not implemented")

            width = result["original_width"]
            height = result["original_height"]
            to_name = result["to_name"]

            rle_decoded = decode_rle(rle)
            mask = np.reshape(rle_decoded, [height, width, 4])[:, :, 3]
            polygons_xy = mask_to_polygons_xy_percent(mask, width, height)
            for polygon in polygons_xy:

                item = {
                    "id": uuid.uuid4().hex[0:10],
                    "original_width": width,
                    "original_height": height,
                    "image_rotation": 0,
                    # "value": {"points": [[64.9, 51.6], [53.0, 69.4], [75.3, 76.64], [84.6, 60.5]], "closed" : True, "polygonlabels": label},
                    "value": {
                        "points": polygon,
                        "closed": True,
                        "polygonlabels": label,
                    },
                    "from_name": prediction_from_name,
                    "to_name": to_name,
                    "type": "polygonlabels",
                }
                items.append(item)

    if len(items) > 0:
        prediction = PredictionValue(
            model_version="brush_annotation_to_polygon_prediction",
            score=0.99,
            result=items,
        )

        ls.predictions.create(task=task_id, **prediction.model_dump())


def all_brush_annotations_to_polygon_prediction(
    ls: LabelStudio, project_id, prediction_from_name
):
    tasks = ls.tasks.list(project=project_id, include=["id", "annotations"])
    for task in tasks:
        if task.annotations is None:
            continue
        for annotation in task.annotations:
            brush_annotation_to_polygon_prediction(
                ls, task.id, annotation, prediction_from_name
            )
