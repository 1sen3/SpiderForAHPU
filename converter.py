# 将 semesterid 转换为年份 + 学期
def trans_sid_to_year(sid):
    if sid < 41:
        if sid == 1:
            return "2003-2004学年2学期"
        else:
            year = 2003 + sid // 2
            semester = sid % 2 + 1
            result = f"{year}-{year + 1}学年{semester}学期"
    else:
        if sid < 101:
            year = 2020 + sid // 40
            semester = sid % 40
            result = f"{year - 1}-{year}学年{semester}学期"
        elif sid < 141:
            sid -= 100
            year = 2022 + sid // 20
            semester = sid % 20
            result = f"{year}-{year + 1}学年{semester}学期"
        elif sid < 181:
            if sid == 141:
                return "2024-2025学年1学期"
            elif sid == 161:
                return "2024-2025学年2学期"
        else:
            sid -= 180
            year = 2025 + sid // 20
            semester = sid % 20
            result = f"{year}-{year + 1}学年{semester}学期"
    return result

# 将年份 + 学期转换为 sid,年份以第一个年份为准
def trans_year_to_sid(year,semester):
    if year < 2003:
        return 0
    if year == 2003:
        return 1
    elif 2003 < year < 2020:
        sid = 1 + (year - 2004) * 2 + semester
    elif 2020 <= year < 2022:
        sid = 40 + (year - 2020) * 40 + semester
    else:
        if year == 2023:
            sid = 120 + semester
        elif year == 2024:
            sid = 121 + semester * 20
        else:
            sid = 180 + (year - 2025) * 20 + semester
    return sid

if __name__ == '__main__':
    sid = int(input("请输入sid:"))
    year = trans_sid_to_year(sid)
    print(year)
    # year = int(input("请输入年份:"))
    # semester = int(input("请输入学期号:"))
    # sid = trans_year_to_sid(year,semester)
    # print(sid)
