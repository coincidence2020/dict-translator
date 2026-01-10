from docx import Document

pair = "es-en"
input_file = rf'F:\PythonProject\tranlate\output\translated_{pair}.txt'  # 输入文件名
output_dir = r"E:\onedrive\桌面\split_files"  # 输出文件目录
lines_per_file = 20000  # 每个文件的行数

# 确保输出目录存在
import os
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 读取输入文件并分割
with open(input_file, 'r', encoding='utf-8') as infile:
    file_count = 1
    doc = Document()
    line_count = 0

    for line in infile:
        parts = line.strip().split('\t')  # 按制表符分割每一行
        if len(parts) >= 2:  # 确保有第二列
            english_word = parts[1]  # 提取第二列
            doc.add_paragraph(english_word)  # 将第二列内容添加到Word文档中
            line_count += 1

        # 每3万条保存一个文件
        if line_count >= lines_per_file:
            output_file = os.path.join(output_dir, f'filtered_translated_{pair}_part{file_count}.docx')
            doc.save(output_file)
            print(f"已保存文件: {output_file}")
            file_count += 1
            doc = Document()  # 创建新的Word文档
            line_count = 0

    # 保存剩余的行
    if line_count > 0:
        output_file = os.path.join(output_dir, f'filtered_translated_{pair}_part{file_count}.docx')
        doc.save(output_file)
        print(f"已保存文件: {output_file}")

print("文件分割完成！")