ARG LABELSTUDIO_TAG

FROM heartexlabs/label-studio:${LABELSTUDIO_TAG}

USER root

# Install system dependencies (e.g. for opencv)
# For versions <= 1.22, label studio container was based on debian.
# In versions >= 1.23, label studio container is based on alpine.
# To infere if debian or alpine, we check the package manager.
RUN if command -v apt-get >/dev/null 2>&1; then \
        echo "Debian-based image detected, using apt-get" && \
        apt-get update && apt-get install -y --no-install-recommends \
            ffmpeg \
            libsm6 \
            libxext6 \
        && rm -rf /var/lib/apt/lists/*; \
    elif command -v apk >/dev/null 2>&1; then \
        echo "Alpine-based image detected, using apk" && \
        apk add --no-cache \
            ffmpeg \
            libsm \
            libxext \
            py3-opencv && \
        VENV_CFG=$(find / -maxdepth 3 -name pyvenv.cfg 2>/dev/null | head -1) && \
        sed -i 's/include-system-site-packages = false/include-system-site-packages = true/' "$VENV_CFG"; \
    else \
        echo "ERROR: unknown base image, no supported package manager found" >&2 && exit 1; \
    fi

USER 1001

# Copy requirements files
COPY ./pip_requirements_label_studio.txt ./

# Install pip dependencies
# Remark : opencv-python was removed from pip_requirements_label_studio.txt
# because no musl wheel on alpine. So we install py3-opencv instead.
# However, on Debian, let's use the "standard way" : install with pip.
RUN pip3 install --upgrade pip \
    && pip3 install -r pip_requirements_label_studio.txt \
    && if command -v apt-get >/dev/null 2>&1; then pip3 install opencv-python; fi