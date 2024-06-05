
import time
from selenium import webdriver
from PIL import Image
from io import BytesIO
from selenium.webdriver.chrome.options import Options



image_path_list = []
i=0
def save_png(screenshot):
    global i
    image_path = f'./image_saves/screenshot{i}.jpg'
    with open(image_path, 'wb') as f:
        f.write(screenshot)
    
    image_path_list.append(image_path)
    i+=1

def combine_images(image_paths, output_path):
    images = [Image.open(path) for path in image_paths]
    widths, heights = zip(*(i.size for i in images))

    max_width = max(widths)
    total_height = sum(heights)

    combined_image = Image.new('RGB', (max_width, total_height), color=(255, 255, 255))

    y_offset = 0
    for image in images:
        combined_image.paste(image, (0, y_offset))
        y_offset += image.size[1]

    combined_image.save(output_path)


# Function to scroll to the bottom of the page based on window size
def scroll_to_bottom(driver):
    window_height = driver.execute_script("return window.innerHeight")
    # print(window_height)
    last_height = driver.execute_script("return document.body.scrollHeight")
    # print(last_height)
    current_scroll = 0
    while current_scroll <= last_height - window_height:
        # Scroll down one window height
        driver.execute_script(f"window.scrollTo(0, {current_scroll + window_height});")
        # Wait for some time to let content load
        time.sleep(3)
        secreenshot = driver.get_screenshot_as_png()
        save_png(screenshot=secreenshot)
        current_scroll += window_height

def scraper_main (url):
    # Initialize a WebDriver instance (you need to have the appropriate driver installed, e.g., chromedriver)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")

    driver = webdriver.Chrome(options=chrome_options)


    # Navigate to the website
    driver.get(url=url)

    time.sleep(5)  # Adjust this time as needed
    driver.execute_script("window.scrollTo(0, 0);")

    # Capture the screenshot after the content has loaded
    screenshot_before_scroll = driver.get_screenshot_as_png()
    save_png(screenshot_before_scroll)

    # Scroll down to the bottom of the page
    scroll_to_bottom(driver)

    # print(image_path_list)
    # Close the WebDriver instance
    driver.quit()
    # Output path for the combined image
    output_path = './test/combined_screenshots.jpg'
    # Combine images into one
    combine_images(image_path_list, output_path)


# scraper_main('https://www.scrapethissite.com/pages/advanced/')