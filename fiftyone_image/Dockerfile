FROM voxel51/fiftyone:latest

# Copy requirements files
COPY ./pip_requirements_fiftyone*.txt ./

RUN apt update

RUN apt install curl

RUN pip3 install --upgrade pip

RUN pip3 install -r pip_requirements_fiftyone.txt

RUN pip3 install -r pip_requirements_fiftyone_pytorch_cpu.txt

RUN echo "before plugins installation"
RUN /opt/.fiftyone-venv/bin/fiftyone plugins list

RUN /opt/.fiftyone-venv/bin/fiftyone plugins download https://github.com/voxel51/fiftyone-plugins --plugin-names @voxel51/annotation @voxel51/brain @voxel51/dashboard @voxel51/evaluation @voxel51/io @voxel51/indexes @voxel51/runs @voxel51/utils @voxel51/zoo

RUN echo "after plugins installation"
RUN /opt/.fiftyone-venv/bin/fiftyone plugins list