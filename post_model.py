import hashlib
import json
import os
import xlrd
from xlutils.copy import copy
import requests
import time

api_url = {
            "civitai.com": "https://civitai.com/api/v1/models",
            "liandange.com": "https://model-api.liandange.com/model/api/models",
        }

model_json = {
            'civitai.com': os.path.join('/data/soft/fetch_mode/file_json', 'civitai_models.json'),
            'liandange.com': os.path.join('/data/soft/fetch_mode/file_json', 'liandange_models.json')
        }

def write_json(file, content) -> None:
    try:
        with open(file, 'w') as f:
            json.dump(content, f, indent=4)
    except Exception as e:
        print(e)

def update_model_json(site: str, models):
    write_json(model_json[site], models)

def get_api_url(model_source: str):
    return api_url[model_source]

def fetch_all_models(model_source: str):
    print('start fetching...')
    endpoint_url = get_api_url(model_source)
    if endpoint_url is None:
        print(f"{model_source} is not supported")
        return []

    print(f"start to fetch model info from '{model_source}':{endpoint_url}")

    limit_threshold = 100

    all_set = []
    response = requests.get(endpoint_url + f'?page=1&limit={limit_threshold}')
    num_of_pages = response.json()['metadata']['totalPages']
    total_items = response.json()['metadata']['totalItems']
    print(f"total pages = {num_of_pages}, total models = {total_items}")

    continuous_error_counts = 0
    fetched_cnt = 0
    miss_img = 0
    miss_file = 0

    for p in range(1, num_of_pages+1):
        #try:
            response = requests.get(endpoint_url + f'?page={p}&limit={limit_threshold}')
            payload = response.json()
            if payload.get("success") is not None and not payload.get("success"):
                print(f"failed to fetch page[{p}]")
                continuous_error_counts += 1
                if continuous_error_counts > 10:
                    break
                else:
                    continue

            continuous_error_counts = 0  # reset error flag
            print(f"start to process page[{p}]")

            for model in payload['items']:
                fetched_cnt += 1

                model_json = {"id": 0, "name": "", "stats": {}, "type": "", "nsfw": False, "tags": {},
                              "modelVersions": []}

                if len(model["modelVersions"]) > 0 and len(model["modelVersions"][0]["files"]) > 0 and "images" in model["modelVersions"][0].keys() and len(model["modelVersions"][0]["images"]) > 0:

                    model_json["id"] = model["id"]
                    model_json["name"] = model["name"]
                    model_json["type"] = model["type"]
                    model_json["nsfw"] = model["nsfw"]
                    model_json["stats"] = model["stats"]
                    model_json["tags"] = model["tags"]

                    EMP_MV_JSON = {"id":0,"name":"","createdAt":"","updatedAt":"","files":[{"name":"", "hashes":{}}],"images":[{"url":"", "nsfw":"None"}]}
                    for mv in model["modelVersions"]:
                        mv_json = {"id":0,"name":"","createdAt":"","updatedAt":"","files":[{"name":"", "hashes":{}}],"images":[{"url":"", "nsfw":"None"}]}
                        mv_json["id"] = mv["id"]
                        mv_json["name"] = mv["name"]
                        if len(mv["files"]) > 0:
                            mv_json["files"][0]["name"] = mv["files"][0]["name"]
                            mv_json["files"][0]["hashes"] = mv["files"][0]["hashes"]
                        else:
                            mv_json["files"][0]["name"] = ""
                            mv_json["files"][0]["hashes"] = {}
                            if model_source == 'liandange.com':
                                mv_json["files"][0]['downloadUrl'] = mv["downloadUrl"]

                        if len(mv["images"]) > 0:
                            mv_json["images"][0]["url"] = mv["images"][0]["url"]
                            mv_json["images"][0]["nsfw"] = mv["images"][0]["nsfw"]
                        else:
                            miss_img +=1
                            mv_json["images"][0]["url"] = "https://msdn.miaoshouai.com/msai/kt/ez/9900922.png"
                            mv_json["images"][0]["nsfw"] = "None"

                        model_json["modelVersions"].append(mv_json)

                    if len(model_json["modelVersions"]) <= 0:
                        model_json["modelVersions"].append(EMP_MV_JSON)


                    print(f"page {p}/{num_of_pages}: {fetched_cnt}/{total_items}")
                    print(f"page {p}/{num_of_pages}: {p*limit_threshold if p*limit_threshold <= total_items else total_items-(p-1)*limit_threshold}/{total_items}")
                    all_set.append(model_json)

            #print(f"page[{p}] : {len(payload['items'])} items added")
        #except Exception as e:
        #    print(f"failed to fetch page[{p}] due to {e}")
        #    time.sleep(3)

    if len(all_set) > 0:
        update_model_json(model_source, all_set)
    else:
        print("fetch_all_models: emtpy body received")


for source in model_json.keys():
    print(f'fetching {source}')
    fetch_all_models(source)

