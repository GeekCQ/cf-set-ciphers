#!/usr/bin/env python

"""
cf-set-ciphers.py

This script allows you to set or list ciphers on a Cloudflare zone.
It provides options to list all zones, list the current ciphers for a specific zone, or update the ciphers for a specific zone.
It supports predefined cipher lists (Modern, Compatible, and Legacy) and custom cipher lists.

Usage:
  - List all zones: python cf-set-ciphers.py --list-zones
  - List current ciphers for a zone: python cf-set-ciphers.py --list-current
  - Update ciphers for a zone: python cf-set-ciphers.py
"""
import argparse
import requests
import getpass
import logging
from datetime import datetime

# Set up argparse
parser = argparse.ArgumentParser(description="Set or list ciphers on a Cloudflare zone.")
parser.add_argument("-lc", "--list-current", action="store_true", help="List the current ciphers for the zone.")
parser.add_argument("-lz", "--list-zones", action="store_true", help="List zones and their names.")
args = parser.parse_args()

# Configure logging
logging.basicConfig(
    filename="cf-set-ciphers.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Prompt for API Token
api_token = getpass.getpass("Please enter your Cloudflare API Token: ")

headers = {
    "Authorization": f"Bearer {api_token}",
    "Content-Type": "application/json",
}

if args.list_zones:
    url = "https://api.cloudflare.com/client/v4/zones"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        zones = response.json()["result"]
        print("Zones:")
        for zone in zones:
            print(f"{zone['id']} - {zone['name']}")
    else:
        print(f"Failed to list zones. Error: {response.status_code} - {response.text}")

elif args.list_current:
    zone_id = input("Please enter the zone ID: ")
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/settings/ciphers"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        cipher_list = response.json()["result"]["value"]
        print("Current cipher list for the zone:")
        print(", ".join(cipher_list))
    else:
        print(f"Failed to get the current cipher list. Error: {response.status_code} - {response.text}")

else:
    # Prompt for zone and desired cipher list
    zone_id = input("Please enter the zone ID: ")
    cipher_choice = input("Please enter the desired cipher list (Modern, Compatible, Legacy, or Custom): ")

    # Log the inputs
    logging.info(f"Zone ID: {zone_id}")
    logging.info(f"Cipher choice: {cipher_choice}")

    # Define default cipher settings
    cipher_settings = {
        "Modern": {
            "description": "Offers best security and performance, limiting your range of clients to modern devices and browsers. Supports TLS 1.2-1.3 cipher suites. All suites are forward-secret and support authenticated encryption (AEAD).",
            "ciphers": ["ECDHE-ECDSA-AES128-GCM-SHA256", "ECDHE-ECDSA-CHACHA20-POLY1305", "ECDHE-RSA-AES128-GCM-SHA256", "ECDHE-RSA-CHACHA20-POLY1305", "ECDHE-ECDSA-AES256-GCM-SHA384", "ECDHE-RSA-AES256-GCM-SHA384"],
        },
        "Compatible": {
            "description": "Provides broader compatibility with somewhat weaker security. Supports TLS 1.2-1.3 cipher suites. All suites are forward-secret.",
            "ciphers": ["ECDHE-ECDSA-AES128-GCM-SHA256", "ECDHE-ECDSA-CHACHA20-POLY1305", "ECDHE-RSA-AES128-GCM-SHA256", "ECDHE-RSA-CHACHA20-POLY1305", "ECDHE-ECDSA-AES256-GCM-SHA384", "ECDHE-RSA-AES256-GCM-SHA384", "ECDHE-ECDSA-AES128-SHA256", "ECDHE-RSA-AES128-SHA256", "ECDHE-ECDSA-AES256-SHA384", "ECDHE-RSA-AES256-SHA384"],
        },
        "Legacy": {
            "description": "NOT RECOMMENDED - Includes all cipher suites that Cloudflare supports today. Broadest compatibility with the weakest security. Supports TLS 1.0-1.3 cipher suites.",
            "ciphers": ["ECDHE-ECDSA-AES128-GCM-SHA256", "ECDHE-ECDSA-CHACHA20-POLY1305", "ECDHE-RSA-AES128-GCM-SHA256", "ECDHE-RSA-CHACHA20-POLY1305", "ECDHE-ECDSA-AES256-GCM-SHA384", "ECDHE-RSA-AES256-GCM-SHA384", "ECDHE-ECDSA-AES128-SHA256", "ECDHE-RSA-AES128-SHA256", "ECDHE-ECDSA-AES256-SHA384", "ECDHE-RSA-AES256-SHA384", "ECDHE-ECDSA-AES128-SHA", "ECDHE-RSA-AES128-SHA", "AES128-GCM-SHA256", "AES128-SHA256", "AES128-SHA", "ECDHE-RSA-AES256-SHA", "AES256-GCM-SHA384", "AES256-SHA256", "AES256-SHA", "DES-CBC3-SHA"],
        }
    }

    if cipher_choice.lower() == "custom":
        cipher_list = input("Please enter the custom cipher list (comma-separated): ").split(",")
    else:
        cipher_list = cipher_settings.get(cipher_choice.capitalize())

    if not cipher_list:
        print("Invalid cipher choice. Please try again.")
        logging.error("Invalid cipher choice.")
    else:
        # Extract the list of ciphers from the dictionary
        cipher_list = cipher_settings.get(cipher_choice.capitalize())["ciphers"]

        # Print the selected ciphers
        print(f"Selected ciphers: {cipher_list}")

        # Set the cipher list for the zone
        url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/settings/ciphers"
        data = {
            "value": cipher_list,
        }
        response = requests.patch(url, headers=headers, json=data)

        if response.status_code == 200:
            print("Successfully updated the cipher list for the zone.")
            logging.info("Successfully updated the cipher list for the zone.")
        else:
            print(f"Failed to update the cipher list. Error: {response.status_code} - {response.text}")
            logging.error(f"Failed to update the cipher list. Error: {response.status_code} - {response.text}")

