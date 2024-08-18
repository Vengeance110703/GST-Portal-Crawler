from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import whisper
from os import path
import os
import re

# Global variables
GSTIN = "27AAAAP0267H2ZN"

chrome_options = webdriver.ChromeOptions()

download_dir = os.getcwd()
AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "audiocaptcha.mp3")

prefs = {
    "download.default_directory": download_dir,
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

captcha = ""

while True:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "video"))
    )

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

    model = whisper.load_model("base.en")
    result = model.transcribe(AUDIO_FILE)

    captcha = result["text"]
    captcha = captcha.replace(" ", "")
    captcha = captcha.replace(",", "")
    print(captcha)

    os.remove("audiocaptcha.mp3")

    driver.switch_to.window(driver.window_handles[0])

    if not re.search("[a-z]|[A-Z]", captcha) and len(captcha) == 6:
        break
    else:
        refresh_captcha_button = driver.find_element(
            By.XPATH,
            "//button[@type='button' and @ng-click='refreshCaptcha()' and @ng-disabled='playingCap']",
        )
        refresh_captcha_button.click()
        driver.switch_to.window(driver.window_handles[1])
        driver.refresh()

captcha_text_box = driver.find_element(By.ID, "fo-captcha")
captcha_text_box.clear()
captcha_text_box.send_keys(captcha)

search_button = driver.find_element(By.XPATH, "//button[@type='submit']")
search_button.click()

time.sleep(20)

driver.quit()
