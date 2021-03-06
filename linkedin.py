from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import sys
import time
from bs4 import BeautifulSoup
import requests
from random import choice
from fake_headers import Headers
'''linkedin have strong security, use VPN or proxies. It'll block your IP address in very few attempts '''
class Linkedin:
    @staticmethod
    def scrap(username):
        try:
            url = f'https://in.linkedin.com/in/{username}?trk=public_profile_browsemap_profile-result-card_result-card_full-click'
            
            
        #automating and opening URL in headless browser
            headers = Headers().generate()
            chrome_option = Options()
            chrome_option.add_argument('--headless')            
            chrome_option.add_argument('--disable-extensions')
            chrome_option.add_argument('--disable-gpu')
            chrome_option.add_argument('--incognito')
            chrome_option.add_argument(f'user-agent={headers}')
            driver = webdriver.Chrome('C:\\webdrivers\\chromedriver.exe',options=chrome_option) #chromedriver's path in first argument
            driver.get(url)
            time.sleep(5)
            response = driver.page_source.encode('utf-8').strip()
            
            soup =  BeautifulSoup(response,'html.parser')    
            
            full_name = soup.find('h1',{
            'class' : 'top-card-layout__title'
        })
            profession = soup.find('h2',{
            'class' : 'top-card-layout__headline'
        })
            address = soup.find('span',{
            'class' : 'top-card__subline-item'
        })
            connections = soup.find('span',{
            'class' : 'top-card__subline-item top-card__subline-item--bullet'
        })
            educations = soup.find_all('span',{
            'class' : 'top-card-link__description'
        })
            websites = soup.find_all('span',{
            'class' : 'websites__url-text'
        })
            summary = soup.find('section',{
            'class' : 'summary pp-section'
        })
            experience = soup.find_all('li',{
            'class' : 'experience-item'
        })
            experience = [experience[i].text.strip().replace('\n','') for i in range(len(experience))]
            websites = [websites[i].text.strip() for i in range(len(websites))]
            educations = [educations[i].text.strip() for i in range(len(educations)-1)]
            education_list = soup.find_all('span',{
            'class' : 'education__item education__item--degree-info'
        })
            education_list = [education_list[i].text.strip() for i in range(len(education_list))]
            skills_list = soup.find_all('li',{
            'class' : 'skills__item'
        })
            skills_list = [skills_list[i].text.strip() for i in range(len(skills_list))]
            honors = soup.find('p',{
            'class' : 'show-more-less-text__text--more'
        })
            profile = soup.find('img',{
                'class' : 'artdeco-entity-image artdeco-entity-image--profile artdeco-entity-image--circle-8 top-card-layout__entity-image lazy-loaded'
            })
            return {
            'full_name' : full_name.text.strip(),
            'profession': profession.text.strip() if type(profession) is not None else 'Not found',
            'address' : address.text.strip() if type(address) is not None else 'Not found',
            'connections' : connections.text.strip(),
            'university' : educations,
            'websites' : websites if type(websites) is not None else 'Not found',
            'experience' : experience,
            'degrees' : education_list,
            'skills' : skills_list,
            'honors' : honors.text if type(honors) is not None else 'Not found!',
            'summary' : summary.text.strip() if type(summary) is not None else 'Not found',
            'profile' : profile['src']
        }
        except Exception as ex:
            print(ex)
if __name__ == "__main__":
    print(Linkedin.scrap(sys.argv[len(sys.argv)-1]))             
'''
author : sajid shaikh
updated : 17th June,2020
'''