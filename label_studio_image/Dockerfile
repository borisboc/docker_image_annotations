FROM heartexlabs/label-studio:latest

# Copy requirements files
COPY ./pip_requirements_label_studio.txt ./

RUN pip3 install --upgrade pip

RUN pip3 install -r pip_requirements_label_studio.txt
