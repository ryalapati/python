import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Set up WebDriver before tests
@pytest.fixture(scope="function")
def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    yield driver  # Yield the driver to be used in tests
    driver.quit()

# Function to remove commas from the article count
def remove_comma(s):
    return s.replace(',', '') if s else '0'

# Function to get the dictionary of languages and articles
def get_languages_and_articles(driver):
    driver.get("https://meta.wikimedia.org/wiki/List_of_Wikipedias/Table")
    languages = driver.find_elements(By.XPATH, "//div[@id='mw-content-text']//table[1]//tr/td[2]/a")
    articles = driver.find_elements(By.XPATH, "//div[@id='mw-content-text']//table[1]//tr/td[5]/a")
    total_languages = []  # collected all Languages in the List
    for r in languages:
        total_languages.append(r.text)
    total_articles = []  # collected all articles in the List
    for r in articles:
        total_articles.append(r.text)
    # Combine the lists into a dictionary
    return dict(zip(total_languages, total_articles))

# Function to calculate total articles for given languages
def find_total_articles_by_languages(dictonary, languages):
    total = 0
    for lang in languages:
        if lang in dictonary:
            article_count = remove_comma(dictonary[lang])
            try:
                total += int(article_count)
            except ValueError:
                print(f"Skipping invalid article count for {lang}: {article_count}")
        else:
            print(f"Language '{lang}' not found in the dictionary.")
    return total

# Test to verify the calculation of total articles for selected languages
def test_find_total_articles(get_driver):
    # Get the driver and fetch language/article data
    driver = get_driver

    dictonary = get_languages_and_articles(driver)

    # Select languages for which to calculate total articles
    languages_to_check = ["English", "German"]

    # Calculate the total articles for the selected languages
    total_articles = find_total_articles_by_languages(dictonary, languages_to_check)

    # Print the total articles (for debugging purposes)
    print(f"Total articles for selected languages: {total_articles}")