# GitHub 连接问题解决方案

## 问题：无法连接到 GitHub (port 443)

错误信息：`Failed to connect to github.com port 443`

## 解决方案

### 方案1：检查网络连接

```powershell
# 测试是否能访问 GitHub
Test-NetConnection github.com -Port 443
```

### 方案2：配置代理（如果你使用代理）

```bash
# 设置 HTTP 代理
git config --global http.proxy http://代理地址:端口
git config --global https.proxy https://代理地址:端口

# 例如：
# git config --global http.proxy http://127.0.0.1:7890
# git config --global https.proxy https://127.0.0.1:7890

# 查看当前代理设置
git config --global --get http.proxy
git config --global --get https.proxy

# 取消代理设置（如果不需要）
# git config --global --unset http.proxy
# git config --global --unset https.proxy
```

### 方案3：使用 SSH 代替 HTTPS（推荐）

SSH 通常比 HTTPS 更稳定，特别是在网络受限的环境中。

#### 3.1 检查是否已有 SSH 密钥

```powershell
# 检查是否存在 SSH 密钥
Test-Path ~\.ssh\id_ed25519
# 或
Test-Path ~\.ssh\id_rsa
```

#### 3.2 如果没有，生成 SSH 密钥

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

- 按回车使用默认路径
- 可以设置密码或直接回车（不设置密码）

#### 3.3 复制公钥

```powershell
# 显示公钥内容
Get-Content ~\.ssh\id_ed25519.pub
```

#### 3.4 添加到 GitHub

1. 访问：https://github.com/settings/keys
2. 点击 **"New SSH key"**
3. Title：填写描述（如：`My Computer`）
4. Key：粘贴刚才复制的公钥
5. 点击 **"Add SSH key"**

#### 3.5 修改远程仓库 URL 为 SSH

```bash
# 查看当前远程仓库
git remote -v

# 删除 HTTPS 远程仓库
git remote remove origin

# 添加 SSH 远程仓库
git remote add origin git@github.com:coincidence2020/dict-translator.git

# 测试 SSH 连接
ssh -T git@github.com

# 推送到 GitHub
git push -u origin main
```

### 方案4：使用 GitHub CLI（gh）

如果上述方法都不行，可以尝试使用 GitHub CLI：

```bash
# 安装 GitHub CLI
# Windows: winget install GitHub.cli
# 或下载：https://cli.github.com/

# 登录
gh auth login

# 然后使用 gh 命令推送
```

### 方案5：检查防火墙和杀毒软件

- 临时关闭防火墙测试
- 检查杀毒软件是否阻止 Git
- 将 Git 添加到防火墙白名单

### 方案6：使用镜像站点（临时方案）

如果在中国大陆，可以尝试：

```bash
# 使用 GitHub 镜像（不推荐用于推送，但可以测试连接）
# 仅用于测试，不要用于实际推送
```

## 快速诊断命令

```powershell
# 1. 测试 GitHub 连接
Test-NetConnection github.com -Port 443

# 2. 测试 DNS 解析
Resolve-DnsName github.com

# 3. 查看 Git 配置
git config --list

# 4. 查看远程仓库设置
git remote -v

# 5. 测试 SSH 连接（如果使用 SSH）
ssh -T git@github.com
```

## 推荐操作顺序

1. **首先尝试方案3（SSH）** - 最稳定可靠
2. 如果使用代理，配置方案2
3. 检查网络和防火墙（方案1、5）

## 成功连接后

一旦连接成功，就可以正常推送：

```bash
git push -u origin main
```

