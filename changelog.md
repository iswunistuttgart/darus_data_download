# Changelog

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.0] - 2024-06-11

Used an incompatibility with the DaRUS update to 6.2 to clean up a little.

- **Replaced** dependency on `pyDataverse` by direct API calls using the `requests` package
  - Removed dependency to `pyDataverse`
  - Added dependency to `requests`
- **Added** version to download for each dataset in `config.json`, i.e.
    ```json
    [{"doi": "doi:10.18419/darus-????", "version": "latest"},
    {"doi": "doi:10.18419/darus-????", "version": "1.0"},
    ```
    The old format is still accepted, but support may be removed in a future version.
- **Added** check for md5 hash before downloading a file from the server. Download only, if file has changed. This should speed up incremental downloads, where only some files were added.
- **Added** program help:
    ```sh
    python scripts/get_data.py -h
    # or
    python scripts/get_data.py --help
    ```
- **Added** possibility to add logging level to program call, e.g.
    ```sh
    python scripts/get_data.py -log info
    ```
- **Updated** `Reamde.md`


