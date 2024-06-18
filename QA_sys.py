import jieba
from langdetect import detect

### 读取知识库
# 定义文件路径
file_path = 'knowledge.txt'

# 初始化知识库字典
knowledge_base = {}

# 读取文件内容
with open(file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()

# 解析文件内容并构建知识库
for line in lines:
    if ": " in line:
        key, value = line.split(": ", 1)
        knowledge_base[key.strip()] = value.strip()

# 检测输入文本的语言
def detect_language(text):
    try:
        return "zh" if detect(text) == "zh-cn" else "en"
    except:
        return "en"  # 默认为英文处理，如果检测失败

# 关键词子集匹配
def is_subquestion(sub_q, full_q,language):
    if language == "en":
        sub_q_words = set(sub_q.split())
        full_q_words = set(full_q.split())
    else:
        sub_q_words = set(jieba.lcut(sub_q))
        full_q_words = set(jieba.lcut(full_q))
    return sub_q_words.issubset(full_q_words)

# 找到候选列表中与question最相近的回答（这里用重合长度比较相似度）
def find_best_match(question, candidates, language):
    """
    从候选答案中找到最佳匹配项。
    基于匹配到的关键词长度进行排序，选择最长的匹配关键词对应的答案。
    """
    # 分割问题为单词列表，用于长度比较
    if language == "en":
        question_words = question.split()
    else:
        question_words = jieba.lcut(question)
    max_len = 0
    best_answer = None
    for candidate_q, candidate_a in candidates.items():
        # 计算当前候选答案中关键词的最大长度
        if language == "en":
            candidate_words = candidate_q.split()
        else:
            candidate_words = jieba.lcut(candidate_q)
        current_max_len = max((len(word) for word in candidate_words if word in question_words), default=0)
        # 更新最大长度及对应的答案
        if current_max_len > max_len:
            max_len = current_max_len
            best_answer = candidate_a
    return best_answer

# 从词库中寻找答案
def find_answer(question):
    # 检测输入文本的语言
    language = detect_language(question)
    # 将问题转换为小写，以便于匹配
    question = question.strip().lower()
    
    # 初始化候选答案集合，用于存储所有部分匹配到的答案
    candidates = {}
    
    for q, a in knowledge_base.items():
        # 首先尝试全量关键词匹配，若问题就在词库中为完全匹配
        if q.lower() == question:
            return a
        # 关键词子匹配，看问题是否是某个回答的子集
        elif is_subquestion(question, q.lower(), language):
            candidates[q] = a
        # 反关键词子匹配，看回答是否是某个提问的子集
        elif is_subquestion(q.lower(), question, language):
            candidates[q] = a
    
    if candidates:
        result = find_best_match(question, candidates, language)
        if result is not None:
            return result
    
    # 在没有全量匹配、子集匹配时进行单词模糊搜索
    matched_answers = []  # 用于收集所有匹配到的答案
    words_in_question = question.split() if language == "en" else jieba.lcut(question)
    
    # 关键词部分匹配
    for word in words_in_question:
        for q, a in knowledge_base.items():
            if word in q.lower():
                matched_answers.append((word, a))

    # 如果有匹配项，根据匹配关键词数量排序并返回最佳答案
    if matched_answers:
        # 根据匹配关键词数量排序
        matched_answers.sort(key=lambda x: len(x[0]), reverse=True)
        return f"您的问题中提到了'{matched_answers[0][0]}', 相关信息为：{matched_answers[0][1]}" + "--输入'退出'来结束（input 'exit' to stop）"
    else:
        return "对不起，我没有找到关于这个问题的答案。" + "--输入'退出'来结束（input 'exit' to stop）"

### 步骤 3: 用户交互

if __name__ == "__main__":
    print("中文:欢迎来到RTOS知识问答系统!请输入您的问题或输入'退出'来结束。\nEnglish:Welcome to the RTOS Q&A System! Please enter your question or type 'exit' to quit.")
    while True:
        user_input = input("> ")
        if user_input.lower() == "退出" or user_input.lower() == "exit":
            print("感谢使用，再见！")
            break
        else:
            answer = find_answer(user_input)
            print(answer + "--输入'退出'来结束（input 'exit' to stop）")
    
# 防止程序闪退，等待用户输入
input("按回车键退出...")