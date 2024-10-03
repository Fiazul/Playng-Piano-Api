from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import os
import shutil
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selectors_1 import *


def setup_driver():
    chrome_options = Options()
    base_dir = os.getcwd()
    driver_dir = os.path.join(base_dir, "driver")
    downloaded_driver_path = os.path.join(driver_dir, "chromedriver.exe")
    os.makedirs(driver_dir, exist_ok=True)

    def find_chromedriver():
        if os.path.exists(downloaded_driver_path):
            return downloaded_driver_path
        return None

    chrome_driver_path = find_chromedriver()
    if chrome_driver_path:
        service = Service(executable_path=chrome_driver_path)
    else:
        downloaded_path = ChromeDriverManager().install()
        try:
            shutil.move(downloaded_path, downloaded_driver_path)
        except Exception as e:
            print(f"Error moving ChromeDriver: {e}")
            raise
        service = Service(executable_path=downloaded_driver_path)

    return webdriver.Chrome(service=service, options=chrome_options)


def play_piano(driver, notes):
    for note in notes:
        xpath = key_xpath.get(note)
        if xpath:
            try:
                key_element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, xpath))
                )
                key_element.click()
                print(f"Played note {note} using XPath: {xpath}")
                time.sleep(0.5)
            except NoSuchElementException:
                print(f"Note {note} not found, skipping...")
            except Exception as e:
                print(f"Error clicking note {note}: {e}")
        else:
            print(f"No XPath found for note {note}, skipping...")


def main():
    driver = webdriver.Chrome()
    driver.get('https://www.musicca.com/piano')
    time.sleep(3)

    notes_to_play = [
        "C", "D", "E", "F", "G", "A", "B",
        "2C", "2D", "2E", "2F", "2G", "2A", "2B",
        "3C", "3D", "3E", "3F", "3G", "3A", "3B",
        "E", "D", "C", "B", "A", "G",
        "2A", "2B", "3C", "3D", "3E",
        "2C", "2D", "2E", "2F", "2G",
        "2B", "3A", "3G", "3F", "3E",
        "C", "D", "E", "F", "G", "A", "B",
    ]

    play_piano(driver, notes_to_play)

    driver.quit()


if __name__ == "__main__":
    main()
