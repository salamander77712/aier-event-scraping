from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime
import time
import os
def load_websites(csv_path):
    name_to_websites = {}
    f = open(csv_path, 'r')
    headers = f.readline().split(',')
    website_index = -1
    university_index = -1
    for index, header in enumerate(headers):
        if 'website' in header.lower():
            website_index = index
            break
    for index, header in enumerate(headers):
        if 'university' in header.lower() or 'college' in header.lower() or 'name' in header.lower():
            university_index = index
            break
    if website_index == -1:
        raise Exception('No websites found')
    for row in f:
        entries = row.split(',')
        website = entries[website_index].replace('\n', '').strip()
        university = entries[university_index].replace('\n', '').strip()
        name_to_websites[university] = website
    f.close()
    return name_to_websites
class Fake_File:
    def __init__(self):
        pass
    def write(self, message):
        print(message.replace('\n', ''))
    def close(self):
        return
def execute_script(browser, script):
        try:
            browser.execute_script(script)
            return True
        except:
            return False
def scrape_recursive(name, website, css_selector, log_file, chrome_path, wait_time = 1, max_recursions = 100):
    def _lost_file(exception):
        nonlocal log_file
        log_file = Fake_File()
        log_file.write('\tLost connection to file')
        log_file.write('\tPrinting logs to command line')
        log_file.write('\t' + str(exception))
    try:
        log_file.write('Starting scraping of ' + name + '\n')
        log_file.write('\tOpening browser\n')
    except Exception as e:
        _lost_file(e)
    try:
        browser = Chrome(chrome_path)
        try:
            log_file.write('\t\tSuccessfullty opened browser\n')
        except Exception as e:
            _lost_file(e)
    except Exception as e:
        try:
            log_file.write('\t\t!!!Failed to open browser, check path to chrome driver\n')
            log_file.write('\t\t' + str(e) + '\n')
            log_file.write('\t\tEnding scraping of ' + name + '\n')
        except Excpetion as e2:
            _lost_file(e2)
        browser.close()
        return
    log_file.write('\tAttempting to open ' + website + '\n')
    try:
        browser.get(website)
        try:
            log_file.write('\t\tSuccesfully opened ' + website + '\n')
        except Exception as e:
            _lost_file(e)
    except Exception as e:
        try:
            log_file.write('\t\t!!!Failed to open ' + website + ', check URL and internet connection\n')
            log_file.write('\t\t' + str(e) + '\n')
            log_file.write('\t\tEnding scraping of ' + name + '\n')
        except Excpetion as e2:
            _lost_file(e2)
        browser.close()
        return
    url_to_current_link = {
        browser.current_url : 0
    }
    def _find_links_and_click(recursions):
        if recursions <= 0:
            try:
                log_file.write('\t\t!!?Max recursions reached\n')
            except Exception as e:
                _lost_file(e)
            return
        if browser.current_url == 'data:,':
            try:
                log_file.write('\t\tAll links found\n')
            except Exception as e:
                _lost_file(e)
            return
        link_index = url_to_current_link[browser.current_url]
        try:
            log_file.write('\t\tLooking for event links on ' + browser.current_url + ' by ' + css_selector + '\n')
        except Exception as e:
            _lost_file(e)
        try:
            links =  WebDriverWait(browser, 3).until(lambda d: d.find_elements_by_css_selector(css_selector))
            try:
                log_file.write('\t\t\tFound ' + str(len(links)) + ' matching links\n')
            except Exception as e:
                _lost_file(e)
        except Exception as e:
            try:
                log_file.write('\t\t\t!??Failed to find any links\n')
                log_file.write('\t\t\t' + str(e) + '\n')
                log_file.write('\t\t\tGoing back\n')
            except Exception as e2:
                _lost_file(e)
            browser.back()
            _find_links_and_click(recursions - 1)
        if len(links) > link_index:
            url_to_current_link[browser.current_url] += 1
            try:
                log_file.write('\t\tAttempting to click on link ' + str(link_index) + ' on ' + browser.current_url + '\n')
            except Exception as e:
                _lost_file(e)
            try:
                links[link_index].click()
                time.sleep(wait_time)
                try:
                    log_file.write('\t\t\tSuccessfully clicked on link\n')
                except Exception as e:
                    _lost_file(e)
            except Exception as e:
                try:
                    log_file.write('\t\t\t!??Failed to click on link\n')
                    log_file.write('\t\t\t' + str(e) + '\n')
                    log_file.write('\t\t\tAttempting to click link using javascript\n')
                except Exception as e2:
                    _lost_file(e2)
                try:
                    javaScript = "document.querySelectorAll('" + css_selector + "')[" + str(link_index) + "].click();"
                    WebDriverWait(browser, 5).until(lambda d: execute_script(browser, javaScript))
                    try:
                        log_file.write('\t\t\t\tSuccessfully clicked link\n')
                    except Exception as e2:
                        _lost_file(e2)
                except Exception as e2:
                    try:
                        log_file.write('\t\t\t\t!!?Failed to click link\n')
                        log_file.write('\t\t\t\t' + str(e2) + '\n')
                        log_file.write('\t\t\t\tContinuing\n')
                    except Exception as e3:
                        _lost_file(e3)
                    _find_links_and_click(recursions - 1)
            if browser.current_url not in url_to_current_link.keys():
                try:
                    log_file.write('\t\t' + browser.current_url + ' not yet discovered\n')
                    log_file.write('\t\tAdding new URL\n')
                except Excetion as e:
                    _lost_file(e)
                url_to_current_link[browser.current_url] = 0
        else:
            try:
                log_file.write('\t\tNo more links on this page\n')
                log_file.write('\t\tGoing back\n')
            except Exception as e:
                _lost_file(e)
            browser.back()
        _find_links_and_click(recursions - 1)
    _find_links_and_click(max_recursions)
    try:
        log_file.write('\tScraping of ' + name + ' finished\n')
    except Excpetion as e:
        _lost_file(e)
    browser.close()
