import argparse
import json
import time
from pathlib import Path
from typing import List

import requests
from bs4 import BeautifulSoup


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--setting_json", default="./setting.json", help="設定jsonへのパス")
    parser.add_argument("--max_image", default=100, type=int, help="最大画像取得数")
    return parser.parse_args()


def main():
    args = get_args()
    with open(args.setting_json, "r") as f:
        settings = json.load(f)
    # 画像のURL取得
    for setting_key in settings.keys():
        url_list = settings[setting_key]["urls"]
        image_url_list = get_image_url_list(url_list)[: args.max_image]
        dst_dir = Path(settings[setting_key]["dst"])
        dst_dir.mkdir(parents=True, exist_ok=True)
        for i, image_url in enumerate(image_url_list):
            time.sleep(0.1)
            dst = dst_dir / f'{settings[setting_key]["prefix"]}{i + 1}.jpg'
            download_and_save_image(image_url, dst)


def download_and_save_image(url: str, dst: str):
    """画像urlを指定保存先に保存する
    Args:
        url: 画像url
        dst: 保存先
    """
    r = requests.get(url, stream=True)
    if r.ok:
        with open(dst, "wb") as f:
            f.write(r.content)


def get_image_url_list(base_url_list: List[str]) -> List[str]:
    """yahoo image search経由で画像をurlリストを取得
    Args:
        base_url_list: 検索結果urlリスト
    Returns:
        複数の画像検索結果から取得した画像urlリスト
    """
    result = []
    for url in base_url_list:
        r = requests.get(url)
        time.sleep(1)
        r.raise_for_status()
        result += _get_partial_url_list(r.text)
    return list(set(result))


def _get_partial_url_list(fetch_txt: str) -> List[str]:
    """1つの検索結果urlからのレスポンスを解析して画像urlリストを取得
    Args:
        fetch_txt: urlからのレスポンス
    Returns:
        画像urlリスト
    """
    soup = BeautifulSoup(fetch_txt, features="html.parser")
    elems = soup.select("#res-cont")[0]
    img_tag_list = elems.find_all("img", limit=1000)
    result = []
    for img_tag in img_tag_list:
        url = img_tag.get("src")
        if url is not None:
            result.append(url)
    return result


if __name__ == "__main__":
    main()
