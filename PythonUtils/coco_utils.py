import json
from pathlib import Path
import copy


def merge_image_duplicates(file_input: Path, file_output: Path = None):
    if not file_input.exists():
        raise FileNotFoundError(str(file_input))

    with open(file_input, "r") as f:
        coco_json = json.load(f)

    filename_id_dict = {}
    id_filename_dict = {}

    cleaned_coco_json = copy.deepcopy(coco_json)
    cleaned_coco_json["images"] = []

    for image in coco_json["images"]:
        filename = image["file_name"]
        id = image["id"]

        id_filename_dict[id] = filename

        if not filename in filename_id_dict:
            filename_id_dict[filename] = id
            cleaned_coco_json["images"].append(copy.deepcopy(image))

    for annotation in cleaned_coco_json["annotations"]:
        img_id = annotation["image_id"]
        equivalent_path = id_filename_dict[img_id]
        uniq_id = filename_id_dict[equivalent_path]
        annotation["image_id"] = uniq_id

    if file_output is not None:
        if not file_output.parent.exists():
            file_output.parent.mkdir(parents=True, exist_ok=True)

        with open(file_output, "w") as f:
            json.dump(cleaned_coco_json, f)

    return coco_json, cleaned_coco_json
