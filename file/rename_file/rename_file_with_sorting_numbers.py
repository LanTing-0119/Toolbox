import os,shutil

def get_subfolder_paths(folder_path): # 判断目录下是否有文件
    subfolder_paths = []
    
    if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
        return subfolder_paths
    
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isdir(item_path):
            subfolder_paths.append(item_path)
    
    return subfolder_paths

def get_max_sorting_order(folder_path,char):
    file_list = os.listdir(folder_path)  # Get the list of files in the folder
    
    max_num = 0
    
    for file_name in file_list:
        nPos = file_name.find(char)
        
        if file_name[nPos+1] not in [str(i) for i in list(range(0,10))]:
            continue
        if max_num <= int(file_name[nPos+1:nPos+1+3]):
            max_num = int(file_name[nPos+1:nPos+1+3])
    return max_num + 1

def rename_files_in_folder(folder_path,char):
    subfolder_paths = get_subfolder_paths(folder_path)
    if subfolder_paths:
        for path in subfolder_paths:
            rename_files(path,char)

    else:
        rename_files(folder_path,char)

# Example renaming rule: add a prefix "new_" to the file name
def add_prefix(file_name,max_num,char): 
    nPos = file_name.find(char)

    if file_name[nPos+1] in [str(i) for i in list(range(0,10))]:
        num = file_name[nPos+1:nPos+1+3]
    sorting_order = max_num - int(num) 
    sorting_order = str(0)*(3-len(str(sorting_order))) + str(sorting_order) # 转换后保留3位自动填充0
    return sorting_order + file_name[nPos+4:]

def rename_files(folder_path,char):

    file_list1 = os.listdir(folder_path)  # Get the list of files in the folder
    file_list = []
    file_name_chaos = []
    is_num = 0 # 用0&1代替True&False,方便计数
    for file_name in file_list1:
        if file_name[0] == '.':
            continue
        file_list.append(file_name)
        if file_name[0] not in [str(i) for i in list(range(0,10))]:
            is_num += 1
            file_name_chaos.append(file_name_chaos)
    if is_num == 0:
        char = '@' # 使用''会索引返回0，但实际上返回-1才避免nPos出错
    elif is_num < len(file_list):
        for file in file_name_chaos:
            print(file,'命名杂糅')
        
            
        
    max_num = get_max_sorting_order(folder_path,char)

    for file_name in file_list:

        nPos = file_name.find(char)

        if file_name[nPos+1] not in [str(i) for i in list(range(0,10))]:
            print(file_name,'不符合命名规范')
            continue
            
        old_file_path = os.path.join(folder_path, file_name)  # Get the full path of the file
        
        if os.path.isfile(old_file_path):  # Check if it's a file (not a subdirectory)
            
            new_file_name = add_prefix(file_name,max_num,char)  # Apply the renaming rule to get the new file name
            new_file_path = os.path.join(folder_path, new_file_name)  # Get the full path of the new file
            
            os.rename(old_file_path, new_file_path)  # Rename the file            

def move_files_2_folder(main_path):

    files = [file for file in os.listdir(main_path) if ((file[0] != '.') and (os.path.isfile(f'{main_path}/{file}')))]
    files.sort()

    for file in files:
        # print(file.split('-')[0])
        folder_name = file.split('-')[0]
        print(f'{main_path}/{folder_name}')
        if not os.path.exists(f'{main_path}/{folder_name}'):
            os.makedirs(f'{main_path}/{folder_name}')
        try:
            shutil.move(f'{main_path}/{file}',f'{main_path}/{folder_name}')
        except:
            print(f'{main_path}/{file}')


### 用于单个文件夹内全部文件:
    #### 要修改sorting num!!!
    #### 文件重命名 eg:

    #支持一下两种文件名输入：
    #Machine Learning-001- Long Short-Term Memory with PyTorch + Lightning
    #001- Long Short-Term Memory with PyTorch + Lightning

    #输出：
    #094- Long Short-Term Memory with PyTorch + Lightning

folder_path = r'/Users/lanting/Downloads/Machine_Learning_in_Computational_Biology_MIT'  # Replace with the actual folder path
char = '-' #设定分隔符

rename_files_in_folder(folder_path,char)
print('---finished!---')


### 此为批量整理文件(不用于单个文件):将以下几行全部取消注释即可



main_path = r'/Volumes/岚霆_临床/大五上/Pathology/YouTube/Virology Lectures 2024'
char = '-' #设定分隔符



# move_files_2_folder(main_path)
# folders_path = [folder_path for folder_path in os.listdir(main_path) if ((folder_path[0] != '.') and (os.path.isdir(folder_path)))]
# for folder_path in folders_path:
#     rename_files_in_folder(f'{main_path}/{folder_path}',char)







# 功能添加：
    #1:为每个相同主题的视频系列创建一个文件夹

        #1.1遍历主主文件夹,获取所有文件名
        #1.2文件名排序并按照“-”切割,保留首位并去重
        #1.3按照去重后列表创建空文件夹.并将文件按“-”前名称移入对应文件夹

    #2:在每个文件夹内重命名文件名














