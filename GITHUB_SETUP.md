# GitHub 上传指南

## 准备工作

在将项目上传到 GitHub 之前，请确保：

1. ✅ 已安装 Git
2. ✅ 已创建 GitHub 账户
3. ✅ 已在 GitHub 上创建新仓库

## 上传步骤

### 1. 初始化 Git 仓库

在项目根目录（`F:\PythonProject\tranlate`）打开终端，执行：

```bash
git init
```

### 2. 添加文件到暂存区

```bash
git add .
```

### 3. 提交更改

```bash
git commit -m "Initial commit: 多语言词典转换工具"
```

### 4. 添加远程仓库

在 GitHub 上创建新仓库后，复制仓库 URL，然后执行：

```bash
git remote add origin https://github.com/你的用户名/仓库名.git
```

### 5. 推送到 GitHub

```bash
git branch -M main
git push -u origin main
```

## 注意事项

1. **敏感信息**: 确保没有提交包含 API 密钥、密码等敏感信息的文件
2. **大文件**: 项目中的 `dataset/`、`output/`、`filiter/` 目录包含大量数据文件，已被 `.gitignore` 排除
3. **首次推送**: 如果遇到认证问题，可能需要配置 GitHub Personal Access Token

## 配置 GitHub Personal Access Token

如果使用 HTTPS 推送需要认证：

1. 访问 GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. 生成新 token，勾选 `repo` 权限
3. 使用 token 作为密码进行推送

或者使用 SSH：

1. 生成 SSH 密钥：`ssh-keygen -t ed25519 -C "your_email@example.com"`
2. 将公钥添加到 GitHub Settings → SSH and GPG keys
3. 使用 SSH URL 添加远程仓库：`git remote add origin git@github.com:用户名/仓库名.git`

## 后续更新

修改代码后，使用以下命令更新：

```bash
git add .
git commit -m "描述你的更改"
git push
```

## 项目描述建议

在 GitHub 仓库设置中，建议添加以下描述：

- **仓库名称**: `multilingual-dictionary-converter` 或 `dict-translator`
- **描述**: 将英文-其他语言词典转换为中文-其他语言词典的工具集
- **标签**: `python`, `translation`, `dictionary`, `multilingual`, `nlp`

## README 徽章（可选）

可以在 README.md 顶部添加徽章：

```markdown
![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
```

