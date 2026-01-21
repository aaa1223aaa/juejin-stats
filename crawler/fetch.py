"""
Python 爬虫脚本，用于抓取掘金用户主页的统计信息并追加到历史记录文件。

该脚本会访问指定的掘金个人主页，解析页面中的文章数量、粉丝数量、关注人数、文章被点赞数、文章被阅读数等数据。
解析完成后，将以 ISO 日期为键写入 `data/history.json`。如果该日期已存在，则更新记录；否则追加新记录。

在 GitHub Actions 中运行时，请确保工作目录位于仓库根目录。

示例使用：

```
python crawler/fetch.py
```

"""

import datetime
import json
import os
import re
from typing import Dict, Optional

import requests


# 修改此处以指定要抓取的掘金用户主页
USER_URL = os.environ.get("JUEJIN_USER_URL", "https://juejin.cn/user/3659622444970574")

# 历史数据文件路径
HISTORY_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "history.json")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:110.0)"
        " Gecko/20100101 Firefox/110.0"
    ),
}


def extract_first_number(pattern: str, text: str) -> Optional[int]:
    """从文本中提取第一个匹配的数字，去除逗号并返回整数。"""
    match = re.search(pattern, text)
    if match:
        num_str = match.group(1)
        # 去除可能存在的千位分隔符，如 1,234
        num_str = num_str.replace(",", "")
        try:
            return int(num_str)
        except ValueError:
            return None
    return None


def fetch_stats(url: str) -> Dict[str, Optional[int]]:
    """
    抓取掘金用户主页的统计数据。

    返回字典包含以下字段：
        - followers: 粉丝数量
        - following: 关注了多少人
        - articles: 文章数量
        - likes: 文章被点赞数
        - views: 文章被阅读数

    如果某个字段未能解析，则值为 None。
    """
    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    html = resp.text

    # 简单的正则匹配。匹配时注意中文字符及空格。数字可能带逗号。
    followers = extract_first_number(r"关注者\s*([\d,]+)", html)
    following = extract_first_number(r"关注了\s*([\d,]+)", html)
    # “文章 65” 这种格式，匹配“文章”后跟数字并可能有空格或换行
    articles = extract_first_number(r"文章\s*([\d,]+)", html)
    likes = extract_first_number(r"文章被点赞\s*([\d,]+)", html)
    views = extract_first_number(r"文章被阅读\s*([\d,]+)", html)

    return {
        "followers": followers,
        "following": following,
        "articles": articles,
        "likes": likes,
        "views": views,
    }


def load_history(filepath: str) -> list:
    """加载历史数据文件，如果不存在则返回空列表。"""
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
        except Exception:
            pass
    return []


def save_history(filepath: str, history: list) -> None:
    """将历史数据保存为 JSON。"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def main() -> None:
    # 当前日期（使用北京时间，UTC+8）。如果需要调整时区，请修改此处。
    today = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=8)
    date_str = today.strftime("%Y-%m-%d")

    try:
        stats = fetch_stats(USER_URL)
    except Exception as exc:
        raise SystemExit(f"抓取数据失败：{exc}")

    history = load_history(HISTORY_FILE)
    # 查找是否已有当日数据
    existing = next((item for item in history if item.get("date") == date_str), None)
    if existing:
        # 更新
        existing.update(stats)
    else:
        new_entry = {"date": date_str, **stats}
        history.append(new_entry)
        # 按日期排序
        history.sort(key=lambda x: x.get("date"))
    save_history(HISTORY_FILE, history)
    print(f"已更新 {date_str} 数据：{stats}")


if __name__ == "__main__":
    main()