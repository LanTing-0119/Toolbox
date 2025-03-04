import subprocess

def get_safari_tabs_urls():
    # AppleScript 代码：获取所有窗口的标签页 URL
    applescript = '''
    tell application "Safari"
        set winList to every window
        set tabUrls to {}
        repeat with aWin in winList
            set tabList to every tab of aWin
            repeat with aTab in tabList
                copy URL of aTab to end of tabUrls
            end repeat
        end repeat
        return tabUrls
    end tell
    '''
    
    try:
        # 执行 AppleScript 并捕获输出
        result = subprocess.run(
            ["osascript", "-e", applescript],
            capture_output=True,
            text=True,
            check=True
        )
        # 按逗号分割并清理空白字符
        urls = [url.strip() for url in result.stdout.split(", ")]
        return urls
    except subprocess.CalledProcessError as e:
        print(f"执行错误: {e.stderr}")
        return []
    except Exception as e:
        print(f"未知错误: {str(e)}")
        return []

# 锁屏
def lock_screen():
    # AppleScript 代码：获取所有窗口的标签页 URL
    applescript2 = '''
    -- 延迟 3 秒，发出提醒
    display dialog "🤔 想清楚为啥要上B站了吗?" with title "劝学" buttons {"确定"} default button "确定" giving up after 5
    display dialog "来个8分钟 🏃‍♂️ 醒醒 🧠 " with title "劝学" buttons {"确定"} default button "确定" giving up after 5

    -- 锁屏
    -- tell application "System Events" to keystroke "q" using {control down, command down}

    '''
    
    try:
        # 执行 AppleScript 并捕获输出
        result = subprocess.run(
            ["osascript", "-e", applescript2],
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"执行错误: {e.stderr}")
        return []
    except Exception as e:
        print(f"未知错误: {str(e)}")
        return []

forbidden_url = 'bilibili'
# 调用函数并打印结果
urls = get_safari_tabs_urls()
print("Safari 当前标签页网址:")
for url in urls:
    if forbidden_url in url:
        lock_screen()
        break