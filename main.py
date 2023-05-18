import hashlib
from PIL import Image, ImageDraw
import tkinter as tk
from tkinter import filedialog
import webbrowser

VERSION = "1.0"
AUTHOR = "AZ Studio"

def hash_string(input_string):
    return hashlib.md5(input_string.encode("utf-8")).hexdigest()


def create_identicon(hash_string, file_name):
    size = 5
    cell_size = 50
    img_size = size * cell_size

    img = Image.new("RGB", (img_size, img_size), color="white")
    draw = ImageDraw.Draw(img)

    colors = (int(hash_string[0:2], 16), int(hash_string[2:4], 16), int(hash_string[4:6], 16))

    for y in range(size):
        for x in range(size):
            if (x < size // 2) and (int(hash_string[y*size + x], 16) % 2 == 0):
                draw.rectangle([x * cell_size, y * cell_size, (x + 1) * cell_size - 1, (y + 1) * cell_size - 1], fill=colors)
                draw.rectangle([(size - x - 1) * cell_size, y * cell_size, (size - x) * cell_size - 1, (y + 1) * cell_size - 1], fill=colors)

    img.save(file_name)


class IdenticonGenerator(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Identicon头像生成器  V"+VERSION+"  By "+AUTHOR)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.input_label = tk.Label(self, text="请输入您的昵称：")
        self.input_label.grid(row=0, column=0, sticky='w', padx=10, pady=10)

        self.input_entry = tk.Entry(self)
        self.input_entry.grid(row=0, column=1, padx=10, pady=10)

        self.file_label = tk.Label(self, text="请选择保存的文件路径及名称：")
        self.file_label.grid(row=1, column=0, sticky='w', padx=10, pady=10)

        self.file_entry = tk.Entry(self)
        self.file_entry.grid(row=1, column=1, padx=10, pady=10)

        self.browse_button = tk.Button(self, text="浏览", command=self.browse_file)
        self.browse_button.grid(row=1, column=2, padx=10, pady=10)

        self.generate_button = tk.Button(self, text="生成 Identicon", command=self.generate_identicon)
        self.generate_button.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        self.quit_button = tk.Button(self, text="退出", command=self.master.destroy)
        self.quit_button.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

        self.version_label = tk.Label(self, text=f"Version: {VERSION}")
        self.version_label.grid(row=4, column=0, sticky='w', padx=10, pady=10)

        self.author_label = tk.Label(self, text=f"By {AUTHOR}     ", cursor='hand2')
        self.author_label.grid(row=4, column=2, sticky='e', padx=10, pady=10)
        self.author_label.bind("<Button-1>", self.open_github)

    def browse_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png")
        if file_path:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, file_path)

    def generate_identicon(self):
        input_string = self.input_entry.get()
        file_name = self.file_entry.get()

        if not file_name.endswith(".png"):
            file_name += ".png"

        hash_value = hash_string(input_string)
        create_identicon(hash_value, file_name)

        tk.messagebox.showinfo("生成成功", "Identicon头像已生成！")

    def open_github(self, event):
        webbrowser.open_new("https://github.com/AZ-Studio-2023")


def main():
    root = tk.Tk()
    root.iconbitmap("icon.ico")
    app = IdenticonGenerator(master=root)
    app.mainloop()


if __name__ == "__main__":
    main()
