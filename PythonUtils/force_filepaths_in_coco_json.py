from pathlib import Path
import json
import copy

def load_coco_json_as_dict(file_input: Path):
    if not file_input.exists():
        raise FileNotFoundError(str(file_input))

    with open(file_input, "r") as f:
        coco_json = json.load(f)
    
    return coco_json

def force_filepaths_in_coco_dict(coco_json_dict: dict, new_img_filepaths:list[str]):
    
    if(len(coco_json_dict["images"]) != len(new_img_filepaths)):
        raise ValueError("nb of images in coco json does not match nb of new filepaths")
    
    cleaned_coco_json = copy.deepcopy(coco_json_dict)

    for i, img in enumerate(cleaned_coco_json["images"]):
        img["path"] = str(new_img_filepaths[i])
        img["file_name"] = Path(new_img_filepaths[i]).name 

    return cleaned_coco_json

def save_coco_dict_to_json_file(coco_dict:dict, file_output:Path):
    if file_output is not None:
        if not file_output.parent.exists():
            file_output.parent.mkdir(parents=True, exist_ok=True)

        print(f"Exporting COCO JSON to {file_output}")
        with open(file_output, "w") as f:
            json.dump(coco_dict, f, indent=2)

def change_filepath_in_coco_using_annotation_key(
    coco_json_path : Path,
    dataset_name : str,
    anno_key: str,
    output_filepath: Path = None):

    # here is the scenario :
    # 1/ You requested some annotations from FiftyOne
    # 2/ You did you annotation on your backend (e.g. label studio)
    #    and you exported the annotations in COCO format.
    #    As you can see, the image file path have changed, because they are uploaded
    #    from Fiftyone to Label Studio.
    # 3/ You want to reintroduce the correct filepath

    # This is the code meant for you ! 

    # But keep in mind that you should have exactly the same nb of images in the same order ! 
    # So it will not work if you deleted some images in your annotation backend.

    import fiftyone as fo

    coco_json_dict = load_coco_json_as_dict(coco_json_path)
    dataset = fo.load_dataset(dataset_name)
    ann_view = dataset.load_annotation_view(anno_key)
    new_img_filepaths = ann_view.values('filepath')
    cleaned_coco_json = force_filepaths_in_coco_dict(coco_json_dict, new_img_filepaths)
    if output_filepath is None : 
        output_filepath = coco_json_path.parent.joinpath(coco_json_path.stem + "_filepaths_from_anno_key_" + anno_key + ".json")
    save_coco_dict_to_json_file(cleaned_coco_json, output_filepath)

