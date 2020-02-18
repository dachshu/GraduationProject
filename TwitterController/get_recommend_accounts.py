#!/usr/bin/python3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import click
import os
import time

twitter_login_url = 'https://twitter.com/login'


def read_auth_info(auth_file):
    '''
    파일의 첫번째 줄은 id, 두번째 줄은 password
    '''
    id = auth_file.readline().strip()
    password = auth_file.readline().strip()
    return id, password


def login_on_twitter(browser, id, pw):
    WebDriverWait(browser, 20).until(EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, 'input[name="session[password]"]')))


    id_fields = browser.find_elements_by_css_selector('input[name="session[username_or_email]"]')
    pw_fields = browser.find_elements_by_css_selector('input[name="session[password]"]')
    submit_btns = browser.find_elements_by_xpath("//*[text()='Log in']")


    time.sleep(1.5)
    for id_elem in id_fields:
        if id_elem.is_displayed():
            id_elem.send_keys(id)
            break
    
    time.sleep(1.5)
    for pw_elem in pw_fields:
        if pw_elem.is_displayed():
            pw_elem.send_keys(pw)
            break

    for submit_elem in submit_btns:
        if submit_elem.is_displayed():
            if submit_elem.tag_name in ["span", "button"]:
                submit_elem.click()
                break
    
    WebDriverWait(browser, 20).until(EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, 'aside[aria-label="팔로우 추천"]>a')))


def pull_recommended_accounts(browser, pull_count):
    recommendation_btn = browser.find_element_by_css_selector(
        'aside[aria-label="팔로우 추천"]>a')

    recoomendation_link = recommendation_btn.get_attribute("href")
    browser.get(recoomendation_link)
    WebDriverWait(browser, 20).until(EC.visibility_of_element_located(
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
    os.environ["MOZ_HEADLESS"]='1'
    try:
        browser = webdriver.Firefox()
        browser.get(twitter_login_url)
        id, pw = read_auth_info(auth_file)
        login_on_twitter(browser, id, pw)
        names = pull_recommended_accounts(browser, pull_count)
        for name in names[:min([len(names), pull_count])]:
            print(name)
    finally:
        browser.quit()

if __name__ == "__main__":
    main()
