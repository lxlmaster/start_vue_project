import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
import re
from pathlib import Path
from semver import Version

class NodeVersionSelector:
    def __init__(self, root):
        self.root = root
        self.root.title("Node版本切换器")
        self.root.geometry("400x300")
        
        self.nvm_path = Path(os.environ.get('NVM_HOME', ''))
        self.current_version = self.get_current_version()
        self.available_versions = self.get_available_versions()
        
        self.create_widgets()
        
    def create_widgets(self):
        # 当前版本显示
        current_frame = ttk.Frame(self.root)
        current_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(current_frame, text="当前Node版本:").pack(side='left')
        ttk.Label(current_frame, text=self.current_version).pack(side='left', padx=(5, 0))
        
        # 可用版本列表
        list_frame = ttk.Frame(self.root)
        list_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        ttk.Label(list_frame, text="可用的Node版本:").pack(anchor='w')
        
        # 创建列表和滚动条
        self.version_list = ttk.Treeview(list_frame, columns=("版本",), show="headings")
        self.version_list.heading("版本", text="版本号")
        
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.version_list.yview)
        self.version_list.configure(yscrollcommand=scrollbar.set)
        
        self.version_list.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # 按钮
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(fill='x', padx=5, pady=5)
        
        switch_btn = ttk.Button(btn_frame, text="切换版本", command=self.switch_version)
        switch_btn.pack(side='left', padx=(0, 5))
        
        refresh_btn = ttk.Button(btn_frame, text="刷新列表", command=self.refresh_versions)
        refresh_btn.pack(side='left')
        
        # 填充版本列表
        self.refresh_versions()
        
    def get_current_version(self):
        try:
            result = subprocess.run('node -v', shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
            return "未检测到Node"
        except Exception:
            return "未检测到Node"
            
    def get_available_versions(self):
        versions = []
        if self.nvm_path.exists():
            for path in self.nvm_path.iterdir():
                if path.is_dir() and re.match(r'v\d+\.\d+\.\d+', path.name):
                    versions.append(path.name)
        return sorted(versions, reverse=True)
        
    def switch_version(self):
        selected_items = self.version_list.selection()
        if not selected_items:
            messagebox.showerror("错误", "请选择要切换的Node版本")
            return
            
        version = self.version_list.item(selected_items[0])["values"][0]
        try:
            subprocess.run(f'nvm use {version}', shell=True, check=True)
            messagebox.showinfo("成功", f"已切换到Node {version}")
            self.current_version = version
            self.refresh_versions()
        except subprocess.CalledProcessError:
            messagebox.showerror("错误", "切换版本失败")
            
    def refresh_versions(self):
        # 清空列表
        for item in self.version_list.get_children():
            self.version_list.delete(item)
            
        # 重新获取版本信息
        self.current_version = self.get_current_version()
        self.available_versions = self.get_available_versions()
        
        # 填充列表
        for version in self.available_versions:
            self.version_list.insert("", "end", values=(version,))

class NodeVersionManager:
    def __init__(self):
        self.nvm_path = os.environ.get('NVM_HOME')
        if not self.nvm_path:
            # 默认 NVM 安装路径
            self.nvm_path = str(Path.home() / "AppData" / "Roaming" / "nvm")
    
    def get_installed_versions(self):
        """获取已安装的 Node.js 版本列表"""
        versions = []
        if os.path.exists(self.nvm_path):
            for item in os.listdir(self.nvm_path):
                if item.startswith('v'):
                    versions.append(item)
        return sorted(versions, reverse=True)
    
    def switch_version(self, version):
        """切换 Node.js 版本"""
        try:
            subprocess.run(['nvm', 'use', version], shell=True, check=True)
            return True
        except subprocess.CalledProcessError:
            return False
    
    def get_current_version(self):
        """获取当前使用的 Node.js 版本"""
        try:
            result = subprocess.run(['node', '-v'], 
                                 capture_output=True, 
                                 text=True, 
                                 shell=True)
            return result.stdout.strip()
        except:
            return None

def get_recommended_node_version():
    # uni-app推荐使用Node.js 14.x或更高版本
    return "14.19.0"

def check_node_compatibility():
    current_version = subprocess.check_output(['node', '--version']).decode().strip()
    recommended = get_recommended_node_version()
    
    if Version(current_version.replace('v', '')) < Version(recommended):
        print(f"警告：当前Node.js版本 {current_version} 可能不完全兼容")
        print(f"建议使用 {recommended} 或更高版本")
        return False
    return True

def main():
    root = tk.Tk()
    app = NodeVersionSelector(root)
    root.mainloop()

if __name__ == "__main__":
    main() 