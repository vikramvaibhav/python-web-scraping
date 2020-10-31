from pathlib import Path
import datetime
import requests as req
import csv
import logging
import pandas as pd
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from .config import BASE_DIR

CURR_DIR = Path.cwd()


def get_session():
    with req.Session() as se:
        se.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
            'Accept-Encoding': 'gzip, deflate',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en'
        }
        return se
# def_end


def get_chrome_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    return webdriver.Chrome(chrome_options=chrome_options)
# def_end


# def get_chrome_driver():
#     try:
#         chrome_options = Options()
#         chrome_options.add_argument("--headless")
#         return webdriver.Chrome(chrome_options=chrome_options)
#     except:
#         print('''ChromeDriver is not installed on sysytem. Use this link(https://chromedriver.chromium.org/downloads) to download latest ChromeDriver''')
# # def_end


def get_logger(site):
    logger = logging.getLogger(__name__)
    formatter = logging.Formatter(
        '%(levelname)s:%(asctime)s:%(name)s:%(message)s')
    if not Path(CURR_DIR / 'logfiles').exists():
        Path.mkdir(CURR_DIR / 'logfiles')
    file_handler = logging.FileHandler('logfiles/%s.log' % site)
    file_handler.setLevel(logging.ERROR)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


def csv2xl(csvFilename, site):
    # function reads csv file as data frame and then writes to a xlsx file
    df = pd.read_csv('scraping_output/%s/%s' % (site, csvFilename))
    xlFilename = csvFilename.replace('.csv', '.xlsx')
    df.to_excel('scraping_output/%s/%s' % (site, xlFilename), index=False)
# def_end


def writeval(s):
    try:
        return noascii(s.text)
    except Exception as e:
        print('exception', e)
        return ''
# def_end


def noascii(text):
    return ''.join([i if ord(i) < 128 else ' ' for i in text])
# def_end


def makedirs(site):
    if not Path.exists(BASE_DIR / 'scraping_output'):
        Path.mkdir(BASE_DIR / 'scraping_output')
    if not Path.exists(BASE_DIR / 'scraping_output' / site):
        Path.mkdir(BASE_DIR / 'scraping_output' / site)
    # if not Path.exists('scraping_output/%s/images/' % site):
    #     Path.mkdir('scraping_output/%s/images/' % site)
# def_end


# function for writing data into a JSON file
def write_json(fname, sitename):
    jsonfile = open(str(BASE_DIR)+'/scraping_output/' +
                    sitename+'/%s.json' % fname, 'a')
    reader = csv.DictReader(
        open(str(BASE_DIR)+'/scraping_output/'+sitename+'/%s.csv' % fname))
    for row in reader:
        jsonfile.write(json.dumps(row)+'\n')
# def_end


# function to read JSON Data
def read_json(fname):
    with open(fname) as f:
        data = json.load(f)
    return data
# end of def


# write csv
def write_csv(fname, column_names):
    df = pd.DataFrame(columns=column_names)
    df.to_csv(fname, index=False, header=True)
# end_of_def


# function to initialize column names
def initialize(site):
    folder = site
    fname = site+'_'+str(datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
    infod = read_json(str(BASE_DIR)+"/core/initial.json")
    column_names = read_json(str(BASE_DIR)+"/core/column_names.json")
    write_csv(str(BASE_DIR)+'/scraping_output/' +
              folder+'/'+fname+'.csv', column_names)
    return fname, infod, column_names
# def_end
