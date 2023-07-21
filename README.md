# Journi Travel Blog Downloader

This script facilitates the download of your personal travel blogs from the Journi app.

## Features

1. Authenticate using Journi credentials.
2. List all the trips associated with the account.
3. Download trips with their associated images.

## Prerequisites

- Python 3.x
- `requests` module (You can install it via `pip install requests`)

## Usage

### Basic Usage

```bash
python downloader.py EMAIL PASSWORD
```

Where `EMAIL` is your Journi email address and `PASSWORD` is your Journi password.

### With Custom Output Directory

```bash
python downloader.py EMAIL PASSWORD --output OUTPUT_DIR
```

Where `OUTPUT_DIR` is the directory where you wish to save the downloaded blogs. By default, blogs are saved in the `journiapp-download` directory.

### Output Structure

- The script will create a directory for each trip using the trip's URL slug.
- Inside the trip's directory, the script will save a `trip.json` file containing the trip's details.
- Images will be downloaded in the trip's directory with the format `ENTRYNUMBER_PICTURENUMBER.jpg`.

## Example

```bash
python downloader.py john@example.com mypassword --output my-trips
```

This will download all trips associated with the account `john@example.com` into the `my-trips` directory.

## Important Notes

1. This is a third-party script and is not officially affiliated with Journi.
2. Always use this script responsibly and respect the terms of service of the Journi app.
3. It is recommended to use this script for personal backup purposes only and not to distribute or misuse the downloaded content.

## Troubleshooting

1. If the script fails to login, ensure your Journi credentials are correct.
2. If the script cannot retrieve specific trips or images, it's possible that there have been changes to the Journi API or the structure of the returned data. In such cases, the script may need adjustments.

## Contribution

Feel free to fork, submit issues or pull requests on the GitHub repository.