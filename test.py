from selenium.webdriver import Chrome
import re
import time
import json
def recent_25_posts(username):
    """With the input of an account page, scrape the 25 most recent posts urls"""
    url = "https://www.instagram.com/" + username + "/"
    browser = Chrome('C:/Users/qwerty/Downloads/chromedriver.exe')
    browser.get(url)
    post = 'https://www.instagram.com/p/'
    post_links = []
    while len(post_links) < 25:
        links = [a.get_attribute('href') for a in browser.find_elements_by_tag_name('a')]
        for link in links:
            if post in link and link not in post_links:
                post_links.append(link)
        scroll_down = "window.scrollTo(0, document.body.scrollHeight);"
        browser.execute_script(scroll_down)
        time.sleep(2)
    else:
        return post_links[:25]
    
def insta_details(urls):
    """Take a post url and return post details"""
    browser = Chrome('C:/Users/qwerty/Downloads/chromedriver.exe')
    post_details = []
    for link in urls:
        browser.get(link)
        try:
        # This captures the standard like count. 
            # likes = browser.find_element_by_partial_link_text(' likes').text
            view_id = '//*[@id="react-root"]/section/main/div/div/article/div[2]/section[2]/div/div/a'
            likes = browser.find_element_by_xpath(view_id).text
        except:
        # This captures the like count for videos which is stored
            view_id = '//*[@id="react-root"]/section/main/div/div/article/div[2]/section[2]/div/span'
            likes = browser.find_element_by_xpath(view_id).text
        try:
            location = browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/header/div[2]/div[2]/div[2]/a').text
        except:
            location="null"
        age = browser.find_element_by_css_selector('a time').text
        xpath_c = '//*[@id="react-root"]/section/main/div/div/article/div[2]/div[1]/ul'
        comment = browser.find_element_by_xpath(xpath_c).text
        post_details.append({'likes/views': likes,'age': age, 'comment':comment,"location":location})
        time.sleep(2)
    return post_details 

def find_hashtags(comment):
    """Find hastags used in comment and return them"""
    hashtags = re.findall('#[A-Za-z]+', comment)
    return hashtags
  #/ //*[@id="react-root"]/section/main/div/div/article/div[2]/div[1]/ul/div[2]/li/div/div/div