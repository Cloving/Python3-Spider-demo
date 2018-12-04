'''
 获取知乎首页的回答，存储到文本文件中
'''
import requests
from pyquery import PyQuery as pq

url = "https://www.zhihu.com/explore"

headers = {
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63."
}

html = requests.get(url, headers=headers).text
doc = pq(html)
items = doc(".tab-panel .feed-item").items()

for item in items:
  question = item.find("h2").text()
  author = item.find(".author-link-line").text()
  # 获取这个节点内部的 HTML 文本
  # class = "content"的标签节点是textarea，所以内部即使是HTML代码也属于文本
  answer = pq(item.find(".content").html()).text()
  with open('explore.txt', 'a', encoding="utf-8") as file:
    file.write('\n'.join([question, author, answer]))
    file.write('\n'+'='*50+'\n')
