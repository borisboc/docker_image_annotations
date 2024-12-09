# docker_image_annotations

Create a docker container dedicated to image annotations based on [label-studio](https://labelstud.io/). Ongoing ...

## Installation / running the container

```
docker compose -f compose_local_files.yaml -p image_annotations up
```

## Usage

Create a subfolder inside folder `local_images/` with the name of your project. E.g. `local_images/myproject`.

Open your web browser and log in label-studio.

Create a project.

To import/sync your image folder, follow the instructions given in [label-studio local storage](https://labelstud.io/guide/storage.html#Set-up-connection-in-the-Label-Studio-UI-4). And pass the full `Absolute local path` as such : `/home/local_images/myproject`






## Sources

[label-studio on dockerhub](https://hub.docker.com/r/heartexlabs/label-studio)

[label-studio : persist data with Docker](https://labelstud.io/guide/storedata#Persist-data-with-Docker)

[label-studio tuto import yolo annotations](https://labelstud.io/blog/tutorial-importing-local-yolo-pre-annotated-images-to-label-studio/)

[label-studio local storage](https://labelstud.io/guide/storage.html#Set-up-connection-in-the-Label-Studio-UI-4)