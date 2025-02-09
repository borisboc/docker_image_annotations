# Docker Image Annotations

This repository is meant to help you create Docker containers dedicated to image annotations.
Currently, this is based on :
 * [label-studio](https://labelstud.io/)
 * [fiftyone](https://docs.voxel51.com/index.html)
 
 Maybe some new features ongoing ...

## Requirements

You must have [docker](https://docs.docker.com/get-started/) installed. E.g. install [docker desktop](https://docs.docker.com/get-started/get-docker/).


## Installation / running the container

Start docker.

Clone this repository with the following command :

```
git clone https://github.com/borisboc/docker_image_annotations.git && cd docker_image_annotations
```

Edit the file `fiftyone_image/fiftyone_secrets.env`. Change the values of the 2 environment variables : 
```
MONGO_INITDB_ROOT_USERNAME
MONGO_INITDB_ROOT_PASSWORD
```
In order to set a proper user name and password for the MongoDB database (used by FiftyOne).

Build and start the containers with the following command : 

```
docker compose -f compose_local_files.yaml -p image_annotations up --build
```

Open your web browser and and go to URL : http://localhost:8080/.
Then log in [label-studio](https://labelstud.io/).

Sign-up / create an account.

Get your label-studio API KEY (acces token) by going to the `account & settings` page. Copy the `Access Token`, and paste it inside the file `label_studio_image/label_studio_secrets.env`

```
LABELSTUDIO_API_KEY="PLEASE PASTE YOUR LABEL STUDIO ACCESS TOKEN HERE, WITHIN THE DOUBLE QUOTES"
```

Stop the containers (e.g. CTRL+C in the terminal you upped the containers, or using Docker Desktop).

Restart the containers (see docker compose command above) so that FiftyOne environment is updated.

## Usage

Start docker.

Start the containers with the following commands : 
```
docker compose -f compose_local_files.yaml -p image_annotations up
```

Or restart it from docker desktop, as you prefere.

Create a subfolder inside folder `local_images/` with the name of your project. E.g. `local_images/myproject`. Place your images within this folder.

Open your web browser and and go to URL : http://localhost:5151/.
to use the [FiftyOne App](https://docs.voxel51.com/user_guide/app.html).

If you don't have any dataset yet, you can create one by clicking on link on the webpage.
TODO : Screenshot when creating a dataset for the first time.

Then you can add samples by clicking on the link `click here` on the webpage.

![Add samples to an empty dataset by clicking on the link](doc/add_samples_to_empty_dataset.png)

Choose what you want to import. It depends on your data : if you have only media (i.e. the images) or you also have the annotations. For more details, you can refere to [FiftyOne import_samples operator](https://github.com/voxel51/fiftyone-plugins/blob/main/plugins/io/README.md#import_samples).

![Choose the type of samples to import](doc/samples_import_type.png)

Then import either all the content of a directory (but not the subdirectories recursively). Or using a glob pattern.
In both cases, your images will be in the folder `/home/local_images` as there is a binding between the container and the folder on your host machine.
In the case you want to browse the folder with the FiftyOne Web App, see the screenshots bellow.

Access the root directory by clicking on the arrow up close to the text bar.
![root directory accessed with arrow up](doc/root_directory.png)

Then go to your directory containing your media. E.g., if your subfolder is named `myproject` (as proposed above), you will find it at the path `/home/local_images/myproject` 

![folder myproject at path /home/local_images/myproject](doc/local_images_directory.png).

Then press execute.

From now you have a dataset created, and some samples. You can see the subparagraphs of this readme depending on what you want to do next.

### Workflow for annotations

And then request for annotations with Label-Studio backend.

TODO : finish this paragraph and add screenshots.

### Connect another instance of FiftyOne to the same database

TODO : finish this paragraph and add screenshots.


### Accessing a container, program with jupyter notebook

You can use Visual Studio remote connexion on a `Dev Container`. Or `Docker Desktop`.
Connect on the container you want to play with (let's say `img_annotations_fiftyone` ).
Inside a container terminal, go to relevant folder. E.g. `/home/local_images/` , then type

```
jupyter notebook --ip 0.0.0.0 --no-browser --allow-root
```
Click on the link provided in the terminal output to start a notebook.



## Sources

[label-studio on dockerhub](https://hub.docker.com/r/heartexlabs/label-studio)

[label-studio : persist data with Docker](https://labelstud.io/guide/storedata#Persist-data-with-Docker)

[label-studio tuto import yolo annotations](https://labelstud.io/blog/tutorial-importing-local-yolo-pre-annotated-images-to-label-studio/)

[label-studio local storage](https://labelstud.io/guide/storage.html#Set-up-connection-in-the-Label-Studio-UI-4)

[Access Jupyter notebook running on Docker container](https://stackoverflow.com/questions/38830610/access-jupyter-notebook-running-on-docker-container)

[FiftyOne on dockerhub](https://hub.docker.com/r/voxel51/fiftyone)

[FiftyOne : Loading data into FiftyOne](https://docs.voxel51.com/user_guide/dataset_creation/index.html#)

[FiftyOne : Using the FiftyOne App](https://docs.voxel51.com/user_guide/app.html)

[Docker and MongoDB](https://www.mongodb.com/resources/products/compatibilities/docker)

## TODOs

Screenshot when creating a dataset for the first time.

More documentation and more screenshots.