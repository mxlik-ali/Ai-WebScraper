import google.generativeai as genai
import pathlib
import textwrap
import google.generativeai as genai
from IPython.display import display
from IPython.display import Markdown
import PIL.Image
import urllib.request 
from PIL import Image
from dotenv import load_dotenv
import os

# with open('image.png','rb')as f:
#     image = f.read()

image = PIL.Image.open('./image_saves/combined_screenshots.jpg')

load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel("gemini-pro-vision")
# response = model.generate_content(image)
response = model.generate_content(
    ['''U are a webscraper that uses vision pro api to scrape the message content.
                            Now scrape the page and make sure to give a response in json format, And do maintain the heirarchy
                            Even remember to skit the contet that occurs twice or thrice in terms of data cleaning
                            Please provide me full webscaping do not leave any content''', image],
    stream=True
)
response.resolve()
print(response.text)

# import asyncio
# from pyppeteer import launch

# async def main():
#     # executable_path = 'C:/web_scraper_vd/chrome\win64-125.0.6422.141\chrome-win64\chrome.exe'
#     browser = await launch()
#     page = await browser.newPage()
#     await page.goto('https://www.scrapethissite.com/pages/ajax-javascript/#2015')
#     await page.screenshot({'path':'screenshot.png'})
#     await browser.close()