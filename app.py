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


def highImport(pyfiledir:str, **kwargs):
    try:
        global custom_module, pyfilename, module_file
        pyfilename = pyfiledir.split('/')[-1].replace(".py", "")
        
        specifications = iu.spec_from_file_location(pyfilename, pyfiledir)
        custom_module = iu.module_from_spec(specifications)
        print(custom_module)
        specifications.loader.exec_module(custom_module)
        
        try:
            with open('modules.json', 'a+', encoding='utf-8') as file:

                file.seek(0)

                modules={f"{pyfilename}": str(custom_module)}
                json.dump(modules, file, indent=2, ensure_ascii=False)
                messagebox.showinfo(title="Import", message="Módulo carregado com sucesso.")
        except Exception as e:
            print(e)


    except:
        messagebox.showerror(title="Erro", message="Falha ao importar arquivo")

    try:
        module_menubar.add_command(label=pyfilename, command=None)
    except:
        messagebox.showwarning(title="Aviso", message="Não foi possível listar o módulo.")








def getTextContent():
    end_time = datetime.datetime.now() + datetime.timedelta(seconds=1)
    while datetime.datetime.now() < end_time:
        text = text_box.get(1.0, END).splitlines() # Utilizando o splitlines, consigo separar cada comando em listas
        return text


def execute():
    if custom_module != None:
        text = getTextContent()
        for line in text:
            with open("modules.txt", "r") as file:
                for file.readline in text:
                    if file.readline == line:
                        args = text.split(f"{pyfilename}")[1]
                        args2 = args.split("(")[1].split(")")[0] # Tem colchete, sendo assim é possível transformar em lista
                        args3 = args2.split("[")[1].split(']')[0]             
                            
                        try:
                            ((importlib.reload().__dict__[pyfilename])(args3))
                        except:
                            messagebox.showerror(title="Erro", message="Erro no código escrito")


root.mainloop()