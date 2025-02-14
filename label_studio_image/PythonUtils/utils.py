from label_studio_sdk.client import LabelStudio
from env import get_labelstudio_url, get_labelstudio_api_key


def connect_labelstudio_client():
    url = get_labelstudio_url()
    key = get_labelstudio_api_key()
    return LabelStudio(base_url=url, api_key=key)


def projects_ids_and_titles(ls: LabelStudio):
    ids = {}
    titles = {}
    pjs_l = ls.projects.list().items
    for pj in pjs_l:
        ids[pj.id] = pj.title
        titles[pj.title] = pj.id

    return ids, titles


def project_id_from_title(ls: LabelStudio, project_title: str):
    pjs = ls.projects.list()
    pj = next(x for x in pjs if x.title == project_title)
    return pj.id
