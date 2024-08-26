# (c) 2022-2023, Akkil MG
# License: GNU General Public License v3.0


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import json
from config import base_url

async def checker(driver, c_html):
    url = f"{base_url}/"
    
    # JavaScript code to perform the POST request
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
        if (text.includes('Rival Regions: world strategy of war and politics Create your own states in RR – simulator of politics, wars, business and media!')) {{
            return {{ success: false }};
        }} else {{
            return {{ success: true }};
        }}
    }})
    .catch(error => {{
        return {{ success: false, message: error }};
    }});
    '''

    # Execute the script within the browser context and retrieve the result
    result = driver.execute_script(js_script)
    return result
