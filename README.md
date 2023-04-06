# Cloudflare Cipher Management Tool

Easily manage SSL/TLS cipher suites for Cloudflare zones with this
Python script. List zones, view/update ciphers using predefined (Modern,
Compatible, Legacy) or custom lists. Features logging for tracking
changes.

## Requires: 
A subscription to CloudFlare Advanced Certificate Manager is **required** to set custom cipher suites

## Installation

1.  Clone the repository or download the *cf-set-ciphers.py* script.

2.  Set up a Python virtual environment and activate it:

    bash:  
    *python3 -m venv venv  
    source venv/bin/activate*

3.  Install the required packages:  
      
    *pip install requests*

## Usage

1.  chmod 0700 cf-set-ciphers.py
2.  Run the script:
    ./cf-set-ciphers.py [-lz -lc]
<!-- -->

1.  Follow the prompts to enter your Cloudflare API token and desired
    options.

### Script options

-   List zoneID's and their names:
    *python cf-set-ciphers.py -lz*
<!-- -->

-   List the current ciphers for the specified zone:  
      
    *python cf-set-ciphers.py -lc*

<!-- -->

-   Update the cipher list for a zone:  
      
    *python cf-set-ciphers.py*

<!-- -->

## Log file

The script logs all actions and errors to the *cf-set-ciphers.log* file
in the same directory as the script. This allows you to track changes
and troubleshoot issues if needed.
