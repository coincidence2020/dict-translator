# GitHub 创建仓库和上传代码完整指南

## 第一步：在 GitHub 上创建仓库

### 1.1 登录 GitHub
访问 [https://github.com](https://github.com) 并登录你的账户

### 1.2 创建新仓库
1. 点击右上角的 **"+"** 按钮
2. 选择 **"New repository"**（新建仓库）

### 1.3 填写仓库信息
- **Repository name（仓库名称）**: 建议使用 `multilingual-dictionary-converter` 或 `dict-translator`
- **Description（描述）**: `将英文-其他语言词典转换为中文-其他语言词典的工具集`
- **Visibility（可见性）**: 
  - 选择 **Public**（公开）**或** **Private**（私有）
- **重要**: 
  - ❌ **不要**勾选 "Add a README file"（我们已经有了）
  - ❌ **不要**勾选 "Add .gitignore"（我们已经有了）
  - ❌ **不要**勾选 "Choose a license"（我们已经有了）

### 1.4 创建仓库
点击 **"Create repository"** 按钮

### 1.5 复制仓库URL
创建成功后，GitHub会显示仓库页面，复制显示的HTTPS URL，例如：
```
https://github.com/你的用户名/仓库名.git
```

---

## 第二步：在本地提交代码

你的项目已经初始化了Git仓库，现在需要提交当前的更改。

### 2.1 查看当前状态
```bash
git status
```

### 2.2 添加所有文件到暂存区
```bash
git add .
```

### 2.3 提交更改
```bash
git commit -m "Initial commit: 多语言词典转换工具"
```

---

## 第三步：连接远程仓库并推送

### 3.1 添加远程仓库
将你刚才复制的GitHub仓库URL替换到下面的命令中：

```bash
git remote add origin https://github.com/你的用户名/仓库名.git
```

**示例**：
```bash
git remote add origin https://github.com/zhangsan/multilingual-dictionary-converter.git
```

### 3.2 将分支重命名为 main（如果当前是master）
```bash
git branch -M main
```

### 3.3 推送到GitHub
```bash
git push -u origin main
```

---

## 第四步：处理认证问题

### 如果推送时要求输入用户名和密码：

#### 方法1：使用 Personal Access Token（推荐）

1. **生成Token**：
   - 访问：https://github.com/settings/tokens
   - 点击 **"Generate new token"** → **"Generate new token (classic)"**
   - 填写 Note（备注）：`Git Push Token`
   - 选择过期时间：建议选择 **90 days** 或 **No expiration**
   - 勾选权限：**repo**（全部勾选）
   - 点击 **"Generate token"**
   - **重要**：复制生成的token（只显示一次！）

2. **使用Token推送**：
   - 用户名：输入你的GitHub用户名
   - 密码：**粘贴刚才复制的token**（不是你的GitHub密码）

#### 方法2：使用SSH（更安全，推荐长期使用）

1. **生成SSH密钥**（如果还没有）：
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ```
   - 按回车使用默认路径
   - 可以设置密码或直接回车（不设置密码）

2. **复制公钥**：
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```
   Windows PowerShell:
   ```powershell
   Get-Content ~\.ssh\id_ed25519.pub
   ```

3. **添加到GitHub**：
   - 访问：https://github.com/settings/keys
   - 点击 **"New SSH key"**
   - Title：填写描述（如：`My Computer`）
   - Key：粘贴刚才复制的公钥
   - 点击 **"Add SSH key"**

4. **使用SSH URL重新添加远程仓库**：
   ```bash
   git remote remove origin
   git remote add origin git@github.com:你的用户名/仓库名.git
   git push -u origin main
   ```

---

## 完整命令序列（复制粘贴版）

```bash
# 1. 添加所有文件
git add .

# 2. 提交更改
git commit -m "Initial commit: 多语言词典转换工具"

# 3. 添加远程仓库（替换为你的仓库URL）
git remote add origin https://github.com/你的用户名/仓库名.git

# 4. 重命名分支为main
git branch -M main

# 5. 推送到GitHub
git push -u origin main
```

---

## 验证上传成功

1. 刷新你的GitHub仓库页面
2. 应该能看到所有文件已经上传
3. README.md 会自动显示在仓库首页

---

## 后续更新代码

当你修改代码后，使用以下命令更新：

```bash
# 1. 查看更改
git status

# 2. 添加更改的文件
git add .

# 3. 提交更改（写清楚你做了什么）
git commit -m "更新：描述你的更改内容"

# 4. 推送到GitHub
git push
```

---

## 常见问题

### Q: 提示 "remote origin already exists"
**A**: 说明已经添加过远程仓库，可以删除后重新添加：
```bash
git remote remove origin
git remote add origin https://github.com/你的用户名/仓库名.git
```

### Q: 提示 "failed to push some refs"
**A**: 可能是远程仓库有文件而本地没有，先拉取：
```bash
git pull origin main --allow-unrelated-histories
git push -u origin main
```

### Q: 忘记提交某些文件
**A**: 可以继续添加并提交：
```bash
git add 文件名
git commit -m "添加遗漏的文件"
git push
```

---

## 需要帮助？

如果遇到问题，可以：
1. 查看错误信息，通常Git会给出提示
2. 检查网络连接
3. 确认GitHub仓库URL是否正确
4. 确认认证信息是否正确

