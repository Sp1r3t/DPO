from tkinter import *
from tkinter import filedialog, font, colorchooser, messagebox
import os

# Главное окно
root = Tk()
root.title("Текстовый редактор")
root.geometry("1000x600")

# Функции
def new_file():
    global current_file
    text_area.delete(1.0, END)
    current_file = None
    root.title("Текстовый редактор")

def open_file():
    global current_file
    file_path = filedialog.askopenfilename(defaultextension=".txt",
                                           filetypes=[("Text Documents", "*.txt"), ("All Files", "*.*")])
    if file_path:
        current_file = file_path
        root.title(f"{os.path.basename(file_path)} - Текстовый редактор")
        with open(file_path, "r", encoding="utf-8") as file:
            text_area.delete(1.0, END)
            text_area.insert(END, file.read())

def save_file():
    global current_file
    if current_file:
        with open(current_file, "w", encoding="utf-8") as file:
            file.write(text_area.get(1.0, END))
    else:
        save_as()

def save_as():
    global current_file
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text Documents", "*.txt"), ("All Files", "*.*")])
    if file_path:
        current_file = file_path
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(text_area.get(1.0, END))
        root.title(f"{os.path.basename(file_path)} - Текстовый редактор")

def choose_font():
    selected_font = font.askfont(root)
    if selected_font:
        text_area.configure(font=(selected_font['family'], selected_font['size']))

def choose_color():
    color = colorchooser.askcolor()[1]
    if color:
        text_area.configure(fg=color)

def about():
    messagebox.showinfo("О программе", "Текстовый редактор на Python\nАвтор: Толстопятов Тимофей")

# Меню
menu_bar = Menu(root)

# Файл
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Новый", command=new_file)
file_menu.add_command(label="Открыть...", command=open_file)
file_menu.add_command(label="Сохранить", command=save_file)
file_menu.add_command(label="Сохранить как...", command=save_as)
file_menu.add_separator()
file_menu.add_command(label="Выход", command=root.quit)
menu_bar.add_cascade(label="Файл", menu=file_menu)

# Настройки
format_menu = Menu(menu_bar, tearoff=0)
format_menu.add_command(label="Шрифт...", command=choose_font)
format_menu.add_command(label="Цвет текста...", command=choose_color)
menu_bar.add_cascade(label="Формат", menu=format_menu)

# Справка
help_menu = Menu(menu_bar, tearoff=0)
help_menu.add_command(label="О программе", command=about)
menu_bar.add_cascade(label="Справка", menu=help_menu)

root.config(menu=menu_bar)

# Текстовое поле с прокруткой
text_area = Text(root, wrap="word", undo=True)
scroll = Scrollbar(root, command=text_area.yview)
text_area.configure(yscrollcommand=scroll.set)
text_area.pack(fill="both", expand=True, side="left")
scroll.pack(fill="y", side="right")

# Запуск
root.mainloop()