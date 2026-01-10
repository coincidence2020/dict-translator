"""
工具函数模块
"""
# 预加载中文字符范围
chinese_chars = set(chr(i) for i in range(0x4e00, 0x9fff + 1))


def is_chinese(text):
    """
    判断字符串是否完全由中文字符组成
    :param text: 输入字符串
    :return: True 如果字符串完全由中文字符组成，否则 False
    """
    if not text:
        return False
    return all(char in chinese_chars for char in text)


def ensure_dir(directory):
    """
    确保目录存在，如果不存在则创建
    :param directory: 目录路径
    """
    import os
    if not os.path.exists(directory):
        os.makedirs(directory)

