# 将folder下 ['1-1 c1','2-1 b1','3-1 a1','4-2 b2','5-2 a2',...] 文件命名为 ['1-1 a1','2-1 b1','3-1 c1','4-2 a2','5-2 b2',...]
# inputs: path of folder
# outputs: a folder with suffix '_copy' with files renamed
# example: rename_files(folder)

from pathlib import Path
import shutil,os

def rename_files(folder):
	# 创建输出的目录
	if not os.path.exists(f"{folder}_copy"):
		os.mkdir(f"{folder}_copy")

	folder_path = Path(folder)  # Replace with your folder path
	files = [f.name for f in folder_path.iterdir() if f.is_file()]

	# Function to extract numbers after the first '-' and numbers before the second '-'
	result_index = {}
	result = {}
	for file in files:
	    parts = file.split('-')

	    if len(parts) > 1:
	        # Extract the number after the first '-', and before the second '-'
	        before_second_dash = parts[0]
	        after_first_dash = parts[1].split(' ')[0]
	    
	        # Initialize the key if it doesn't exist
	        if after_first_dash not in result_index:
	            result_index[after_first_dash] = []
	            result[after_first_dash] = []

	        # Directly append the value to the list for the key
	        result_index[after_first_dash].append(before_second_dash)
	        result[after_first_dash].append(file)

	# Sort the lists for each key in the dictionary
	for key in result:
	    result[key].sort()

	# Display the results
	# result
	# len(result)

	# rename files
	for key, files in result.items():
	    # Generate pairs for renaming
	    for i in range(0, len(files)):
	        old_file = files[i]
	        new_file = files[len(files)-i-1]
	        
	        # Rename files in your file system (for illustration purposes)
	        print(f"Renaming {old_file} to {new_file}")
	        
	        # You can perform the actual renaming on your system using os.rename
	        shutil.copy(f"{folder}/{old_file}",f"{folder}_copy/{new_file}")  # Uncomment if you want to rename on disk
	        
folder = '/Volumes/岚霆_科研/[AI/动手学深度学习_李沐'
rename_files(folder)
