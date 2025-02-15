from PIL import Image
from pathlib import Path
import os
from tqdm import tqdm


def recursive_change_image_type(
    trunk_folder: Path, img_glob="*.bmp", new_ext=".png", delete_file=True
):
    img_files_glob = trunk_folder.rglob(img_glob)
    img_files_list = list(img_files_glob)
    errors = []
    for img_file in tqdm(img_files_list):
        try:
            Image.open(img_file).save(img_file.parent.joinpath(img_file.stem + new_ext))
            if delete_file:
                os.remove(img_file)
        except Exception as e:
            errors.append(e)

    return errors
