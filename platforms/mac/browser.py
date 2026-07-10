"""Mac 浏览器管理"""
import os, time, subprocess
from pathlib import Path

def launch_chrome(cdp_port=9223, user_data_dir='/tmp/taobao-scrape'):
    """启动带CDP的Chrome"""
    os.system('killall "Google Chrome" 2>/dev/null')
    time.sleep(2)

    chrome = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
    subprocess.Popen([
        chrome, f'--remote-debugging-port={cdp_port}',
        f'--user-data-dir={user_data_dir}',
        '--disable-blink-features=AutomationControlled',
        '--window-size=1400,900',
        'https://www.1688.com'
    ])
    time.sleep(5)

def get_chrome_path():
    return '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'

def get_data_paths():
    return {
        'desktop': Path.home() / 'Desktop',
        'downloads': Path.home() / 'Downloads',
        'results': Path.home() / 'Desktop' / '1688_results',
    }
