import fiftyone as fo
import argparse
from IPython import embed
from fiftyone import ViewField as F
from change_all_strs_and_paths import change_all_strs_and_paths


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Change all filepath in samples inside a dataset. Useful if your files were moved."
    )
    parser.add_argument(
        "dataset_name",
        type=str,
        help="The name of the dataset where the samples are",
    )
    parser.add_argument(
        "old_str",
        type=str,
        help="The old str in the file path that must be replaced by new str value",
    )
    parser.add_argument(
        "new_str",
        type=str,
        help="The new str in the file path that must replace the old str value",
    )
    parser.add_argument(
        "-fa",
        "--filepath-attribute",
        type=str,
        default="filepath",
        help="The name of the attribute for the file path",
    )
    parser.add_argument(
        "-pe",
        "--persistent",
        type=bool,
        default=True,
        help="If the modifications on the dataset must be persistent",
    )

    args = parser.parse_args()

    dataset_name = args.dataset_name
    old_str = args.old_str
    new_str = args.new_str
    filepath_attribute = args.filepath_attribute
    persistent = args.persistent
    change_all_strs_and_paths(
        dataset_name, old_str, new_str, filepath_attribute, persistent
    )
