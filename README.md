# 链家爬虫

使用`make`即可自动爬取、解析、清晰数据。`spider.py`是爬虫的代码，`clean.py`是清晰数据的代码。

## 依赖
* Scrapy：爬取数据
* BeautifulSoap4：解析网页（scrapy内置parser获取文本有bug）
* Pandas：数据清洗