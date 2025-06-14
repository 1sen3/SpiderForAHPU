import os
import json

if not os.path.exists("settings.json"):
    default_settings = {
        "username": "",
        "password": "",
        "is_unified_identity_auth": False,
        "is_first_start": True
    }
    with open("settings.json", 'w', encoding='utf-8') as settings_json:
        json.dump(default_settings, settings_json, ensure_ascii=False)

with open("settings.json", 'r', encoding='utf-8') as settings_json:
    settings = json.load(settings_json)

def edit_settings(username, password, is_unified_identity_auth):
    settings["username"] = username
    settings["password"] = password
    settings["is_unified_identity_auth"] = is_unified_identity_auth
    settings["is_first_start"] = False

    with open("settings.json", 'w', encoding='utf-8') as settings_json:
        json.dump(settings, settings_json, ensure_ascii=False)

username = settings["username"]
password = settings["password"]
# 是否使用统一身份认证登录
is_unified_identity_auth = settings["is_unified_identity_auth"]
# 是否首次启动
is_first_start = settings["is_first_start"]

# 获取当前路径
current_path = os.getcwd()

# 创建 scores 文件夹（如果不存在）
scores_dir = os.path.join(current_path, "scores")
os.makedirs(scores_dir, exist_ok=True)

# 创建 exams 文件夹（如果不存在）
exams_dir = os.path.join(current_path, "exams")
os.makedirs(exams_dir, exist_ok=True)

# 从年份创建成绩文件路径
def get_scores_file(year):
    file_name = year + " 成绩.csv"
    scores_file = os.path.join(scores_dir,file_name)
    return scores_file

# 从学期创建考试文件路径
def get_exams_file(year):
    file_name = year + " 考试.csv"
    exams_file = os.path.join(exams_dir,file_name)
    return exams_file