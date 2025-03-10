# -*- coding: utf-8 -*-
import os

# 快速根据转换list转换文件:
# 输入: newnames:转换list; path:转换文件所在目录
# 输出: 转换好的文件(位于原目录)

# List of new names you want for the files (ensure it has exactly 48 names)
new_names = ["01精神病学绪论-1.1 概述","01精神病学绪论-1.2 精神病学发展史的回顾","01精神病学绪论-1.3 精神障碍的神经科学、心理学基础及精神病学的展望","02精神障碍的症状学-2.1 概论","02精神障碍的症状学-2.2 感觉障碍","02精神障碍的症状学-2.3 知觉障碍","02精神障碍的症状学-2.4 思维形式障碍","02精神障碍的症状学-2.5 思维内容障碍","02精神障碍的症状学-2.6 注意、记忆、智能、定向力障碍和自知力","02精神障碍的症状学-2.7 情感、意志、动作与行为障碍","02精神障碍的症状学-2.8 意识障碍、常见的精神症状综合征","03精神障碍的检查和诊断-3.1 精神检查中的一般原则","03精神障碍的检查和诊断-3.2 病史采集","03精神障碍的检查和诊断-3.3 精神状态检查","03精神障碍的检查和诊断-3.4 躯体检查与特殊检查","04精神认知障碍及相关疾病-4 神经认知障碍及相关疾病","05精神活性物质所致精神障碍-5.1 什么是成瘾","05精神活性物质所致精神障碍-5.2 成瘾行为有哪些，为什么会成瘾","05精神活性物质所致精神障碍-5.3 如何试别、诊断成瘾者","05精神活性物质所致精神障碍-5.4 如何处理成瘾","06精神分裂症-6.1 精神分裂症名称的演变过程","06精神分裂症-6.2 精神分裂症的临床表现","06精神分裂症-6.3 精神分裂症的诊断","06精神分裂症-6.4 精神分裂症的治疗","07心境障碍-7.1_1 为什么会患抑郁症","07心境障碍-7.1_2 抑郁症发作的临床表现及诊断标准","07心境障碍-7.1_3 抑郁症能治好吗","07心境障碍-7.2 躁狂发作的临床表现及诊断标准","07心境障碍-7.3 双相情感障碍的诊断及治疗","08焦虑与恐惧相关障碍-8.1 概述","08焦虑与恐惧相关障碍-8.2 广泛性焦虑","08焦虑与恐惧相关障碍-8.3 惊恐障碍","08焦虑与恐惧相关障碍-8.4 恐惧障碍","08焦虑与恐惧相关障碍-8.5 分离性焦虑障碍","09强迫症-9 强迫症","10神经发育性障碍-10.1 概述及ADHD的表现","10神经发育性障碍-10.2 ADHD诊断治疗","11治疗学（药物治疗）-11.1 概述","11治疗学（药物治疗）-11.2 抗精神病药（上）","11治疗学（药物治疗）-11.3 抗精神病药（下）","11治疗学（药物治疗）-11.4 抗抑郁药","11治疗学（药物治疗）-11.5 心境稳定剂","11治疗学（药物治疗）-11.6 治疗焦虑的药物","12治疗学（物理治疗）-12.1 电休克治疗","12治疗学（物理治疗）-12.2 经颅磁刺激治疗","13精神科临床中常见的法律伦理问题-13 精神科临床中常见的法律伦理问题"]

# Path where the files are located
path = '/Volumes/岚霆_临床/大五上/Pathology/163'

# Get all mp4 files sorted by name
files = sorted([f for f in os.listdir(path) if (f.endswith('.mp4') and f[0]!='.')])

# Rename the files
for file, new_name in zip(files, new_names):
    # print(file)
    # print(file,'-',new_name)
    os.rename(os.path.join(path, file), os.path.join(path, f"{new_name}.mp4"))

print("Files have been renamed!")
