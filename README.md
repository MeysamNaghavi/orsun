# orsun scraper
[![app icon](https://s6.uupload.ir/files/_f9317f49d82a58ded15b4e5d_d862.png)](http://orsun.ir/)

## How it works:
This is a simple program that can use Python and Selenium library to extract classroom data from the university website and store it in the database.
The university site is a dynamic site that is very badly designed and is not available most of the time.therefore, this robot can work to collect the time of classes.

## Requirements:
#### Python:
You must have [Python](https://www.python.org/) installed.
#### Geckodriver:
Go to the [geckodriver releases page](https://github.com/mozilla/geckodriver/releases). Find the latest version of the driver for your platform and download it , then you should either have it in the PATH of your system or put it next to the project files.
#### Config:
In order for the scraper to enter the site, the username and password and url of site must be defined in the [orsun.py](https://github.com/MeysamNaghavi/orsun/blob/master/orsun.py) file. like this:
```python
config = {
    'password': MY_USERNAME,
    'username': MY_PASS,
    'site_url': 'http://89.43.5.10/orsun/',
    'tables_name': db.get_tables_name(),
}
```
#### Config telegram_bot (optional if you want):
- `BOT_TOKEN` - Get it by contacting to [BotFather](https://t.me/botfather)
- `API_KEY` - and put it on [tgbot.py](https://github.com/MeysamNaghavi/orsun/blob/master/tgbot.py) like this:
```python
# api
API_KEY = 'uhfaq24378huighfsf_get_from_BotFather'
```
## Installation
- Clone this git repository.
```sh 
git clone https://github.com/MeysamNaghavi/orsun.git
```
- Change Directory
```sh 
cd orsun
```
- Install requirements with pip3
```sh 
pip3 install -r requirements.txt
```
