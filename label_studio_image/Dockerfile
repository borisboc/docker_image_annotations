FROM heartexlabs/label-studio:latest

# Copy requirements files
COPY ./pip_requirements_label_studio.txt ./

# Install dependencies
RUN pip3 install --upgrade pip \
  && pip3 install -r pip_requirements_label_studio.txt
