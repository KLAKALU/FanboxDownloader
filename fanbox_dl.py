import time
import urllib.error
import urllib.request
from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


def main():
    driver = webdriver.Firefox('C:/Users/playe/fanboxdownloader')
    file = open('data.txt', 'r')
    datalist = file.readlines()
    target_url = datalist[0]
    target_dir = datalist[1]
    mail = datalist[2]
    password = datalist[3]
    # login(driver, mail, password)
    res = driver.get(target_url)
    button = driver.find_element(By.XPATH, '/html/body/div/div[4]/div[2]/div/div/div/div[5]/button')
    button.click()
    articlelist = []
    for i in range(999):
        page = driver.get(target_url + '?page=' + str(i + 1))
        print(target_url + '?page=' + str(i + 1))
        time.sleep(1)
        if i != 0 and driver.current_url == target_url:
            print("serch finish!")
            break
        articles = driver.find_elements(By.XPATH, '//a[@class="sc-1bjj922-0 gwbPAH"]')
        print(str(i) + " page " + str(len(articles)) + " articles")
        for j in range(len(articles)):
            article = driver.find_element(By.XPATH, "/html/body/div/div[5]/div[1]/div[2]/div[4]/div/div/div/div[1]/a[{}]".format(j + 1))
            articlelist.append(article.get_attribute('href'))
            print(article.get_attribute('href'))
    print("get {} artcles!".format(len(articlelist)))
    # imglist = get_imglist(driver, articlelist)
    driver.close


def login(driver, mail, password):
    loginpage = driver.get('https://accounts.pixiv.net/login')
    time.sleep(1)
    mailElement = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[3]/div[1]/div[2]/div/div/div/form/fieldset[1]/label/input')
    passwordElement = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[3]/div[1]/div[2]/div/div/div/form/fieldset[2]/label/input') 
    mailElement.send_keys(mail)
    passwordElement.send_keys(password)
    button = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[3]/div[1]/div[2]/div/div/div/form/button')
    # ログインボタンをクリック
    button.click()
    # ログイン判定を実装予定
    time.sleep(3)


def get_imglist(driver, articlelist, bool):
    imglist = []
    for i in range(len(articlelist)):
        article = driver.get(articlelist[len(articlelist) - i - 1])
        driver.maximize_window()
        height = driver.execute_script("return document.body.scrollHeight")
        height = height / 750
        for i in range(1, int(height)):
            driver.execute_script("window.scrollTo(0, "+str(i * 750)+");")
            time.sleep(1)
        is_div = driver.find_elements(By.XPATH, 'div[@class="sc-1uv5uvv-2 fyPKbV"]')
        print("is_div=" + str(len(is_div)))
        # 特定のdivが1の場合課金しないとダメ
        if is_div != 1:
            article_name = driver.find_element(By.XPATH, '//h1[@class="sc-1vjtieq-4 jPGGNN"]').get_attribute("innerHTML")
            print("cullentDL is {}".format(article_name))
            imgs = driver.find_elements(By.XPATH, '//div[@class="sc-aak26t-2 klekfM"]')
            print(len(imgs))
            for j in range(len(imgs)):
                if len(imgs) == 1:
                    img = driver.find_element(By.XPATH, "/html/body/div[1]/div[5]/div[1]/div/div[3]/div/div[1]/div/article/div[3]/div/div/div/div/a/div/img")
                else:
                    img = driver.find_element(By.XPATH, "/html/body/div[1]/div[5]/div[1]/div/div[3]/div/div[1]/div/article/div[3]/div[{}]/div/div/div/a/div/img".format(j + 1))
                imgurl = img.get_attribute('href')
                imglist.append([article_name, imgurl])
                # download_file(imgurl, target_dir, article_name + "p" + str(i + 1))
        else:
            print("{} is need maney".format(article_name))
    print(imglist)


def download_file(url, target_dir, name):
    try:
        with urllib.request.urlopen(url) as web_file, open(target_dir + name, 'wb') as local_file:
            local_file.write(web_file.read())
    except urllib.error.URLError as e:
        print(e)


main()
