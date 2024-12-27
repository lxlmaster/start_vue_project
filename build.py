import PyInstaller.__main__
import os
import sys
import platform

# 获取当前目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 基础配置
common_args = [
    'start_vue_project.py',  # 主程序文件
    '--name=Vue项目启动器',  # 生成的可执行文件名称
    '--windowed',  # 使用GUI模式，不显示控制台窗口
    '--onefile',  # 打包成单个文件
    '--clean',  # 清理临时文件
    f'--distpath={os.path.join(current_dir, "dist")}',  # 输出目录
    '--noconfirm',  # 覆盖输出目录
    '--collect-all=tkinter',  # 收集所有tkinter相关文件
    '--collect-all=ttkbootstrap',  # 收集ttkbootstrap相关文件
    '--debug=all',  # 添加调试信息
]

# 根据操作系统添加特定配置
if platform.system() == 'Darwin':  # macOS
    common_args.extend([
        '--icon=resources/app_icon.icns',  # macOS图标
        '--target-arch=universal2',  # 支持Intel和Apple Silicon
        '--codesign-identity=Developer ID Application',  # 代码签名身份
        '--osx-bundle-identifier=com.vuelauncher.app'  # Bundle ID
    ])
elif platform.system() == 'Windows':  # Windows
    common_args.extend([
        '--icon=resources/app_icon.ico',  # Windows图标
        '--version-file=version_info.txt',  # 版本信息文件
        '--uac-admin'  # 请求管理员权限
    ])

# 运行PyInstaller
PyInstaller.__main__.run(common_args)

# 构建完成后的提示
def print_build_info():
    system = platform.system()
    arch = platform.machine()
    dist_path = os.path.join(current_dir, "dist")
    
    print("\n=== 构建信息 ===")
    print(f"操作系统: {system}")
    print(f"架构: {arch}")
    print(f"输出目录: {dist_path}")
    
    if system == 'Darwin':
        print("\n在macOS上运行前，请确保：")
        print("1. 已安装开发者证书")
        print("2. 已授予应用必要的权限")
    elif system == 'Windows':
        print("\n在Windows上运行前，请确保：")
        print("1. 已安装所需的Visual C++ Runtime")
        print("2. 以管理员身份运行（如需要）")

print_build_info() 