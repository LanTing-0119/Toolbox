# 在另一个folder找到folder下mp4文件对应的srt(srt文件命名和mp4不一致但是有包含关系)，重命名并移动
# inputs: path of folder(mp4) and folder(srt)
# outputs: folder(mp4) with srt added
# example: match_mp4_srt(folder_mp4, folder_srt)

from pathlib import Path
import shutil,os

def match_mp4_srt(folder_mp4, folder_srt):

	folder_path = Path(folder_mp4)  # Replace with your folder path
	files_mp4 = [''.join(Path(f.name).stem.split(' ')[1:]) for f in folder_path.iterdir() if (f.is_file() and f.name[-4:]=='.mp4')]
	files_mp4_original = [Path(f.name).stem for f in folder_path.iterdir() if (f.is_file() and f.name[-4:]=='.mp4')]

	folder_path = Path(folder_srt)  # Replace with your folder path
	files_srt = [Path(f.name).stem for f in folder_path.iterdir() if (f.is_file() and f.name[-4:]=='.srt')]

	i=-1
	for file_mp4 in files_mp4:
		i+=1
		for file_srt in files_srt:
			if file_mp4 in file_srt:
				shutil.copy(f"{folder_srt}/{file_srt}.srt",f"{folder_mp4}/{files_mp4_original[i]}.srt")  # Uncomment if you want to rename on disk
				# print(file_srt)

folder_mp4 = '/Volumes/岚霆_科研/[AI/动手学深度学习_李沐_理论'
folder_srt = '/Volumes/岚霆_科研/[AI/字幕'
match_mp4_srt(folder_mp4,folder_srt)



