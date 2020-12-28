from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup as bs


class InstagramBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = webdriver.Firefox()

    def closebrowser(self):
        self.driver.close()

    def login(self):
        driver = self.driver
        driver.get('http://www.instagram.com')
        time.sleep(5)
        print("firefox opened")

        usernamebox = driver.find_element_by_xpath(
            '/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[1]/div/label/input')
        passwordbox = driver.find_element_by_xpath(
            '/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[2]/div/label/input')
        loginbutton = driver.find_element_by_xpath(
            '/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[3]/button')
        usernamebox.clear()
        passwordbox.clear()
        usernamebox.send_keys(self.username)
        passwordbox.send_keys(self.password)
        loginbutton.click()
        time.sleep(5)

    def like_more(self):
        driver = self.driver
        likes = driver.find_elements_by_tag_name('span')
        i = 0
        time.sleep(5)
        for like in likes:
            i = i+1
            try:
                soup = bs(like.get_attribute('innerHTML'), 'html.parser')
                if(soup.find('svg')['aria-label'] == 'Like'):
                    print(soup)
                    like.click()
                    print(str(i)+"liked")
                    driver.execute_script(
                        'window.scrollTo(0,document.body.scrollHeight)')
                    time.sleep(3)
                elif(soup.find('svg')['aria-label'] == 'Unlike'):
                    print(str(i)+"already liked")
            except Exception as e:
                print(e)

    def like_in_feeds(self):
        driver = self.driver
        driver.get('http://www.instagram.com/')
        try:
            time.sleep(2)
            not_now = driver.find_element_by_xpath(
                '/html/body/div[4]/div/div/div/div[3]/button[2]')
            not_now.click()
        except Exception as e:
            time.sleep(2)
       
        for i in range(1, 3):
            driver.execute_script(
                'window.scrollTo(0,document.body.scrollHeight);')
            time.sleep(2)
            print('scrolling')
            self.like_more()

    def like_by_hashtag(self, hashtag):
        driver = self.driver
        driver.get('https://www.instagram.com/explore/tags/'+hashtag+'/')
        for i in range(1, 3):
            driver.execute_script(
                "window.scrollTo(0,document.body.scrollHeight);")
            time.sleep(2)
        hrefs = driver.find_elements_by_tag_name('a')
        pics_hrefs = [elem.get_attribute('href') for elem in hrefs]

        pics_hrefs = [href for href in pics_hrefs if "/p/" in href]
        print(hashtag + "Photos" + str(len(pics_hrefs)))
        i = 0
        for pic_href in pics_hrefs:
            i = i+1
            driver.get(pic_href)
            time.sleep(2)
            driver.execute_script(
                'window.scrollTo(0,document.body.scrollHeight)')
            try:
                like = driver.find_element_by_xpath(
                    '/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[1]/span[1]/button/div/span')
                soup = bs(like.get_attribute('innerHTML'), 'html.parser')
                if(soup.find('svg')['aria-label'] == 'Like'):
                    like.click()
                    print(str(i)+" liked")
                else:
                    print(str(i)+" already liked")
            except Exception as e:
                time.sleep(2)
                print(e)


file = open("user.txt", 'r')

username = file.readline().split("=")[1]
password = file.readline().split("=")[1]
hashtags = file.readline().split("=")[1].split(",")
bot = InstagramBot(username, password)

bot.login()
bot.like_in_feeds()

[bot.like_by_hashtag(tag) for tag in hashtags]
bot.closebrowser()
