# Docker Image Annotations

This repository is meant to help you create Docker containers dedicated to image annotations.
Currently, this is based on :
 * [label-studio](https://labelstud.io/)
 
 Maybe some new features ongoing ...

## Installation / running the container

```
docker compose -f compose_local_files.yaml -p image_annotations up
```

## Usage

Create a subfolder inside folder `local_images/` with the name of your project. E.g. `local_images/myproject`. Place your images within this folder.

Open your web browser and and go to URL : http://localhost:8080/.
Then log in [label-studio](https://labelstud.io/)

Create a project.

To import/sync your image folder, follow the instructions given in [label-studio local storage](https://labelstud.io/guide/storage.html#Set-up-connection-in-the-Label-Studio-UI-4). And pass the full `Absolute local path` as such : `/home/local_images/myproject`


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