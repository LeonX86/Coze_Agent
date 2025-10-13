# 在这里，您可以通过 'args'  获取节点中的输入变量，并通过 'ret' 输出结果

from datetime import datetime, timedelta
import json

async def main(args: Args) -> Output:
    # 获取参数
    params = args.params
    data = params.get('data', {})
    
    # 构建输出列表
    result_list = []
    
    # 从 data 字典中获取 items 列表
    items = data.get('items', [])
    
    if not items:
        result_list.append("错误：data 中没有 items 或 items 为空")
        return {"result": result_list}
    
    # 获取上个月的时间戳范围（毫秒）
    today = datetime.now()
    first_day_this_month = datetime(today.year, today.month, 1)
    last_day_last_month = first_day_this_month - timedelta(days=1)
    first_day_last_month = datetime(last_day_last_month.year, last_day_last_month.month, 1)
    start_timestamp = int(first_day_last_month.timestamp() * 1000)
    end_timestamp = int(first_day_this_month.timestamp() * 1000)
    
    # 从字段数据中提取文本内容并清除换行符
    def extract_text(field_data):
        if not field_data:
            return "无"
        texts = []
        for item in field_data:
            if isinstance(item, dict) and 'text' in item:
                text = str(item['text']).replace('\n', ' ').replace('\r', ' ')
                texts.append(text)
        return ' '.join(texts) if texts else "无"
    
    # 遍历所有项目记录
    count = 0
    for item in items:
        # 解析 fields 字段（它是一个 JSON 字符串）
        fields_str = item.get('fields', '{}')
        try:
            fields = json.loads(fields_str)
        except:
            continue
        
        # 获取更新日期
        update_date = fields.get('更新日期', 0)
        
        # 判断是否在上个月范围内
        if start_timestamp <= update_date < end_timestamp:
            count += 1
            
            # 提取项目名称
            project_name_list = fields.get('项目名称', [])
            project_name = extract_text(project_name_list)
            
            # 提取最新进展记录
            latest_progress = fields.get('最新进展记录', [])
            latest_text = extract_text(latest_progress)
            
            # 提取上月记录
            last_month_record = fields.get('上月记录', [])
            last_month_text = extract_text(last_month_record)
            
            # 组合成字符串
            result_str = f"（{count}）{project_name}\n最新进展记录：{latest_text}\n上月进展记录：{last_month_text}"
            result_list.append(result_str)
    
    # 如果没有找到记录
    if count == 0:
        result_list.append(f"未找到上个月（{first_day_last_month.strftime('%Y年%m月')}）更新的记录")
    
    # 返回结果
    ret: Output = {
        "result": result_list
    }
    
    return ret