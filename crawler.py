from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import os

# Global variables
GSTIN = "27AAAAP0267H2ZN"
file_name = "audio.mp3"

chrome_options = webdriver.ChromeOptions()

prefs = {
    "download.default_directory": os.getcwd(),
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True,
}

chrome_options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(options=chrome_options)

driver.get("https://services.gst.gov.in/services/searchtp")

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(
        (By.XPATH, '//div[@class="dimmer-holder"][contains(@style, "display: none;")]')
    )
)

gstin_text_box = driver.find_element(
    By.XPATH, '//input[@placeholder="Enter GSTIN/UIN of the Taxpayer"]'
)
gstin_text_box.clear()
gstin_text_box.send_keys(GSTIN)

driver.execute_script(
    "window.open('https://services.gst.gov.in/services/audiocaptcha');"
)

driver.switch_to.window(driver.window_handles[1])

driver.execute_script(
    """
    // Javascript Code to create the anchor tag and download the file
    let aLink = document.createElement("a");
    let videoSrc = document.querySelector("video").firstChild.src;
    aLink.href = videoSrc;
    aLink.download = "";
    aLink.click();
    aLink.remove();
"""
)

time.sleep(100)

driver.quit()
