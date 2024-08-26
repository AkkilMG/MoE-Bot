# (c) 2022-2023, Akkil MG
# License: GNU General Public License v3.0


import datetime
from config import base_url, resource, resourcesData

async def law_passer(driver, c_html, res):
    url = f"{base_url}/parliament/donew/42/{res}/0"
    
    try:
        # JavaScript code to perform the POST request within the browser context
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
        result = driver.execute_script(js_script)

        if result['success']:
            print(f"Law passed @{datetime.datetime.now()}")
            # print(result['response'])
            return { 'success': True }
        else:
            print("Failed to pass law")
            # print(result['message'])
            return { 'success': False }
    
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
