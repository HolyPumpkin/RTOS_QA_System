# RTOS_QA_System

RTOS based question &amp; answer system

# 程序运行前准备

- 开发时使用的 python 版本为**3.7.1**

- 参照以下库列表将项目所需 python 依赖库提前安装（若有错误，可根据报错补充安装或更改版本）
  - bs4
  - jieba
  - langdetect
  - urllib
  - requests
  - pyinstaller

# GetData.py

- 用于从百度百科对应的关键词网页爬取数据
- 最终会在目标路径下生成并写入 key_word.txt，文件内包含整个网页数据，可直接将后缀改为.html 打开，会展示解析后的网页

# ReadData.py

- 用于从上一步读取到的网页数据中读取相应关键词对应的数据

# QA_sys.py

- 用于生成智能问答系统，数据可由上一步导入，也可自定义，这里读取 knowledge.txt 进行系统生成
- 使用基于传统规则的关键词识别技术，对问题进行搜索并回答

# 程序运行

- 在此路径下打开终端，可使用**python QA_sys.py**命令运行程序
- 在此路径下打开终端，可使用**pyinstaller --onefile QA_sys.py**命令将程序打包为 exe 可执行文件
  - 生成的 exe 在./dist/路径下，注意需要将 knowledge.txt 数据放在同路径下，或者修改源代码，将数据存在源文件中
