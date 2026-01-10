import os

def count_lines_in_file(file_path):
    """统计单个文件的行数"""
    with open(file_path, 'r', encoding='utf-8') as file:
        return sum(1 for line in file)

def count_lines_in_directory(directory):
    """统计目录下所有文件的行数"""
    total_lines = 0
    for root, dirs, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            try:
                lines = count_lines_in_file(file_path)
                total_lines += lines
                print(f"{os.path.basename(file_path)}: {lines} 行")
            except (UnicodeDecodeError, PermissionError):
                # 忽略无法读取的文件（如二进制文件或没有权限的文件）
                print(f"{os.path.basename(file_path)}: 无法读取")
    return total_lines

def is_chinese(text):
    """
    判断字符串是否为中文
    :param text: 输入字符串
    :return: True 如果字符串是中文，否则 False
    """
    # 中文字符的 Unicode 范围
    for char in text:
        if not ('\u4e00' <= char <= '\u9fff'):
            return False
    return True

def count_non_chinese_ratio_in_file(file_path, column_index):
    """
    统计文件中指定列的非中文内容比例
    :param file_path: 文件路径
    :param column_index: 列索引（0 表示第一列，1 表示第二列）
    :return: 非中文内容的比例（0 到 1 之间的浮点数）
    """
    total_lines = 0
    non_chinese_count = 0

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                total_lines += 1
                columns = line.strip().split('\t')  # 假设列之间用制表符分隔
                if len(columns) > column_index:  # 确保列存在
                    target_column = columns[column_index]
                    if not is_chinese(target_column):  # 判断目标列是否为中文
                        non_chinese_count += 1
    except (UnicodeDecodeError, PermissionError):
        print(f"{os.path.basename(file_path)}: 无法读取")
        return None
    except FileNotFoundError:
        print(f"文件未找到: {os.path.basename(file_path)}")
        return None
    except Exception as e:
        print(f"读取文件时出错: {str(e)}")
        return None

    if total_lines == 0:
        print(f"文件为空: {os.path.basename(file_path)}")
        return 0.0

    ratio = non_chinese_count / total_lines
    return ratio

def count_non_chinese_ratio_in_directory(directory_path):
    """
    统计目录中所有文件的非中文内容比例
    :param directory_path: 目录路径
    :return: 字典，键为文件名，值为非中文内容的比例
    """
    results = {}

    # 遍历目录中的所有文件
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path) and filename.endswith('.txt'):  # 确保是文本文件
            # 根据文件名决定统计的列
            if filename.startswith("zh-"):
                column_index = 0  # 第一列
            elif filename.endswith("-zh.txt"):
                column_index = 1  # 第二列
            else:
                print(f"跳过不支持的文件: {filename}")
                continue

            ratio = count_non_chinese_ratio_in_file(file_path, column_index)
            if ratio is not None:
                # 去掉文件名中的前缀
                clean_filename = os.path.basename(filename)
                results[clean_filename] = ratio

    return results

def calculate_average_chinese_ratio(results):
    """
    计算平均中文比例
    :param results: 字典，键为文件名，值为非中文内容的比例
    :return: 平均中文比例（0 到 1 之间的浮点数）
    """
    if not results:
        return 0.0

    # 计算中文比例的平均值
    total_ratio = sum(1 - ratio for ratio in results.values())
    average_ratio = total_ratio / len(results)
    return average_ratio

if __name__ == "__main__":
    from config import FILTER_DIR
    
    directory = FILTER_DIR
    total_lines = count_lines_in_directory(directory)
    print(f"总行数: {total_lines} 行")

    results = count_non_chinese_ratio_in_directory(directory)

    tmp=0
    if results:
        print("非中文内容的比例统计：")
        for filename, ratio in results.items():
            print(f"{filename}: {ratio:.2%}")
            tmp+=ratio

        # 计算平均中文比例
        average_chinese_ratio = (tmp-1)/(len(results))
        print(f"平均中文比例: {average_chinese_ratio:.2%}")
    else:
        print("目录中没有文件或所有文件为空。")