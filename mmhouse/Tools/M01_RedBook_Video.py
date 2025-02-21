import requests_async as requests
import re
import json

async def get_xhs_video(url: str) -> dict:
    r = await requests.get(url)
    if r.status_code == 200:
        url_with_watermark = re.findall(r'<meta name="og:video" content="(.*?)">', r.text)
        if url_with_watermark:
            url_with_watermark = url_with_watermark[0]
        else:
            url_with_watermark = None

        key = re.findall(r'{\"originVideoKey\":\".*?\"}', r.text)
        if key:
            url_without_watermark = "http://sns-video-bd.xhscdn.com/" + json.loads(key[0])["originVideoKey"]
        else:
            url_without_watermark = None
        return {
            "视频有水印": url_with_watermark,
            "视频无水印": url_without_watermark
        }
    else:
        print(f"status code: {r.status_code}")
        return {
            "视频有水印": None,
            "视频无水印": None
        }

async def main(args: Args) -> Output:

    params = args.params

    links = [word for word in params['input'].split() if word.startswith(('http://', 'https://'))]
    link = links[0]
    result_dict = await get_xhs_video(link)
    output = f"视频无水印：{result_dict['视频无水印']}\n视频有水印：{result_dict['视频有水印']}"
    # 构建输出对象
    ret: Output = {
        # "key0": params['input'] + params['input'],
        "key0": output
    }
    return ret