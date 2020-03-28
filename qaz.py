import requests
from bs4 import BeautifulSoup
import re
import time
import os
from cfscrape import get_cookie_string
from re import  search


# 通过cloudscraper获取可用的cookie以通过5s检测
def steal_library_header(url):
    print('正在尝试通过', url, '的5秒检测...')
    for retry in range(10):
        try:
            cookie_value, user_agent = get_cookie_string(url, timeout=15)
            print('通过5秒检测！\n')
            return {'User-Agent': user_agent, 'Cookie': cookie_value}
        except:
            print('通过失败，重新尝试...')
            continue
    print('>>无法通过javlibrary的5秒检测：', url)


# 找到访问页面所有页码的网址
def get_url(url, page_number):
    url_list = []
    url_initial = url
    for page in range(1, page_number + 1):
        url = f"{url_initial}{page}"
        url_list.append(url)
    return url_list


# '找到每一页的code，title，comment
def get_code(soup, issue_date, comment_number, header):
    path_page = 'D:/我/'
    code_list = []
    for item in soup.find_all(name='div', id=re.compile('vid_javli')):
        path = f'{path_page}{soup.title.string}/'
        if not os.path.isdir(path):
            os.makedirs(f'{path}/')
        address = item.a['href'].replace('./', '')
        link = 'http://www.n43a.com/cn/' + address
        picture_url = 'http:' + item.img['src'].replace('ps', 'pl')
        web_data_2 = requests.get(link, headers=header)
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
            if os.path.isfile(f"{path}{date}-{code}.{wanted_number}.jpg"):
                continue
            else:
                code_list.append(code)
                print('标题: ', name)
                print('发行日期: ', date)
                print('点击想要的数目: ', wanted_number)
                print('代码: ', code)
                print('link: ', link)
                print('picture_link: ', picture_url)
                for retry in range(8):
                    try:
                        picture_data = requests.get(picture_url, timeout=(6, 10))
                        with open(f"{path}{date}-{code}.{wanted_number}.jpg", 'wb') as f:
                            f.write(picture_data.content)
                            f.close()
                            print('>下载成功...')
                            print('-' * 100)
                            break
                    except:
                        # print(format_exc())
                        print('  >下载失败，重新下载...')
                        continue
    return code_list


# '返回codelist列表
def get_page_code(url, issue_date, comment_number, page_number, header):
    # 爬取所有页面
    url_list = get_url(url, page_number)
    count = 0
    code_list = []
    for url in url_list:
        count += 1
        print('\n', '*' * 40, f'第{count}页', '*' * 40)
        web_data = requests.get(url, headers=header)
        soup = BeautifulSoup(web_data.text, 'lxml')
        code_list += get_code(soup, issue_date, comment_number, header)
    return code_list


