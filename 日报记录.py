import tkinter as tk
from tkinter import ttk, messagebox
import csv
from datetime import datetime
import os

class DailyLoggerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("蓝队防护日报记录系统")
        self.root.geometry("880x780")
        self.root.configure(bg="#000000")

        self.colors = {
            'bg_main': '#000000',
            'panel_bg': '#111111',
            'text_primary': '#00ffff',
            'text_secondary': '#00ff99',
            'text_dim': '#cccccc',
            'highlight': '#00ff00',
            'danger': '#ff0033',
            'button_bg': '#1f2a44',
            'button_text': '#00ff00',
            'input_bg': '#1f2a44'
        }

        self.entries = {}
        self.setup_styles()
        self.build_layout()
        self.update_time()

    def setup_styles(self):
        s = ttk.Style()
        s.configure("TFrame", background=self.colors['bg_main'])
        s.configure("Panel.TFrame", background=self.colors['panel_bg'])
        s.configure("Title.TLabel", font=('微软雅黑', 20, 'bold'),
                    background=self.colors['bg_main'], foreground=self.colors['text_primary'])
        s.configure("Sub.TLabel", font=('微软雅黑', 13),
                    background=self.colors['bg_main'], foreground=self.colors['highlight'])
        s.configure("Info.TLabel", font=('微软雅黑', 12, 'bold'),
                    background=self.colors['panel_bg'], foreground=self.colors['text_dim'])
        s.configure("Value.TLabel", font=('微软雅黑', 13, 'bold'),
                    background=self.colors['panel_bg'], foreground=self.colors['highlight'])
        s.configure("Status.TLabel", font=('微软雅黑', 10),
                    background=self.colors['bg_main'], foreground=self.colors['text_secondary'])
        
        # 创建自定义按钮样式
        s.configure("Custom.TButton",
                    font=('微软雅黑', 11, 'bold'),
                    padding=8)
        # 设置按钮样式映射
        s.map("Custom.TButton",
              background=[('!active', self.colors['button_bg']), ('active', self.colors['highlight'])],
              foreground=[('!active', self.colors['button_text']), ('active', '#000000')])

    def build_layout(self):
        header = ttk.Frame(self.root)
        header.pack(pady=(10, 0))
        ttk.Label(header, text="蓝队防护日报记录系统", style="Title.TLabel").pack()
        ttk.Label(header, text="SAFETY FIRST · 护网值守 · 日志归档", style="Sub.TLabel").pack(pady=(0, 10))

        info_panel = ttk.Frame(self.root, style="Panel.TFrame", padding=15)
        info_panel.pack(fill='x', padx=20, pady=10)

        self.time_label = self._info_row(info_panel, "当前时间", "--:--:--")
        self.status_label = self._info_row(info_panel, "系统状态", "系统就绪")

        input_panel = ttk.Frame(self.root, style="Panel.TFrame", padding=15)
        input_panel.pack(fill='x', padx=20, pady=10)

        self._add_input(input_panel, "事件名称", "扫描")
        self._add_input(input_panel, "攻击IP")
        self._add_input(input_panel, "受害IP")
        self._add_input(input_panel, "处置建议", "封禁", field_type='text')
        self._add_input(input_panel, "备注", "", field_type='text')

        button_frame = ttk.Frame(self.root, style="TFrame")
        button_frame.pack(pady=15)

        ttk.Button(button_frame, text="保存记录 [Ctrl+S]", command=self.save_record, style="Custom.TButton").pack(side='left', padx=20)
        ttk.Button(button_frame, text="清空内容 [Ctrl+R]", command=self.clear_fields, style="Custom.TButton").pack(side='left', padx=20)

        self.status_var = tk.StringVar(value="系统就绪")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, style="Status.TLabel", anchor='w')
        status_bar.pack(fill='x', padx=20, pady=(10, 0))

        self.root.bind("<Control-s>", lambda e: self.save_record())
        self.root.bind("<Control-r>", lambda e: self.clear_fields())

    def _info_row(self, parent, label, value):
        frame = ttk.Frame(parent, style="Panel.TFrame")
        frame.pack(anchor='w', pady=5)
        ttk.Label(frame, text=label + "：", style="Info.TLabel").pack(side='left')
        val_label = ttk.Label(frame, text=value, style="Value.TLabel")
        val_label.pack(side='left')
        return val_label

    def _add_input(self, parent, label, default="", field_type='entry'):
        frame = ttk.Frame(parent, style="Panel.TFrame")
        frame.pack(fill='x', pady=5)
        ttk.Label(frame, text=label + "：", style="Info.TLabel").pack(anchor='w')
        if field_type == 'entry':
            e = tk.Entry(frame, font=('微软雅黑', 12), bg=self.colors['input_bg'],
                         fg=self.colors['text_dim'], insertbackground=self.colors['highlight'])
            e.insert(0, default)
            e.pack(fill='x', padx=5)
        else:
            e = tk.Text(frame, font=('微软雅黑', 12), height=3, bg=self.colors['input_bg'],
                        fg=self.colors['text_dim'], insertbackground=self.colors['highlight'])
            e.insert("1.0", default)
            e.pack(fill='x', padx=5)
        self.entries[label] = e

    def update_time(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 显示年月日+时分秒
        self.time_label.config(text=now)
        self.root.after(1000, self.update_time)

    def get_field_value(self, label, is_text=False):
        widget = self.entries[label]
        if is_text:
            return widget.get("1.0", tk.END).strip()
        else:
            return widget.get().strip()

    def save_record(self):
        try:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            event = self.get_field_value("事件名称") or "扫描"
            ip = self.get_field_value("攻击IP")
            victim_ip = self.get_field_value("受害IP")
            suggestion = self.get_field_value("处置建议", is_text=True) or "封禁"
            remarks = self.get_field_value("备注", is_text=True)

            if not ip:
                messagebox.showerror("错误", "攻击IP为必填项")
                self.status_var.set("错误：攻击IP不能为空")
                return

            os.makedirs("records", exist_ok=True)
            date_str = datetime.now().strftime("%Y-%m-%d")
            filename = f"records/日报记录.csv"
            write_header = not os.path.exists(filename)

            with open(filename, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                if write_header:
                    writer.writerow(["记录时间", "事件名称", "攻击IP", "受害IP", "处置建议", "备注"])
                writer.writerow([current_time, event, ip, victim_ip, suggestion, remarks])

            messagebox.showinfo("成功", "记录已保存")
            self.status_var.set(f"记录已保存 - {current_time}")
            self.clear_fields(keep_event=True)
        except Exception as e:
            messagebox.showerror("错误", f"保存失败: {str(e)}")
            self.status_var.set(f"保存失败: {str(e)}")

    def clear_fields(self, keep_event=False):
        for key, widget in self.entries.items():
            if isinstance(widget, tk.Entry):
                if key == "事件名称" and keep_event:
                    continue
                widget.delete(0, tk.END)
            elif isinstance(widget, tk.Text):
                widget.delete("1.0", tk.END)
        self.entries["事件名称"].insert(0, "扫描")
        self.entries["处置建议"].insert("1.0", "封禁")
        self.status_var.set("所有字段已清空")

if __name__ == "__main__":
    root = tk.Tk()
    app = DailyLoggerApp(root)
    root.mainloop()
