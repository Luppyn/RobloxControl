import tkinter as tk
from tkinter import filedialog, messagebox
import importlib.util
import importlib
import datetime
import json

def getPythonFile():
    pyfiledir = filedialog.askopenfilename(filetypes=[("Python files", "*.py")])
    if pyfiledir:
        highImport(pyfiledir)

def json_handle(module_name):
    json_file = 'modules.json'
    try:
        with open(json_file, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}

    if module_name not in data:
        data[module_name] = str(datetime.datetime.now())
        with open(json_file, 'w') as file:
            json.dump(data, file, indent=4)
        return True
    return False

def highImport(pyfiledir):
    module_name = pyfiledir.split('/')[-1].replace('.py', '')
    spec = importlib.util.spec_from_file_location(module_name, pyfiledir)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if json_handle(module_name):
        modulos_menu.add_command(label=module_name, command=lambda: None)
    return module

def execute():
    code = text_box.get("1.0", tk.END)
    try:
        exec(code, globals())
    except Exception as e:
        messagebox.showerror("Execution Error", str(e))

root = tk.Tk()
root.title("RobloxControl")
root.iconphoto(False, tk.PhotoImage(file='icon.png'))
root.geometry("500x500")
root.resizable(False, False)

scrollbar = tk.Scrollbar(root)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

text_box = tk.Text(root, yscrollcommand=scrollbar.set, font=("Helvetica", 12), selectbackground="yellow", selectforeground="black")
text_box.pack(expand=True, fill=tk.BOTH)
scrollbar.config(command=text_box.yview)

menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=lambda: text_box.delete("1.0", tk.END))
file_menu.add_command(label="Load", command=getPythonFile)
file_menu.add_command(label="Save", command=lambda: filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python files", "*.py")]))

import_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Import", menu=import_menu)
import_menu.add_command(label="Load Python File", command=getPythonFile)

run_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Run", menu=run_menu)
run_menu.add_command(label="Start Execution", command=execute)

modulos_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Modulos", menu=modulos_menu)

root.mainloop()
