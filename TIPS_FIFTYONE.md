# Tips and Tricks for FiftyOne

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


