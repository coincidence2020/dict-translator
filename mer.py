from docx import Document

def merge_files(original_file, non_chinese_docx_file, index_file, output_file):
    """
    将提取的第二列重新插入到原始文件的对应位置。
    :param original_file: 原始文件路径
    :param non_chinese_docx_file: 不完全由中文字符组成的第二列 .docx 文件路径
    :param index_file: 行号索引文件路径
    :param output_file: 合并后的输出文件路径
    """
    # 读取 .docx 文件中的非中文第二列
    doc = Document(non_chinese_docx_file)
    non_chinese_second_columns = [paragraph.text for paragraph in doc.paragraphs]

    # 读取行号索引
    with open(index_file, 'r', encoding='utf-8') as idxfile:
        indices = [int(line.strip()) for line in idxfile]

    # 检查行号索引和非中文第二列数量是否一致
    if len(indices) != len(non_chinese_second_columns):
        raise ValueError("行号索引和非中文第二列数量不匹配！")

    # 逐行读取原始文件并合并
    with open(original_file, 'r', encoding='utf-8') as original, open(output_file, 'w', encoding='utf-8') as outfile:
        line_number = 0
        non_chinese_index = 0
        for line in original:
            line_number += 1
            parts = line.strip().split('\t')
            if non_chinese_index < len(indices) and line_number == indices[non_chinese_index]:
                parts[0] = non_chinese_second_columns[non_chinese_index]  # 替换第二列
                non_chinese_index += 1
            outfile.write('\t'.join(parts) + '\n')  # 写入整行


# pair =input()
language_pairs = [
    "en-af", "en-ar", "en-bg", "en-bn", "en-bs", "en-ca", "en-cs", "en-da", "en-de",
    "en-el", "en-es", "en-et", "en-fa", "en-fi", "en-fr", "en-he", "en-hi",
    "en-hr", "en-hu", "en-id", "en-it", "en-ja", "en-ko", "en-lt", "en-lv", "en-mk",
    "en-ms", "en-nl", "en-no", "en-pl", "en-pt", "en-ro", "en-ru", "en-sk", "en-sl",
    "en-sq", "en-sv", "en-ta", "en-th", "en-tl", "en-tr", "en-uk", "en-vi"
]
for pair in language_pairs:
    original_file = rf'F:\PythonProject\tranlate\output\translated_{pair}.txt'

    non_chinese_docx_file = rf"D:\user_edge下载\language\{pair}.docx"  # 不完全由中文字符组成的行 .docx 文件路径
    index_file = rf"E:\onedrive\桌面\lan\{pair}_index.txt"  # 行号索引文件路径
    output_file = rf"F:\PythonProject\tranlate\filiter\filtered_translated_{pair}.txt"  # 合并后的输出文件路径

    merge_files(original_file, non_chinese_docx_file, index_file, output_file)
    print(f"文件已合并并保存到: {output_file}")