import random
import time
import os
from tqdm import tqdm
from googletrans import Translator
from config import GOOGLE_TRANSLATE_URLS, OUTPUT_DIR, FILTER_DIR, TRANSLATION_CONFIG
from utils import is_chinese, ensure_dir

translator = Translator(service_urls=GOOGLE_TRANSLATE_URLS)


def translate_worker(args):
    """
    翻译工作函数
    :param args: 元组 (行索引, 原文, 待翻译文本)
    :return: 元组 (行索引, 翻译结果)
    """
    time.sleep(1)
    idx, src, text = args
    max_retries = TRANSLATION_CONFIG['max_retries']
    source_lang = TRANSLATION_CONFIG['source_lang']
    target_lang = TRANSLATION_CONFIG['target_lang']
    
    for attempt in range(max_retries):
        try:
            # 使用翻译实例进行翻译
            translated = translator.translate(text, src=source_lang, dest=target_lang).text
            if not translated:
                print(f"空翻译结果: {text}")
                return (idx, text)  # 直接返回原文

            # 二次校验逻辑优化
            if not is_chinese(translated):
                retry_trans = translator.translate(src, dest=target_lang).text

                if is_chinese(retry_trans):
                    return (idx, retry_trans)
                return (idx, text)

            return (idx, translated)

        except Exception as e:
            # 错误处理逻辑
            error_msg = str(e).split('\n')[0]  # 取错误信息首行
            print(f"第{idx}行翻译失败 (尝试{attempt + 1}/10): {error_msg}")

            time.sleep(random.randint(1, 5))

    return (idx, text)


def process_file(input_path, output_path):
    """
    处理单个文件的完整流程
    :param input_path: 输入文件路径
    :param output_path: 输出文件路径
    """
    # 读取所有内容到内存
    with open(input_path, 'r', encoding='utf-8') as f:
        original_lines = [line.strip() for line in f]

    # 预处理待翻译内容
    translation_tasks = []
    for idx, line in enumerate(original_lines):
        if not line:
            continue

        # 优化分割逻辑
        separator = '\t' if '\t' in line else ' '
        parts = line.split(separator, 1)
        if len(parts) < 2:
            continue

        src, trans = parts
        if not is_chinese(trans):
            translation_tasks.append((idx, src, trans))

    # 单线程顺序执行翻译任务
    translated_results = {}
    for task in tqdm(translation_tasks, desc='Translating'):
        idx, trans = translate_worker(task)
        translated_results[idx] = trans

    # 构建最终结果
    processed_lines = []
    for idx, line in enumerate(original_lines):
        if idx in translated_results:
            separator = '\t' if '\t' in line else ' '
            src = line.split(separator, 1)[0]
            processed_lines.append(f"{src}\t{translated_results[idx]}\n")
        else:
            processed_lines.append(f"{line}\n")

    # 批量写入结果
    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(processed_lines)


# 输入输出目录配置
input_dir = OUTPUT_DIR
output_dir = FILTER_DIR

ensure_dir(output_dir)

# 批量处理文件
for filename in os.listdir(input_dir):
    if not filename.startswith("translated_en-"):
        continue

    input_file = os.path.join(input_dir, filename)
    output_file = os.path.join(output_dir, f"filtered_{filename}")

    if not os.path.isfile(input_file):
        continue

    print(f"Processing {filename}...")
    start = time.time()
    process_file(input_file, output_file)
    print(f"Completed in {time.time() - start:.2f}s\n")