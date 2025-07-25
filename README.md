# Docker Image Annotations

This repository is meant to help you create Docker containers dedicated to image annotations.
Currently, this is based on :
 * [fiftyone](https://docs.voxel51.com/index.html)
 * [label-studio](https://labelstud.io/)
 * [Segment Anything Model 2 (SAM2)](https://github.com/facebookresearch/sam2)
 

## Requirements & some important remarks

You must have [docker](https://docs.docker.com/get-started/) installed. 

Please note that if you installed and use [docker desktop](https://docs.docker.com/get-started/get-docker/), it starts with a context called `desktop-linux`. In this context, you can have access to GPU only with sudo privilege.

If you don't want to run with privilege, you must run [docker in rootless mode](https://docs.docker.com/engine/security/rootless/). In this case, you can switch to rootless context by running

`docker context use rootless`  

If you want the containers to have access to the NVIDIA GPUs please follow the instructions given in [docker : Access an NVIDIA GPU](https://docs.docker.com/engine/containers/resource_constraints/#gpu). Briefly, you will have to install NVIDIA driver and NVIDIA container toolkit. Once done, you should be able to successfully run the following command : 

`docker run --rm --runtime=nvidia --gpus all ubuntu nvidia-smi`

If you need sudo privilege for this command, please read the remark above (same paragraph). 

If you run with rootless privilege, all the folders (volumes) that will be created with the containers (e.g. `fiftyone_data`, `label_studio_data` etc.) will NOT be owned by your current user. Which may be anoying for some usage. In this case, you may `chmod -R g+w` each folder.

## Installation / running the container

Start docker.

Clone this repository with the following command :

```
git clone https://github.com/borisboc/docker_image_annotations.git && cd docker_image_annotations
```

Edit the file `fiftyone_image/fiftyone_secrets.env`. Change the values of the 2 environment variables : 
```
MONGO_INITDB_ROOT_USERNAME=YourMongoDbUsernameHere
MONGO_INITDB_ROOT_PASSWORD=YourMongoDbPasswordHere
```
In order to set a proper user name and password for the MongoDB database (used by FiftyOne). Please do **NOT** use the `@` symbol (for both username and password).

Build and start the containers with the following command : 

 * If you have GPU access : 
   * `./start_gpu.sh`
 * Otherwise, for CPU : 
   * `./start_cpu.sh` 

If you use Windows, you can execute the shell scripts using GitBash.

Check that the fiftyone plugins are installed. Sometimes, they are not and currently I can't say why. See this [issue](https://github.com/borisboc/docker_image_annotations/issues/1).

```bash
docker exec -it img-annotations-fiftyone fiftyone plugins list
```

If you don't see the plugins in the output (e.g. @voxel51/io @voxel51/annotation etc.), please run

```bash
docker exec -it img-annotations-fiftyone fiftyone plugins download https://github.com/voxel51/fiftyone-plugins --plugin-names @voxel51/annotation @voxel51/brain @voxel51/dashboard @voxel51/evaluation @voxel51/io @voxel51/indexes @voxel51/runs @voxel51/utils @voxel51/zoo
```

Open your web browser and and go to URL : http://localhost:8080/.
Then log in [label-studio](https://labelstud.io/).

Sign-up / create an account.

Get your label-studio API KEY (acces token). Somewhere in 2025, Label Studio have changed their authorization / tokens methods. But FiftyOne still uses the old method.<br>
So you first need to go to `Organization > API Tokens Settings` and activate `Legacy Tokens`. <br>
Then go to your `account & settings` page, go to `Legacy Token` section and copy the `Access Token`, and paste it inside the file [label_studio_image/label_studio_secrets.env](label_studio_image/label_studio_secrets.env)

```
LABELSTUDIO_API_KEY="PLEASE PASTE YOUR LABEL STUDIO ACCESS TOKEN HERE, WITHIN THE DOUBLE QUOTES"
```

Stop the containers (e.g. CTRL+C in the terminal you upped the containers, or using Docker Desktop).

Restart the containers (see docker compose command above) so that FiftyOne environment is updated.

## Usage

Start docker.

Start the containers with the following commands : 

Build and start the containers with the following command : 

 * If you have GPU access : 
   * `./start_gpu.sh`
 * Otherwise, for CPU : 
   * `./start_cpu.sh` 

Or restart it from docker desktop, as you prefere.

If you use Windows, you can execute the shell scripts using GitBash.

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

CAUTION : annotation name (also call `anno_key`) cannot start with numbers ! E.g. `20250724_ann_key` is **NOT** valid !

And then request for annotations with Label-Studio backend.

TODO : finish this paragraph and add screenshots.

### Using Segment Anything Model 2 during annotations

During annotations on Label-Studio, if you need to annotate segmentation (e.g. semantic segmentation, or instance segmentation) you can use Segment Anything Model 2 ([SAM2](https://github.com/facebookresearch/sam2)) to generate you segmentations/masks from a provided seed on the image (which can be some keypoints, a brushed region, or a axis-aligend rectangle). The result of SAM2 will be `BrushLabel`.

You can find a [youtube video tutorial](https://youtu.be/FTg8P8z4RgY?feature=shared) from Label Studio, to show you how to use SAM2.

Concerning the configuration in the menu `Settings > Model`, in our case, please set the following Backend URL : 

```
http://img-annotations-sa2-label-studio:9090
```

And toogle ON the parameter `Interactive preannotations`.

For further details, please refere to [label-studio-ml-backend github : using sam2](https://github.com/HumanSignal/label-studio-ml-backend/tree/master/label_studio_ml/examples/segment_anything_2_image#using-sam2-with-label-studio-for-image-annotation)

Remark : for keypoints, add a "bellong to" point with left click, and a "does not bellong to" with ALT + left click. 

For the labeling interface, you use SAM2 with keypoints or rectangle, you can base it on the example in [labeling_interface_sam2.xml](label_studio_image/PythonUtils/labeling_interface_sam2.xml)

### Connect another instance of FiftyOne to the same database

Because the MongoDB database used by FiftyOne runs in its own container, and ports are bound, it is fine to connect another instance of FifytOne to this database. The typical usecase is that you develop a neural network on your host machine, or inside another container, and you want to access the samples in one of your FiftyOne dataset.

Do do so, in the session running your own FiftyOne instance, you can either modify the fiftyone congiguration json file, or declare the environment variable `FIFTYONE_DATABASE_URI`, which is the prefered option explained bellow.

In your session, please export : 

```
export FIFTYONE_DATABASE_URI=mongodb://YourMongoDbUsernameHere:YourMongoDbPasswordHere@127.0.0.1:27017
```

Please set the correct values for your mongodb username and password. They must match the content in file [fiftyone_image/fiftyone_secrets.env](fiftyone_image/fiftyone_secrets.env)


Once exported, you can run all your python codes with FifytOne and access the FifytOne datasets. E.g. :

``` python
import fiftyone as fo
ds = fo.load_dataset("NameOfYouDatasetHere")
```

A convenient way is to save this command with the correct connection details within a `.sh`file. And you can `source` this file.

<br/>

If your FiftyOne session is within another container of the same docker compose (e.g. you have edited your own docker compose file instead of `compose_local_files.yaml`), within your own container, please use the mongodb container name. E.g. :

```
export FIFTYONE_DATABASE_URI=mongodb://YourMongoDbUsernameHere:YourMongoDbPasswordHere@img-annotations-mongodb:27017
```

This is what is done in file [fiftyone_image/fiftyone.env](fiftyone_image/fiftyone.env)

For further details, please refere to [FiftyOne : configuring mongodb connection](https://docs.voxel51.com/user_guide/config.html#configuring-mongodb-connection).

### Accessing a container, program with jupyter notebook

#### For label-studio container

To start a jupyter notebook server on the label-studio container, simply start a new terminal and run : 

```
./jupyter_label_studio.sh
```

You will see the URL with the AUTH token printed in the console. Go to this URL on the web browser to work with jupyter notebook. For instance, you may want to use the scripts that are in `PythonUtils/` folder.

#### For fiftyone container

Same as for label-studio container, but instead you may run :

```
./jupyter_fiftyone.sh
```


#### For other containers

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

[label-studio-ml-backend github : using sam2](https://github.com/HumanSignal/label-studio-ml-backend/tree/master/label_studio_ml/examples/segment_anything_2_image#using-sam2-with-label-studio-for-image-annotation)

[Access Jupyter notebook running on Docker container](https://stackoverflow.com/questions/38830610/access-jupyter-notebook-running-on-docker-container)

[FiftyOne on dockerhub](https://hub.docker.com/r/voxel51/fiftyone)

[FiftyOne : Loading data into FiftyOne](https://docs.voxel51.com/user_guide/dataset_creation/index.html#)

[FiftyOne : Using the FiftyOne App](https://docs.voxel51.com/user_guide/app.html)

[FiftyOne : configuring mongodb connection](https://docs.voxel51.com/user_guide/config.html#configuring-mongodb-connection)

[Docker and MongoDB](https://www.mongodb.com/resources/products/compatibilities/docker)

[docker : Access an NVIDIA GPU](https://docs.docker.com/engine/containers/resource_constraints/#gpu)


## TODOs

Screenshot when creating a dataset for the first time.

More documentation and more screenshots.