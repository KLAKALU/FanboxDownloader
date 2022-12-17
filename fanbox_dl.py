import time
import sys
import os
import shutil
import csv
from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


def main():
    driver = webdriver.Firefox('C:/Users/playe/fanboxdownloader')
    file = open('data.txt', 'r', encoding='utf-8')
    datalist = file.readlines()
    print(datalist)
    mail = datalist[0]
    password = datalist[1]
    download_path = datalist[2]
    download_path = download_path.replace("\n", "")
    target_url = datalist[3]
    target_url = target_url.replace("\n", "")
    tgt_dir = datalist[4]
    tgt_dir = tgt_dir.replace("\n", "")
    print(tgt_dir)
    target_name = datalist[5]
    target_name = target_name.replace("\n", "")
    print("Downloading " + target_name + "s fanbox imgs!")
    # R18 varification
    driver.get(target_url)
    button = driver.find_element(By.XPATH, '/html/body/div/div[4]/div[2]/div/div/div/div[5]/button')
    button.click()
    if os.path.isfile(tgt_dir + 'imglist.csv') is False:
        articlelist = get_articlelist(driver, target_url)
        print(articlelist)
        login(driver, mail, password)
        imglist = get_imglist(driver, articlelist)
        with open(tgt_dir + 'imglist.csv', 'x', encoding='utf-8') as file:
            writer = csv.writer(file, lineterminator='\n')
            writer.writerows(imglist)
            # f.writelines([d+"\n" for d in imglist])
            file.close
    else:
        with open(tgt_dir + 'imglist.csv', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            imglist = [row for row in reader]
            file.close
        login(driver, mail, password)
    write_img(driver, imglist, tgt_dir, target_name, download_path)
    print("Download Done!")
    driver.close


def login(driver, mail, password):
    driver.get('https://accounts.pixiv.net/login?prompt=select_account&return_to=https%3A%2F%2Fwww.fanbox.cc%2Fauth%2Fstart&source=fanbox')
    time.sleep(0.5)
    mailElement = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[3]/div[1]/div[2]/div/div/div/form/fieldset[1]/label/input')
    passwordElement = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[3]/div[1]/div[2]/div/div/div/form/fieldset[2]/label/input')
    mailElement.send_keys(mail)
    passwordElement.send_keys(password)
    button = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[3]/div[1]/div[2]/div/div/div/form/button')
    # ログインボタンをクリック
    button.click()
    time.sleep(2)
    if driver.current_url == "https://www.fanbox.cc/":
        print("login sucsess!")
    else:
        print("login Failled")
        sys.exit(1)


def get_articlelist(driver, target_url):
    articlelist = []
    for i in range(1, 999):
        driver.get(target_url + '?page=' + str(i))
        time.sleep(1)
        # print(target_url + '?page=' + str(i))
        print(driver.current_url)
        if driver.current_url == target_url:
            print("serch finish!")
            break
        articles = driver.find_elements(By.XPATH, '//a[@class="sc-1bjj922-0 gwbPAH"]')
        for j in range(len(articles)):
            article = driver.find_element(By.XPATH, "/html/body/div/div[5]/div[1]/div[2]/div[4]/div/div/div/div[1]/a[{}]".format(j + 1))
            articlelist.append(article.get_attribute('href'))
            print(article.get_attribute('href'))
        print(str(i) + " page " + str(len(articles)) + " articles")
    print("get {} artcles!".format(len(articlelist)))
    return articlelist


def get_imglist(driver, articlelist):
    imglist = []
    for i in range(len(articlelist)):
        driver.get(articlelist[len(articlelist) - i - 1])
        height = driver.execute_script("return document.body.scrollHeight")
        height = height / 430
        time.sleep(0.8)
        # scroll(driver, height, True)
        article_name: str = driver.find_element(By.XPATH, '//h1[@class="sc-1vjtieq-4 jPGGNN"]').get_attribute("innerHTML")
        idx = article_name.find("<")
        if idx != -1:
            shaped_article_name = article_name[:idx]
        else:
            shaped_article_name = article_name
        is_div = driver.find_elements(By.XPATH, '//div[@class="sc-1uv5uvv-0 dfWOmG"]')
        # 特定のdivが1の場合課金しないとダメ
        if len(is_div) == 1:
            print("{} is need maney".format(shaped_article_name))
        else:
            print("cullentservei is " + shaped_article_name + "  " + str(len(articlelist)) + "/" + str(i + 1) + ' {:.2%}'.format(i / len(articlelist)))
            imgparelent = driver.find_elements(By.XPATH, '//div[@class="sc-1vjtieq-1 eLScmM"]')
            if len(imgparelent) == 0:
                print("this article has not image")
            else:
                bool = True
                for k in range(10):
                    scroll(driver, height, bool)
                    nom = 1
                    count = 0
                    imgparelent = driver.find_elements(By.XPATH, '//div[@class="sc-1vjtieq-1 eLScmM"]')
                    imgs = imgparelent[0].find_elements(By.TAG_NAME, "img")
                    if len(imgs) == 0:
                        break
                    print("imgsnom is {}".format(len(imgs)))
                    imglistpart = []
                    for l in imgs:
                        imgurl = l.get_attribute('src')
                        if imgurl is not None:
                            count += 1
                        imglistpart.append([shaped_article_name + " P" + str(nom), imgurl])
                        nom += 1
                    print(count)
                    if len(imgs) == count:
                        for m in imglistpart:
                            imglist.append(m)
                        break
                    else:
                        bool = False
                # sys.exit(1)
            
    return imglist


def scroll(driver, height, bool):
    if bool:
        for i in range(1, int(height) - 2):
            driver.execute_script("window.scrollTo(0, "+str(i * 430)+");")
            time.sleep(0.35)
    else:
        for i in reversed(range(1, int(height))):
            driver.execute_script("window.scrollTo(0, "+str(i * 430)+");")
            time.sleep(0.35) 


def write_img(driver, imglist, tgt_dir, target_name, download_path):
    for i in imglist:
        print("downloading File :" + i[0])
        driver.get(i[1])
        img_name = target_name + " - " + i[0] + ".png"
        script_str = """
        window.URL = window.URL || window.webkitURL;
        var xhr = new XMLHttpRequest(),
        a = document.createElement('a'), file;
        xhr.open('GET', '""" + i[1] + """', true);
        xhr.responseType = 'blob';
        xhr.onload = function () {
        file = new Blob([xhr.response], { type : 'application/octet-stream' });
        a.href = window.URL.createObjectURL(file);
        a.download = '""" + img_name + """';
        a.click();
        };
        xhr.send();
        """
        driver.execute_script(script_str)
        # while os.path.isfile(download_path + img_name) is False:
        # time.sleep(0.2)
        time.sleep(1)
        download_bar = str(imglist.index(i) + 1) + "/" + str(len(imglist))
        print("{} downloaded!".format(download_bar))
        if os.path.isfile(download_path + img_name) is True:
            shutil.move(download_path + img_name, tgt_dir + img_name)


main()
