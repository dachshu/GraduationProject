from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import click

twitter_login_url = 'https://twitter.com/login'


def read_auth_info(auth_file):
    '''
    파일의 첫번째 줄은 id, 두번째 줄은 password
    '''
    id = auth_file.readline().strip()
    password = auth_file.readline().strip()
    return id, password


def login_on_twitter(browser, id, pw):
    id_field = browser.find_element_by_css_selector('input.js-username-field')
    pw_field = browser.find_element_by_css_selector('input.js-password-field')
    submit_btn = browser.find_element_by_css_selector('button.submit')

    id_field.send_keys(id)
    pw_field.send_keys(pw)
    submit_btn.click()
    WebDriverWait(browser, 10).until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, 'aside[aria-label="팔로우 추천"]')))


def pull_recommended_accounts(browser, pull_count):
    recommendation_btn = browser.find_element_by_css_selector(
        'aside[aria-label="팔로우 추천"]>a')
    recommendation_btn.click()
    WebDriverWait(browser, 10).until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, 'div[data-testid="UserCell"]')))
    users = browser.find_elements_by_css_selector(
        'div[data-testid="UserCell"]>div')
    names = []
    for user in users:
        user_name = user.find_element_by_xpath(
            './div[last()]/div[1]/div[1]/a/div/div[last()]//span')
        names.append(user_name.text.lstrip('@'))

    return names


@click.command()
@click.argument('auth-file', type=click.File())
@click.option('--pull-count', '-c', type=click.IntRange(1,30), default=5)
def main(auth_file, pull_count):
    browser = webdriver.Firefox()
    browser.get(twitter_login_url)
    id, pw = read_auth_info(auth_file)
    login_on_twitter(browser, id, pw)
    names = pull_recommended_accounts(browser, pull_count)
    for name in names[:min([len(names), pull_count])]:
        print(name)


if __name__ == "__main__":
    main()
