import json
import os
import sys
import unicodedata
import re

from pyDataverse.api import DataAccessApi, NativeApi
from pyDataverse.models import Dataverse
from pyDataverse.models import Dataset


def get_script_path() -> str:
    return os.path.dirname(os.path.realpath(sys.argv[0]))

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
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')

if __name__ == "__main__":
    with open(os.path.join(get_script_path(),'config.json'), 'r') as config_file:
        config_txt = config_file.read()

    config_obj = json.loads(config_txt)
    #print(json.dumps(config_obj, indent=4))

    api_key = ''
    with open(os.path.join(get_script_path(),'.apikey'), 'r') as api_file:
        api_key = api_file.read()
        # todo: verify api_key format

    api = NativeApi(config_obj["dataverse_url"], api_token=api_key)
    data_api = DataAccessApi(config_obj["dataverse_url"], api_token=api_key)
    
    for dataset_identifier in config_obj['datasets']:
        dataset_ref = api.get_dataset(dataset_identifier)
        #print(json.dumps(dataset_ref.json(), indent=4))
        if dataset_ref.json()['status'] == 'OK':
            dataset = Dataset(dataset_ref.json()['data'])
            #print(dataset.get()["title"])

            citation_info = dataset.get()['latestVersion']['metadataBlocks']['citation']['fields']
            title = ''
            for c in citation_info:
                if c['typeName'] == "title":
                    title = c['value']
                    break
            folder_name  = slugify(title) # extract from JSON
            folder = os.path.join(get_script_path(), '../data', folder_name)
            try:
                os.mkdir(folder)
            except FileExistsError:
                print('Folder exists')

            files_list = dataset_ref.json()['data']['latestVersion']['files']

            for file in files_list:
                filename = file["dataFile"]["filename"]
                file_id = file["dataFile"]["id"]
                response = data_api.get_datafile(file_id)
                with open( os.path.join(folder, filename), "wb") as f:
                    f.write(response.content)

            with open( os.path.join(folder, 'info.json'), "w") as json_metadata_f:
                metadata = dataset_ref.json()['data']
                json.dump(metadata, json_metadata_f, indent=4)
