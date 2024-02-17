# Streamable Video Downloader

This Python script enables users to download videos from Streamable by supplying links in a text file. It utilizes Selenium for handling dynamic web content and extracting direct video URLs, and then employs Python's requests library for downloading the videos.

### Features
- **Extracts direct video URLs** from Streamable links using Selenium.
- **Downloads videos with progress indication**.
- **Supports batch processing** of multiple Streamable links provided in a text file.

### Prerequisites
To run this script, the following must be installed:

- **Python 3.x**
- **Selenium**
- **Requests**
- **A WebDriver for Chrome browser**

### Setup
#### Install Python Dependencies
Install the necessary Python libraries by running the following command:

    pip install selenium requests

#### WebDriver
Download the WebDriver for Chrome browser, which can be found here:

   https://googlechromelabs.github.io/chrome-for-testing/

#### Configuration
- Update the `WEBDRIVER_PATH` in the script to the location where your WebDriver is stored.
- Adjust `SLEEP_TIME_AFTER_PAGE_LOAD` as needed to ensure pages are fully loaded before the extraction process begins.

### Usage
1. Create a text file (default is `links.txt`) and populate it with Streamable links, one per line.
2. Execute the script with:

       python streamable_video_downloader.py

   If the script is located elsewhere, replace `streamable_video_downloader.py` with the correct path.

The script will process each link sequentially, providing updates on the download progress and saving the downloaded videos in the same directory as the script.

### Notes
- This script is designed for personal use and educational purposes. Ensure you are authorized to download and use the content from Streamable.
- Web page structures may change over time, potentially necessitating updates to the script.

### License
- MIT License