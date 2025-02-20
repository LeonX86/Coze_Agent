import requests_async as requests
import json

url = "http://127.0.0.1/dialogue"

async def main(args: Args) -> Output:
    params = args.params
    # 去除首尾的方括号

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    data = {
        "task_id": params["task_id"],
        "coze_uid": params["uid"],
        "raw_query": params["bot_response"],
        "query": "",
        "role":"bot"
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
        "key1": response.text
    }
    return ret