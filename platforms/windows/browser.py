"""Windows 浏览器管理"""
import os, time, subprocess
from pathlib import Path

def launch_chrome(cdp_port=9222):
    """启动带CDP的Chrome"""
    os.system('taskkill /F /IM chrome.exe /T 2>nul')
    time.sleep(3)

    subprocess.Popen([
        r'C:\Program Files\Google\Chrome\Application\chrome.exe',
        f'--remote-debugging-port={cdp_port}',
        r'--user-data-dir=C:\taobao-scrape',
        '--disable-blink-features=AutomationControlled',
        '--window-size=1400,900',
        'https://www.1688.com'
    ], shell=True)
    time.sleep(5)

def get_chrome_path():
    return r'C:\Program Files\Google\Chrome\Application\chrome.exe'

def get_data_paths():
    return {
        'desktop': Path.home() / 'Desktop',
        'results': Path.home() / 'Desktop' / '1688_results',
    }
