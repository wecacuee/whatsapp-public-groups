# script to go through a list of whatsapp groups and join them.

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys,time,random
from selenium.webdriver.remote.remote_connection import LOGGER
import logging,os
LOGGER.setLevel(logging.WARNING)
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

# encoding=utf8 
# reload(sys)  
# sys.setdefaultencoding('utf8')
 

directory = "group_data_html/";
if not os.path.exists(directory):
    os.makedirs(directory)

# Replace below path with the absolute path
# to chromedriver in your computer

#driver = webdriver.Chrome();
driver = webdriver.Firefox()
driver.set_page_load_timeout(15) 
 
filename = sys.argv[1];
f = open(filename); # file containing the links to the whatsapp groups
lines = f.readlines();
count = 1;

driver.get("https://web.whatsapp.com");
wait = WebDriverWait(driver, 600)

time.sleep(15); # sleep for some time while I use my phone to scan the QR code

SLEEP_RANGE = (15,20)

for line in lines:
    line = line.strip().strip("/");
    group_id = line.split("/")[-1];
    print("processing", line, file=sys.stderr)
    driver.get(line);
#    try:
    for i in range(1,2):
        join_button = driver.find_element(By.CSS_SELECTOR, "#action-button");
        join_button.click();
        print("clicked join button", group_id, file=sys.stderr)
        sleep_time = random.randint(*SLEEP_RANGE);
        print("sleeping for", sleep_time, file=sys.stderr)
        time.sleep(sleep_time); # allow time for page to load
        # continue_link = driver.find_element(
        #     By.CSS_SELECTOR,
        #     'a[href="https://chat.whatsapp.com/accept?code={group_id}"]'.format(group_id=group_id))
        # continue_link.click()
        use_whatsapp_web = driver.find_element(By.PARTIAL_LINK_TEXT, "use WhatsApp Web")
        use_whatsapp_web.click()
        print("clicked 'use WhatsApp Web' button", group_id, file=sys.stderr)
        sleep_time = random.randint(*SLEEP_RANGE);
        print("sleeping for", sleep_time, file=sys.stderr)
        time.sleep(sleep_time); # allow time for page to load
        group_info = driver.find_elements(By.CSS_SELECTOR, "div[data-testid='popup-contents']");
        if not len(group_info):
            print("Unable to find group info")

            continue
        else:
            group_info = group_info[0]

        out = open(directory + "/" + group_id + ".html","w");
        print("saving info", file=sys.stderr)
        out.write(group_info.get_attribute('innerHTML') + "\n");
        out.close();
        join_group_buttons = driver.find_elements(By.CSS_SELECTOR, "div[data-testid='popup-controls-ok']");

        if not len(join_group_buttons):
            print("Unable to find 'Join Group' button")

            continue
        else:
            join_group_button = join_group_buttons[0]
        join_group_button.click()
        print ("joined group" + group_id, file=sys.stderr)


driver.close();
