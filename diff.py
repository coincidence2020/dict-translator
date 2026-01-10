# from docx import Document
#
# def read_docx(file_path):
#     """读取 .docx 文件内容并返回文本"""
#     doc = Document(file_path)
#     return [para.text for para in doc.paragraphs]
#
# def compare_files(file1, file2, output_diff_file):
#     """
#     比较两个 .docx 文件的不同，并将差异输出到一个新文件中。
#
#     :param file1: 第一个文件的路径
#     :param file2: 第二个文件的路径
#     :param output_diff_file: 输出差异文件的路径
#     """
#     content1 = read_docx(file1)
#     content2 = read_docx(file2)
#
#     with open(output_diff_file, 'w', encoding='utf-8') as diff_file:
#         line_number = 0
#         diff_count = 0
#
#         for line1, line2 in zip(content1, content2):
#             line_number += 1
#             if line1 != line2:
#                 diff_count += 1
#                 diff_file.write(f"差异第 {diff_count} 处，行号: {line_number}\n")
#                 diff_file.write(f"文件1: {line1.strip() if line1 else '<空行>'}\n")
#                 diff_file.write(f"文件2: {line2.strip() if line2 else '<空行>'}\n")
#                 diff_file.write("-" * 50 + "\n")
#
#         if diff_count == 0:
#             diff_file.write("两个文件内容完全相同。\n")
#         else:
#             diff_file.write(f"总共发现 {diff_count} 处差异。\n")
#
#     print(f"比较完成！差异已保存到: {output_diff_file}")


def compare_files(file1, file2, output_diff_file):
    """
    比较两个文本文件的不同，并将差异输出到一个新文件中。

    :param file1: 第一个文件的路径
    :param file2: 第二个文件的路径
    :param output_diff_file: 输出差异文件的路径
    """
    with open(file1, 'r', encoding='utf-8') as f1, open(file2, 'r', encoding='utf-8') as f2, open(output_diff_file, 'w', encoding='utf-8') as diff_file:
        line_number = 0
        diff_count = 0

        while True:
            line_number += 1
            line1 = f1.readline()
            line2 = f2.readline()

            # 如果两个文件都读取完毕，退出循环
            if not line1 and not line2:
                break

            # 如果文件1的行与文件2的行不同
            if line1 != line2:
                diff_count += 1
                diff_file.write(f"差异第 {diff_count} 处，行号: {line_number}\n")
                diff_file.write(f"文件1: {line1.strip() if line1 else '<空行>'}\n")
                diff_file.write(f"文件2: {line2.strip() if line2 else '<空行>'}\n")
                diff_file.write("-" * 50 + "\n")

        if diff_count == 0:
            diff_file.write("两个文件内容完全相同。\n")
        else:
            diff_file.write(f"总共发现 {diff_count} 处差异。\n")

    print(f"比较完成！差异已保存到: {output_diff_file}")

# 示例调用
file1 = r"F:\PythonProject\tranlate\output\translated_es-en.txt"  # 第一个文件路径
file2 = r"F:\PythonProject\tranlate\filiter\filtered_translated_es-en.txt"  # 第二个文件路径
output_diff_file = r"F:\PythonProject\tranlate\output\diff_output.txt"  # 差异输出文件路径

compare_files(file1, file2, output_diff_file)