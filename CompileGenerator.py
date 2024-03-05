import tkinter as tk
from tkinter import filedialog, messagebox
import ast
import pyperclip
import os
import subprocess
import sys


def compile_file():
    selected_file = file_label.cget("text")
    libraries = [library for library, var in library_vars.items() if var.get()]

    compile_command = f"pyinstaller {selected_file} --onefile"
    if no_console_var.get() == 1:
        compile_command += " --noconsole"
    for library in libraries:
        compile_command += f" --hidden-import {library}"

    output_text.config(state=tk.NORMAL)
    output_text.insert(tk.END, compile_command)
    # здесь можно добавить вызов subprocess для выполнения компиляции
    output_text.config(state=tk.DISABLED)


def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Python files", "*.py")])
    file_label.config(text=file_path)
    check_imported_libraries(file_path)


def check_imported_libraries(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        tree = ast.parse(content)
        imported_libraries = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imported_libraries.add(alias.name)
            elif isinstance(node, ast.ImportFrom):
                imported_libraries.add(node.module)

        missing_libraries = [library for library in imported_libraries if library not in library_vars]
        if missing_libraries:
            messagebox.showwarning("Warning",
                                   f"The following libraries in the file are not in the generator: {', '.join(missing_libraries)}")

        for library, var in library_vars.items():
            if library in imported_libraries:
                var.set(1)
            else:
                var.set(0)


def copy_command():
    compile_command = output_text.get("1.0", tk.END)
    pyperclip.copy(compile_command)


def auto_pip_install():
    selected_libraries = [library for library, var in library_vars.items() if var.get()]
    for library in selected_libraries:
        subprocess.run([sys.executable, "-m", "pip", "install", "--user", library])


root = tk.Tk()
root.title("Compile Command generator by ErkinKraft")

file_button = tk.Button(root, text="Choose File", command=select_file)
file_button.pack()

file_label = tk.Label(root, text="No file selected")
file_label.pack()

library_vars = {}
for library in ['os', 'sys', 'art', 'PyQt5', 'tkinter', 'socket', 'pandas', 'time', 'platform', 'math',
                'turtle', 'psutil', 'cv2', 'kivy', 'Qt.py', 'PyQtWeb', 'aiogram', 'pygame', 'threading',
                'random', 'serial', 'datetime', 'colorama', 'subprocess', 'json', 'argparse', 'pyautogui',
                'configparser', 'telegram', 'ctypes', 'requests', 'ast', 'pyperclip']:
    var = tk.IntVar()
    library_vars[library] = var
    checkbox = tk.Checkbutton(root, text=library, variable=var)
    checkbox.pack()

no_console_var = tk.IntVar()
no_console_checkbox = tk.Checkbutton(root, text="Remove Console", variable=no_console_var)
no_console_checkbox.pack()

determine_button = tk.Button(root, text="Determine", command=lambda: check_imported_libraries(file_label.cget("text")))
determine_button.pack()

compile_button = tk.Button(root, text="Compile", command=compile_file)
compile_button.pack()

output_text = tk.Text(root, height=10, width=50)
output_text.pack()

copy_button = tk.Button(root, text="Copy", command=copy_command)
copy_button.pack(side=tk.RIGHT, padx=5, pady=5)

auto_pip_button = tk.Button(root, text="Auto pip", command=auto_pip_install)
auto_pip_button.pack(side=tk.LEFT, padx=5, pady=5)

output_text.config(state=tk.DISABLED)

root.mainloop()
