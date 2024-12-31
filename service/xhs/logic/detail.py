import json
import re

from bs4 import BeautifulSoup

from lib import logger, requests

from .common import COMMON_HEADERS, common_request


async def request_detail(id: str, xsec_token: str, cookie: str) -> tuple[dict, bool]:
    """
    请求小红书获取视频信息
    """
    # 获取xsec_token
    url = f"https://www.xiaohongshu.com/explore/{id}"
    headers = {"cookie": cookie}
    headers.update(COMMON_HEADERS)
    resp = await requests.get(url, headers=headers, params={"xsec_token": xsec_token})
    if resp.status_code != 200 or resp.text == "":
        return {}, False
    try:
        soup = BeautifulSoup(resp.text, "html.parser")
        pattern = re.compile("window\\.__INITIAL_STATE__={.*}")
        text = (
            soup.body.find("script", text=pattern)
            .text.replace("window.__INITIAL_STATE__=", "")
            .replace("undefined", '""')
        )
        target = json.loads(text)
        detail_data = target.get("note", {}).get("noteDetailMap", {}).get(id, {})
    except Exception as e:
        logger.error(f"failed to get detail: {id}, err: {e}")
        return {}, False
    return detail_data, True
