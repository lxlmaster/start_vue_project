# Vue项目启动器

一个简单而优雅的Vue项目管理工具，帮助你轻松管理和启动多个Vue项目。

## 功能特点

- 🚀 快速启动Vue项目
- 📦 支持多种包管理器（npm/pnpm/yarn）
- 🔄 自动切换Node.js版本
- 💾 本地保存项目配置
- 🎨 现代化UI设计（Element UI风格）
- 💻 跨平台支持（Windows/macOS）

## 安装说明

### 方式一：直接运行

1. 确保已安装Python 3.x
2. 克隆此仓库：

   ```bash
   git clone https://github.com/yourusername/vue-project-starter.git
   cd vue-project-starter
   ```

3. 安装依赖：

   ```bash
   pip install -r requirements.txt
   ```

4. 运行程序：

   ```bash
   python start_vue_project.py
   ```

### 方式二：使用打包版本

1. 从 [Releases](https://github.com/yourusername/vue-project-starter/releases) 页面下载最新版本
2. 解压文件
3. 运行可执行文件 `vue-project-starter.exe` (Windows) 或 `vue-project-starter` (macOS)

## 使用说明

1. 添加项目
   - 点击"添加项目"按钮
   - 选择项目目录
   - 配置项目信息（名称、包管理器、Node.js版本等）
   - 保存配置

2. 启动项目
   - 从列表中选择项目
   - 点击"启动"按钮
   - 程序会自动：
     - 切换到正确的Node.js版本
     - 安装依赖（如果需要）
     - 启动开发服务器

## 系统要求

- Python 3.x
- Node.js (建议使用 nvm 或 nvm-windows 管理Node.js版本)
- 支持的包管理器：
  - npm
  - yarn
  - pnpm

## 配置文件

项目配置保存在 `config.json` 文件中，包含以下信息：

```json
{
"projects": [
{
"name": "项目名称",
"path": "项目路径",
"package_manager": "包管理器",
"node_version": "Node.js版本"
}
]
}
```

## 常见问题

1. **Q: 如何更改已添加项目的配置？**  
   A: 在项目列表中右键点击项目，选择"编辑配置"。

2. **Q: 支持哪些Node.js版本？**  
   A: 支持所有通过nvm安装的Node.js版本。

## 贡献指南

欢迎提交 Pull Request 或创建 Issue！

1. Fork 本仓库
2. 创建新分支：`git checkout -b feature/your-feature`
3. 提交更改：`git commit -am 'Add some feature'`
4. 推送分支：`git push origin feature/your-feature`
5. 提交 Pull Request

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 作者

[你的名字] - [你的邮箱]

## 致谢

- [Element UI](https://element.eleme.io/) - UI框架
- [PyQt](https://www.riverbankcomputing.com/software/pyqt/) - GUI框架
