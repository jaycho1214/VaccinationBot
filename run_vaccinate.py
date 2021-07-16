#!/usr/bin/env python
# -*- coding: utf-8 -*-

import configparser
import glob
from multiprocessing import Process
from pathlib import Path

import chromedriver_autoinstaller
import selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

URL = 'https://ncvr.kdca.go.kr/'
FIRST_PAGE_TIMEOUT = 5 * 60 * 60 # 처음 로딩할때 기다리는 시간 (대기하는거 포함)
TIMEOUT = 30 # 로딩된 이후 기다리는 시간

def load_main_page(driver: webdriver) -> bool:
    driver.get(URL)
    element1_present = expected_conditions.presence_of_element_located((By.XPATH, '//frame[@src="/cobk/index.jsp"]'))
    element2_clickable = expected_conditions.presence_of_element_located((By.XPATH, '//div[contains(@class, "banner01")]'))
    try:
        WebDriverWait(driver, FIRST_PAGE_TIMEOUT).until(element1_present)
        driver.switch_to.frame(driver.find_element(By.XPATH, '//frame[@src="/cobk/index.jsp"]'))
        WebDriverWait(driver, FIRST_PAGE_TIMEOUT).until(element2_clickable)
        return True
    except:
        return False

def privacy(driver: webdriver, config: dict) -> bool:
    # 사이트가 완전히 로딩되었는지 확인
    element1_present = expected_conditions.presence_of_element_located((By.ID, 'ptntRrn2'))
    try:
        WebDriverWait(driver, TIMEOUT).until(element1_present)
        # 카카오톡
        driver.find_element(By.ID, 'smsRcptAgrmYn2').click()
        # 개인정보 채우기
        driver.find_element(By.ID, 'patnam').send_keys(config['피접종자']['이름'])
        driver.find_element(By.ID, 'ptntRrn1').send_keys(config['피접종자']['주민등록번호'])
        driver.find_element(By.ID, 'ptntRrn2').send_keys(config['피접종자']['주민등록번호'])
        driver.find_element(By.ID, 'apnmNm').send_keys(config['대리인']['이름'])
        driver.find_element(By.ID, 'apnmMtnoTofmn').send_keys(config['대리인']['휴대폰번호'].split('-')[0])
        driver.find_element(By.ID, 'apnmMtno1').send_keys(config['대리인']['휴대폰번호'].split('-')[1])
        driver.find_element(By.ID, 'apnmMtno2').send_keys(config['대리인']['휴대폰번호'].split('-')[2])
        driver.find_element(By.ID, 'apnmRrn1').send_keys(config['대리인']['주민등록번호'].split('-')[0])
        driver.find_element(By.ID, 'apnmRrn2').send_keys(config['대리인']['주민등록번호'].split('-')[1])
        return True
    except:
        return False

def authenticate(driver: webdriver, config: dict) -> None:
    # 사이트가 완전히 로딩되었는지 확인
    element1_present = expected_conditions.presence_of_element_located((By.XPATH, '//a[@href="#kt"]'))
    try:
        WebDriverWait(driver, TIMEOUT).until(lambda driver: len(driver.window_handles) == 2)
        driver.switch_to.window(driver.window_handles[1])
        WebDriverWait(driver, TIMEOUT).until(element1_present)
        driver.find_element(By.XPATH, '//a[@href="#kt"]').click()
        driver.find_element(By.XPATH, '//a[@class="tabApp"]').click()
        driver.find_element(By.ID, 'nm').send_keys(config['피접종자']['이름'])
        driver.find_element(By.ID, 'mbphn_no').send_keys(''.join(config['대리인']['휴대폰번호'].split('-')))
        driver.find_element(By.ID, 'certi01').click()
        driver.find_element(By.ID, 'certi02').click()
        driver.find_element(By.ID, 'certi03').click()
        driver.find_element(By.ID, 'certi04').click()
        # driver.switch_to.window(driver.window_handles[0])
        # driver.switch_to.frame(driver.find_element(By.XPATH, '//frame[@src="/cobk/index.jsp"]'))
    except:
        return False

def main(filename: str) -> None:
    chromedriver_autoinstaller.install()
    driver = webdriver.Chrome()
    config = configparser.ConfigParser()
    config.read(filename)

    # 화면 보일때 까지 계속 로딩하기
    while not load_main_page(driver):
        pass

    # 백신 예약 버튼 클릭
    driver.find_element(By.XPATH, '//div[contains(@class, "banner01")]').click()

    # 대리 예약 버튼 클릭
    driver.find_element(By.ID, 'rsrvAgntBtn').click()

    # 개인정보입력
    privacy(driver, config)

    # 휴대폰 본인인증 클릭
    driver.find_element(By.XPATH, '//div[contains(@class, "auth01")]').click()

    # 본인인증하기
    authenticate(driver, config)

    # 창 닫으면 프로그램 종료
    WebDriverWait(driver, TIMEOUT).until(lambda driver: len(driver.window_handles) == 0) 
    driver.quit()


if __name__ == '__main__':
    target = glob.glob(str(Path(__file__).parent / 'target' / '*.ini'))
    p = [Process(target=main, args=(t,)) for t in target]
    [_p.start() for _p in p]
    [_p.join() for _p in p]
