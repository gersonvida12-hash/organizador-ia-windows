# app_ui.py - VERSÃO 2
import tkinter as tk
from tkinter import ttk, filedialog
import os

# Função para encontrar as pastas padrão do usuário (sem alterações)
def get_user_folders():
    base_path = os.path.expanduser('~')
    folders = {
        "Documentos": os.path.join(base_path, 'Documents'),
        "Downloads": os.path.join(base_path, 'Downloads'),
        "Imagens": os.path.join(base_path, 'Pictures'),
        "Vídeos": os.path.join(base_path, 'Videos'),
        "Música": os.path.join(base_path, 'Music'),
        "Área de Trabalho": os.path.join(base_path, 'Desktop')
    }
    return {name: path for name, path in folders.items() if os.path.exists(path)}

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Organizador de Arquivos IA")
        self.geometry("600x450") # Aumentei a altura ligeiramente

        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill="both", expand=True)

        source_frame = ttk.LabelFrame(main_frame, text="1. Selecione as Pastas para Organizar", padding="10")
        source_frame.pack(fill="x", pady=5)

        self.source_vars = {}
        user_folders = get_user_folders()
        for i, (name, path) in enumerate(user_folders.items()):
            var = tk.BooleanVar()
            cb = ttk.Checkbutton(source_frame, text=f"{name}", variable=var)
            cb.pack(anchor="w")
            self.source_vars[path] = var

        dest_frame = ttk.LabelFrame(main_frame, text="2. Selecione a Pasta de Destino", padding="10")
        dest_frame.pack(fill="x", pady=5)

        self.dest_path_var = tk.StringVar(value="Nenhuma pasta de destino selecionada")
        dest_label = ttk.Label(dest_frame, textvariable=self.dest_path_var, wraplength=500)
        dest_label.pack(side="left", fill="x", expand=True, padx=5)
        
        # MODIFICADO: O botão agora chama uma função
        dest_button = ttk.Button(dest_frame, text="Selecionar...", command=self.select_dest_folder)
        dest_button.pack(side="right")

        action_frame = ttk.Frame(main_frame, padding="10")
        action_frame.pack(fill="x", pady=10)

        start_button = ttk.Button(action_frame, text="Iniciar Organização")
        start_button.pack(pady=5)
        
        self.status_var = tk.StringVar(value="Pronto.")
        status_bar = ttk.Label(self, textvariable=self.status_var, relief="sunken", anchor="w", padding="5")
        status_bar.pack(side="bottom", fill="x")

    # NOVO: Método que é chamado pelo botão "Selecionar..."
    def select_dest_folder(self):
        path = filedialog.askdirectory(title="Selecione a pasta de destino")
        if path: # Se o usuário selecionou uma pasta e não cancelou
            self.dest_path_var.set(path)
            self.status_var.set(f"Pasta de destino definida: {path}")

if __name__ == "__main__":
    app = App()
    app.mainloop()
