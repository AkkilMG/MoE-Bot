# (c) 2022-2023, Akkil MG
# License: GNU General Public License v3.0


import datetime
import random
from time import sleep
from config import base_url, resource, resourcesData, republic
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

async def law_passer(driver, c_html, res):
    url = f"{base_url}/parliament/donew/42/{res}/0"
    try:
        js_script = f'''
        return fetch('{url}', {{
            method: 'POST',
            headers: {{
                'Content-Type': 'application/x-www-form-urlencoded',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }},
            body: new URLSearchParams({{ 'c': '{c_html}' }})
        }})
        .then(response => response.text())
        .then(text => {{
            return {{ success: true, response: text }};
        }})
        .catch(error => {{
            return {{ success: false, message: error }};
        }});
        '''
        # Execute the script within the browser context
        def human_delay(min_delay=0.5, max_delay=2.0):
            sleep(random.uniform(min_delay, max_delay))

        if republic:
            print("Republic detected, moving to the parliament page")
            driver.refresh()
            try:
                driver.find_element(By.CSS_SELECTOR, '.item_menu.parliament_menu.ajax_action.header_menu_item.tc').click()
            except Exception:
                driver.find_element(By.CSS_SELECTOR, '.button_link.majax.index_parliament').click()
            # human_delay()
        result = driver.execute_script(js_script)
        human_delay(4,10)
        if result['success']:
            if republic:
                try:
                    print("Trying to pass law")
                    driver.refresh()
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.parliament_law.ib.pointer.tc'))) # mslide parliament_law ib pointer tc
                    human_delay()
                    driver.find_element(By.CSS_SELECTOR, '.parliament_law.hov2.ib.pointer.tc').click()
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.offer_do_vote.button_green')))
                    human_delay()
                    driver.find_element(By.CSS_SELECTOR, '.offer_do_vote.button_green').click()
                    human_delay()
                    driver.find_element(By.ID, 'slide_close').click()
                    human_delay()
                    driver.refresh()
                    print(f"Law passed @{datetime.datetime.now()}")
                    return { 'success': True }
                except Exception as e:
                    print(e)
                    return { 'success': False }
            else:
                print(f"Law passed @{datetime.datetime.now()}")
                return { 'success': True }
        else:
            print("Failed to pass law")
            return { 'success': False }
            # print(result['response'])
    except Exception as e:
        print(f"Exception occurred: {e}")
        return { 'success': False }

async def moe(driver, c_html):
    if resource == 5:
        for i in range(0, 5):
            result = await law_passer(driver, c_html, resourcesData[i])
            if not result['success']:
                return { 'success': False }
    elif resource < 5:
        result = await law_passer(driver, c_html, resourcesData[resource])
        if not result['success']:
            return { 'success': False }
    return { 'success': True }
