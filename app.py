from tkinter import *
from tkinter import filedialog, messagebox
import importlib.util as iu
import datetime
import importlib
import json

root = Tk()
root.title('RobloxControl')
root.iconphoto(False, PhotoImage(file="icon.png"))
root.geometry(f"500x500+{int(root.winfo_screenwidth()/2)-200}+{int(root.winfo_screenwidth()/2)-600}")
root.resizable(False, False)

# Main Frame

text_box_scroll = Scrollbar(root)
text_box_scroll.pack(side=RIGHT, fill=Y)

global text_box
text_box = Text(root, 
                width=97,
                height=25,
                font=('Helvetica', 14),
                selectbackground="gray90",
                selectforeground="black",
                undo=True,
                yscrollcommand=text_box_scroll.set)
text_box.pack()

text_box_scroll.config(command=text_box.yview)

# Menu
menubar = Menu(root)
root.config(menu=menubar)

# Add File
file_menubar = Menu(menubar, tearoff=False)
menubar.add_cascade(label="File", menu=file_menubar)

file_menubar.add_command(label="New", command=__file__)
file_menubar.add_command(label="Load")
file_menubar.add_command(label="Save")

# Add Functions
import_menubar = Menu(menubar, tearoff=False)
menubar.add_cascade(label="Import", menu=import_menubar)
import_menubar.add_command(label="Load", command=lambda:(getPythonFile()))

# Add Run
run_menubar = Menu(menubar, tearoff=False)
menubar.add_cascade(label="Run", menu=run_menubar)
run_menubar.add_command(label="Start", command=lambda:(execute()))

# Add high modules imported
module_menubar = Menu(menubar, tearoff=False)
menubar.add_cascade(label="Modulos", menu=module_menubar)

# Add functions
def getPythonFile(**kwargs):
        global pyfilename
        pyfiledir = filedialog.askopenfilename(title="Select python file", filetypes=[("Python Files", "*.py")])
        highImport(pyfiledir)

# Save in Solid Disk
def json_handle():
    try:
        with open("modules.json", "r") as file:
            json_content = json.load(file)

        # Verificar se a chave já existe
        chave_existente = any(pyfilename in dicionario for dicionario in json_content)

        if not chave_existente:
            # Adicionar novo objeto ao conteúdo existente
            json_content.append({f"{pyfilename}": str(custom_module)})

            # Escrever de volta no arquivo
            with open("modules.json", "w") as file:
                json.dump(json_content, file, indent=2)
            
            messagebox.showinfo(title="Info", message="Módulo importado com sucesso")
        else:
            messagebox.showwarning(title="Aviso", message="Módulo já importado")

    except FileNotFoundError:
        # Se o arquivo não existe, criar um novo
        with open("modules.json", 'w') as file:
            json.dump([{f"{pyfilename}": str(custom_module)}], file, indent=2)


def highImport(pyfiledir:str, **kwargs):
    try:
        global pyfilename, custom_module
        pyfilename = pyfiledir.split('/')[-1].replace(".py", "")
        
        specifications = iu.spec_from_file_location(pyfilename, pyfiledir)
        custom_module = iu.module_from_spec(specifications)
        specifications.loader.exec_module(custom_module)

        json_handle()

    except:
        messagebox.showerror(title="Erro", message="Falha ao importar arquivo")

    try:
        module_menubar.add_command(label=pyfilename, command=None)
    except:
        messagebox.showwarning(title="Aviso", message="Não foi possível listar o módulo.")


def execute():
    text = text_box.get(1.0, END).splitlines()

    try:

        print(text)

        for line in text:
            if line[-1] == ";":
                if line.find("(") != -1 & line.find(")") != -1:
                    line = line[:line.find("(")]
                    args = line[line.find("("):line.find(")")]
            else:
                messagebox.showerror(title="Sintax Error", message=f"Missing ';' in line {text.index(f'{line}')}")
                break

            
        with open("modules.json", "r", encoding="utf") as file:
                json_content = json.load(file)

                for module in json_content:
                    for module_name in module:
                        if line == module_name:
                            ...

                        else:
                            break

                        #(importlib.reload().__dict__[pyfilename])(args3)


    except IndexError:
        # Isso ocorre porque existe um breakline após um ";"
        ...


root.mainloop()