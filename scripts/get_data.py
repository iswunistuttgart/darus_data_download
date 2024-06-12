import argparse
import json
import logging
import os
import sys
import unicodedata
import re
from typing import List
import hashlib
import requests


config_template = {
    "dataverse_url": "https://darus.uni-stuttgart.de/",
    "datasets": [
        {"id": "doi:10.18419/darus-????", "version": ":latest"}
    ],
}


def get_script_path() -> str:
    return os.path.dirname(os.path.realpath(sys.argv[0]))


def get_search_dirs() -> List[str]:
    return [
        get_script_path(),
        os.path.join(get_script_path(), ".."),
        os.path.join(get_script_path(), "../.."),
    ]


def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize("NFKC", value)
    else:
        value = (
            unicodedata.normalize("NFKD", value)
            .encode("ascii", "ignore")
            .decode("ascii")
        )
    value = re.sub(r"[^\w\s-]", "", value.lower())
    return re.sub(r"[-\s]+", "-", value).strip("-_")


def create_config_template_if_needed() -> bool:
    config_file = os.path.join(get_script_path(), "darus_config.json")
    if not any(
        [
            os.path.exists(os.path.join(config_dir, "darus_config.json"))
            for config_dir in get_search_dirs()
        ]
    ):
        print("No configuration file exists.")
        with open(os.path.join(get_script_path(), "darus_config.json"), "w") as cf:
            json.dump(config_template, cf, indent=4)
        print(
            "Created a config template.\nRemember to fill in your dataset identifiers and crate a .darus_apikey file for your API key."
        )
        return True
    else:
        return False


def load_api_key_from_file():
    for d in get_search_dirs():
        path = os.path.join(d, ".darus_apikey")
        if os.path.exists(path):
            with open(path, "r") as key_file:
                return key_file.read()

    print("no file .darus_apikey found. Proceeding with public authentication.")
    return None


def load_config_from_file():
    config_txt = ""
    for d in get_search_dirs():
        path = os.path.join(d, "darus_config.json")
        if os.path.exists(path):
            with open(path, "r") as config_file:
                config_txt = config_file.read()
            break

    return json.loads(config_txt)

def get_headers(api_token:str|None=None):
    headers = {}
    if api_token and api_token != "":
        headers["X-Dataverse-key"] = api_token
    
    return headers

def get_dataset_info(dataset_obj : dict, config: dict, api_token: str|None = None):

    # legacy:
    if not isinstance(dataset_obj, dict):
        logging.warn(f"""You are using the old format for darus_config.json, where only a doi is passed for each repository.
The new version supports passing a version as well for reprducibility of results.
Consider updating the darus_config.json, support for the old format will be removed in a future version.

example:
{config_template}
""")
        dataset_id = dataset_obj
        dataset_version = "latest"
    else:
        dataset_id = dataset_obj["id"]
        dataset_version = dataset_obj["version"]

    if dataset_version in ["latest", "latest-published","draft"]:
        dataset_version = ":" + dataset_version # prepend : as requested by DaRUS API, see https://guides.dataverse.org/en/6.2/api/dataaccess.html#download-by-dataset-by-version 

    headers = get_headers(api_token)
    return requests.get(f"{config_obj["dataverse_url"]}api/v1/datasets/:persistentId/versions/{dataset_version}/?persistentId=doi:{dataset_id.replace("doi:", "")}", headers=headers)

def get_whole_dataset_zipped(dataset_id : str, config: dict, api_token: str|None = None):
    # this is slow:
    headers = get_headers(api_token)
    return requests.get(f"{config_obj["dataverse_url"]}api/v1/access/dataset/:persistentId/versions/:latest/?persistentId=doi:{dataset_id.replace("doi:", "")}", headers=headers, timeout=999)

def get_file(file_id:int, config: dict, api_token : str|None = None):
    headers = get_headers(api_token)
    return requests.get(f"{config_obj["dataverse_url"]}api/v1/access/datafile/{file_id}", headers=headers, timeout=None)


def calcuate_md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(100*4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


# main program:
if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="get_data", description="downloads data from configured DaRUS repositories. See <https://github.com/iswunistuttgart/darus_data_download/blob/master/Readme.md>")
    parser.add_argument(
        "-log", 
        "--log", 
        default="warning",
        help=(
            "Provide logging level. "
            "Example --log debug', default='warning'"),
    )

    options = parser.parse_args()
    levels = {
        'critical': logging.CRITICAL,
        'error': logging.ERROR,
        'warn': logging.WARNING,
        'warning': logging.WARNING,
        'info': logging.INFO,
        'debug': logging.DEBUG
    }
    level = levels.get(options.log.lower())
    if level is None:
        level = logging.WARNING

    logging.basicConfig(level=level)

    if create_config_template_if_needed():
        exit(0)

    config_obj = load_config_from_file()
    api_key = load_api_key_from_file()

    for dataset_identifier in config_obj["datasets"]:
        dataset_resp = get_dataset_info(dataset_identifier, config_obj, api_key)

        if dataset_resp.ok:

            citation_info = dataset_resp.json()["data"]["metadataBlocks"]["citation"]["fields"]
            dataset_title = ""
            for c in citation_info:
                if c["typeName"] == "title":
                    dataset_title = c["value"]
                    break

            folder_name = slugify(dataset_title)  # extract from JSON
            folder = os.path.normpath(
                os.path.join(get_script_path(), "..", "data", folder_name)
            )
            if os.path.exists(folder):
                download_data = input(
                    f"The folder {folder} already exists. Do you want to download it again? (y/n)"
                )
                if download_data.lower() == "n":
                    continue
            os.makedirs(folder, exist_ok=True)

            for file in dataset_resp.json()["data"]["files"]:
                logging.info(f"Start downloading file: {file["dataFile"]}")
                file_name = file["dataFile"]["filename"]
                file_id = file["dataFile"]["id"]
                file_md5 = file["dataFile"]["md5"]
                subfolder = file["directoryLabel"] if "directoryLabel" in file.keys() else ""

                fullpath = os.path.join(folder, subfolder, file_name)

                if os.path.exists(file_name) and os.path.isfile(file_name) and calcuate_md5(file_name)==file_md5: # early abort for matching md5
                    logging.info("File `{file_name}` is up to date according to md5.")
                    continue
                
                file_resp = get_file(file_id, config_obj, api_key)
                if file_resp.ok:
                    os.makedirs(os.path.dirname(fullpath), exist_ok=True)

                    with open(fullpath, "wb") as f:
                            f.write(file_resp.content)
                else:
                    logging.warn(file_resp.text)

            with open(os.path.join(folder, "info.json"), "w") as json_metadata_f:
                    metadata = dataset_resp.json()["data"]
                    json.dump(metadata, json_metadata_f, indent=4)

        else:
            logging.warn()
