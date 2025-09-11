# 部署指南 / Deployment Guide

## 🚀 部署到Streamlit Cloud（推荐）

### 步骤1：上传到GitHub
1. 在GitHub上创建新仓库（比如命名为 `course-topic-selection`）
2. 将本地代码推送到GitHub：
```bash
git remote add origin https://github.com/YOUR_USERNAME/course-topic-selection.git
git branch -M main
git push -u origin main
```

### 步骤2：部署到Streamlit Cloud
1. 访问 [share.streamlit.io](https://share.streamlit.io)
2. 使用GitHub账号登录
3. 点击 "New app"
4. 选择您的GitHub仓库
5. 主文件路径填写：`app.py`
6. 点击 "Deploy!"

### 步骤3：获取公网地址
部署成功后，您会得到一个类似这样的网址：
```
https://your-app-name.streamlit.app
```

## 🌐 其他部署选项

### 选项1：Heroku（免费层已停止）
- 需要创建 `Procfile` 文件
- 适合有经验的用户

### 选项2：Railway
1. 访问 [railway.app](https://railway.app)
2. 连接GitHub仓库
3. 自动部署

### 选项3：Render
1. 访问 [render.com](https://render.com)
2. 连接GitHub仓库
3. 选择Web Service
4. 构建命令：`pip install -r requirements.txt`
5. 启动命令：`streamlit run app.py --server.port $PORT --server.address 0.0.0.0`

## 📝 部署后的使用

### 给学生的访问方式：
1. **分享网址**：直接给学生云端网址
2. **二维码**：可以生成二维码方便手机访问
3. **课堂投影**：在课堂上展示网址

### 数据管理：
- 云端部署的数据会在应用重启时重置
- 如需持久化数据，建议使用数据库（如SQLite）

## 🔧 故障排除

### 常见问题：
1. **部署失败**：检查requirements.txt中的包版本
2. **应用崩溃**：查看Streamlit Cloud的日志
3. **数据丢失**：云端应用重启会重置数据

### 解决方案：
- 定期下载PDF报告备份数据
- 考虑添加数据库支持（进阶功能）
