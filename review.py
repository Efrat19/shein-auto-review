import logging
import os
from time import sleep
from selenium import webdriver
import random
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException,ElementNotInteractableException,NoSuchElementException        
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

WINDOW_WIDTH = 1440
WINDOW_LENGTH = 900
HISTORY_PERIOD = 12

class Review:
    login_url = 'https://il.shein.com/user/auth/login'
    review_url = 'https://il.shein.com/user/orders/list?status_type=5'
    content_pool = [
        'Love this item, looks courages',
        'Amazing piece, would buy is again',
    ]
    image_to_upload = os.getcwd()+'/image_to_upload.jpeg'

    def __init__(self):
        self.driver = webdriver.Firefox( executable_path='./geckodriver')
        self.driver_wait_timeout = 15

    def verify_xpath(self,xpath_str):
        wait = WebDriverWait(self.driver, self.driver_wait_timeout)
        moved = wait.until(ec.visibility_of_element_located((
            By.XPATH, xpath_str)))
        return moved

    def login(self):
        password = ''
        user = ''
        user_input_xpath = '/html/body/div[1]/div[2]/div/div/div[2]/div[1]/div[1]/div/form/div[1]/input'
        password_input_xpath = '/html/body/div[1]/div[2]/div/div/div[2]/div[1]/div[1]/div/form/div[2]/input'
        login_btn_xpath = '//button[@class = "she-btn-black she-btn-l she-btn-block"][contains(., "Sign In")]'
        after_login_xpath = '/html/body/div[1]/header/div[2]/div[1]/div/div[1]/div/div[3]/div[1]/a/i'
        self.driver.get(self.login_url)
        self.verify_xpath(login_btn_xpath)
        user_input = self.driver.find_element_by_xpath(user_input_xpath)
        password_input = self.driver.find_element_by_xpath(password_input_xpath)
        login_btn = self.driver.find_element_by_xpath(login_btn_xpath)
        user_input.send_keys(user)
        password_input.send_keys(password)
        login_btn.click()
        sleep(4)
        self.verify_xpath(after_login_xpath)
        self.driver.save_screenshot('tmp/after_login.png')

    def go_to_review_page(self):
        review_xpath = '/html/body/div[1]/div[1]/div[1]/div[2]/div[5]/ul[2]/li[1]/div[2]/div[5]/div/div/a'
        self.driver.get(self.review_url)
        self.verify_xpath(review_xpath)
        self.driver.save_screenshot('tmp/in_review_page.png')

    def get_review_links(self):
        review_btn_xpath = '//a[@da-action="ClickWriteAReview"]'
        review_btns = self.driver.find_elements_by_xpath(review_btn_xpath)
        return review_btns
    
    def review_orders(self):
        self.go_to_review_page()
        links = self.get_review_links()
        for idx in range(len(links)):
            links = self.get_review_links()
            links[idx].click()
            self.verify_xpath('/html/body/div[1]/div[2]/h2')
            self.review_order()
            break
            self.go_to_review_page()
    
    def rate_logistics_service(self):
        try:
            fifth_star_xpath = self.driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[3]/div[2]/div/div/div[2]/div/div/span/i[5]')
            fifth_star_xpath.click()
        except Exception as e:
            pass
    
    
    def get_review_text(self):
        return random.choice(self.content_pool)
    
    def review_order(self):
        self.rate_logistics_service()
        rows = self.driver.find_elements_by_xpath('//div[@class="col-md-10 col-sm-10 review-textarea"]')
        print(rows)
        submit_btn_xpath = '/html/body/div[1]/div[2]/div[5]/button'
        # while self.check_exists_by_xpath(submit_btn_xpath):
        for row in rows:
            content_area = row.find_element_by_xpath('.//textarea')
            review_text = self.get_review_text()
            content_area.send_keys(review_text)
            print(review_text)
            upload_image_btn = row.find_element_by_xpath('.//button[@class="upload-img-btn"]')
            print(self.image_to_upload)
            # upload_image_btn.click()
            upload_image_btn.send_keys(self.image_to_upload)
            
        submit_btn = self.driver.find_element_by_xpath('//button[@class="S-button hLawYm S-button__primary S-button__H44PX"]')    
        submit_btn.click()
        sleep(10)
            
            
    def check_exists_by_xpath(self,xpath):
        try:
            self.driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return False
        return True
                        