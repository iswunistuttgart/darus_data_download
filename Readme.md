# DaRUS data retreiver

Pull data from [DaRUS](https://darus.uni-stuttgart.de/), the Data Repository of the University of Stuttgart, to a local folder (`./data`) with Python3.

Use it to organize the data of multiple datasets locally on your computer and to integrate your open data in git repositories.

- [DaRUS data retreiver](#darus-data-retreiver)
  - [How to get it running](#how-to-get-it-running)
    - [Where does get\_data.py look for darus\_config.json and .darus\_apikey files?](#where-does-get_datapy-look-for-darus_configjson-and-darus_apikey-files)
  - [Example `darus_config.json`](#example-darus_configjson)
    - [A quick note about versions:](#a-quick-note-about-versions)
  - [Direction/Future plans](#directionfuture-plans)
  - [Contribute](#contribute)

## How to get it running

1. Install [Python3](https://www.python.org/) + pip (Python package manager)
2. Clone this repository to the place you need it. If it is a git repository add it as [submodule](https://git-scm.com/book/en/v2/Git-Tools-Submodules) via
   
   ```bash
   git submodule add https://github.com/iswunistuttgart/darus_data_download.git
   ```

3. Install required package requests (to make HTTP requests to the REST API):
   
    ```bash
    # cd to directory of this repository, then:
    pip install --user -r requirements.txt
    ```

4. Create the configuration file (`scripts/darus_config.json`) template by running

   ```bash
    python scripts/get_data.py
   ```

5. If the dataset(s) you want to use are not (yet) public, then get your API Token on <https://darus.uni-stuttgart.de/dataverseuser.xhtml?selectTab=apiTokenTab> and fill it in a file named`.darus_apikey`. **Warning:** never check in your api_key via git! Within this repository it is added to .gitignore
6. Configure the data to download in `scripts/darus_config.json`. The doi of each dataset is in the format `doi:10.18419/darus-????` (find your own data on <https://darus.uni-stuttgart.de/dataverseuser.xhtml?selectTab=dataRelatedToMe>)
7. If you are using this module as submodule: move the `darus_config.json` file to the directory above this repository and check it in with your parent git project to keep data configuration reproducible 
8. Download/update all data by running

    ```bash
    python scripts/get_data.py
    ```

    The metadata is also downloaded as as `info.json` in each folder 

### Where does get_data.py look for darus_config.json and .darus_apikey files?

1. in `./scripts/` (directory of `get_data.py`)
2. in `./` (the parent directory, where `Readme.md` is located)
3. in `../` (one directory above this project)


## Example `darus_config.json`

For downloading two datasets

```json
{
    "dataverse_url": "https://darus.uni-stuttgart.de/",
    "datasets": [
        {"id": "doi:10.18419/darus-1234", "version": "latest"},
        {"id": "doi:10.18419/darus-1235", "version": "2.0"}
    ]
}
```

### A quick note about versions:

To have reproducible results you should refer to a fixed version after the repository was published. Otherwise the data may change on repository updates.

Latest (`"version": "latest"`) is the default setting, will also use unpublished versions. You can also use a version number or any string of the version descriptions given [here](https://guides.dataverse.org/en/6.2/api/dataaccess.html#download-by-dataset-by-version)

## Direction/Future plans

- [ ] Handle ENV variables(especially for API key) to use it in Docker, etc.
- [ ] Make it more robust against failure/misconfiguration
- [ ] Allow upload of files (maybe use [pyDaRUS](https://github.com/JR-1991/pyDaRUS))
- [x] Allow specifying version

## Contribute

- You are welcome to contribute bugfixes directly as pull requests
- For new features or changed functionality please open an issue first, or feel free to discuss it directly. 
