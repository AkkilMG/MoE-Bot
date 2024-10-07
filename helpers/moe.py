import datetime
import random
from time import sleep
from config import base_url, resource, resourcesData, republic
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException

MAX_RETRIES = 5  # Número máximo de intentos
RETRY_DELAY = 60  # Tiempo de espera entre intentos en segundos

async def law_passer(driver, c_html, res, law_name):
    url = f"{base_url}/parliament/donew/42/{res}/0"
    for attempt in range(MAX_RETRIES):
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
            
            def human_delay(min_delay=0.5, max_delay=2.0):
                sleep(random.uniform(min_delay, max_delay))

            if republic:
                print(f"Republic detected, moving to the parliament page (Attempt {attempt + 1})")
                driver.refresh()
                try:
                    driver.find_element(By.CSS_SELECTOR, '.item_menu.parliament_menu.ajax_action.header_menu_item.tc').click()
                except Exception:
                    driver.find_element(By.CSS_SELECTOR, '.button_link.majax.index_parliament').click()
            
            result = driver.execute_script(js_script)
            human_delay(4,10)
            
            if result['success']:
                if republic:
                    print(f"Trying to pass law: {law_name} (Attempt {attempt + 1})")
                    driver.refresh()
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.parliament_law.hov2.ib.pointer.tc')))
                    human_delay()
                    
                    # Find the specific law by its exact name
                    law_elements = driver.find_elements(By.CSS_SELECTOR, '.parliament_law.hov2.ib.pointer.tc')
                    target_law = None
                    for law in law_elements:
                        law_text = law.find_element(By.CSS_SELECTOR, '.parliament_sh1.small').text.strip()
                        if law_text == law_name:
                            target_law = law
                            break
                    
                    if target_law is None:
                        print(f"Law '{law_name}' not found (Attempt {attempt + 1})")
                        if attempt < MAX_RETRIES - 1:
                            print(f"Retrying in {RETRY_DELAY} seconds...")
                            sleep(RETRY_DELAY)
                            continue
                        else:
                            return {'success': False, 'message': 'Law not found after maximum retries'}
                    
                    # Scroll the element into view
                    driver.execute_script("arguments[0].scrollIntoView(true);", target_law)
                    human_delay()
                    
                    # Try different methods to click the element
                    try:
                        # Method 1: Regular click
                        target_law.click()
                    except ElementClickInterceptedException:
                        try:
                            # Method 2: JavaScript click
                            driver.execute_script("arguments[0].click();", target_law)
                        except:
                            # Method 3: Action chains
                            ActionChains(driver).move_to_element(target_law).click().perform()
                    
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.offer_do_vote.button_green')))
                    human_delay()
                    driver.find_element(By.CSS_SELECTOR, '.offer_do_vote.button_green').click()
                    human_delay()
                    driver.find_element(By.ID, 'slide_close').click()
                    human_delay()
                    driver.refresh()
                    print(f"Law '{law_name}' passed @{datetime.datetime.now()}")
                    return { 'success': True }
                else:
                    print(f"Law '{law_name}' passed @{datetime.datetime.now()}")
                    return { 'success': True }
            else:
                print(f"Failed to pass law: {law_name} (Attempt {attempt + 1})")
                if attempt < MAX_RETRIES - 1:
                    print(f"Retrying in {RETRY_DELAY} seconds...")
                    sleep(RETRY_DELAY)
                else:
                    return {'success': False, 'message': 'Failed to pass law after maximum retries'}
        except Exception as e:
            print(f"Exception occurred: {e} (Attempt {attempt + 1})")
            if attempt < MAX_RETRIES - 1:
                print(f"Retrying in {RETRY_DELAY} seconds...")
                sleep(RETRY_DELAY)
            else:
                return {'success': False, 'message': f'Exception occurred after maximum retries: {e}'}

async def moe(driver, c_html):
    resource_names = ["gold", "oil", "ore", "uranium", "diamond"]
    if resource == 5:
        for i in range(0, 5):
            result = await law_passer(driver, c_html, resourcesData[i], f"Resources exploration: state, {resource_names[i]} resources")
            if not result['success']:
                return { 'success': False }
    elif resource < 5:
        result = await law_passer(driver, c_html, resourcesData[resource], f"Resources exploration: state, {resource_names[resource]} resources")
        if not result['success']:
            return { 'success': False }
    return { 'success': True }

# Asegúrate de que esta línea esté al final del archivo
__all__ = ['moe', 'law_passer']