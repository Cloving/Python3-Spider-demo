import os
from hashlib import md5
from multiprocessing.pool import Pool
from urllib.parse import urlencode

import requests
from requests import codes

GROUP_START = 1
GROUP_END = 2

headers = {
  "User_Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
               AppleWebKit/537.36 (KHTML, like Gecko) \
               Chrome/70.0.3538.102 Safari/537.36",
}

def get_Pages(offset):
  params = {
    "offset": offset,
    "format": "json",
    "keyword": "街拍",
    "autoload": "true",
    "count": "20",
    "cur_tab": '1',
    "from": "search_tab",
    "pd": "synthesis"
  }
  baseurl = "https://www.toutiao.com/search_content"
  url = baseurl + "/?" + urlencode(params)
  try:
    response = requests.get(url, headers=headers)
    if response.status_code == codes.ok:
      return response.json()
  except requests.ConnectionError as e:
    print("连接错误，错误原因：", e)

def get_images(json):
  if json.get("data"):
    data = json.get("data")
    for item in data:
      if item.get("cell_type") is not None:
        continue
      title = item.get("title")
      images = item.get("image_list")
      for image in images:
        yield {
          "title": title,
          "image": "https:" + image.get("url")
        }

def save_image(item):
  image_path = 'img' + os.path.sep + item.get("title")
  if not os.path.exists(image_path):
    os.makedirs(image_path)
  try:
    resp = requests.get(item.get("image"))
    if resp.status_code == codes.ok:
      file_path = image_path + os.path.sep + '{file_name}.{file_suffix}'.format(
        file_name = md5(resp.content).hexdigest(),
        file_suffix = "jpg"
      )
      if not os.path.exists(file_path):
        with open(file_path, 'wb') as f:
          f.write(resp.content)
          print("Downloaded image path is %s" % file_path)
      else:
        print("Already download path is ", file_path)
  except requests.ConnectionError as e:
    print("Fail to save image: ERROR REASON: ", e.args)      

def main(offset):
  json = get_Pages(offset)
  for index, item in enumerate(get_images(json)):
    print('第' + str(index) + '条: ', item)
    save_image(item)

if __name__ == "__main__":
  pool = Pool()
  groups = ([x*20 for x in range(GROUP_START, GROUP_END+1)])
  pool.map(main, groups)
  pool.close()
  pool.join()
