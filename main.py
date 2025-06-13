from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import config
import csv
import os

# 指定 ChromeDriver 的路径
chromedriver_path = r"C:\Program Files\Google\Chrome\Application\chromedriver.exe"

# 创建一个 Service 对象，并传递 chromedriver 的路径
service = Service(executable_path=chromedriver_path)

# 实例化配置对象
options = webdriver.ChromeOptions()

# 配置对象添加开启无界面模式的命令
options.add_argument("--headless")

# 实例化带有配置对象的 driver 对象
options.add_argument("--disable-gpu")

# 创建WebDriver对象
driver = webdriver.Chrome(service=service,options=options)

# 获取当前路径
current_path = os.getcwd()

# 创建 scores 文件夹（如果不存在）
scores_dir = os.path.join(current_path, "scores")
os.makedirs(scores_dir, exist_ok=True)

# 成绩文件路径
scores_file = os.path.join(scores_dir, "scores.csv")

def login(username,password):
    wait = WebDriverWait(driver, 10)
    url = 'http://xjwxt.ahpu.edu.cn/ahpu/localLogin.action'
    driver.get(url)

    # 账号输入框
    username = driver.find_element(By.XPATH,'//*[@id="username"]')
    username.send_keys('3231002141')

    # 密码输入框
    password = driver.find_element(By.XPATH,'//*[@id="password"]')
    password.send_keys('02439X')

    time.sleep(1)

    # 登录按钮
    login_btn = driver.find_element(By.XPATH,'//*[@id="loginForm"]/table[2]/tbody/tr[6]/td/input')
    login_btn.click()

    print('开始查询')
    time.sleep(1)

    # 获取成绩
    driver.find_element(By.XPATH,'//*[@id="menu_panel"]/ul/li[1]/ul/div/li[12]/a').click()
    wait = WebDriverWait(driver, 20)
    scores = wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/table/tbody/tr[1]/td[3]/div/div/div[3]/div/table')))
    scores_text = scores.text
    print(scores_text)

    # 写入CSV文件
    lines = scores_text.split('\n')
    with open(scores_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for line in lines:
            row = line.split()
            writer.writerow(row)

    print('成绩已保存到scores.csv')

if __name__ == "__main__":
    login(config.username, config.password)