from datetime import datetime

async def main(args: Args) -> Output:
    # 获取当前日期
    today = datetime.now()
    
    # 判断应该筛选哪个月的数据
    # 如果当前日期是当月的最后10天（day > 20），筛选当月数据
    # 如果日期是月初20天内（day <= 20），筛选上个月数据
    if today.day > 20:
        # 筛选当月数据
        month_value = "CurrentMonth"
    else:
        # 筛选上个月数据
        month_value = "LastMonth"
    
    # 构建完整的 filter 对象
    filter_obj = {
        "filter": {
            "conjunction": "and",
            "conditions": [
                {
                    "field_name": "更新日期",
                    "operator": "is",
                    "value": [month_value]
                }
            ]
        }
    }
    
    # 返回结果
    ret: Output = {
        "filter": filter_obj
    }
    
    return ret

