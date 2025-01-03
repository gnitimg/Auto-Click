import tkinter as tk
from tkinter import messagebox
import pyautogui
import time
import threading
import keyboard

class AutoClickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("连点器")
        self.root.geometry("450x350")  # 扩展界面大小
        self.root.resizable(False, False)  # 禁止调整窗口大小

        self.mode = None  # 单点或多点模式
        self.points = []  # 存储选择的点位
        self.click_count = 0  # 连点次数
        self.click_interval = 0.1  # 默认点击间隔时间
        self.running = False  # 是否正在运行
        self.stop_triggered = False  # 用于防止多次弹出提示框

        self.create_widgets()

    def create_widgets(self):
        # 模式选择
        tk.Label(self.root, text="请选择模式:").pack(pady=5)
        tk.Button(self.root, text="单点模式", command=lambda: self.set_mode("single"), cursor="hand2", width=20).pack(pady=5)
        tk.Button(self.root, text="多点模式", command=lambda: self.set_mode("multi"), cursor="hand2", width=20).pack(pady=5)

        # 点位选择提示
        self.point_label = tk.Label(self.root, text="")
        self.point_label.pack(pady=5)

        # 连点次数输入
        tk.Label(self.root, text="请输入连点次数 (0为无限):").pack(pady=5)
        self.count_entry = tk.Entry(self.root, width=25)
        self.count_entry.pack(pady=5)

        # 点击频率输入
        tk.Label(self.root, text="请输入点击间隔时间 (秒):").pack(pady=5)
        self.interval_entry = tk.Entry(self.root, width=25)
        self.interval_entry.pack(pady=5)

        # 开始连点按钮
        self.start_button = tk.Button(self.root, text="开始连点", command=self.start_clicking, state=tk.DISABLED, cursor="hand2", width=20)
        self.start_button.pack(pady=10)

        # 停止提示
        tk.Label(self.root, text="按下 ESC 键可停止连点", fg="gray").pack(pady=5)

    def set_mode(self, mode):
        self.mode = mode
        self.points = []  # 重置点位
        self.point_label.config(text=f"已选择 {mode} 模式，请选择点位")
        self.select_points()

    def select_points(self):
        if self.mode == "single":
            self.select_point("点1")
        elif self.mode == "multi":
            self.select_point("点1")

    def select_point(self, point_name):
        messagebox.showinfo("选择点位", f"请将鼠标移动到 {point_name} 的位置，点击确定后等待1秒选择。")
        time.sleep(1)  # 给用户1秒时间移动鼠标
        point = pyautogui.position()
        confirm = messagebox.askyesno("确认点位", f"已选择 {point_name} 为 {point}，确认吗？")
        if confirm:
            self.points.append(point)
            self.point_label.config(text=f"已选择 {point_name}: {point}")
            if self.mode == "multi" and len(self.points) < 2:
                self.select_point("点2")
            else:
                self.start_button.config(state=tk.NORMAL)  # 启用开始按钮

    def start_clicking(self):
        try:
            self.click_count = int(self.count_entry.get())
            self.click_interval = float(self.interval_entry.get())
            if self.click_interval < 0:
                raise ValueError("点击间隔时间不能为负数")
        except ValueError as e:
            messagebox.showerror("错误", f"请输入有效的数字！\n{str(e)}")
            return

        if not self.points:
            messagebox.showwarning("警告", "请先选择点位！")
            return

        self.running = True
        self.stop_triggered = False  # 重置标志位
        threading.Thread(target=self.run_clicker).start()

    def run_clicker(self):
        # 监听 ESC 键
        keyboard.on_press_key("esc", lambda _: self.stop_clicking())

        if self.mode == "single":
            self.single_point_click()
        elif self.mode == "multi":
            self.multi_point_click()

    def single_point_click(self):
        point = self.points[0]
        count = 0
        while self.running and (self.click_count == 0 or count < self.click_count):
            pyautogui.click(point.x, point.y)
            count += 1
            time.sleep(self.click_interval)  # 使用自定义点击间隔时间
        self.running = False

    def multi_point_click(self):
        count = 0
        while self.running and (self.click_count == 0 or count < self.click_count):
            for point in self.points:
                if not self.running:
                    break
                pyautogui.click(point.x, point.y)
                time.sleep(self.click_interval)  # 使用自定义点击间隔时间
            count += 1
        self.running = False

    def stop_clicking(self):
        if not self.stop_triggered:  # 确保提示框只弹出一次
            self.stop_triggered = True
            self.running = False
            messagebox.showinfo("提示", "连点已停止")

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoClickerApp(root)
    root.mainloop()
