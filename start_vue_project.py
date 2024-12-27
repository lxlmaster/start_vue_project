import tkinter as tk
from tkinter import messagebox, filedialog
import ttkbootstrap as ttk
from ttkbootstrap.constants import *  # 导入常量
from ttkbootstrap.scrolled import ScrolledFrame
import json
import subprocess
import os
from pathlib import Path
from node_version_selector import NodeVersionManager

class VueProjectLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("Vue项目启动器")
        self.root.geometry("900x650")
        
        # 使用更柔和的主题
        self.style = ttk.Style(theme="litera")  # litera主题更接近Element UI的风格
        
        # 自定义样式，模仿Element UI
        self.style.configure('Element.TLabelframe', 
                            borderwidth=1,
                            relief="solid",
                            bordercolor="#DCDFE6")  # Element UI的边框颜色
        
        self.style.configure('Element.TButton',
                            font=('Arial', 10),
                            borderwidth=1,
                            background="#409EFF",  # Element UI的主题蓝
                            foreground="white")
        
        # 设置窗口背景色为Element UI的背景色
        self.root.configure(background="#F5F7FA")
        
        # 初始化其他组件
        self.node_manager = NodeVersionManager()
        self.config_file = Path.home() / '.vue_projects.json'
        self.projects = self.load_projects()
        
        self.create_widgets()
        
    def create_widgets(self):
        # 主容器
        main_container = ScrolledFrame(self.root, autohide=True, bootstyle="light")
        main_container.pack(fill=BOTH, expand=YES, padx=20, pady=20)
        
        # 项目信息卡片
        info_card = ttk.LabelFrame(main_container, 
                                  text="项目信息", 
                                  padding=15,
                                  style='Element.TLabelframe')
        info_card.pack(fill=X, padx=5, pady=5)
        
        # 路径选择区域
        path_frame = ttk.Frame(info_card)
        path_frame.pack(fill=X, pady=10)
        
        ttk.Label(path_frame, 
                 text="项目路径", 
                 font=("Arial", 10)).pack(side=LEFT)
        
        self.path_var = tk.StringVar()
        path_entry = ttk.Entry(path_frame, 
                              textvariable=self.path_var,
                              width=50,
                              bootstyle="light")  # 使用浅色样式
        path_entry.pack(side=LEFT, fill=X, expand=YES, padx=10)
        
        browse_btn = ttk.Button(path_frame, 
                              text="浏览", 
                              command=self.browse_path,
                              style="info-outline",  # 使用描边按钮
                              width=8)
        browse_btn.pack(side=LEFT)
        
        # 选项区域
        options_frame = ttk.Frame(info_card)
        options_frame.pack(fill=X, pady=15)
        
        # 包管理器选择
        pkg_frame = ttk.LabelFrame(options_frame, 
                                 text="包管理器", 
                                 padding=15,
                                 style='Element.TLabelframe')
        pkg_frame.pack(side=LEFT, padx=(0, 20))
        
        self.pkg_var = tk.StringVar(value="npm")
        for pkg in ["npm", "pnpm", "yarn"]:
            ttk.Radiobutton(pkg_frame, 
                           text=pkg, 
                           variable=self.pkg_var,
                           value=pkg, 
                           bootstyle="info-toolbutton").pack(side=LEFT, padx=10)
        
        # Node版本选择
        node_frame = ttk.LabelFrame(options_frame, 
                                  text="Node版本", 
                                  padding=15,
                                  style='Element.TLabelframe')
        node_frame.pack(side=LEFT)
        
        self.node_var = tk.StringVar()
        node_versions = self.node_manager.get_installed_versions()
        current_version = self.node_manager.get_current_version()
        
        node_combo = ttk.Combobox(node_frame, 
                                textvariable=self.node_var,
                                values=node_versions, 
                                width=15,
                                state="readonly",
                                bootstyle="light")
        if current_version:
            self.node_var.set(current_version)
        node_combo.pack(side=LEFT, padx=5)
        
        # 添加项目按钮
        ttk.Button(options_frame, 
                  text="添加到列表", 
                  command=self.add_project,
                  style="primary",  # 使用主要按钮样式
                  width=10).pack(side=RIGHT, padx=5)
        
        # 项目列表区域
        list_card = ttk.LabelFrame(main_container, 
                                 text="项目列表", 
                                 padding=15,
                                 style='Element.TLabelframe')
        list_card.pack(fill=BOTH, expand=YES, pady=15)
        
        # 创建树形视图
        columns = ("路径", "包管理器", "Node版本")
        self.project_tree = ttk.Treeview(list_card, 
                                       columns=columns,
                                       show="headings", 
                                       bootstyle="light",
                                       height=8)
        
        # 设置列
        for col in columns:
            self.project_tree.heading(col, text=col)
            
        self.project_tree.column("路径", width=450)
        self.project_tree.column("包管理器", width=100)
        self.project_tree.column("Node版本", width=100)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(list_card, 
                                orient=VERTICAL,
                                command=self.project_tree.yview,
                                bootstyle="light-round")
        self.project_tree.configure(yscrollcommand=scrollbar.set)
        
        self.project_tree.pack(side=LEFT, fill=BOTH, expand=YES, padx=(0, 10))
        scrollbar.pack(side=RIGHT, fill=Y)
        
        # 底部按钮区域
        btn_frame = ttk.Frame(main_container)
        btn_frame.pack(fill=X, pady=15)
        
        ttk.Button(btn_frame, 
                  text="启动项目",
                  command=lambda: self.start_project(self.project_tree),
                  style="success-outline",  # 使用描边样式
                  width=10).pack(side=RIGHT, padx=5)
        
        ttk.Button(btn_frame, 
                  text="删除项目",
                  command=lambda: self.delete_project(self.project_tree),
                  style="danger-outline",  # 使用描边样式
                  width=10).pack(side=RIGHT, padx=5)
        
        # 刷新项目列表
        self.refresh_project_list()

    def add_project(self):
        path = self.path_var.get().strip()
        if not path:
            messagebox.showerror("错误", "请选择项目路径")
            return
            
        pkg_manager = self.pkg_var.get()
        
        # 查是否已存在
        for project in self.projects:
            if project["path"] == path:
                messagebox.showerror("错误", "该项目已在列表中")
                return
                
        self.projects.append({
            "path": path,
            "package_manager": pkg_manager,
            "node_version": self.node_var.get()
        })
        
        self.save_projects()
        self.refresh_project_list()
        
    def start_project(self, tree):
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("错误", "请选择要启动的项目")
            return
            
        values = tree.item(selected_item[0])["values"]
        path = values[0]
        pkg_manager = values[1]
        node_version = values[2]
        
        try:
            # 切换到项目指定的 Node.js 版本
            if not self.node_manager.switch_version(node_version):
                messagebox.showerror("错误", f"切换 Node.js 版本失败: {node_version}")
                return
                
            # 直接使用 Vue 的启动命令
            cmd = f"{pkg_manager} run dev"
            subprocess.Popen(f'start cmd /k "{cmd}"', shell=True, cwd=path)
        except Exception as e:
            messagebox.showerror("错误", f"启动项目失败: {str(e)}")
    
    def delete_project(self, tree):
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("错误", "请选择要删除的项目")
            return
            
        path = tree.item(selected_item[0])["values"][0]
        self.projects = [p for p in self.projects if p["path"] != path]
        
        self.save_projects()
        self.refresh_project_list()
        
    def refresh_project_list(self):
        try:
            # 清空列表
            for item in self.project_tree.get_children():
                self.project_tree.delete(item)
            
            # 重新填充列表
            for project in self.projects:
                package_manager = project.get("package_manager", "npm")
                path = project.get("path", "")
                node_version = project.get("node_version", "")
                
                values = (path, package_manager, node_version)
                self.project_tree.insert("", "end", values=values)
        except Exception as e:
            messagebox.showerror("错误", f"刷新项目列表失败: {str(e)}")
    
    def browse_path(self):
        path = filedialog.askdirectory()
        if path:
            self.path_var.set(path)
            
    def load_projects(self):
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    projects = json.load(f)
                    # 确保每个项目都有必要的字段
                    for project in projects:
                        if "package_manager" not in project:
                            project["package_manager"] = "npm"  # 默认使用npm
                    return projects
            except Exception as e:
                messagebox.showwarning("警告", f"加载项目配置失败: {str(e)}\n将使用空配置")
                return []
        return []
        
    def save_projects(self):
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.projects, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    root = ttk.Window(themename="litera")  # 使用更适合的主题
    app = VueProjectLauncher(root)
    root.mainloop()
