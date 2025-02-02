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

Clone this repository :

```
git clone https://github.com/borisboc/docker_image_annotations.git && cd docker_image_annotations
```

Build and start the containers

```
docker compose -f compose_local_files.yaml -p image_annotations up
```

Open your web browser and and go to URL : http://localhost:8080/.
Then log in [label-studio](https://labelstud.io/).

Sign-up / create an account.

Get your label-studio API KEY (acces token) by going to the `account & settings` page. Copy the `Access Token`, and paste it inside the file `fiftyone_image/fiftyone_secrets.env`

```
FIFTYONE_LABELSTUDIO_API_KEY: "PLEASE PASTE YOUR LABEL STUDIO ACCESS TOKEN HERE, WITHIN THE DOUBLE QUOTES"
```

Stop the containers (e.g. CTRL+C in the terminal you upped the containers, or using Docker Desktop).

Restart the containers (see docker compose command above) so that FiftyOne environment is updated.

## Usage

Create a subfolder inside folder `local_images/` with the name of your project. E.g. `local_images/myproject`. Place your images within this folder.

Open your web browser and and go to URL : http://localhost:5151/.
to use the [FiftyOne App](https://docs.voxel51.com/user_guide/app.html).

You can then create a dataset.

And then request for annotations with Label-Studio backend.


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

## TODOs

Proper MongoDB server (in a container) for FiftyOne