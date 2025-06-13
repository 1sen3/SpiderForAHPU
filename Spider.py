from prettytable import PrettyTable
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import config
import csv

# 指定 ChromeDriver 的路径
chromedriver_path = r"C:\Program Files\Google\Chrome\Application\chromedriver.exe"

# 创建一个 Service 对象，并传递 chromedriver 的路径
service = Service(executable_path=chromedriver_path)

# 实例化配置对象
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.page_load_strategy = "eager"
options.add_argument("--disable-gpu")

# 创建WebDriver对象
driver = webdriver.Chrome(service=service,options=options)

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

    print("登录成功")

def comple_score(row):
    if len(row) == 10:
        row.insert(6,' ')
        row.insert(7,' ')
    elif len(row) == 11:
        row.insert(6,' ')

def get_scores():
    print('开始查询成绩')
    time.sleep(1)
    # 获取成绩
    driver.find_element(By.XPATH,'//*[@id="menu_panel"]/ul/li[1]/ul/div/li[12]/a').click()
    wait = WebDriverWait(driver, 20)
    scores = wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/table/tbody/tr[1]/td[3]/div/div/div[3]/div/table')))
    scores_text = scores.text
    # 写入CSV文件
    lines = scores_text.split('\n')
    if len(lines) == 1:
        print("当前学期暂无成绩信息")
        return
    year = lines[1].split()[0] + "学年第" +  lines[1].split()[1] + "学期"
    with open(config.get_scores_file(year), 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        # 处理表头
        header = lines[0].split()
        table = PrettyTable(header)
        writer.writerow(header)

        for line in lines[1:]:
            row = line.split()
            row[0] = row[0] + ' ' + row[1]
            del row[1]
            if len(row) != 12:
                comple_score(row)
            table.add_row(row)
            writer.writerow(row)
    print(table)
    print(f'成绩已保存到{year} 成绩.csv')

def get_courses():
    print('开始查询课表')
    time.sleep(1)
    # 获取课表

def get_exams():
    print('开始查询考试')
    time.sleep(1)
    # 获取考试
    driver.find_element(By.XPATH,'//*[@id="menu_panel"]/ul/li[1]/ul/div/li[11]/a').click()
    wait = WebDriverWait(driver, 20)
    exams = wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/table/tbody/tr[1]/td[3]/div/div[3]/div[2]/table')))
    exams_text = exams.text
    print(exams_text)

    # 写入 CSV 文件
    lines = exams_text.split('\n')
    with open(config.exams_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for line in lines:
            row = line.split()
            writer.writerow(row)

    print('考试信息已保存到exams.csv')

if __name__ == "__main__":
    if config.is_first_start:
        username = input("请输入学号:")
        password = input("请输入密码:")
        choice = input("是否使用统一身份认证登录? (y:n):")
        if choice in ("y","Y"):
            is_unified_identity_auth = True
        else:
            is_unified_identity_auth = False
        config.edit_settings(username,password,is_unified_identity_auth)

    login(config.username, config.password)
    get_scores()
    # get_exams()