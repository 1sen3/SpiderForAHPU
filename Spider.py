import os

from prettytable import PrettyTable
from requests import session
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import requests
from bs4 import BeautifulSoup as bs
import lxml
import converter
import config
import sys

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

session = requests.Session()

query_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
    'Connection': 'keep-alive',
    'Referer': 'http://xjwxt.ahpu.edu.cn/ahpu/localLogin.action',
}

url = 'http://xjwxt.ahpu.edu.cn/ahpu/localLogin.action'
query_scores_url = 'http://xjwxt.ahpu.edu.cn/ahpu/teach/grade/course/person!search.action?semesterId='
query_exams_url = 'http://xjwxt.ahpu.edu.cn/ahpu/stdExamTable!examTable.action?semester.id='

def edit_settings():
    username = input("请输入学号:")
    password = input("请输入密码:")

    # 暂不考虑实现统一身份认证登录
    # choice = input("是否使用统一身份认证登录? (y:n):")
    # if choice in ("y","Y"):
    #     is_unified_identity_auth = True
    # else:
    #     is_unified_identity_auth = False

    config.edit_settings(username, password, True)
    driver.quit()
    main()

def init():
    if config.get_is_first_start():
        edit_settings()

def get_cookies(username, password):
    driver.get(url)

    # 账号输入框
    usernamebox = driver.find_element(By.XPATH,'//*[@id="username"]')
    usernamebox.send_keys(username)

    # 密码输入框
    passwordbox = driver.find_element(By.XPATH,'//*[@id="password"]')
    passwordbox.send_keys(password)

    time.sleep(1)

    # 登录按钮
    login_btn = driver.find_element(By.XPATH,'//*[@id="loginForm"]/table[2]/tbody/tr[6]/td/input')
    login_btn.click()

    got_cookies = driver.get_cookies()
    cookies = {}
    for cookie in got_cookies:
        if cookie['name'] in ['JSESSIONID', 'srv_id', 'GSESSIONID', 'semester.id']:
            cookies[cookie['name']] = cookie['value']
    return cookies

    return cookies

def login(username, password):
    print("登录中...")
    cookies = get_cookies(username, password)

    for name, value in cookies.items():
        session.cookies.set(name, value)

    print("登录成功...")

def get_scores(sid):
    print('开始查询成绩...')
    query_score = session.post(query_scores_url + f"{sid}", headers=query_headers)
    soup = bs(query_score.text, 'lxml')
    grades_table = soup.find("table")

    headers = [th.text.strip() for th in grades_table.find_all('th')]
    table = PrettyTable(headers)

    all_rows = []
    for row in grades_table.find_all('tr')[1:]:
        row_data = [td.text.strip() for td in row.find_all('td')]
        if row_data:
            all_rows.append(row_data)
            table.add_row(row_data)

    filename = config.get_scores_file(converter.trans_sid_to_year(sid))

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(all_rows)

    print(table)
    print(f"已将成绩保存到 {filename}")

def get_exams(sid):
    print('开始查询考试')
    query_exams = session.post(query_exams_url + f"{sid}", headers=query_headers)
    soup = bs(query_exams.text, 'lxml')
    exams_table = soup.find('table')
    headers = [th.text.strip() for th in exams_table.find_all('th')]
    table = PrettyTable(headers)

    all_rows = []
    for row in exams_table.find_all('tr')[1:]:
        row_data = [td.text.strip() for td in row.find_all('td')]
        if row_data:
            all_rows.append(row_data)
            table.add_row(row_data)

    filename = config.get_exams_file(converter.trans_sid_to_year(sid))

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(all_rows)

    print(table)
    print(f"已将考试保存到 {filename}")


def show_main_menu():
    print("\n" + "=" * 30)
    print("安徽工程大学成绩查询系统")
    print("=" * 30)
    print("1. 查询成绩")
    print("2. 查询考试")
    print("3. 修改账号")
    print("4. 退出系统")
    print("=" * 30)


def get_semester_input():
    while True:
        try:
            year = int(input("请输入年份 (以第一年为标准，如 2024-2025 则输入2024): "))
            semester = int(input("请输入学期 (1 - 2): "))
            if semester not in (1, 2):
                print("学期输入错误，请输入1或2")
                continue
            return converter.trans_year_to_sid(year, semester)
        except ValueError:
            print("输入无效，请输入数字")


def main():
    init()
    login(config.get_useraname(), config.get_password())

    while True:
        os.system("cls")
        show_main_menu()
        try:
            choice = int(input("请选择操作 (1 - 4): "))
            os.system("cls")
            if choice == 1:
                print("\n" + "-" * 20 + "成绩查询" + "-" * 20)
                sid = get_semester_input()
                get_scores(sid)
            elif choice == 2:
                print("\n" + "-" * 20 + "考试查询" + "-" * 20)
                sid = get_semester_input()
                get_exams(sid)
            elif choice == 3:
                print("\n" + "-" * 20 + "修改账号" + "-" * 20)
                edit_settings()
                return
            elif choice == 4:
                driver.quit()
                sys.exit(0)
            else:
                print("输入无效，请输入 1 - 4 之间的数字")

            input("\n按任意键返回主菜单...")

        except ValueError:
            print("输入无效，请输入数字")
        except KeyboardInterrupt:
            print("\n检测到中断，正在退出...")
            driver.quit()
            sys.exit(0)

if __name__ == "__main__":
    main()