# Tips and Tricks for FiftyOne

## Additional exports/imports

Some python scripts have been developed to simplify / automate the import / export of Fiftyone dataset in there own format, with file compression / decompression.



To Export : 

```shell
docker exec -it img-ann-fiftyone python3 /home/PythonUtils/export_fiftyone_dataset.py DATASET_NAME
```

In this case the exported .7z archive my in the temp folder. You may want another folder. So pass `-e` argument : 


```shell
docker exec -it img-ann-fiftyone python3 /home/PythonUtils/export_fiftyone_dataset.py DATASET_NAME -e /home/local_images/exports/DATASET_NAME
```


To import : 

```shell
docker exec -it img-ann-fiftyone python3 /home/PythonUtils/import_fiftyone_dataset.py DATASET_NAME DATASET_DIR_OR_7Z
```

For example : 

```shell
docker exec -it img-ann-fiftyone python3 /home/PythonUtils/import_fiftyone_dataset.py DATASET_NAME /home/local_images/exports/DATASET_NAME.7z
```

## Recursively adding images as samples

Fiftyone has some tools to imports. And also the method `from_images_patt`. If this does not work well for you, you can also you the script [recursive_add_images_to_fifytone.py](PythonUtils/recursive_add_images_to_fifytone.py)


```shell
docker exec -it img-ann-fiftyone python3 /home/PythonUtils/recursive_add_images_to_fifytone.py DATASET_NAME TRUNK_FOLDER GLOB_PATTERN
```

For example : 

```shell
docker exec -it img-ann-fiftyone python3 /home/PythonUtils/recursive_add_images_to_fifytone.py aff260707 /home/local_images/Projects/aff260707 *.png
```


## The View bar of the Web App

The view bar of the Web App is really handy because you can create your custom (and complex) filtering and staging requests directly in the Web App. Rather than using the Python SDK and creating a saved view.

But sadly, this is not documented in the [FiftyOne documentation](https://docs.voxel51.com/user_guide/app.html#using-the-view-bar).

### Display your current filters and/or sorting to view stages

 * Create a view / a selection in the method you prefere : either via the Web App, or the Python SDK :
   * via Web App :
     * this is "simply" a matter of filtering the sample/label tags, the labels attributes, the primitives attributes etc. Once you are happy of the filtered samples, here are 2 options : 
       * using the bookmark button named "Convert current filters and/or sorting to view stages"
       * with a saved view :
            * create a saved view : `browse operations > Save view`
            * Refresh the Web App with F5
            * Select the view in the list box at the top left corner (below FiftyOne logo).
            * Once the view selected, all the filtering stages are displayed in the view bar.  
   * via Python SDK : 
     * you can refer to the very good [Filtering Cheat Sheet](https://docs.voxel51.com/cheat_sheets/filtering_cheat_sheet.html) and [Views Cheat Sheet](https://docs.voxel51.com/cheat_sheets/views_cheat_sheet.html).
     * once you are happy with your filtering / view, you must save it and give it a name : `dataset.save_view("NameOfYourView", view_with_filetered_samples)`
     * Go back to the Web App, and select the view in the list box at the top left corner (below FiftyOne logo). You may need to refresh the page with F5
     * Once the view selected, all the filtering stages are displayed in the view bar.
 * Now that your filtering stages are displayed in the viewbar, you can see how it is build. And then you can "learn" to reproduce it. You can also save this view (`browse operations > Save view`) to serve as a "template" for the next time.

### Some useful view stage examples

#### Filter samples with filepath

Select `Match` operation and then paste the json code bellow:

```json
{
  "$expr": {
    "$regexMatch": {
      "input": "$filepath",
      "regex": "YOUR_REGEX",
      "options": null
    }
  }
}
```

## Generating thumbnails

Images (as thumbnails) can be long to generate and load on Fiftyone web app, especially for high resolution images (e.g. 120Mpx). So you can precompute them with the script `compute_thumbnails.py` or its notebook version `compute_thumbnails.ipynb`.


Here is an example : 

```shell
docker exec -it img-ann-fiftyone python3 /home/PythonUtils/compute_thumbnails.py DATASET_NAME /home/local_images/thumbnails --rel-dir /home/local_images --skip-already --size -1 128
```

Refresh web app with F5.

You may adapt the thumbnail size. And to force to regenerate already generated thumbnails, please replace `--skip-already` with `--no-skip-already` 
