from bs4 import BeautifulSoup
import requests
import csv
from selenium import webdriver
import os

# Declare current level, unit and lesson number
CUR_LEVEL = "upper-intermediate"  # needs to match Levels inside dict below
UNIT = 2
LESSON = 3
# Yoyochinese usage for MP3 file name and urls
LEVELS = {
    "beginner": ["CCR", "beginner-conversational"],
    "intermediate": ["ICC", "intermediate-conversational"],
    "upper-intermediate": ["UICC", "upper-intermediate-conversational"]
}
# Declare URL
#   URL below will only work for UPPER-intermediate URLs.
#   Change URL manually for Beginner and intermediate course URL link
URL = f"https://yoyochinese.com/lesson/{LEVELS[CUR_LEVEL][1]}-unit-{UNIT}-lesson-{LESSON}/dialogue"
# URL = "https://yoyochinese.com/lesson/intermediate-conversational-unit-56-lesson-3-Talking-About-Music-Pop/dialogue"
# Declare HTML class with "Inspect" on your web browser
HTML_CLASS = "Lynmuf9J_7kHUCdOFb3r"  # Class of the <li> element
AUDIO_URL = "https://cdn.yoyochinese.com/audio/dialoguereplay/"
MP3_FILE_PREFIX = f"{LEVELS[CUR_LEVEL][0]}"
# Audio name pattern is not always the same on Yoyochinese,
# Change string accordingly and inside get_audio_file_name()
# "N" not always positioned at the end...


def format_unit_num():
    """
    Add extra 0 if unit < 10
    """
    u = 0
    if UNIT < 10:
        u = f"0{UNIT}"
    else:
        u = UNIT
    return u


def format_tag():
    """
    Declare tag name for CSV file for Anki
    """
    unit = format_unit_num()
    tag = f"yoyochinese::{CUR_LEVEL}::unit-{unit}"
    return tag


def get_audio_file_name(index, unit):
    """
    Format string depending on unit and lesson number
    and append an index for each dialogue sentence inside a lesson.
    """
    u = 0
    if (index + 1) < 10:
        n = f"0{index + 1}"
    else:
        n = index + 1
    # LEVEL-UNIT-LESSON-INDEX-N
    # DR-LEVEL-UNIT-LESSON-N-INDEX
    return f"DR-{MP3_FILE_PREFIX}-0{unit}-0{LESSON}-N-0{n}.mp3"


def save_audio(audio_file_name):
    """
    Save dialogue sentences MP3 files inside current directory
    with the same file name saved inside the CSV.
    """

    response = requests.get(f"{AUDIO_URL}{audio_file_name}")
    if response.status_code == 200:
        open(f"{audio_file_name}", "wb").write(response.content)
        print(audio_file_name)
    else:
        print(f"Invalid MP3 URL status code: {response.status_code}")


def parser():
    """
    Get a page source after the JavaScript has executed, parse the HTML,
    and format it, then save to CSV file. Save the accompanying audio files.
    """
    driver = webdriver.Chrome()
    driver.get(URL)
    # Get page source after the JavaScript has executed
    page_source = driver.page_source
    print("URL: ", URL)
    # Parse HTML
    soup = BeautifulSoup(page_source, 'html.parser')
    job_elements = soup.find_all("li", class_=HTML_CLASS)

    file = open('output.csv', 'a', newline='', encoding='utf-8')
    writer = csv.writer(file)

    if os.path.getsize("output.csv") == 0:
        print("File is empty, adding headers...")
        headers = ['sentence', 'pinyin', 'translation', 'audio', 'tags']
        writer.writerow(headers)
    else:
        print("File is NOT empty")

    unit = format_unit_num()
    tag = format_tag()
    # For each row get the sentence dialogue elements
    for index, job_element in enumerate(job_elements):
        chinese = job_element.find("p", class_="characters").get_text()
        pinyin = job_element.find("p", class_="pinyin").get_text()
        english = job_element.find("p", class_="english").get_text()

        # Get matching file name and save audio file
        audio_file_name = get_audio_file_name(index, unit)
        save_audio(audio_file_name)
        audio_to_anki = f"[sound:{audio_file_name}]"  # Formatted for Anki audio field

        # Append to CSV file
        rows = ([chinese, pinyin, english, audio_to_anki, tag])
        writer.writerow(rows)

    file.close()

    # Close the browser
    driver.quit()
    print("Done !")


if __name__ == '__main__':
    parser()
