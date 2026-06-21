import tkinter as tk
from tkinter import messagebox


def on_button_click():
    name = entry_name.get().strip()
    if name:
        messagebox.showinfo("歡迎", f"你好，{name}！歡迎使用 Tkinter！")
    else:
        messagebox.showwarning("提醒", "請輸入你的名字")


# 建立主視窗
root = tk.Tk()
root.title("Tkinter 簡單範例")
root.geometry("400x250")
root.resizable(False, False)

# 標題標籤
label_title = tk.Label(root, text="Tkinter 入門範例", font=("Arial", 18, "bold"))
label_title.pack(pady=20)

# 輸入框區域
frame_input = tk.Frame(root)
frame_input.pack(pady=10)

label_name = tk.Label(frame_input, text="請輸入名字：", font=("Arial", 12))
label_name.pack(side=tk.LEFT, padx=5)

entry_name = tk.Entry(frame_input, font=("Arial", 12), width=15)
entry_name.pack(side=tk.LEFT, padx=5)

# 按鈕
btn_submit = tk.Button(root, text="打招呼", font=("Arial", 12), command=on_button_click)
btn_submit.pack(pady=20)

# 啟動主迴圈
root.mainloop()
