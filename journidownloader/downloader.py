#!/usr/bin/python3
# Journiapp Travel Blog Downloader

# Expect email address and password as CLI arguments

import argparse
import os
import sys
import time
from requests import Session
import pathlib

# Parse arguments
parser = argparse.ArgumentParser(description='Journiapp Travel Blog Downloader')
parser.add_argument('email', help='Journi email address')
parser.add_argument('password', help='Journi password')
parser.add_argument('--output', help='Output directory', default='journiapp-download', type=pathlib.Path, metavar='DIR')

args = parser.parse_args()

# Create session
s = Session()

# Request https://www.journiapp.com/app/login to get CSRF token, session cookie
LOGIN_URL = 'https://www.journiapp.com/app/login'
r = s.get(LOGIN_URL)

# Simulate XHR to https://www.journiapp.com/api/v8.0/user/login to do the login
LOGIN_API_URL = 'https://www.journiapp.com/api/v8.0/user/login'
r = s.post(LOGIN_API_URL, json={'email': args.email, 'password': args.password})

# Check if login was successful
if r.status_code != 200:
    print('Login failed')
    sys.exit(1)

# List profile, including existing trips
PROFILE_URL = 'https://www.journiapp.com/api/v8.0/user/profile'
r = s.get(PROFILE_URL)

# Check if profile was successfully retrieved
if r.status_code != 200:
    print('Profile retrieval failed')
    sys.exit(1)

# Get profile data
profile = r.json()

# Show some information (nicely formatted): user's name, list all trips.
print(f"User: {profile['firstName']} {profile['lastName']}")

for trip in profile['trips']:
    print(f" - {trip['title']}")

def download_picture(picture_id, target_path):
    # If the target file already exists and is not empty, skip
    if target_path.exists() and target_path.stat().st_size > 0:
        return

    # Define the picture's URL
    PICTURE_URL = f"https://www.journiapp.com/picture/{picture_id}_mob_full.jpg"

    # Download the picture
    r = s.get(PICTURE_URL)

    # Check if picture was successfully retrieved
    if r.status_code != 200:
        print(f"Picture {picture_id} retrieval failed")
        return
    
    # Save the picture to a file
    with open(target_path, 'wb') as f:
        f.write(r.content)

def download_trip(trip_info):
    # Define the output directory using the trip's url slug (called "url")
    output_dir = args.output / trip_info['url']

    # Create the output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)

    # Get the trip's details
    TRIP_URL = f"https://www.journiapp.com/api/v7.9/trip/url/{trip_info['url']}/entries/0"

    r = s.get(TRIP_URL)

    # Check if trip details were successfully retrieved
    if r.status_code != 200:
        print(f"Trip {trip_info['url']} retrieval failed")
        return

    # Save the JSON response to a file
    with open(output_dir / 'trip.json', 'w') as f:
        f.write(r.text)

    details = r.json()

    # Download the title picture
    download_picture(details['trip']['pictureGuid'], output_dir / '00_title.jpg')

    for entry_id, entry in enumerate(reversed(details['entries'])):
        # download all the pictures in the entry to files named 00_00.jpg, 00_01.jpg, ..., where the first number is the 
        # entry number and the second number is the picture number.
        for picture_id, picture in enumerate(entry['pictures']):
            download_picture(picture['guid'], output_dir / f"{entry_id:02}_{picture_id:02}.jpg")


# Download all trips
for trip in profile['trips']:
    download_trip(trip)

