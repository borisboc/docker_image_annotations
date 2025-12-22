docker container rm img-ann-sa2-label-studio ;\
docker container rm img-ann-fiftyone ;\
echo "starting with profile gpu" && \
IMG_ANNOTATIONS_BUILD_PROFILE=gpu docker compose -f compose_local_files.yaml --profile gpu -p img-ann up $@