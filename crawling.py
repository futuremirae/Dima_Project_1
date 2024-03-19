from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions, NoSuchElementException
import time

def href_click(href_list, first_page):
   
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

    chrome_options.add_argument(f'user-agent={user_agent}')
    
    try:
        all_text = []
        all_text.append(first_page)  # 첫페이지 어팬드
        driver = webdriver.Chrome(options=chrome_options)

        for url in href_list:
            try:
                driver.get(url)

                # 대기 시간 설정 (10초)
                wait = WebDriverWait(driver, 5)

                # <body> 태그를 기다림
                body_element = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
                page_text = body_element.text

                if page_text:
                    all_text.append(page_text)
            except NoSuchElementException as e:
                # print(f'태그 찾기 실패: {e}')
                pass
                # 다른 태그 또는 로직 추가
        return all_text

    except exceptions.WebDriverException as e:
        pass
    finally:
        driver.quit()

def input_urls(url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

    chrome_options.add_argument(f'user-agent={user_agent}')

    driver = webdriver.Chrome(options=chrome_options)

    href_list = []
    all_text_list = []

    try:
        driver.get(url)

        # 대기 시간 설정 (10초)
        wait = WebDriverWait(driver, 5)

        # <body> 태그를 기다림
        body_element = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        first_page = body_element.text

        if first_page:
            pass
        else:
            print('없어!')

        # Find all <a> tags
        a_tags = driver.find_elements(By.TAG_NAME, 'a')

        if a_tags:
            # Filter out links with the 'download' attribute
            a_tags_filtered = [a_tag for a_tag in a_tags if not a_tag.get_attribute('download')]

            # href 값이 없는 a태그는 제외
            a_tags_with_href = [a_tag for a_tag in a_tags_filtered if a_tag.get_attribute('href')]

            # 최대 30개의 a_tags만 가져옴
            a_tags_limited = a_tags_with_href[:30]

            for a_tag in a_tags_limited:
                href = a_tag.get_attribute('href')
                href_list.append(href)

        all_text = href_click(href_list, first_page)
        return all_text

    except NoSuchElementException as e:
        pass

    except Exception as e:
        pass

    finally:
        driver.quit()

    

import numpy as np
import pandas as pd
from selenium import webdriver
import argparse

def main(input_file):
    # 이전 코드를 그대로 가져옵니다
    data = pd.read_csv(input_file)


    urls = data['HOMEPAGE'][2401:3600]
    # 'http://'를 URL 앞에 추가하기
    urls = urls.apply(lambda x: f"http://{x}" if not x.startswith("http") else x)
    result_file_path = 'text.csv'
    
    for index, url in enumerate(urls):
        print(f'{index}번 url 출력중****************************')
        all_text = input_urls(url)

        # Create a DataFrame with the current data
        current_data = pd.DataFrame({
            'url': [url],
            'text': [all_text]
        })

        # Append the DataFrame to the existing CSV file
        current_data.to_csv(result_file_path, mode='a', header=False, index=False, encoding='utf-8-sig')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process CSV file with URLs.")
    parser.add_argument("input_file", help="Path to the input CSV file")

    args = parser.parse_args()
    main(args.input_file)