# type_dict = {
#     1:"1. 新建文案任务",
#     2:"2. 修改最近文案",
#     3:"3. 确认文案并开始制作视频"
# }
import requests_async as requests
import json
import datetime
import hashlib
# 获取当前时间并精确到毫秒
current_time = datetime.datetime.now().isoformat(timespec='milliseconds') + 'Z'
url = "http://127.0.0.1/task"


def generate_task_id(uid: str, timestamp: str) -> str:
    """
    生成唯一的task id

    参数:
        uid: 用户ID
        timestamp: ISO格式的时间戳 (例如: "2025-01-21T11:32:07.862Z")

    返回:
        生成的task id (格式: USER_时间戳哈希值_UID哈希值)
    """
    # 1. 处理uid: 取uid的md5值的前6位
    uid_hash = hashlib.md5(uid.encode()).hexdigest()[:6]
    # 2. 处理时间戳: 转换成简洁格式后取md5值的前6位
    dt = datetime.datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
    time_str = dt.strftime('%Y%m%d%H%M%S%f')  # 包含微秒的完整时间字符串
    time_hash = hashlib.md5(time_str.encode()).hexdigest()[:6]
    # 3. 组合ID
    task_id = f"{time_hash}{uid_hash}"
    return task_id

async def main(args: Args) -> Output:
    params = args.params
    # 去除首尾的方括号
    task_id = generate_task_id(params["uid"],current_time)

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    data = {
        "task_id": task_id,
        "task_type": params["task_type"],
        "task_num": int(params["task_num"]),
        "coze_uid": params["uid"],
        "product":params["product_id"]
    }

    response = await requests.post(
        url=url,
        headers=headers,
        data=json.dumps(data),
        timeout=10
    )

    # 构建输出对象
    ret: Output = {
        "key0": data,
        "key1": response.text,
        "task_id": task_id,
    }
    return ret