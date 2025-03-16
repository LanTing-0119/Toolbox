# 背景:有些自己上传到B站字幕只能从后台下载下来不能用downie爬；而下载下来的是json格式需要改成srt才能让mpv较好识别
# 功能说明: 将B站后台下载的bcc字幕内容转换成srt格式
# input: a folder with scripts
# output: scripts update in ~/Downloads
# run: 1.修改path 2.Build


import json
import datetime
from pathlib import Path
import os

def seconds_to_srt_time(seconds):
    """Convert seconds to SRT time format (HH:MM:SS,mmm)."""
    milliseconds = int((seconds % 1) * 1000)
    time_format = str(datetime.timedelta(seconds=int(seconds))) + f",{milliseconds:03d}"
    return time_format

def json_to_srt(json_file, srt_file):
    """Convert a JSON subtitle file to SRT format."""
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    srt_entries = []
    
    for i, entry in enumerate(data["body"], start=1):
        start_time = seconds_to_srt_time(entry["from"])
        end_time = seconds_to_srt_time(entry["to"])
        content = entry["content"]
        
        srt_entries.append(f"{i}\n{start_time} --> {end_time}\n{content}\n")

    with open(srt_file, "w", encoding="utf-8") as f:
        f.writelines(srt_entries)



# Example usage
path = '/Users/lanting/Downloads/srts'

folder_path = Path(path)
files = [file.name for file in folder_path.iterdir() if file.is_file()]

i=1
for file in files:
    file_name = os.path.splitext(file)[0]
    file_path=f"{path}/{file}"
    json_to_srt(file_path, f"/Users/lanting/Downloads/{file_name}.srt")

    print(f'--- {i} / {len(files)} ---')
    i+=1

