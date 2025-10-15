from datetime import datetime, timedelta
import json

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

# 生成统计表格
def generate_stats_table(stats_data):
    table_lines = []
    # 表头
    table_lines.append("| 类型 | 战客 | 锡山 | 惠山 | 其他 | 数智化 | 网络 | 工程 | 综合 | 市场 | 工会 | 品管 | 财务 | 一线网格 |")
    table_lines.append("|------|------|------|------|------|--------|------|------|------|------|------|------|------|----------|")
    
    # 数据行
    for project_type in ['售中', '售前', '开发', '合计']:
        row = [project_type]
        for dept in ['战客', '锡山', '惠山', '其他', '数智化', '网络', '工程', '综合', '市场', '工会', '品管', '财务', '一线网格']:
            count = stats_data.get(project_type, {}).get(dept, 0)
            row.append(str(count))
        table_lines.append("| " + " | ".join(row) + " |")
    
    return "\n".join(table_lines)

# 生成项目清单表格（售中、售前）
def generate_project_table(projects):
    if not projects:
        return "| 类型 | 技术方向 | 内/外 | 支撑部门 | 项目名称 |\n|------|----------|-------|----------|----------|"
    
    table_lines = []
    table_lines.append("| 类型 | 技术方向 | 内/外 | 支撑部门 | 项目名称 |")
    table_lines.append("|------|----------|-------|----------|----------|")
    
    for project in projects:
        table_lines.append(f"| {project['类型']} | {project['技术方向']} | {project['内外']} | {project['支撑部门']} | {project['项目名称']} |")
    
    return "\n".join(table_lines)

# 生成需求清单表格（开发）
def generate_requirement_table(requirements):
    if not requirements:
        return "| 类型 | 技术方向 | 内/外 | 支撑部门 | 需求名称 | 当前进度 |\n|------|----------|-------|----------|----------|----------|"
    
    table_lines = []
    table_lines.append("| 类型 | 技术方向 | 内/外 | 支撑部门 | 需求名称 | 当前进度 |")
    table_lines.append("|------|----------|-------|----------|----------|----------|")
    
    for req in requirements:
        table_lines.append(f"| {req['类型']} | {req['技术方向']} | {req['内外']} | {req['支撑部门']} | {req['需求名称']} | {req['当前进度']} |")
    
    return "\n".join(table_lines)

