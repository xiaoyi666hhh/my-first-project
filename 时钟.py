import tkinter as tk
from tkinter import ttk, messagebox
import time
import datetime

class CuteTimeTool:
    def __init__(self, root):
        self.root = root
        self.root.title("可爱时间工具")
        self.root.geometry("600x400")
        self.root.resizable(True, True)
        
        # 设置中文字体支持
        self.font_families = ["SimHei", "Microsoft YaHei", "Arial", "Comic Sans MS"]
        self.current_font = self.font_families[0]
        
        # 样式设置
        self.style_options = {
            "可爱风格": {"bg": "#FFF0F5", "fg": "#FF69B4", "btn_bg": "#FFB6C1"},
            "简约风格": {"bg": "#F0F0F0", "fg": "#333333", "btn_bg": "#DDDDDD"},
            "清新风格": {"bg": "#E6F7FF", "fg": "#1890FF", "btn_bg": "#B3D1FF"},
            "活力风格": {"bg": "#FFFACD", "fg": "#FFA500", "btn_bg": "#FFD700"}
        }
        self.current_style = "可爱风格"
        
        # 功能状态
        self.mode = "clock"  # clock, stopwatch, countdown
        self.stopwatch_running = False
        self.stopwatch_start_time = 0
        self.stopwatch_elapsed = 0
        self.countdown_time = 0  # 以秒为单位
        self.countdown_running = False
        self.countdown_end_time = 0
        
        # 创建界面
        self.create_widgets()
        
        # 启动时钟更新
        self.update_clock()
    
    def create_widgets(self):
        # 顶部样式选择器
        self.style_frame = tk.Frame(self.root, bg=self.style_options[self.current_style]["bg"])
        self.style_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(self.style_frame, text="选择样式:", bg=self.style_options[self.current_style]["bg"], 
                fg=self.style_options[self.current_style]["fg"]).pack(side=tk.LEFT, padx=5)
        
        self.style_var = tk.StringVar(value=self.current_style)
        self.style_menu = ttk.Combobox(self.style_frame, textvariable=self.style_var, 
                                      values=list(self.style_options.keys()), 
                                      width=15, state="readonly")
        self.style_menu.pack(side=tk.LEFT, padx=5)
        self.style_menu.bind("<<ComboboxSelected>>", lambda e: self.change_style())
        
        # 功能切换按钮
        self.button_frame = tk.Frame(self.root, bg=self.style_options[self.current_style]["bg"])
        self.button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.clock_btn = tk.Button(self.button_frame, text="时钟", command=self.switch_to_clock,
                                  bg=self.style_options[self.current_style]["btn_bg"],
                                  fg=self.style_options[self.current_style]["fg"],
                                  font=(self.current_font, 12, "bold"), relief=tk.RAISED)
        self.clock_btn.pack(side=tk.LEFT, padx=5, pady=5, expand=True, fill=tk.X)
        
        self.stopwatch_btn = tk.Button(self.button_frame, text="秒表", command=self.switch_to_stopwatch,
                                      bg=self.style_options[self.current_style]["btn_bg"],
                                      fg=self.style_options[self.current_style]["fg"],
                                      font=(self.current_font, 12), relief=tk.FLAT)
        self.stopwatch_btn.pack(side=tk.LEFT, padx=5, pady=5, expand=True, fill=tk.X)
        
        self.countdown_btn = tk.Button(self.button_frame, text="倒计时", command=self.switch_to_countdown,
                                      bg=self.style_options[self.current_style]["btn_bg"],
                                      fg=self.style_options[self.current_style]["fg"],
                                      font=(self.current_font, 12), relief=tk.FLAT)
        self.countdown_btn.pack(side=tk.LEFT, padx=5, pady=5, expand=True, fill=tk.X)
        
        # 时间显示区域
        self.display_frame = tk.Frame(self.root, bg=self.style_options[self.current_style]["bg"],
                                     height=200)
        self.display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.time_display = tk.Label(self.display_frame, text="00:00:00",
                                    font=(self.current_font, 48, "bold"),
                                    bg=self.style_options[self.current_style]["bg"],
                                    fg=self.style_options[self.current_style]["fg"])
        self.time_display.pack(expand=True)
        
        # 操作按钮区域
        self.controls_frame = tk.Frame(self.root, bg=self.style_options[self.current_style]["bg"])
        self.controls_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # 秒表和倒计时的控制按钮
        self.start_btn = tk.Button(self.controls_frame, text="开始", command=self.start,
                                  bg=self.style_options[self.current_style]["btn_bg"],
                                  fg=self.style_options[self.current_style]["fg"],
                                  font=(self.current_font, 12))
        
        self.stop_btn = tk.Button(self.controls_frame, text="停止", command=self.stop,
                                 bg=self.style_options[self.current_style]["btn_bg"],
                                 fg=self.style_options[self.current_style]["fg"],
                                 font=(self.current_font, 12))
        
        self.reset_btn = tk.Button(self.controls_frame, text="重置", command=self.reset,
                                  bg=self.style_options[self.current_style]["btn_bg"],
                                  fg=self.style_options[self.current_style]["fg"],
                                  font=(self.current_font, 12))
        
        # 倒计时提示
        self.countdown_hint = tk.Label(self.controls_frame, 
                                      text="鼠标滚轮可调整时间 (时/分/秒)",
                                      bg=self.style_options[self.current_style]["bg"],
                                      fg=self.style_options[self.current_style]["fg"],
                                      font=(self.current_font, 10))
        
        # 绑定鼠标滚轮事件
        self.display_frame.bind("<MouseWheel>", self.on_mouse_wheel)  # Windows
        self.display_frame.bind("<Button-4>", self.on_mouse_wheel)    # Linux 滚轮上
        self.display_frame.bind("<Button-5>", self.on_mouse_wheel)    # Linux 滚轮下
        
        # 初始隐藏控制按钮
        self.hide_controls()
    
    def change_style(self):
        """更改界面样式"""
        self.current_style = self.style_var.get()
        style = self.style_options[self.current_style]
        
        # 更新所有框架背景
        for widget in [self.root, self.display_frame, self.controls_frame, 
                      self.button_frame, self.style_frame]:
            widget.configure(bg=style["bg"])
        
        # 更新所有标签
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Label):
                widget.configure(bg=style["bg"], fg=style["fg"])
        
        # 更新所有按钮
        for btn in [self.clock_btn, self.stopwatch_btn, self.countdown_btn,
                   self.start_btn, self.stop_btn, self.reset_btn]:
            btn.configure(bg=style["btn_bg"], fg=style["fg"])
        
        # 更新时间显示
        self.time_display.configure(bg=style["bg"], fg=style["fg"])
    
    def switch_to_clock(self):
        """切换到时钟模式"""
        self.mode = "clock"
        self.update_button_states()
        self.hide_controls()
    
    def switch_to_stopwatch(self):
        """切换到秒表模式"""
        self.mode = "stopwatch"
        self.update_button_states()
        self.show_controls()
        self.update_stopwatch_display()
    
    def switch_to_countdown(self):
        """切换到倒计时模式"""
        self.mode = "countdown"
        self.update_button_states()
        self.show_controls()
        self.update_countdown_display()
    
    def update_button_states(self):
        """更新按钮状态"""
        # 重置所有按钮样式
        for btn in [self.clock_btn, self.stopwatch_btn, self.countdown_btn]:
            btn.configure(relief=tk.FLAT, font=(self.current_font, 12))
        
        # 设置当前模式按钮样式
        if self.mode == "clock":
            self.clock_btn.configure(relief=tk.RAISED, font=(self.current_font, 12, "bold"))
        elif self.mode == "stopwatch":
            self.stopwatch_btn.configure(relief=tk.RAISED, font=(self.current_font, 12, "bold"))
        elif self.mode == "countdown":
            self.countdown_btn.configure(relief=tk.RAISED, font=(self.current_font, 12, "bold"))
    
    def show_controls(self):
        """显示控制按钮"""
        for btn in [self.start_btn, self.stop_btn, self.reset_btn]:
            btn.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        if self.mode == "countdown":
            self.countdown_hint.pack(side=tk.BOTTOM, pady=5)
        else:
            self.countdown_hint.pack_forget()
    
    def hide_controls(self):
        """隐藏控制按钮"""
        for btn in [self.start_btn, self.stop_btn, self.reset_btn]:
            btn.pack_forget()
        self.countdown_hint.pack_forget()
    
    def start(self):
        """开始计时（秒表或倒计时）"""
        if self.mode == "stopwatch" and not self.stopwatch_running:
            self.stopwatch_running = True
            self.stopwatch_start_time = time.time() - self.stopwatch_elapsed
        elif self.mode == "countdown" and not self.countdown_running and self.countdown_time > 0:
            self.countdown_running = True
            self.countdown_end_time = time.time() + self.countdown_time
    
    def stop(self):
        """停止计时（秒表或倒计时）"""
        if self.mode == "stopwatch" and self.stopwatch_running:
            self.stopwatch_running = False
            self.stopwatch_elapsed = time.time() - self.stopwatch_start_time
        elif self.mode == "countdown" and self.countdown_running:
            self.countdown_running = False
            self.countdown_time = int(self.countdown_end_time - time.time())
            self.update_countdown_display()
    
    def reset(self):
        """重置计时（秒表或倒计时）"""
        if self.mode == "stopwatch":
            self.stopwatch_running = False
            self.stopwatch_elapsed = 0
            self.update_stopwatch_display()
        elif self.mode == "countdown":
            self.countdown_running = False
            self.countdown_time = 0
            self.update_countdown_display()
    
    def on_mouse_wheel(self, event):
        """处理鼠标滚轮事件，用于调整倒计时时间"""
        if self.mode != "countdown" or self.countdown_running:
            return
        
        # 确定滚轮方向 (Windows/Linux)
        delta = 1 if (event.delta > 0 if hasattr(event, 'delta') else event.num == 4) else -1
        
        # 获取鼠标位置，确定调整时、分还是秒
        x = event.x
        display_width = self.display_frame.winfo_width()
        
        # 三等分区域，分别对应时、分、秒
        if x < display_width / 3:
            # 调整小时
            self.countdown_time += delta * 3600
        elif x < display_width * 2 / 3:
            # 调整分钟
            self.countdown_time += delta * 60
        else:
            # 调整秒钟
            self.countdown_time += delta
        
        # 确保时间不为负数
        if self.countdown_time < 0:
            self.countdown_time = 0
        
        self.update_countdown_display()
    
    def update_clock(self):
        """更新时钟显示"""
        if self.mode == "clock":
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            self.time_display.config(text=current_time)
        
        elif self.mode == "stopwatch" and self.stopwatch_running:
            self.stopwatch_elapsed = time.time() - self.stopwatch_start_time
            self.update_stopwatch_display()
        
        elif self.mode == "countdown" and self.countdown_running:
            remaining = int(self.countdown_end_time - time.time())
            if remaining <= 0:
                self.countdown_running = False
                self.countdown_time = 0
                self.update_countdown_display()
                # 倒计时结束提醒
                self.time_display.config(text="时间到!")
                messagebox.showinfo("倒计时结束", "设定的时间已经到啦!")
            else:
                self.countdown_time = remaining
                self.update_countdown_display()
        
        # 每100毫秒更新一次（0.1秒）
        self.root.after(100, self.update_clock)
    
    def update_stopwatch_display(self):
        """更新秒表显示"""
        hours = int(self.stopwatch_elapsed // 3600)
        minutes = int((self.stopwatch_elapsed % 3600) // 60)
        seconds = int(self.stopwatch_elapsed % 60)
        milliseconds = int((self.stopwatch_elapsed % 1) * 100)
        self.time_display.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:02d}")
    
    def update_countdown_display(self):
        """更新倒计时显示"""
        hours = int(self.countdown_time // 3600)
        minutes = int((self.countdown_time % 3600) // 60)
        seconds = int(self.countdown_time % 60)
        self.time_display.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CuteTimeTool(root)
    root.mainloop()
