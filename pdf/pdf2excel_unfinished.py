import fitz  # PyMuPDF
import pandas as pd
import re

# 打开PDF文件
doc = fitz.open("PICSEW_20250321193944.PDF")

# 读取第一页文本内容
page_text = doc[0].get_text()

# 分类关键词
roles = ['论坛主席', '报告嘉宾', '主持嘉宾']

# 初始化存储
data = []
current_role = None

# 正则匹配“姓名 + 单位”模式
lines = page_text.splitlines()
for line in lines:
    print(line)
    line = line.strip()
    if not line:
        continue
    # 检查是否为角色类别行
    if any(role in line for role in roles):
        for role in roles:
            if role in line:
                current_role = role
                break
        continue
    # 检查是否为“姓名 + 单位”格式
    matches = re.findall(r'([\u4e00-\u9fa5·]{2,10})\s+(.+)', line)
    for match in matches:
        name, affiliation = match
        data.append({
            '类别': current_role,
            '姓名': name,
            '单位': affiliation
        })

# 转换为DataFrame
df = pd.DataFrame(data)

# 输出为Excel或CSV
df.to_excel("论坛嘉宾信息.xlsx", index=False)
# 或 df.to_csv("论坛嘉宾信息.csv", index=False)

print(df)
