# 掘金数据统计项目

该项目用于自动抓取掘金个人主页的主要指标，并使用 GitHub Actions 每天运行一次来更新历史数据。然后通过 GitHub Pages 展示数据的趋势图表。

## 项目结构

```
juejin-stats/
├── crawler/
│   └── fetch.py      # 爬虫脚本，负责抓取数据并更新历史文件
├── data/
│   └── history.json  # 历史数据（每天一条记录）
├── web/
│   ├── index.html    # 静态网页，负责显示趋势
│   └── chart.js      # JavaScript，用于渲染图表
└── .github/
    └── workflows/
        └── daily.yml # GitHub Actions 定时任务配置
```

## 使用方法

1. **创建仓库**：在 GitHub 上创建一个新的仓库，例如 `juejin-stats`。
2. **上传文件**：将本项目中的所有文件上传到仓库根目录。
3. **配置 Actions**：仓库包含的 `.github/workflows/daily.yml` 文件会自动在每天北京时间 08:00 运行爬虫脚本。首次运行前请务必确认仓库设置中启用了 GitHub Actions。
4. **启用 GitHub Pages**：在仓库设置（Settings → Pages）中，将站点来源选择为 `main` 分支的 `web` 文件夹。保存后，稍候即可通过 `https://<你的用户名>.github.io/<仓库名>/` 访问网页。

## 自定义

- **目标用户ID**：默认脚本抓取的用户主页为 `https://juejin.cn/user/3659622444970574`。如需抓取其他用户，请修改 `crawler/fetch.py` 中的 `USER_URL` 变量。
- **时间安排**：如需调整定时运行时间，请修改 `.github/workflows/daily.yml` 中的 `cron` 表达式。当前设定为每日北京时间 08:00 运行。

## 历史数据格式

`data/history.json` 存储每一天的统计数据，每条记录包含：

```json
{
  "date": "2026-01-21",       // 抓取日期（ISO 格式）
  "followers": 195,             // 粉丝数量
  "following": 9,              // 关注了多少人
  "articles": 65,             // 文章数量
  "likes": 1623,              // 文章被点赞总数
  "views": 138596            // 文章被阅读总数
}
```

网页通过读取此文件并以折线图方式展示趋势。

## 本地测试

如果想在本地运行爬虫脚本，可以在 Python 3 环境下安装依赖并执行：

```bash
pip install -r requirements.txt
python crawler/fetch.py
```

脚本会从掘金获取数据并写入 `data/history.json`。
