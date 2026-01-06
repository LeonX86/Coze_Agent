from datetime import datetime

async def main(args: Args) -> Output:
    # 获取当前年份
    current_year = datetime.now().year
    
    # 转换为四位数字的字符串
    year_str = str(current_year)
    
    # 返回结果
    ret: Output = {
        "year": year_str
    }
    return ret