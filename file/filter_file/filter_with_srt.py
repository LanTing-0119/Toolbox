# 将folder下没有srt的mp4文件复制到另一个文件夹
# inputs: path of folder
# outputs: a folder with suffix '_copy' with mp4 files
# example: filter_files(folder)

from pathlib import Path
import shutil,os

def filter_files(folder):
	# 创建输出的目录
	if not os.path.exists(f"{folder}_copy"):
		os.mkdir(f"{folder}_copy")

	folder_path = Path(folder)  # Replace with your folder path
	files_srt = [Path(f.name).stem for f in folder_path.iterdir() if (f.is_file() and f.name[-4:]=='.srt')]
	files_mp4 = [Path(f.name).stem for f in folder_path.iterdir() if (f.is_file() and f.name[-4:]=='.mp4')]

	i = 0
	for file in files_mp4:
		if file in files_srt:
			continue
		else:
			i+=1
			shutil.copy(f"{folder}/{file}.mp4",f"{folder}_copy/{file}.mp4")  # Uncomment if you want to rename on disk

	print(f"文件总数: {i}")


    # You can perform the actual renaming on your system using os.rename
    # shutil.copy(f"{folder}/{old_file}",f"{folder}_copy/{new_file}")  # Uncomment if you want to rename on disk
	        
folder = '/Volumes/岚霆_科研/[AI/深度学习_台大_2024'
filter_files(folder)



