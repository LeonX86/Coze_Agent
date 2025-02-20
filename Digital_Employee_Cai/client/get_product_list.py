import requests_async as requests

url = "http://127.0.0.1/products"

async def main(args: Args) -> Output:
    params = args.params
    # 发送GET请求
    response = await requests.get(url)
    data = response.json()

    # 构建输出对象
    ret: Output = {
        "key0": data
    }
    return ret