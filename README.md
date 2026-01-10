# 多语言词典转换工具

这是一个将英文-其他语言词典转换为中文-其他语言词典的工具集。项目使用 Google 翻译 API 将英文词典条目翻译成中文，生成多语言词典文件。

## 功能特性

- 📥 **下载词典**: 从 Facebook AI Research 的 MUSE 项目下载多语言词典
- 🔄 **批量翻译**: 使用 Google 翻译 API 批量将英文词典翻译成中文
- ✅ **质量检查**: 自动检测翻译结果中的非中文字符并进行修正
- 📊 **统计分析**: 统计词典文件的行数和中文比例
- 🔧 **文件处理**: 支持文件重命名、统计分析等操作

```
# 数据目录
├── dataset/              # 原始词典文件
├── output/               # 翻译后的文件
└── filiter/              # 过滤后的最终文件
```

## 安装

### 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 1. 下载词典文件

首先下载多语言词典文件：

```bash
python download_dataset.py
```

这将从 `urls.txt` 中读取 URL 列表，下载所有词典文件到 `dataset/` 目录。

### 2. 翻译词典

将英文-其他语言词典翻译成中文-其他语言词典：

```bash
python translate_pair.py
```

该脚本会：
- 读取 `dataset/` 目录中所有以 `en-` 开头的文件
- 将每行的英文单词翻译成中文
- 保存翻译结果到 `output/` 目录

### 3. 质量检查和修正

检查翻译结果并修正非中文字符：

```bash
python pre_en.py
```

该脚本会：
- 检查 `output/` 目录中的翻译文件
- 识别第二列中非中文字符的行
- 重新翻译这些行
- 保存结果到 `filiter/` 目录

### 4. 文件重命名

将翻译后的文件重命名为标准格式（如 `zh-en.txt`）：

```bash
python rename.py
```

### 5. 统计信息

统计词典文件的行数和中文比例：

```bash
python count_line.py
```

## 配置说明

主要配置在 `config.py` 文件中：

- `DATASET_DIR`: 原始词典文件目录
- `OUTPUT_DIR`: 翻译输出目录
- `FILTER_DIR`: 过滤后的文件目录
- `LANGUAGE_PAIRS`: 支持的语言对列表
- `TRANSLATION_CONFIG`: 翻译配置（批次大小、重试次数等）

## 支持的语言

项目支持以下语言对：

- 欧洲语言: de, fr, es, it, pt, ru, pl, nl, cs, sv, da, fi, no, ro, hu, sk, sl, hr, bg, el, et, lv, lt, mk, sq, bs
- 亚洲语言: zh, ja, ko, hi, th, vi, ta, id, ms, tl
- 中东语言: ar, he, fa, tr
- 其他: af, bn, ca, uk

## 注意事项

1. **翻译API限制**: Google 翻译 API 有请求频率限制，脚本已内置重试机制和延迟处理
2. **网络连接**: 需要稳定的网络连接来访问 Google 翻译服务
3. **文件大小**: 大型词典文件可能需要较长时间处理
4. **翻译质量**: 由于机器自动翻译，可能存在错误，但处于合理范围内