async def main(args: Args) -> Output:
    # 获取参数
    params = args.params
    data = params.get('data', {})
    
    # 从 data 字典中获取 items 列表
    items = data.get('items', [])
    
    if not items:
        return {
            "result": ["错误：data 中没有 items 或 items 为空"],
            "report_title": "数据错误",
            "stats_table": "",
            "project_table": "",
            "requirement_table": "",
            "summary_stats": ""
        }
    
    # 获取上个月的时间戳范围（毫秒）
    today = datetime.now()
    first_day_this_month = datetime(today.year, today.month, 1)
    last_day_last_month = first_day_this_month - timedelta(days=1)
    first_day_last_month = datetime(last_day_last_month.year, last_day_last_month.month, 1)
    start_timestamp = int(first_day_last_month.timestamp() * 1000)
    end_timestamp = int(first_day_this_month.timestamp() * 1000)
    
    # 生成月报标题
    report_title = f"数智化中心软研月报（{last_day_last_month.strftime('%Y年%m月')}）"
    
    # 初始化统计数据
    stats = {
        '售中': {'战客': 0, '锡山': 0, '惠山': 0, '其他': 0, '数智化': 0, '网络': 0, '工程': 0, '综合': 0, '市场': 0, '工会': 0, '品管': 0, '财务': 0, '一线网格': 0},
        '售前': {'战客': 0, '锡山': 0, '惠山': 0, '其他': 0, '数智化': 0, '网络': 0, '工程': 0, '综合': 0, '市场': 0, '工会': 0, '品管': 0, '财务': 0, '一线网格': 0},
        '开发': {'战客': 0, '锡山': 0, '惠山': 0, '其他': 0, '数智化': 0, '网络': 0, '工程': 0, '综合': 0, '市场': 0, '工会': 0, '品管': 0, '财务': 0, '一线网格': 0},
        '合计': {'战客': 0, '锡山': 0, '惠山': 0, '其他': 0, '数智化': 0, '网络': 0, '工程': 0, '综合': 0, '市场': 0, '工会': 0, '品管': 0, '财务': 0, '一线网格': 0}
    }
    
    # 项目和需求列表
    projects = []  # 售中、售前项目
    requirements = []  # 开发需求
    
    # 总体统计
    total_count = 0
    sell_count = 0
    presale_count = 0
    dev_count = 0
    completed_count = 0
    ongoing_count = 0
    external_count = 0
    internal_count = 0
    ai_count = 0
    rpa_count = 0
    
    # 构建输出列表
    result_list = []
    
    # 遍历所有项目记录
    filtered_count = 0
    for item in items:
        # 解析 fields 字段（它是一个 JSON 字符串）
        fields_str = item.get('fields', '{}')
        try:
            fields = json.loads(fields_str)
        except:
            continue
        
        # 获取更新日期
        update_date = fields.get('更新日期', 0)
        
        # 判断是否在上个月范围内更新
        if start_timestamp <= update_date < end_timestamp:
            filtered_count += 1
            
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
            result_str = f"（{filtered_count}）{project_name}\n最新进展记录：{latest_text}\n上月进展记录：{last_month_text}"
            result_list.append(result_str)
            
            # 统计上个月更新的项目
            project_type = fields.get('项目类型', '')
            project_attr = fields.get('项目属性', '')
            tech_direction = fields.get('技术方向', '')
            dept_list = fields.get('归属', [])
            dept = extract_text(dept_list) if dept_list else '其他'
            progress = fields.get('进展', '')
            
            # 映射部门名称
            dept_mapping = {
                '战客': '战客', '锡山': '锡山', '惠山': '惠山', '数智化': '数智化',
                '网络': '网络', '工程': '工程', '综合': '综合', '市场': '市场',
                '工会': '工会', '一线网格': '一线网格', '一线': '一线网格',
                '品管': '品管', '财务': '财务'
            }
            mapped_dept = dept_mapping.get(dept, '其他')
            
            if project_type in ['售中', '售前', '开发']:
                total_count += 1
                
                # 统计各维度数据
                if project_type == '售中':
                    sell_count += 1
                elif project_type == '售前':
                    presale_count += 1
                elif project_type == '开发':
                    dev_count += 1
                
                if progress == '已完成':
                    completed_count += 1
                elif progress == '进行中':
                    ongoing_count += 1
                
                if project_attr == '对外':
                    external_count += 1
                elif project_attr == '对内':
                    internal_count += 1
                
                if '大模型' in tech_direction or 'AI' in tech_direction:
                    ai_count += 1
                elif 'RPA' in tech_direction:
                    rpa_count += 1
                
                # 更新统计表
                if project_type in stats and mapped_dept in stats[project_type]:
                    stats[project_type][mapped_dept] += 1
                    stats['合计'][mapped_dept] += 1
                
                # 添加到项目/需求列表
                project_info = {
                    '类型': project_type,
                    '技术方向': tech_direction,
                    '内外': '对外' if project_attr == '对外' else '对内',
                    '支撑部门': mapped_dept,
                    '项目名称': extract_text(fields.get('项目名称', [])),
                    '当前进度': progress
                }
                
                if project_type in ['售中', '售前']:
                    projects.append(project_info)
                elif project_type == '开发':
                    project_info['需求名称'] = project_info['项目名称']
                    requirements.append(project_info)
    
    # 生成各种表格
    stats_table = generate_stats_table(stats)
    project_table = generate_project_table(projects)
    requirement_table = generate_requirement_table(requirements)
    
    # 生成统计概述
    summary_stats = f"""时间：{last_day_last_month.strftime('%Y年%m月')}
项目总数：{total_count}
售中项目数：{sell_count}
售前项目数：{presale_count}
开发项目数：{dev_count}
完成项目数：{completed_count}
进行中项目数：{ongoing_count}
对外项目数：{external_count}
对内项目数：{internal_count}
大模型项目数：{ai_count}
RPA项目数：{rpa_count}"""
    
    # 如果没有找到上月更新的记录
    if filtered_count == 0:
        result_list.append(f"未找到上个月（{first_day_last_month.strftime('%Y年%m月')}）更新的记录")
    
    # 返回结果
    ret: Output = {
        "result": result_list,
        "report_title": report_title,
        "stats_table": stats_table,
        "project_table": project_table,
        "requirement_table": requirement_table,
        "summary_stats": summary_stats
    }
    
    return ret