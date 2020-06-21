import requests
import urllib.request
import urllib.parse
import urllib.error
from bs4 import BeautifulSoup
import ssl
import json
from selenium import webdriver  
import time
import re
from test import recent_25_posts, insta_details

class Insta_Info_Scraper:
    
    #GET HEADER ARGUMENTS
    def getinfo(self, url):
        ww_url=recent_25_posts('fquthb._.v')
        ww_url_info=insta_details(ww_url)
        print(ww_url_info)

        # Now that the page is fully scrolled, grab the source code.

        html = urllib.request.urlopen(url, context=self.ctx).read()
        soup = BeautifulSoup(html, 'html.parser')
        script = soup.find('script', text=lambda t: \
                           t.startswith('window._sharedData'))
        page_json = script.text.split(' = ', 1)[1].rstrip(';')
        data = json.loads(page_json)
        data_from_post = ww_url_info
        
        info={}
        
        info["FullName"]=data["entry_data"]["ProfilePage"][0]['graphql']['user']['full_name']
        info["Followers"]=data["entry_data"]["ProfilePage"][0]['graphql']['user']['edge_followed_by']['count']
        info["Folowing"]=data["entry_data"]["ProfilePage"][0]['graphql']['user']['edge_follow']['count']

        info["Actual"]=data["entry_data"]["ProfilePage"][0]['graphql']['user']['highlight_reel_count']
        info["is_private"]=data["entry_data"]["ProfilePage"][0]['graphql']['user']['is_private']
        info["popularity"]=data["entry_data"]["ProfilePage"][0]['graphql']['user']['is_verified']

        info["profile_pic_url"]=data["entry_data"]["ProfilePage"][0]['graphql']['user']['profile_pic_url']

        info["facebook"]=data["entry_data"]["ProfilePage"][0]['graphql']['user']['connected_fb_page']

        post_info={}
        number_of_post=data["entry_data"]["ProfilePage"][0]['graphql']['user']['edge_owner_to_timeline_media']['count']

        info['posts'] = data_from_post
        self.info_arr.append(info)  



    def main(self):
        self.ctx = ssl.create_default_context()
        self.ctx.check_hostname = False
        self.ctx.verify_mode = ssl.CERT_NONE
        self.info_arr=[]
        #self.data=[]
        with open('users.txt') as f:
            self.content = f.readlines()
        self.content = [x.strip() for x in self.content]
        for url in self.content:
            self.getinfo(url)
        with open('instagram.json', 'w', encoding="utf-8") as outfile:
            json.dump(self.info_arr, outfile, indent=4,ensure_ascii=False)
        print("Json file containing required info is created............")    
        
if __name__ == '__main__':
    obj = Insta_Info_Scraper()
    obj.main()  