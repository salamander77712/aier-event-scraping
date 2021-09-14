# AIER Event Scraper
Download 'Download Files.zip"

Unzip archive

Keep all files in same directory

Run AIER-Event--Scraper.cpython-38.pyc

## Changing Setting
### Config File
Open aier-event-scraper-config.txt

The first line is the directory of the log file

The second line is the path to the website .csv

The third line is the css selector used to find elements

The fourth line is the path to chromedriver.exe

th fifth line is how long to wait between clicks, in seconds and must be a number

The sixth line is the maximum nunber of clicks per website and must be an integer

### Using the CLI
When a config file is not present, the program will ask you for the required information

### Changing Websites
Create a new spreadsheet

Make the first column 'name'

Make the second column 'website'

Add in all names and sites

Save spreadsheet as a .csv

Change line 2 in aier-event-scraper-config.txt to .csv's path

or enter the path of the .csv when prompted in the command line

## Issues
### Browser not opening
#### With default config file:
Make sure chromedriver.exe is in the same directory as AIER-Event--Scraper.cpython-38.pyc
#### With custom config file / CLI:
Make sure the path to chromedriver.exe is correct
### Website not opening
Make sure to include 'https://' in the website addresses
### No log file
Make sure to inclue a \ at the end of the directory
### Can't find downloaded files
Files downloaded by the program are saved to your default downloads folder, not the directory with AIER-Event--Scraper.cpython-38.pyc
### Can't find any elements
Make sure that your css selector is valid
### Config file not loading
Make sure the config file is in the same directory as AIER-Event--Scraper.cpython-38.pyc

Make sure the name of the file is exactly aier-event-scraper-config.txt

Make sure to follow the guidlines in Config File
### Reading error logs
Errors are denoted with !

The number of ! indicate how serious the error is
### !
possible error

error has not casued program to miss any elements

used when the browser failes to click an element on first attempt

### !!
normal error

may have caused program to miss an element

program continues with current website

used when browser fails to click element with javasript or the website has been clicked the maximum number of times


### !!!
fatal error

causes scraping of current website to stop

used when brwoser fails to start, when browser fails to open website, or for an unknown error

### !!!?
file i/o error

used when program can't create log file

program will print logs to command line instead
