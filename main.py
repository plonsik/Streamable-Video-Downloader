import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import requests

# Configuration variables
WEBDRIVER_PATH = 'chromedriver.exe'  # Adjust this path to your WebDriver location
SLEEP_TIME_AFTER_PAGE_LOAD = 5  # Time in seconds to wait for the page and videos to load
FILE_PATH = 'links.txt'  # Path to your file containing Streamable links

def download_video(url, filename):
    print(f"Attempting to download video from {url}")
    response = requests.get(url, stream=True)

    if response.status_code == 200:
        total_length = response.headers.get('content-length')

        if total_length is None:
            print("Couldn't retrieve content length, downloading without progress indication.")
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
        else:
            total_length = int(total_length)
            downloaded = 0

            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        downloaded += len(chunk)
                        f.write(chunk)
                        done = int(50 * downloaded / total_length)
                        print(f"\r[{'=' * done}{' ' * (50-done)}] {downloaded * 100 / total_length:.2f}%", end='', flush=True)
            print("\nVideo downloaded successfully as {}".format(filename))

    else:
        print(f"Failed to download video from {url}. Status code: {response.status_code}")

def is_streamable_link(url):
    return "streamable.com" in url

def extract_direct_video_url_with_selenium(streamable_url):
    print(f"\nExtracting direct video URL from {streamable_url} using Selenium")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--log-level=3")

    if os.name == 'nt':
        log_path = 'NUL'
    else:
        log_path = '/dev/null'

    webdriver_service = Service(WEBDRIVER_PATH, log_path=log_path)

    driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

    try:
        driver.get(streamable_url)
        time.sleep(SLEEP_TIME_AFTER_PAGE_LOAD)

        video_elements = driver.find_elements(By.TAG_NAME, "video")
        for video in video_elements:
            sources = video.find_elements(By.TAG_NAME, "source")
            for source in sources:
                video_url = source.get_attribute('src')
                if video_url:
                    print(f"Found video URL: {video_url}")
                    return video_url

        print("No video URL found with Selenium.")
    finally:
        driver.quit()

    return None

def download_streamable_videos_from_file(file_path):
    streamable_links = []
    with open(file_path, 'r') as file:
        for line in file:
            if is_streamable_link(line.strip()):
                streamable_links.append(line.strip())

    total_links = len(streamable_links)
    print(f"Found {total_links} Streamable links.")

    for index, link in enumerate(streamable_links, start=1):
        print(f"\nChecking link {index} of {total_links}: {link}")
        video_url = extract_direct_video_url_with_selenium(link)
        if video_url:
            filename = link.split('/')[-1] + '.mp4'
            download_video(video_url, filename)
        else:
            print(f"Could not extract a direct video URL for {link}")

download_streamable_videos_from_file(FILE_PATH)
