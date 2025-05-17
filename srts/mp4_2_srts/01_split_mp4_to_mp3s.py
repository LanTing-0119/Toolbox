"""
2个功能：
    1. 将一个mp4视频切割为多个mp4片段(可以设置时长上限);
    2. 将切割的mp4片段转换成mp3;

Usage:
    1. 设置inputs所在的文件夹 input_folder → 用于产生切割后的mp4s
    2. 设置转换后的mp3的文件夹输出位置 path_output_mp3
"""

from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import os,shutil
from moviepy.video.io.VideoFileClip import VideoFileClip
from IPython.display import clear_output as clear
import time
import os
import subprocess

def get_mp4_list(path_folder):
# 获得需要转换为mp3的mp4路径

    list_mp4_2_mp3=[]

    for file in os.listdir(path_folder):
        if file[0]=='.':
            continue
        if '-' in file:
            continue
        if (file[-4:]=='.mp4') or (file[-4:]=='.MOV') or (file[-4:]=='.mov'):
            list_mp4_2_mp3.append(path_folder+'/'+file)

    return list_mp4_2_mp3


def mov_2_mp4(path_mov,output_folder):

    files = os.listdir(path_mov)

    # Filter out video files (assuming mp4 format, you can adjust as needed)
    # video_files = [file for file in files if file.endswith('.mp4')]
    # Filter out .MOV video files
    mov_files = [file for file in files if file.endswith('.MOV')]

    # Convert and rename each .MOV video file to .mp4, with names from 1 to 25
    for i, file in enumerate(mov_files, 1):
        new_name = file[:-4] + '.mp4'
        # Use ffmpeg to convert the file
        subprocess.run(['ffmpeg','-i', os.path.join(path_mov, file), os.path.join(output_folder, new_name)])

        try:
            os.remove(output_folder+'/'+file)
        except:
            print('未删除的mov:',file)

def split_videos(input_folder, output_directory,subclip_duration=6900, overlap_duration=300):
    """ 将一文件夹下全部总时长超过一定时间的文件裁剪成更短的(便于转录出字幕)
    :input_folder:待输入文件夹
    :output_directory:输出文件夹
    :subclip_duration:Define the duration of each subclip in seconds
    :overlap_duration:Define the overlap duration in seconds

    """

    # Get the total duration of the input video
    from moviepy.video.io.VideoFileClip import VideoFileClip


    # Create the output directory if it doesn't exist
    import os
    os.makedirs(output_directory, exist_ok=True)

    mp4_files = get_mp4_list(input_folder)
    print('splitting mp4:',mp4_files)
    # mp4_files = get_files_in_foldes(root_directory=input_folder)
    
    for index,video_file in enumerate(mp4_files):
        print(str(index)+'/'+str(len(mp4_files))+' continue...')

        video_clip = VideoFileClip(video_file)
        total_duration = video_clip.duration
    
        start_time = 0
        subclip_index = 1

        if start_time + total_duration <= subclip_duration:
            continue

        while start_time < total_duration:

            end_time = min(start_time + subclip_duration, total_duration)
            if end_time == total_duration:

                if start_time == 0:
                    subclip_name = os.path.join(output_directory, video_file.split('/')[-1].split('.')[0]+'.mp4')
                    ffmpeg_extract_subclip(video_file, start_time, end_time, targetname=subclip_name)
                    break

            # Extract the subclip
            subclip_name = os.path.join(output_directory, video_file.split('/')[-1].split('.')[0]+f'-{subclip_index}.mp4')
            print(subclip_name)

            # subclip_name = output_directory+video_file.split('.')[0]+f'subclip_{subclip_index}.mp4'
            ffmpeg_extract_subclip(video_file, start_time, end_time, targetname=subclip_name)


            if end_time == total_duration:
                break

            # Update the start time for the next subclip
            start_time = end_time - overlap_duration
            subclip_index += 1

        os.remove(video_file)
    print('------MP4 SPLITTING FINISHED!------')


# 获取缺乏srt文件的文件列表
def get_files_without_srt(path_folder,path_output_mp3):
    print('以下是等待转换的视频文件:')
    list_mp4_2_mp3=[]
    total_frames = 0
    files_already_with_mp3 = os.listdir(path_output_mp3)

    for file in os.listdir(path_folder):

        if file[0]=='.':
            continue
        if (file[-4:]=='.mp4') or (file[-4:]=='.MOV') or (file[-4:]=='.mov'):
            if file[:-4]+'.srt' in os.listdir(path_folder):
                continue
            if file[:-4]+'.mp3' in files_already_with_mp3:
                continue

            else:
                print(file)
                list_mp4_2_mp3.append(path_folder+'/'+file)

                video = VideoFileClip(path_folder+'/'+file)
                frames = int(video.reader.nframes)
                total_frames += frames
                video.close()

    print('文件转换时间:',round(total_frames/120000),'min')

    return list_mp4_2_mp3         


def mp4_2_mp3(list_mp4_2_mp3,path_output):
# 转换mp4文件为mp3文件
    for file in list_mp4_2_mp3:

        video = VideoFileClip(file)                                    # Load the MP4 file
        video.audio.write_audiofile(path_output+'/'+file.split('/')[-1][:-4]+'.mp3')        # Convert the video to audio (MP3)
        video.close()
        clear()

    print('------MP3 TRANSFORMING FINISHED!------')

# Define for splitting mp4: the input video file and output directory
input_folder="/Volumes/岚霆_临床/视频_学习/校内医学参考/实习前培训"
path_output_mp3 = r'/Volumes/岚霆_临床/[]mp3_cn_wait'

output_folder = input_folder
path_mov = input_folder

mov_2_mp4(path_mov,output_folder)
split_videos(input_folder=input_folder, output_directory=output_folder, subclip_duration=3600, overlap_duration=100)
list_mp4_2_mp3 = get_files_without_srt(input_folder,path_output_mp3) # 除了排除已经有srt的还要排出已经转换成了mp3的
mp4_2_mp3(list_mp4_2_mp3,path_output_mp3)

## 没有视频剪辑时检查文件是不是含有"-"符号








