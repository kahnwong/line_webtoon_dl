import requests
import os
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#~ """Profile"""
#~ fp = webdriver.FirefoxProfile()
#~ fp.set_preference("browser.preferences.instantApply",True)
#~ fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/plain, application/octet-stream, application/binary, text/csv, application/csv, application/excel, text/comma-separated-values, text/xml, application/xml, image/jpg")
#~ fp.set_preference("browser.helperApps.alwaysAsk.force",False)
#~ fp.set_preference("browser.download.manager.showWhenStarting",False)
#~ fp.set_preference("browser.download.folderList",0)
#~ fp.set_preference("browser.download.dir", '/Users/kahnwong/Downloads')


#~ driver = webdriver.Firefox(firefox_profile=fp)
driver = webdriver.Firefox()


def get_all_pages(url):
    #~ url = 'http://www.webtoons.com/en/slice-of-life/my-giant-nerd-boyfriend/001-introduction/viewer?title_no=958&episode_no=1'
    driver.get(url)

    # """get cookies?"""
    # eng_button = driver.find_element(By.XPATH, '//*[@id="selectLanguageLayer"]/ul/li[2]/label')
    # webdriver.ActionChains(driver).move_to_element(eng_button).click().perform()
    # ok_button = driver.find_element(By.XPATH, '//*[@id="selectLanguageLayer"]/a')
    # webdriver.ActionChains(driver).move_to_element(ok_button).click().perform()
    #
    # driver.get(url) # go back to comic 1

def get_all_comics():
    pages = driver.find_elements_by_xpath('//*[@id="topEpisodeList"]/div/div[1]/ul/li/a')
    return [page.get_attribute('href') for page in pages]

def get_images(page):
    driver.get(page)
    images = driver.find_elements_by_xpath('//*[@id="_imageList"]/img')
    return [image.get_attribute('data-url') for image in images]

def download_images(folder, prefix, url):

    headers={"Referer": 'http://www.webtoons.com'}
    image = requests.get(url, headers=headers)

    parsed = urlparse(url)
    filename = parsed.path.split('/')[-1]



    with open(folder + '/' + str(prefix) + ' ' + filename, 'wb') as img_obj:
        img_obj.write(image.content)
    print('Download', filename, 'complete!')



def main():
    story = 'http://www.webtoons.com/en/slice-of-life/my-giant-nerd-boyfriend/001-introduction/viewer?title_no=958&episode_no=1'  # my giant nerd boyfriend - up to 202, use 202 next
    #~ story = 'http://www.webtoons.com/en/comedy/safely-endangered/ep-82-two-kinds-/viewer?title_no=352&episode_no=82' # safely endangered – up to 191
    #~ story = 'http://www.webtoons.com/en/slice-of-life/lunarbaboon/ep-204-honeybee-/viewer?title_no=523&episode_no=205' # lunarbaboon – 205
    #~ story = 'http://www.webtoons.com/en/challenge/cat-loaf-adventures/a-fan-asks-2/viewer?title_no=62997&episode_no=11' # cat loaf adventures – 11
    #~ story = 'http://www.webtoons.com/en/challenge/mushroom-movie/netflix-and-chill/viewer?title_no=45042&episode_no=188' # mushroom movie – 188
    #~ story = 'http://www.webtoons.com/en/challenge/broke-ninjas/too-much/viewer?title_no=32404&episode_no=110' # broke ninjas – 110
    #~ story = 'http://www.webtoons.com/en/challenge/chicks/take-him-away/viewer?title_no=20994&episode_no=20' # chicks – 20



    get_all_pages(story)

    pages = get_all_comics()[31:]

    for page in pages:
        #~ print(page)
        images = get_images(page)
        #~ print(images)

        folder = page.split('=')[-1]
        os.mkdir(folder)

        for index, image in enumerate(images, 1):
            download_images(folder, index, image)

    print('------DONE------')







main()