def scrape_all(log_file_path, websites, css_selector, chrome_path, wait_time, max_recursions):
    try:
        now = datetime.now()
        f = open(log_file_path + 'AIER Event Scraping Utility Started at ' + now.strftime("%d-%m-%Y @ %H;%M;%S") +'.log','a')
    except Exception as e:
        print('!!!?Failed to create log file')
        print('Printing log file to console')
        print(e)
        f = Fake_File()
    for name, website in websites.items():
        try:
            scrape_recursive(name, website, css_selector, f, chrome_path, wait_time, max_recursions)
        except Exception as e:
            f.write('!!!Scraping of ' + name + ' failed\n')
            f.write(str(e) + '\n')
    f.close()
def check_chrome_path(path):
    browser = Chrome(path)
    browser.close()
def check_log_file_path(path):
    f = open(path + 'test.txt', 'a')
    f.close()
    os.remove(path + 'test.txt')
def command_line_interface():
    print('Enter css selector:')
    time.sleep(0.25)
    css_selector = input()
    while True:
        print('Enter path to .csv with instititute name and website:')
        csv_path = input()
        csv_path = csv_path.replace('"','')
        print('Loading websites...')
        try:
            websites = load_websites(csv_path)
            print('Websites loaded')
            break
        except Exception as e:
            print('Website loading failed')
            print(e)
    while True:
        print('Enter path to chromedriver:')
        chrome_path = input()
        chrome_path = chrome_path.replace('"','')
        try:
            check_chrome_path(chrome_path)
            print('Chromedriver loaded')
            break
        except Exception as e:
            print('Chromedriver loading failed')
            print(e)
    while True:
        print('Enter path for log file:')
        log_file_path = input()
        log_file_path = log_file_path.replace('"','') + '\\'
        try:
            check_log_file_path(log_file_path)
            print('Log file path accepted')
            break
        except Exception as e:
            print('Log file rejected')
            print(e)
    while True:
        print('Enter wait time between click (in seconds, must be a number):')
        try:
            wait_time = float(input())
            break
        except Exception as e:
            print('Input must be a number')
            print(e)
    while True:
        print('Enter maximum number of clicks per website (must be an integer):')
        try:
            max_recursions = int(input())
            break
        except Exception as e:
            print('Input must be an integer')
    print('Running program...')
    scrape_all(log_file_path, websites, css_selector, chrome_path, wait_time, max_recursions)
    print('Done')
def find_config_file():
    try:
        f = open('aier-event-scraper-config.txt')
        print('Config file found')
        log_file_path = f.readline().replace('\n','').replace('"','')
        print('log file: ' + log_file_path)
        csv_path = f.readline().replace('\n','').replace('"','')
        print('csv: ' + csv_path)
        websites = load_websites(csv_path)
        css_selector = f.readline().replace('\n','')
        print('css selector: ' + css_selector)
        chrome_path = f.readline().replace('\n','').replace('"','')
        print('chrome path' + chrome_path)
        wait_time = float(f.readline())
        print('wait time: ' + str(wait_time))
        max_recursions = int(f.readline())
        print('max rescursions: ' + str(max_recursions))
        scrape_all(log_file_path, websites, css_selector, chrome_path, wait_time, max_recursions)
    except Exception as e:
        print(e)
        command_line_interface()
find_config_file()
