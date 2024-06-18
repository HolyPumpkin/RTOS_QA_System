from bs4 import BeautifulSoup

# 加载HTML文件
with open("E://crawler_data//RTOS.txt", 'r', encoding='utf-8') as file:
    html_content = file.read()

# 解析HTML
soup = BeautifulSoup(html_content, 'html.parser')

# 定义要提取的信息关键词
keywords = [
    "实时操作系统",
    "定义",
    "特点",
    "特征",
    "分类",
    "应用",
    "优势",
    "挑战",
    "历史",
    "发展",
    "结构",
    "组件",
    "实时任务",
    "调度算法",
    "分时系统",
    "实例"
]

# 提取信息并生成问答对
qa_pairs = []

for keyword in keywords:
    found = False
    for paragraph in soup.find_all('p'):
        if keyword in paragraph.get_text():
            answer = paragraph.get_text(strip=True)
            qa_pairs.append((f"什么是{keyword}？", answer))
            found = True
            break
    if not found:
        qa_pairs.append((f"什么是{keyword}？", "相关信息未找到。"))

# 打印问答对
for question, answer in qa_pairs:
    print(f"问题: {question}\n回答: {answer}\n")