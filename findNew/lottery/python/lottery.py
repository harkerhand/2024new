import os
from wordcloud import WordCloud
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import random
import json

class LotteryApp:
    def __init__(self, master):

        def load_students_from_json(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
            
        self.students = load_students_from_json(os.path.join(os.path.dirname(__file__), 'assets/students.json'))
        
        self.master = master
        master.title("I++ 迎新抽奖系统")

        # 添加大标题
        self.title_frame = tk.Frame(master)
        self.title_frame.pack(side=tk.TOP, fill=tk.X, pady=10)

        self.title_label = tk.Label(self.title_frame, text="I++ 迎新抽奖系统", font=("微软雅黑", 24))
        self.title_label.pack() 


        # 使用 ttk 样式
        style = ttk.Style()
        style.theme_use('clam')  # 使用扁平化的主题
        style.configure('TFrame', background='#F0F0F0')
        style.configure('TLabel', background='#F0F0F0', font=("微软雅黑", 12))
        style.configure('TButton', font=("微软雅黑", 12))

        # 创建三个模块
        self.create_student_list(master)
        self.create_logo_and_button(master)
        self.create_result_display(master)

    def create_student_list(self, master):
        self.wordcloud_frame = ttk.Frame(master, style='TFrame')
        self.wordcloud_frame.pack(side=tk.LEFT, padx=10, pady=10, expand=True, fill=tk.BOTH)

        # 生成词云
        names = " ".join(student['name'] for student in self.students)
        wordcloud = WordCloud(
            width=400, 
            height=400, 
            background_color='#F0F0F0',
            font_path='msyh.ttc',
            max_font_size=40,
            min_font_size=10
        ).generate(names)

        # 将词云转换为图像
        image = wordcloud.to_image()
        self.wordcloud_image = ImageTk.PhotoImage(image)

        # 显示词云图像
        self.wordcloud_label = ttk.Label(self.wordcloud_frame, image=self.wordcloud_image)
        self.wordcloud_label.pack(expand=True, fill=tk.BOTH)

    def create_logo_and_button(self, master):
        self.logo_input_frame = tk.Frame(master)
        self.logo_input_frame.pack(side=tk.LEFT, padx=10, pady=10, expand=True, fill=tk.BOTH)

        # 引入logo图片，使用相对路径
        logo_path = os.path.join(os.path.dirname(__file__), "imgs/logo.png")
        self.logo_image = Image.open(logo_path)
        self.logo_image = self.logo_image.resize((200, 200), Image.LANCZOS)
        self.logo_photo = ImageTk.PhotoImage(self.logo_image)

        self.logo_label = tk.Label(self.logo_input_frame, image=self.logo_photo)
        self.logo_label.pack(pady=20)

        # 添加输入框和按钮
        self.num_label = ttk.Label(self.logo_input_frame, text="输入抽奖人数：")
        self.num_label.pack(pady=5)

        self.num_entry = ttk.Entry(self.logo_input_frame)
        self.num_entry.pack(pady=5)

        self.start_button = ttk.Button(self.logo_input_frame, text="开始抽奖", command=self.start_lottery)
        self.start_button.pack(pady=20)

    def create_result_display(self, master):
        self.result_frame = tk.Frame(master)
        self.result_frame.pack(side=tk.LEFT, padx=10, pady=10, expand=True, fill=tk.BOTH)

        self.result_label = tk.Label(self.result_frame, text="抽奖结果:", font=("微软雅黑", 16))
        self.result_label.pack(pady=10)

        self.result_display = tk.Frame(self.result_frame)
        self.result_display.pack(pady=10)

    def start_lottery(self):
        number_of_winners = self.get_number_of_winners()
        if number_of_winners <= 0:
            self.show_result(["请输入有效的抽奖人数！"])
            return
        
        winners = random.sample(self.students, min(number_of_winners, len(self.students)))
        winner_names = [f"{winner['studentNumber']}-{winner['name']}" for winner in winners]
        self.show_result(winner_names)

    def show_result(self, results):
        for widget in self.result_display.winfo_children():
            widget.destroy()
        
        for i, result in enumerate(results):
            label = tk.Label(self.result_display, text=result, font=("微软雅黑", 12), anchor="w")
            label.grid(row=i // 2, column=i % 2, padx=10, pady=5, sticky="w")

    def get_number_of_winners(self):
        try:
            return int(self.num_entry.get())
        except ValueError:
            return 0

if __name__ == "__main__":
    root = tk.Tk()
    root.minsize(900, 0)
    app = LotteryApp(root)
    root.mainloop()
