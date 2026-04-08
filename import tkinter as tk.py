import tkinter as tk
from tkinter import filedialog, messagebox

class ScriptEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Editor de Script de Atendimento")
        self.root.geometry("600x400")
        
        # Área de texto para editar o script
        self.text_area = tk.Text(self.root, wrap=tk.WORD, font=("Arial", 12))
        self.text_area.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        # Barra de menu
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Novo", command=self.new_script)
        file_menu.add_command(label="Abrir", command=self.open_script)
        file_menu.add_command(label="Salvar", command=self.save_script)
        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=self.root.quit)
        menubar.add_cascade(label="Arquivo", menu=file_menu)
        self.root.config(menu=menubar)
        
        self.current_file = None
    
    def new_script(self):
        self.text_area.delete(1.0, tk.END)
        self.current_file = None
        self.root.title("Editor de Script de Atendimento - Novo")
    
    def open_script(self):
        file_path = filedialog.askopenfilename(filetypes=[("Arquivos de Texto", "*.txt"), ("Todos os Arquivos", "*.*")])
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, content)
            self.current_file = file_path
            self.root.title(f"Editor de Script de Atendimento - {file_path}")
    
    def save_script(self):
        if self.current_file:
            with open(self.current_file, 'w', encoding='utf-8') as file:
                file.write(self.text_area.get(1.0, tk.END))
            messagebox.showinfo("Salvo", "Script salvo com sucesso!")
        else:
            self.save_as_script()
    
    def save_as_script(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Arquivos de Texto", "*.txt"), ("Todos os Arquivos", "*.*")])
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(self.text_area.get(1.0, tk.END))
            self.current_file = file_path
            self.root.title(f"Editor de Script de Atendimento - {file_path}")
            messagebox.showinfo("Salvo", "Script salvo com sucesso!")

if __name__ == "__main__":
    root = tk.Tk()
    editor = ScriptEditor(root)
    root.mainloop()