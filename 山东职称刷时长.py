import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ChromeOptions, ActionChains

url = 'http://sdld.gxk.yxlearning.com/my/learning'
#url = 'http://sdld.zyk.yxlearning.com/my/learning'
options = webdriver.ChromeOptions()
options.add_argument(r"user-data-dir=C:/Users/Lizard/Desktop/abc") #设置自动软件临时工作文件夹，否则出data页面
options.add_argument('disable-infobars') #不显示正在受自动软件控制
driver = webdriver.Chrome(chrome_options=options)

# 打开页面，并设置等待时间，防止加载缓慢
driver.get(url)
wait = WebDriverWait(driver, 10)

# 手动login，找到btn元素
login = driver.find_element_by_class_name('btn-change-block')
login.click()

# 设置等待时间，并完成cross-check
time.sleep(5)
driver.refresh() #刷新页面

# 定位总元素，并统计所有元素的数量
learning = driver.find_elements_by_xpath('//div[@class="col-xs-12 col-sm-12 col-md-6 col-lg-4"]')
total_num = int(len(learning))
print(f'共有{total_num}个课程')

for abc in range(total_num):
    time.sleep(5)
    # 通过父节点定位子节点，找到元素的总进度current_progress
    learning = driver.find_elements_by_xpath('//div[@class="col-xs-12 col-sm-12 col-md-6 col-lg-4"]')
    current_learn_progress_top = (learning[abc].find_elements_by_xpath('//div[@class="progress progress-striped progress-border"]'))[abc]     #爷爷节点
    current_learn_progress_mid = (current_learn_progress_top.find_elements_by_xpath('//div[@class="progress-bar progress-bar-info"]'))[int(2*abc)]  #父亲节点
    current_learn_progress_bot = (current_learn_progress_mid.find_elements_by_xpath('//span[@class="sr-only"]'))[int(2*abc)]                       #子孙节点
#    current_learn_progress_bot =current_learn_progress_bot[abc]
    current_learn_value = current_learn_progress_bot.text
    print(f'第{abc+1}个课程进度为{current_learn_value}')
    print('*****')

    # 如果该总进度未完成，则进入该课程
    if current_learn_value != '100.0%':
        sublearn = learning[abc]
        sublearn.click()
        time.sleep(5)
        # 找到本元素
        # ******************************************************************************************************************************是否可删除待定
        parents = driver.find_element_by_xpath('//ul[@class="pt5"]')
        print(parents)

        # 找到本元素中所有子课程，以判断是否停止
        children = driver.find_elements_by_xpath('//ul[@class="pt5"]/li')
        print(f'共有{len(children)}个子课程')
        print(children)

        # 找到最后一个小节，并查询该小节，判断是否都完成
        position = int(len(children))-1
        print(position)
        last = children[position]
        print(last)
        sub_learn_progress_top = last.find_elements_by_xpath('//div[@class="progress video-progress"]')[-1]
        sub_learn_progress_final = sub_learn_progress_top.find_elements_by_xpath('//span[@class="badge"]')[-1]
        sub_learn_value = sub_learn_progress_final.text
        print(f'最后一个子课程已完成{sub_learn_value}')

        # 判断元素的进度
        count = 0
        while count < 500000:
            if sub_learn_value != '100%':
                time.sleep(10)
                position = int(len(children)) - 1
                last = children[position]
                sub_learn_progress_top = last.find_elements_by_xpath('//div[@class="progress video-progress"]')[-1]
                sub_learn_progress_final = sub_learn_progress_top.find_elements_by_xpath('//span[@class="badge"]')[-1]
                sub_learn_value = sub_learn_progress_final.text
                print(f'最后一个子课程已完成{sub_learn_value}')
            else:
                print('本课程已完成')
                driver.back()
                time.sleep(5)
                break
            count = count + 1
    else:
        continue