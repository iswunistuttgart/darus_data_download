# DaRUS data retreiver

Pull data from [DaRUS](https://darus.uni-stuttgart.de/), the DAta Repository of the University of Stuttgart, to a local folder with Python3.

Use it to organize the uploaded data of multiple datasets locally on your computer and to systematically integrate your open data in git repositories.

## How to get it running

1. Install [Python3](https://www.python.org/) + pip (Python package manager)
2. Clone this repository to the place you need it. If it is a git repository add it as [submodule](https://git-scm.com/book/en/v2/Git-Tools-Submodules) via
   
   ```bash
   git submodule add https://git.isw.uni-stuttgart.de/projekte/forschung/2020_dfg_slimorek/darus_data.git
   ```

3. Install required [pyDataverse](https://pydataverse.readthedocs.io/) packet by
   
    ```bash
    # cd to directory of this repository, then:
    pip install --user -r requirements.txt

    # or install directly:
    pip install --user pyDataverse
    ```

4. Create the configuration file (`scripts/config.txt`) template by running

   ```bash
    python scripts/get_data.py
   ```

5. If the dataset(s) you want to use are not (yet) public, then get your API Token on <https://darus.uni-stuttgart.de/dataverseuser.xhtml?selectTab=apiTokenTab> and fill it in `scripts/config.json`. Otherwise, leave the `'api_key'` field empty.
6. Configure the data to download in `scripts/config.json`. The doi of each dataset is in the format `doi:10.18419/darus-????` (find your own data on <https://darus.uni-stuttgart.de/dataverseuser.xhtml?selectTab=dataRelatedToMe>)
7. Download/update all data by running

    ```bash
    python scripts/get_data.py
    ```

    The metadata is also downloaded as as `info.json` in each folder 

## Directory structure

```bash
data/       # your data will appear here (in subfolders for each dataset) 
scripts/    # scripts for getting the data and adding the directory to the search path.
```

## Example config.json

For downloading two datasets

```json
{
    "dataverse_url": "https://darus.uni-stuttgart.de/",
    "api_key": "d12e77cc-267a-11ec-9621-0242ac130002",
    "datasets": [
        "doi:10.18419/darus-2177",
        "doi:10.18419/darus-2178",
    ]
}
```

## Direction/Future plans

- [ ] Make it more robust
- [ ] Allow upload of files

## Contribute

- You are welcome to contribute bugfixes directly as pull requests
- For new features or changed functionality please open an issue first, or feel free to discuss it directly. 