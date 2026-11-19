import requests
import json
import random
import os
import sys

# 快貓加速器 API 端點
API_URL = "https://api.kuaimiaov4.com/appV4api/manusAi/applyLogin"

# 模擬捷徑的請求頭
HEADERS = {
    "User-Agent": "Dart/3.12 (dart:io)",
    "Content-Type": "application/json",
    "Accept-Encoding": "gzip"
}

# 配置文件儲存路徑 (在 GitHub Actions 中會被設置為相對路徑)
CONFIG_FILE_PATH = os.environ.get("CONFIG_FILE_PATH", "proxies/kuaimiao_config.yaml")

def get_dynamic_config():
    """
    模擬捷徑邏輯，獲取動態的 ymlUrl，然後下載其內容。
    """
    # 生成隨機 deviceKey
    random_number = random.randint(10000000, 99999999)
    device_key = f"{random_number}-f3ca-4bd8-b7c1-57bb85060000"
    
    payload = {"deviceKey": device_key}

    try:
        # 步驟 1: 發送 POST 請求獲取 ymlUrl
        print(f"Sending POST request to {API_URL} with deviceKey: {device_key[:4]}...")
        response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=15)
        response.raise_for_status() # 檢查 HTTP 錯誤

        response_data = response.json()
        
        # 提取 ymlUrl
        yml_url = response_data.get('data', {}).get('ymlUrl')

        if not yml_url:
            raise ValueError(f"無法從響應中獲取 ymlUrl. 響應: {response_data}")

        print(f"Successfully obtained ymlUrl: {yml_url}")

        # 步驟 2: 下載 ymlUrl 指向的實際配置內容
        print(f"Downloading configuration from {yml_url}...")
        config_response = requests.get(yml_url, timeout=30)
        config_response.raise_for_status() # 檢查 HTTP 錯誤

        config_content = config_response.text
        print("Configuration content downloaded successfully.")
        return config_content

    except requests.exceptions.RequestException as e:
        print(f"網絡請求錯誤: {e}", file=sys.stderr)
        return None
    except ValueError as e:
        print(f"數據解析錯誤: {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"發生未知錯誤: {e}", file=sys.stderr)
        return None

def save_config_to_file(content):
    """
    將配置內容保存到指定文件。
    """
    if not content:
        print("沒有內容可保存，跳過文件寫入。", file=sys.stderr)
        return

    # 確保目錄存在
    os.makedirs(os.path.dirname(CONFIG_FILE_PATH), exist_ok=True)
    
    with open(CONFIG_FILE_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Configuration saved to {CONFIG_FILE_PATH}")

if __name__ == "__main__":
    config = get_dynamic_config()
    if config:
        save_config_to_file(config)
    else:
        print("未能獲取配置，操作失敗。", file=sys.stderr)
        sys.exit(1) # 退出並指示失敗