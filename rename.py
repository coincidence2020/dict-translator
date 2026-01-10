import os


def batch_rename(directory, start_num=1):
    """
    批量重命名目录下的文件

    :param directory: 目标目录路径
    :param start_num: 起始编号，默认为1
    """
    # 确保目录存在
    if not os.path.exists(directory):
        print(f"目录 {directory} 不存在")
        return

    # 获取目录下的所有文件
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

    # 遍历文件并重命名
    for i, filename in enumerate(files, start=start_num):
        # 获取文件扩展名
        file_ext=filename.split('_')[-1].replace("en","zh")

        # 构建新的文件名
        new_filename = f"{file_ext}"

        # 获取文件的完整路径
        old_file = os.path.join(directory, filename)
        new_file = os.path.join(directory, new_filename)

        # 重命名文件
        os.rename(old_file, new_file)
        print(f"重命名: {filename} -> {new_filename}")


if __name__ == "__main__":
    from config import FILTER_DIR
    
    # 设置目录路径、前缀和起始编号
    directory = FILTER_DIR
    start_num = 1  # 起始编号

    # 调用批量重命名函数
    batch_rename(directory, start_num)