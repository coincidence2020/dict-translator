import time
import os
from googletrans import Translator
from config import DATASET_DIR, OUTPUT_DIR, TRANSLATION_CONFIG
from utils import is_chinese, ensure_dir

translator = Translator()

def translate_text(text):
    max_retries = TRANSLATION_CONFIG['max_retries']
    retry_delay = TRANSLATION_CONFIG['retry_delay']
    source_lang = TRANSLATION_CONFIG['source_lang']
    target_lang = TRANSLATION_CONFIG['target_lang']
    
    for attempt in range(max_retries):
        time.sleep(retry_delay)
        try:
            # 第一次翻译
            translated = translator.translate(text, src=source_lang, dest=target_lang).text
            if not translated:  # 如果翻译结果为空（例如发生异常），返回一个错误信息
                raise ValueError("Empty translation result")

            # 检查翻译结果是否为中文，如果不是，对非中文字符部分单独翻译
            if not is_chinese(translated):
                # 将翻译结果按行拆分
                lines = translated.split("\n")
                translated_lines = []
                text_lines = text.split("\n")
                for i in range(len(lines)):
                    # 如果某一行不是中文，保留原文
                    if not is_chinese(lines[i]) and i < len(text_lines):
                        lines[i] = text_lines[i]
                    translated_lines.append(lines[i])
                # 重新组合翻译结果
                translated = "\n".join(translated_lines)

            return translated
        except Exception as e:
            time.sleep(5)  # 等待 5 秒后重试



def translate_batch(lines, max_workers=5):
    translated_lines = []

    try:
        s = "\n".join(line.split(' ')[0] for line in lines)
        src_lines = [line.split(' ')[1] for line in lines]
    except:
        s = "\n".join(line.split('\t')[0] for line in lines)
        src_lines = [line.split('\t')[1] for line in lines]

    # 获取翻译结果
    res_lines = translate_text(s).split("\n")
    print(res_lines)
    for i in range(len(src_lines)):
        translated_lines.append(res_lines[i] + "\t" + src_lines[i])
    return translated_lines


# 输入和输出目录
input_dir = DATASET_DIR
output_dir = OUTPUT_DIR

# 确保输出目录存在
ensure_dir(output_dir)

# 遍历输入目录中的所有文件
for filename in os.listdir(input_dir):
    if not filename.startswith("en-"):
        print(f"Skipping file: {filename} (does not match naming pattern)")
        continue

    input_file = os.path.join(input_dir, filename)
    output_file = os.path.join(output_dir, f"translated_{filename}")

    # 检查是否是文件（跳过子目录）
    if not os.path.isfile(input_file):
        continue

    print(f"Processing file: {input_file}")

    # 读取文件
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 计时开始
    start_time = time.time()

    # 分批翻译
    batch_size = TRANSLATION_CONFIG['batch_size']
    translated_lines = []

    for i in range(0, len(lines), batch_size):
        batch = lines[i:i + batch_size]
        translated_batch = translate_batch(batch)
        translated_lines.extend(translated_batch)

        # 每翻译完一个批次保存一次
        with open(output_file, 'a', encoding='utf-8') as output_f:
            output_f.writelines(translated_lines)
        translated_lines = []  # 清空已保存的行
        print(f"Processed batch starting from line {i + 1} in file {filename}.")

    # 计时结束
    end_time = time.time()
    total_time = end_time - start_time

    # 输出总耗时
    print(f"Translation completed for file: {filename}")
    print(f"Results saved to: {output_file}")
    print(f"Total time taken: {total_time:.2f} seconds.")