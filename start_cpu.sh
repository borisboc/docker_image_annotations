docker container rm img-ann-sa2-label-studio ;\
docker container rm img-ann-fiftyone ;\
echo "starting with profile cpu" && \
IMG_ANNOTATIONS_BUILD_PROFILE=cpu docker compose -f compose_local_files.yaml --profile cpu -p img-ann up $@