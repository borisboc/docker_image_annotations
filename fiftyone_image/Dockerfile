FROM voxel51/fiftyone:latest

# Copy requirements files
COPY ./pip_requirements_fiftyone*.txt ./

#In 20250208, it looks necessary to update fiftyone because current release is v1.3.0 but Docker image has version v1.2.0  
RUN /opt/.fiftyone-venv/bin/pip3 install --upgrade pip \
  && /opt/.fiftyone-venv/bin/pip3 install --upgrade fiftyone \
  && /opt/.fiftyone-venv/bin/pip3 install -r pip_requirements_fiftyone.txt \
  && /opt/.fiftyone-venv/bin/fiftyone plugins download https://github.com/voxel51/fiftyone-plugins --plugin-names @voxel51/annotation @voxel51/brain @voxel51/dashboard @voxel51/evaluation @voxel51/io @voxel51/indexes @voxel51/runs @voxel51/utils @voxel51/zoo

RUN /opt/.fiftyone-venv/bin/pip3 install -r pip_requirements_fiftyone_pytorch_cpu.txt