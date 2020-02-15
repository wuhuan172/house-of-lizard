from bs4 import BeautifulSoup
import re
import time
import os
import cloudscraper
import requests

headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}


def get_url(url, page_number):
    url_list = []
    url_initial = url
    for page in range(1, page_number + 1):
        url = f"{url_initial}{page}"  # all
        url_list.append(url)
    return url_list


def get_code(soup, issue_date, comment_number):
    path_page = r'D:/我/'
    code_list = []
    for item in soup.find_all(name='div', id=re.compile('vid_javli')):
        path = f'{path_page}{soup.title.string}/'
        if not os.path.isdir(path):
            os.makedirs(f'{path}/')
        address = item.a['href'].replace('./', '')
        link = 'http://www.n43a.com/cn/' + address
        picture_url = 'http:' + item.img['src'].replace('ps', 'pl')

        web_data_2 = requests.get(link, headers=headers)
        soup_2 = BeautifulSoup(web_data_2.text, 'lxml')

        name = soup_2.title.text
        date = soup_2.find(name='td', class_='text', string=re.compile(r'^\d'))
        date = date.string
        wanted_number = soup_2.find(name='a', href=re.compile('userswanted.php'))
        wanted_number = int(wanted_number.string)
        code = soup_2.find(name='td', class_='text', string=re.compile(r'^[a-zA-Z]'))
        code = code.string
        # print(name, date, code, wanted_number)
        if date > issue_date and wanted_number > comment_number:
            comment_url =link = 'http://www.n43a.com/cn/' + 'videocomments.php' + address
            comment_page_number = get_page_num(comment_url)
            code_list.append(code)
            print('name: ' + name)
            print('issue date: ', date)
            print('comment number: ', wanted_number)
            print('code: ', code)
            print('link: ', link)
            print('picture_link: ', picture_url)
            picture_data = requests.get(picture_url)
            with open(f"{path}{date}-{code}.jpg", 'wb') as f:
                f.write(picture_data.content)
                f.close()
                print("picture saved")
                print('-'*120)
    return code_list


def get_page_code(url, issue_date, comment_number, page_number):
    url_list = get_url(url, page_number)
    count =0
    code_list = []
    for url in url_list:
        count += 1
        print('*'*40, f'第{count}页', '*'*40)
        web_data = requests.get(url, headers=headers)
        soup = BeautifulSoup(web_data.text, 'lxml')
        code_list += get_code(soup,issue_date, comment_number)
    return code_list


def get_page_num(url):
    web_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(web_data.text, 'lxml')
    page_url = soup.find(name='a', attrs={'class': 'page last'})
    pattern = re.compile('\=(\d+)$')
    page_num = re.findall(pattern, page_url['href'])
    return page_num[0]


if __name__ == '__main__':

    # href = 's=p43q'  #希崎杰西卡
    # href = 's=amka'  #篠田ゆう
    href = 's=ayuf2'
    href = 's=aebfc'
    start_url = 'http://www.n43a.com/cn/vl_star.php?&mode=&' + href + '&page='  # 爬取喜欢的页面
    # start_url = 'http://www.n43a.com/cn/vl_mostwanted.php?&mode=1&page='    # 爬取上月最想要页面
    # start_url = 'http://www.n43a.com/cn/vl_mostwanted.php?&mode=2&page='    # 爬取全部最想要页面
    # start_url = 'http://www.n43a.com/cn/vl_bestrated.php?&mode=1&page='     # 爬取上月最高评价页面
    # start_url = 'http://www.n43a.com/cn/vl_bestrated.php?&mode=2&page='     # 爬取全部最高评价页面
    issue_date = '2018-01-01'
    comment_number = 1000

    page_number = int(get_page_num(start_url))
    web_data = requests.get(start_url, headers=headers)
    soup = BeautifulSoup(web_data.text, 'lxml')

    print(soup.title.string)
    print(f"该页面一共有{page_number}页")  # 爬取页码范围是1-page_number
    localtime = time.asctime(time.localtime(time.time()))
    print("本地时间为 :", localtime)
    code_list = (get_page_code(start_url, issue_date, comment_number, page_number))
    print(code_list)
    with open(f'c:/Users/wuhua/desktop/{soup.title.string}.txt', 'a') as f:
        f.write(str(code_list))
        f.close()
