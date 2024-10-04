# (c) 2022-2023, Akkil MG
# License: GNU General Public License v3.0


import os
from dotenv import load_dotenv
load_dotenv()

resourcesData = [
    0, # Gold
    3, # Oil
    4, # Ore
    11, # Uranium
    15 # Diamond
]

mail =  os.environ["mail"]
password = os.environ["password"]

# base url
base_url = os.environ["base_url"]

# user requirementz
try:
    resource = int(os.environ["resource"])
except:
    resource = 0
# regions = int(os.environ["regions"])

if 'true' in os.environ["republic"]:
    republic = True
elif 'false' in os.environ["republic"]:
    republic = False
