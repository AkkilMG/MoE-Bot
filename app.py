# (c) 2022-2023, Akkil MG & Saiesh Savant
# License: GNU General Public License v3.0


import asyncio, time, datetime, pytz
from helpers import checker, moe, login

async def main():
    print('------------------- MoE-Bot -------------------')
    print('----------------------- Service Started -----------------------')
    try:
        while True:
            auth = await login()
            if auth['success'] == False:
                print('Login failed')
                return
            checked = await checker(auth['driver'], auth['c_html'])
            while checked['success']:
                print(f"--------------------------------------------")
                await moe(auth['driver'], auth['c_html'])
                time.sleep(605)
    except Exception as e:
        print(f"Exception occurred (main): {e}")
        return
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('----------------------- Service Stopped -----------------------')