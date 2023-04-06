# Cloudflare Cipher Management Tool

Easily manage SSL/TLS cipher suites for Cloudflare zones with this
Python script. List zones, view/update ciphers using predefined (Modern,
Compatible, Legacy) or custom lists. Features logging for tracking
changes.

## Installation

1.  Clone the repository or download the *cf-set-ciphers.py* script.

2.  Set up a Python virtual environment and activate it:

    bash:  
    *python3 -m venv venv  
    source venv/bin/activate*

3.  Install the required packages:  
      
    *pip install requests*

## Usage

1.  Run the script:

<!-- -->

1.  Follow the prompts to enter your Cloudflare API token and desired
    options.

### Script options

-   List zones and their names:

<!-- -->

-   List the current ciphers for the specified zone:  
      
    *python cf-set-ciphers.py -lc*

<!-- -->

-   Update the cipher list for the specified zone:  
      
    *python cf-set-ciphers.py*

<!-- -->

## Log file

The script logs all actions and errors to the *cf-set-ciphers.log* file
in the same directory as the script. This allows you to track changes
and troubleshoot issues if needed.
