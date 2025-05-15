from tkinter import *
from tkinter import filedialog, font, colorchooser, messagebox
import os

# Главное окно
root = Tk()
root.title("Текстовый редактор")
root.geometry("1000x600")

current_file = None

# Функции работы с файлами
def new_file():
    global current_file
    text_area.delete(1.0, END)
    current_file = None
    root.title("Новый файл - Текстовый редактор")

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

def about():
    messagebox.showinfo("О программе", "Текстовый редактор на Python\nАвтор: Толстопятов Тимофей")

def choose_color():
    color = colorchooser.askcolor()[1]
    if color:
        text_area.configure(fg=color)

# Форматирование текста
def apply_tag(tag):
    try:
        current_tags = text_area.tag_names("sel.first")
        if tag in current_tags:
            text_area.tag_remove(tag, "sel.first", "sel.last")
        else:
            text_area.tag_add(tag, "sel.first", "sel.last")
    except TclError:
        pass

def update_font(*args):
    selected_font = font_family.get()
    selected_size = font_size.get()
    text_area.configure(font=(selected_font, selected_size))

# Выравнивание текста
def align_left():
    try:
        text_area.tag_remove("center", "sel.first", "sel.last")
        text_area.tag_remove("right", "sel.first", "sel.last")
        text_area.tag_add("left", "sel.first", "sel.last")
    except TclError:
        pass

def align_center():
    try:
        text_area.tag_remove("left", "sel.first", "sel.last")
        text_area.tag_remove("right", "sel.first", "sel.last")
        text_area.tag_add("center", "sel.first", "sel.last")
    except TclError:
        pass

def align_right():
    try:
        text_area.tag_remove("left", "sel.first", "sel.last")
        text_area.tag_remove("center", "sel.first", "sel.last")
        text_area.tag_add("right", "sel.first", "sel.last")
    except TclError:
        pass

# ======== Интерфейс ========
# Меню
menu_bar = Menu(root)

file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Новый", command=new_file)
file_menu.add_command(label="Открыть...", command=open_file)
file_menu.add_command(label="Сохранить", command=save_file)
file_menu.add_command(label="Сохранить как...", command=save_as)
file_menu.add_separator()
file_menu.add_command(label="Выход", command=root.quit)
menu_bar.add_cascade(label="Файл", menu=file_menu)

format_menu = Menu(menu_bar, tearoff=0)
format_menu.add_command(label="Цвет текста...", command=choose_color)
menu_bar.add_cascade(label="Формат", menu=format_menu)

help_menu = Menu(menu_bar, tearoff=0)
help_menu.add_command(label="О программе", command=about)
menu_bar.add_cascade(label="Справка", menu=help_menu)

root.config(menu=menu_bar)

# Панель инструментов
toolbar = Frame(root)
toolbar.pack(fill=X)

font_family = StringVar(value="Arial")
font_size = IntVar(value=12)

font_families = list(font.families())
font_box = OptionMenu(toolbar, font_family, *font_families, command=update_font)
font_box.pack(side=LEFT, padx=5)
font_box.config(width=15)

size_box = Spinbox(toolbar, from_=8, to=72, textvariable=font_size, command=update_font, width=5)
size_box.pack(side=LEFT)

# Кнопки стиля текста
Button(toolbar, text="B", command=lambda: apply_tag("bold")).pack(side=LEFT, padx=2)
Button(toolbar, text="I", command=lambda: apply_tag("italic")).pack(side=LEFT, padx=2)
Button(toolbar, text="U", command=lambda: apply_tag("underline")).pack(side=LEFT, padx=2)
Button(toolbar, text="S", command=lambda: apply_tag("overstrike")).pack(side=LEFT, padx=2)

# Отделённая рамка для выравнивания
align_frame = Frame(toolbar)
align_frame.pack(side=LEFT, padx=20)

Button(align_frame, text="L", command=align_left).pack(side=LEFT, padx=2)
Button(align_frame, text="C", command=align_center).pack(side=LEFT, padx=2)
Button(align_frame, text="R", command=align_right).pack(side=LEFT, padx=2)

# Текстовое поле с прокруткой
text_area = Text(root, wrap="word", undo=True)
text_area.pack(fill=BOTH, expand=True, side=LEFT)

scroll = Scrollbar(root, command=text_area.yview)
scroll.pack(fill=Y, side=RIGHT)
text_area.config(yscrollcommand=scroll.set)

# Настройка тегов
text_area.tag_configure("bold", font=font.Font(weight="bold"))
text_area.tag_configure("italic", font=font.Font(slant="italic"))
text_area.tag_configure("underline", font=font.Font(underline=1))
text_area.tag_configure("overstrike", font=font.Font(overstrike=1))

# Теги выравнивания
text_area.tag_configure("left", justify=LEFT)
text_area.tag_configure("center", justify=CENTER)
text_area.tag_configure("right", justify=RIGHT)

text_area.configure(font=(font_family.get(), font_size.get()))

# Запуск
root.mainloop()