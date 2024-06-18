import requests
import urllib

# 从百度百科爬取指定关键词页面数据
url1 = 'https://baike.baidu.com/item/'
key_word = (input())
filename = key_word
lens = len(key_word)
key_word = urllib.parse.quote(key_word,encoding = 'utf-8', errors = 'replace')
headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
}
html = requests.get(url1+key_word,headers = headers)
print(url1+key_word)# 验证链接是否正确
html.encoding = html.apparent_encoding
fo = open("E://crawler_data//"+ filename + ".txt",'wb') # 爬取百度百科的内容保存到本地中
fo.write((html.content))
print("写入文件成功")