if __name__ == '__main__':
    main_url = 'http://www.n43a.com/cn/'  # 主网页
    issue_date = '2018-01-01'             # 起始日期
    comment_number = 500                  # 想要的数量
    # #########################################  通过获得的cookie取得爬虫header ##############################
    header = steal_library_header(url=main_url)
    # ################################################ 选择执行的选项 ########################################
    while True:
        selection = input('>>请输入数字以选择要更新的内容：\n'
                          '0. 更新今日热门\n'
                          '1. 更新数据库\n'
                          '2. 更新上月最想要\n'
                          '3. 更新上月评价最高\n'
                          '4. 更新全部最想要\n'
                          '5. 更新全部评价最高\n')
        try:
            if int(selection) == 0:
                start_url = main_url
                # #########################################  打印当前时间  ###############################################
                localtime = time.asctime(time.localtime(time.time()))
                print("本地时间为 :", localtime)
                # #########################################  找到爬取页面的页码和标题 #####################################
                web_data = requests.get(start_url, headers=header)
                soup = BeautifulSoup(web_data.text, 'lxml')
                page_title = soup.find('div', class_='boxtitle')
                print(f'页面标题是 {page_title.string}')
                # #########################################  打印该页面所有车牌号，并写入txt文件  #########################
                code_list = get_code(soup, issue_date, comment_number, header)
                print(code_list)
                code_path = os.path.join(os.path.expanduser('~'), 'Desktop')
                with open(f'{code_path}/{soup.title.string}.txt', 'a') as f:
                    f.write(str(code_list))
                    f.close()
                print('>>>>>>>已完成<<<<<<')
            if int(selection) == 1:
                player = {
                    '葵': 's=aevfo',
                    '希崎杰西卡': 's=p43q',
                    # '篠田ゆう': 's=amka',
                    '園田みおん': 's=ayuf2',
                    '岬ななみ': 's=aebfc',
                    '橋本ありな': 's=azfuu',
                    '三上悠亚': 's=ayera',
                    '铃村爱里': 's=ayote',
                    '深田えいみ': 's=ae4ua',
                    '春咲りょう': 's=aedcy',
                    '柏木胡桃': 's=aerck',
                    '水トさくら': 's=aepqm',
                    '野々浦暖': 's=aesse'
                }
                hrefs = list(player.values())
                for href in hrefs:
                    start_url = main_url + 'vl_star.php?' + href + '&page='  # 爬取该演员的所有页面
                    # #########################################  打印当前时间  ###############################################
                    localtime = time.asctime(time.localtime(time.time()))
                    print("本地时间为 :", localtime)
                    # #########################################  找到爬取页面的页码和标题 #####################################
                    web_data = requests.get(start_url, headers=header)
                    soup = BeautifulSoup(web_data.text, 'lxml')
                    page_url = soup.find('a', class_='page last')
                    page_num = re.findall(r'\=(\d+)$', page_url['href'])
                    page_number = int(page_num[0])
                    print(f'页面标题是 {soup.title.string}')
                    print(f"该页面一共有{page_number}页")  # 爬取页码范围是1-page_number
                    # #########################################  打印该页面所有车牌号，并写入txt文件  #########################
                    code_list = get_page_code(start_url, issue_date, comment_number, page_number, header)
                    print(code_list)
                    code_path = os.path.join(os.path.expanduser('~'), 'Desktop')
                    with open(f'{code_path}/{soup.title.string}.txt', 'a') as f:
                        f.write(str(code_list))
                        f.close()
                print('>>>>>>>已完成<<<<<<')
                break
            if int(selection) == 2:
                start_url = main_url + 'vl_mostwanted.php?&mode=1&page='    # 爬取上月最想要页面
                break
            if int(selection) == 3:
                start_url = main_url + 'vl_bestrated.php?&mode=1&page='     # 爬取上月最高评价页面
                break
            if int(selection) == 4:
                start_url = main_url + 'vl_mostwanted.php?&mode=2&page='    # 爬取全部最想要页面
                issue_date = '2018-01-01'  # 起始日期
                comment_number = 1500  # 想要的数量
                break
            if int(selection) == 5:
                start_url = main_url + 'vl_bestrated.php?&mode=2&page='     # 爬取全部最高评价页面
                issue_date = '2018-01-01'  # 起始日期
                comment_number = 1500  # 想要的数量
        except ValueError:
            print('\n>>>>>>>输入有误，请重新输入<<<<<<\n')
    if int(selection) != 1:
        # #########################################  打印当前时间  ###############################################
        localtime = time.asctime(time.localtime(time.time()))
        print("本地时间为 :", localtime)
        # #########################################  找到爬取页面的页码和标题 #####################################
        web_data = requests.get(start_url, headers=header)
        soup = BeautifulSoup(web_data.text, 'lxml')
        page_url = soup.find('a', class_='page last')
        page_num = re.findall(r'\=(\d+)$', page_url['href'])
        page_number = int(page_num[0])
        print(f'页面标题是 {soup.title.string}')
        print(f"该页面一共有{page_number}页")  # 爬取页码范围是1-page_number
        # #########################################  打印该页面所有车牌号，并写入txt文件  #########################
        code_list = get_page_code(start_url, issue_date, comment_number, page_number, header)
        print(code_list)
        code_path = os.path.join(os.path.expanduser('~'), 'Desktop')
        with open(f'{code_path}/{soup.title.string}.txt', 'a') as f:
            f.write(str(code_list))
            f.close()
        print('>>>>>>>已完成<<<<<<')

