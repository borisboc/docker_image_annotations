FROM heartexlabs/label-studio:latest

# Install deb dependancies (e.g. for opencv)
USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

USER 1001

# Copy requirements files
COPY ./pip_requirements_label_studio.txt ./

# Install pip dependencies
RUN pip3 install --upgrade pip \
  && pip3 install -r pip_requirements_label_studio.txt
