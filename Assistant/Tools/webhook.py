import requests

def send_webhook():
    """
    发送Webhook请求到指定的API端点。

    :return: 响应对象，如果请求失败则返回None。
    """
    url = 'https://api.coze.cn/api/trigger/v1/webhook/biz_id/bot_platform/hook/xxxxxxxxxxxxxxxx'
    headers = {
        'Authorization': 'Bearer xxxxxxxxxxxxxxxx',
        'Content-Type': 'application/json'
    }
    data = {
        "content": "1"
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        print(f"Webhook请求出错: {e}")
        return None

# 使用示例
if __name__ == "__main__":
    result = send_webhook()
    if result:
        print("Webhook发送成功")
        print(result.json())