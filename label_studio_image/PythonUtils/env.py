import os


def get_labelstudio_api_key():
    return os.environ["LABELSTUDIO_API_KEY"]


def get_labelstudio_url():
    return "http://localhost:8080"
