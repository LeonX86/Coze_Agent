import requests_async as requests

async def main(args: Args) -> Output:

    params = args.params
    coze_uid = params["coze_uid"]
    # API端点
    url = "http://127.0.0.1/history"
    user = {
        "uid": coze_uid,
        "limit": 100
    }

    try:
        # 发送GET请求
        response = await requests.get(url,params=user)

        # 解析JSON数据
        data = response.json()

        # 构建输出对象
        ret: Output = {
            "key0": data
        }
        return ret

    except Exception as e:
        # 错误处理
        ret: Output = {
            "key0": str(e)
        }
        return ret