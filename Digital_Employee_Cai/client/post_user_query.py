import requests_async as requests
import json

# 获取当前时间并精确到毫秒
url = "http://127.0.0.1/dialogue"

async def main(args: Args) -> Output:
    params = args.params


    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    data = {
        "task_id":"",
        "coze_uid": params["uid"],
        "raw_query": params["raw_query"],
        "query": params["query"],
        "role":"user",
    }

    response = await requests.post(
        url=url,
        headers=headers,
        data=json.dumps(data),
        timeout=10
    )

    # 构建输出对象
    ret: Output = {
        "key0": response.text,
    }
    return ret