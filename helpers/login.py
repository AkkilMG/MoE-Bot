# (c) 2022-2023, Akkil MG
# License: GNU General Public License v3.0


from config import mail, password
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import random
from fake_useragent import UserAgent

async def login():
    options = Options()
    # Ensure the browser window size is set to a desktop resolution to force the PC version of the website
    # options.add_argument("--headless")
    # I am using the selenium and it automatically makes the browser of mobile, as all website interact with mobile version of website, could you please help me to make it desktop version of website. I am using the following code: 
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-web-security")
    options.add_argument("--disable-site-isolation-trials")
    options.add_argument('--log-level=1')
    options.add_argument("--lang=en")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    driver.refresh()
    def human_delay(min_delay=0.5, max_delay=2.0):
        sleep(random.uniform(min_delay, max_delay))

    try:
        human_delay()
        driver.get("https://google.com")
        
        driver.refresh()
        human_delay()
        driver.get("https://rivalregions.com")
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.NAME, 'mail')))
        if 'Rival Regions: world strategy of war and politics Create your own states in RR – simulator of politics, wars, business and media!' in driver.page_source:
            print("Login page detected")

        email_input = driver.find_element(By.NAME, 'mail')
        driver.execute_script("arguments[0].scrollIntoView(true);", email_input)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'mail')))
        email_input.send_keys(mail)
        human_delay()

        password_input = driver.find_element(By.NAME, 'p')
        driver.execute_script("arguments[0].scrollIntoView(true);", password_input)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'p')))
        password_input.send_keys(password)
        human_delay()

        login_button = driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]')
        login_button.click()
        WebDriverWait(driver, 10).until(EC.url_changes("https://rivalregions.com"))

        driver.refresh()
        cookies = driver.get_cookies()
        actual_cookie = {cookie['name']: cookie['value'] for cookie in cookies}
        # print("All Cookies:", actual_cookie)
        
        html = driver.page_source
        c_html = html.split("var c_html = '")[1].split("';")[0]
        # print(c_html)
        return { 'success': True, 'c_html': c_html, 'cookies': actual_cookie, 'driver': driver }
    except Exception as e:
        print(f"Exception occurred: {e}")
        return { 'success': False }
