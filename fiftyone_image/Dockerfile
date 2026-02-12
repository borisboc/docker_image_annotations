FROM voxel51/fiftyone:latest

ARG BUILD_PROFILE
ENV BUILD_PROFILE=${BUILD_PROFILE}

# Copy requirements files
COPY ./pip_requirements_fiftyone*.txt ./

# CURL for testing API with label studio
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# By default, the plugins are stored in the local bound volume "fiftyone_data", 
# which is not OK : downloaded plugins in this dockerfile will be overwritten by bound volume.
# So let's change the directory
RUN mkdir /home/fiftyone_plugins && chmod -R a+rwx /home/fiftyone_plugins
ENV FIFTYONE_PLUGINS_DIR=/home/fiftyone_plugins    

RUN /opt/.fiftyone-venv/bin/pip3 install --upgrade pip \
  && /opt/.fiftyone-venv/bin/pip3 install -r pip_requirements_fiftyone.txt \
  && /opt/.fiftyone-venv/bin/fiftyone plugins download https://github.com/voxel51/fiftyone-plugins --plugin-names @voxel51/annotation @voxel51/brain @voxel51/dashboard @voxel51/evaluation @voxel51/io @voxel51/indexes @voxel51/runs @voxel51/utils @voxel51/zoo

# Install CPU or GPU-specific dependencies
RUN if [ $BUILD_PROFILE = "gpu"  ]; then \
echo "Installing GPU dependencies..." && \
/opt/.fiftyone-venv/bin/pip3 install -r pip_requirements_fiftyone_pytorch_gpu.txt ;\
else \
echo "Installing CPU dependencies..." && \
/opt/.fiftyone-venv/bin/pip3 install -r pip_requirements_fiftyone_pytorch_cpu.txt ;\
fi