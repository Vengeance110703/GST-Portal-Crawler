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
GSTIN = "27AAFCI3309E1ZV"

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
    captcha = captcha.replace(".", "")
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

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "tbl-format"))
)

with open("page_source.html", "w") as fs:
    fs.write(driver.page_source)

main_table = driver.find_element(By.CLASS_NAME, "tbl-format")
rows = main_table.find_elements(By.XPATH, "div")

# Row 1
row_1 = rows[0].find_element(By.XPATH, "div")
columns = row_1.find_elements(By.XPATH, "div")
legal_name = columns[0].find_elements(By.XPATH, "p")[1].text
trade_name = columns[1].find_elements(By.XPATH, "p")[1].text
effective_date_registration = columns[2].find_elements(By.XPATH, "p")[1].text
print(legal_name)
print(trade_name)
print(effective_date_registration)

# Row 2
row_2 = rows[1].find_element(By.XPATH, "div")
columns = row_2.find_elements(By.XPATH, "div")
constitution_business = columns[0].find_elements(By.XPATH, "p")[1].text
gstin_status = columns[1].find_elements(By.XPATH, "p")[1].text
taxpayer_type = columns[2].find_elements(By.XPATH, "p")[1].text
print(constitution_business)
print(gstin_status)
print(taxpayer_type)

# Row 3
row_3 = rows[2].find_element(By.XPATH, "div")
columns = row_3.find_elements(By.XPATH, "div")
# constitution_business = columns[0].find_elements(By.XPATH, "p")[1].text
# gstin_status = columns[1].find_elements(By.XPATH, "p")[1].text
principal_place_business = columns[2].find_elements(By.XPATH, "p")[1].text
print(principal_place_business)

# Row 4
row_4 = rows[3].find_element(By.XPATH, "div")
columns = row_4.find_elements(By.XPATH, "div")
aadhar_authenticated = columns[0].find_elements(By.XPATH, "p")[1].text
e_kyc = columns[1].find_elements(By.XPATH, "p")[1].text
print(aadhar_authenticated)
print(e_kyc)

time.sleep(20)

driver.quit()
