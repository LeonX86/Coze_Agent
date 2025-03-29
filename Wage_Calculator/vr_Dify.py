import requests
import datetime
import calendar

def get_month_work_days(year: int, month: int, week_days: int = 5) -> dict:
    """
    计算指定月份的工作天数、休息日天数等信息

    参数:
    year: 年份
    month: 月份
    week_days: 每周工作天数，默认为5（周一至周五）

    返回:
    包含月份信息的字典
    """
    # 构建日期字符串
    date_str = f"{year}-{month:02d}"

    # 添加请求头，模拟浏览器请求
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Referer': 'http://timor.tech/'
    }

    # 调用节假日API
    url = f"http://timor.tech/api/holiday/year/{date_str}"
    response = requests.get(url, headers=headers)

    # 获取当月总天数
    total_days = calendar.monthrange(year, month)[1]

    # 初始化工作日和休息日计数
    work_days = 0
    rest_days = 0
    rest_day_list = []  # 休息日列表
    work_day_list = []  # 工作日列表

    # 检查响应状态
    if response.status_code == 200:
        holiday_info = response.json()

        # 遍历当月每一天
        for day in range(1, total_days + 1):
            date = datetime.date(year, month, day)
            day_str = f"{month:02d}-{day:02d}"
            weekday = date.weekday()  # 0-6，0是周一，6是周日

            # 判断是否为节假日或补班
            if day_str in holiday_info.get('holiday', {}):
                day_info = holiday_info['holiday'][day_str]
                if day_info.get('holiday', False):
                    # 是节假日
                    rest_days += 1
                    rest_day_list.append(date.strftime("%Y-%m-%d"))
                else:
                    # 是补班
                    work_days += 1
                    work_day_list.append(date.strftime("%Y-%m-%d"))
            else:
                # 不是特殊日期，根据week_days参数判断
                if weekday < week_days:  # 如果week_days=6，则0-5(周一至周六)为工作日
                    work_days += 1
                    work_day_list.append(date.strftime("%Y-%m-%d"))
                else:  # 其余为休息日
                    rest_days += 1
                    rest_day_list.append(date.strftime("%Y-%m-%d"))
    else:
        # API请求失败，按照week_days参数计算
        print("API请求失败，按照常规周末和工作日计算")
        for day in range(1, total_days + 1):
            date = datetime.date(year, month, day)
            weekday = date.weekday()
            if weekday < week_days:
                work_days += 1
                work_day_list.append(date.strftime("%Y-%m-%d"))
            else:
                rest_days += 1
                rest_day_list.append(date.strftime("%Y-%m-%d"))

    return {
        "year_month": f"{year}-{month:02d}",
        "total_days": total_days,
        "work_days": work_days,
        "rest_days": rest_days,
        "rest_day_list": rest_day_list,
        "work_day_list": work_day_list  # 新增：返回工作日列表
    }



def main(salary: float, start_time: int, end_time: int, week_days: int, month: str) -> dict:
    daily_work_time = end_time - start_time
    if daily_work_time < 0:
        daily_work_time += 24


    # 处理月份参数
    if month == "0":
        # 获取当前月份
        current_date = datetime.datetime.now()
        year = current_date.year
        month_num = current_date.month
        month_str = f"{year}-{month_num:02d}"
    else:
        # 解析格式为 "2025-03" 的月份字符串
        year, month_num = map(int, month.split('-'))
        month_str = month


    # total_days = get_month_work_days(year, month_num, week_days)['work_days']
    days_info = get_month_work_days(year, month_num, week_days)
    total_days = days_info['total_days']
    work_days = days_info['work_days']
    rest_days = days_info['rest_days']
    rest_day_list = days_info['rest_day_list']
    work_day_list = days_info['work_day_list']

    #计算月度总工作时间
    monthly_work_time = daily_work_time * work_days
    #计算时薪
    hourly_rate = salary /  (work_days * daily_work_time)

    return {
        "daily_work_time": daily_work_time,
        "monthly_work_time": monthly_work_time,
        "hourly_rate": hourly_rate,
        "total_days": total_days,
        "work_days": work_days,
        "rest_days": rest_days,
        "rest_day_list": rest_day_list,
        "work_day_list": work_day_list,
        "month_str": month_str  # 新增：返回月份字符串
    }

main(12000, 9, 18, 5, "0")