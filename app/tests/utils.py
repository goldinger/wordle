from selenium.webdriver.common.by import By


def type_word(browser, word: str):
    for letter in word.lower():
        browser.find_element(By.ID, f'keyboard-letter-{letter}').click()