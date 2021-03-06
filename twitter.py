from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import sys
from fake_headers import Headers
class Twitter:

    @staticmethod   
    def init_driver(driver_path:str,browser_name:str):
        def set_properties(browser_option):
            ua = Headers().generate()      #fake user agent
            browser_option.add_argument('--headless')
            browser_option.add_argument('--disable-extensions')
            browser_option.add_argument('--incognito')
            browser_option.add_argument('--disable-gpu')
            browser_option.add_argument('--log-level=3')
            browser_option.add_argument(f'user-agent={ua}')
            return browser_option
        try:
            browser_name = browser_name.strip().title()

            
            #automating and opening URL in headless browser
            if browser_name == "Chrome":
                browser_option = ChromeOptions()
                browser_option = set_properties(browser_option)    
                driver = webdriver.Chrome(driver_path,options=browser_option) #chromedriver's path in first argument
            elif browser_name == "Firefox":
                browser_option = FirefoxOptions()
                browser_option = set_properties(browser_option)
                driver = webdriver.Firefox(driver_path,options=browser_option)
            else:
                driver = "Browser Not Supported!"
            return driver
        except Exception as ex:
            print(ex)
    
    @staticmethod
    def scrap(username):
        try:
            #generating URL according to the username
            url = f"https://twitter.com/{username}"

            driver = Twitter.init_driver('C:\\webdrivers\\chromedriver.exe',"Chrome")  #chromedriver's path in first argument
            driver.get(url)
            
            wait = WebDriverWait(driver, 10)
            element = wait.until(EC.title_contains(f"@{username}"))
            response = driver.page_source.encode('utf-8').strip()
            soup =  BeautifulSoup(response,'html.parser')
        
            spans = soup.find_all('span',{
            "class" : 'css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0'
        })  

            images = soup.find_all('img',{
            'class' : 'css-9pa8cd'
        })
            
            is_verified = soup.find("svg",{
           "class" : "r-13gxpu9 r-4qtqp9 r-yyyyoo r-1xvli5t r-9cviqr r-dnmrzs r-bnwqim r-1plcrui r-lrvibr",
           "aria-label" : 'Verified account'
       })   
            
            dates = soup.find_all('span',{
                'class' : 'css-901oao css-16my406 r-1re7ezh r-4qtqp9 r-1qd0xha r-ad9z0x r-zso239 r-bcqeeo r-qvutc0'
            })

            if len(images) == 2:
                profile = images[1]['src']
                banner = images[0]['src']
            elif len(images) ==1:
                profile = images[0]['src']
                banner = "Not Found"
            else:
                profile = "Not Found!"
                banner = "Not Found!"
            follows = soup.find_all('a',{
                'class' : "r-hkyrab r-1loqt21 r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-qvutc0 css-4rbku5 css-18t94o4 css-901oao",
                "role" : "link",
                "data-focusable" : "true"
            })
            bio = soup.find("div",{
                "class" :"css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-qvutc0",
                "data-testid" : "UserDescription",
                "dir" : "auto"
            })
            return{
                'full_name' : spans[5].text,
                'banner' : banner,
                'profile_image_link' : profile,
                 "account_verified" : True if is_verified is not None else False,
                 "birth_date" : "Not Given" if len(dates) < 3 else dates[1].text,
                 "location" : dates[0].text,
                
                 "bio" : bio.text if bio is not None else "Bio Not Found!",
                 "followers" : follows[1]['title'],
                 "following" : follows[0]['title'],
                 "joined_date" : dates[1].text if len(dates) < 3 else dates[2].text

            }
              
        except Exception as ex:
            print(ex)   

if __name__ == "__main__":
    print(Twitter.scrap(sys.argv[len(sys.argv)-1]))  #can pass username here or from command line
    


'''
author : sajid shaikh
last modified : 1st July,2020
'''