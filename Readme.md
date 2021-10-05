# DaRUS data storage

Pull data from DaRUS to local folder with Python3.

Use it to organize the uploaded data of multiple datasets locally on your computer.

## How to get it running

1. Install Python3 + pip (Python package manager)
2. Install required pyDataverse packet by
   
    ```bash
    # cd to this directory
    pip install --user -r requirements.txt
    ```
3. Get your API Token on <https://darus.uni-stuttgart.de/dataverseuser.xhtml?selectTab=apiTokenTab>
4. Configure the data to download in `scripts/config.json`. The doi of each dataset is in the format `doi:10.18419/darus-????`
5. Download all data via

    ```bash
    python scripts/get_data.py
    ```