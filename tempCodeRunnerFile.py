if not re.search("[a-z]|[A-Z]", captcha) and len(captcha) == 6:
#     captcha_text_box = driver.find_element(By.ID, "fo-captcha")
#     captcha_text_box.clear()
#     captcha_text_box.send_keys(captcha)