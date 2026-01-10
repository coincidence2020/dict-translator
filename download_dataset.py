import requests
import logging
import os
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse

# 配置日志
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def download_file(url, output_dir):
    """
    下载文件并保存到指定目录。
    :param url: 文件 URL
    :param output_dir: 输出目录
    """
    try:
        # 发送 HTTP 请求获取文件内容
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # 检查请求是否成功

        # 从 URL 中提取文件名
        filename = os.path.basename(urlparse(url).path)
        output_path = os.path.join(output_dir, filename)

        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)

        # 将文件内容保存到本地
        with open(output_path, "wb") as file:
            file.write(response.content)
        logging.info(f"文件已保存到 {output_path}")

    except requests.exceptions.RequestException as e:
        logging.error(f"下载文件时出错: {url} - {e}")

def process_multiple_urls(urls, output_dir, max_workers=5):
    """
    批量处理多个 URL。
    :param urls: URL 列表
    :param output_dir: 输出目录
    :param max_workers: 最大线程数（用于并发处理）
    """
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)

    # 使用多线程并发处理 URL
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(download_file, url, output_dir) for url in urls]
        for future in futures:
            future.result()  # 等待所有任务完成

def load_urls_from_file(file_path):
    """
    从文件中加载 URL 列表。
    :param file_path: 文件路径
    :return: URL 列表
    """
    with open(file_path, "r", encoding="utf-8") as file:
        urls = [line.strip() for line in file if line.strip()]
    return urls

if __name__ == "__main__":
    from config import URLS_FILE, DATASET_DIR
    
    # 从文件中加载 URL 列表
    urls = load_urls_from_file(URLS_FILE)
    logging.info(f"共加载 {len(urls)} 个 URL")

    # 批量处理 URL
    process_multiple_urls(urls, DATASET_DIR)

    logging.info("所有文件下载完成！")