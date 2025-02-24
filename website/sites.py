import os
import requests
from PIL import Image
from io import BytesIO

website_name = ["shein.com",
"zara.com",
"nike.com",
"hm.com",
"myntra.com",
"mercari.com",
"shop.app",
"zalando.de",
"uniqlo.com",
"asos.com",
"adidas.com",
"farfetch.com",
"macys.com",
"net-a-porter.com",
"boohoo.com",
"urbanoutfitters.com",
"matchesfashion.com",
"ssense.com",
"louisvuitton.com",
"revolve.com",
"gap.com",
"zozo.jp",
 "llbean.com",
"puma.com",
"levi.com",
"bloomingdales.com",
"depop.com"]


for website in website_name:
    try:
        # Fetch the logo using Clearbit Logo API
        logo_url = f"https://logo.clearbit.com/{website}?size=800&format=png"
        response = requests.get(logo_url)
        response.raise_for_status()

        # Open the image
        img = Image.open(BytesIO(response.content))

        img.save(f"static/images/{website}.png", "PNG")
        print(f"Saved logo for {website}")
    except Exception as e:
        print(f"Failed to save logo for {website}: {e}")