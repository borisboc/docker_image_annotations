import fiftyone as fo
from fiftyone import ViewField as F


def change_all_strs_and_paths(
    dataset_name: str,
    old_str: str,
    new_str: str,
    str_or_path_attribute: str,
    persistent: bool = True,
):
    dataset = fo.load_dataset(dataset_name)
    dataset.persistent = persistent

    dataset_with_thumbnails = dataset.match(F(str_or_path_attribute))
    thumbnails_path = dataset_with_thumbnails.values(str_or_path_attribute)

    print(
        f"Changing {len(thumbnails_path)} str or paths {str_or_path_attribute} on dataset {dataset_name} which has {len(dataset)} samples"
    )

    new_thumbnails_path = [tp.replace(old_str, new_str) for tp in thumbnails_path]

    print(
        f"Example of first element : {thumbnails_path[0]} is now {new_thumbnails_path[0]}"
    )

    # Automatically saves sample edits in efficient batches
    for i, sample in enumerate(
        dataset_with_thumbnails.iter_samples(autosave=persistent)
    ):
        sample[str_or_path_attribute] = new_thumbnails_path[i]

    return
