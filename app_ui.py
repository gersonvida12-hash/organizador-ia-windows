# app_ui.py
import tkinter as tk
from tkinter import ttk, filedialog
import os

# Função para encontrar as pastas padrão do usuário
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
    # Retorna apenas as pastas que realmente existem no sistema
    return {name: path for name, path in folders.items() if os.path.exists(path)}

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Organizador de Arquivos IA")
        self.geometry("600x400")

        # --- Frame Principal ---
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill="both", expand=True)

        # --- Seção de Pastas de Origem ---
        source_frame = ttk.LabelFrame(main_frame, text="1. Selecione as Pastas para Organizar", padding="10")
        source_frame.pack(fill="x", pady=5)

        self.source_vars = {}
        user_folders = get_user_folders()
        for i, (name, path) in enumerate(user_folders.items()):
            var = tk.BooleanVar()
            cb = ttk.Checkbutton(source_frame, text=f"{name} ({path})", variable=var)
            cb.pack(anchor="w")
            self.source_vars[path] = var

        # --- Seção de Pasta de Destino ---
        dest_frame = ttk.LabelFrame(main_frame, text="2. Selecione a Pasta de Destino", padding="10")
        dest_frame.pack(fill="x", pady=5)

        self.dest_path_var = tk.StringVar(value="Nenhuma pasta de destino selecionada")
        dest_label = ttk.Label(dest_frame, textvariable=self.dest_path_var, wraplength=500)
        dest_label.pack(side="left", fill="x", expand=True, padx=5)
        dest_button = ttk.Button(dest_frame, text="Selecionar...")
        dest_button.pack(side="right")

        # --- Seção de Ação ---
        action_frame = ttk.Frame(main_frame, padding="10")
        action_frame.pack(fill="x", pady=10)

        start_button = ttk.Button(action_frame, text="Iniciar Organização")
        start_button.pack(pady=5)
        
        # --- Barra de Status ---
        self.status_var = tk.StringVar(value="Pronto.")
        status_bar = ttk.Label(self, textvariable=self.status_var, relief="sunken", anchor="w", padding="5")
        status_bar.pack(side="bottom", fill="x")

if __name__ == "__main__":
    app = App()
    app.mainloop()
