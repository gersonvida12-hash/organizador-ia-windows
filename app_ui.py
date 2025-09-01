# app_ui.py - VERSÃO 1.1 (FINAL + TEMA VISUAL)
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import threading
import queue
import shutil
from organizador_core import IACore
import sv_ttk # NOVO: Importa a biblioteca do tema

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # APLICA O TEMA VISUAL MODERNO
        sv_ttk.set_theme("dark")

        self.title("Organizador de Arquivos IA v1.1")
        self.geometry("600x450")

        self.ia_core = IACore()
        self.queue = queue.Queue()

        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill="both", expand=True)

        # (O restante do código permanece exatamente o mesmo da Página 36)
        # --- Seção de Pastas de Origem ---
        source_frame = ttk.LabelFrame(main_frame, text="1. Selecione as Pastas para Organizar", padding="10")
        source_frame.pack(fill="x", pady=5)
        self.source_vars = {}
        user_folders = get_user_folders()
        for name, path in user_folders.items():
            var = tk.BooleanVar()
            cb = ttk.Checkbutton(source_frame, text=name, variable=var)
            cb.pack(anchor="w")
            self.source_vars[path] = var

        # --- Seção de Pasta de Destino ---
        dest_frame = ttk.LabelFrame(main_frame, text="2. Selecione a Pasta de Destino", padding="10")
        dest_frame.pack(fill="x", pady=5)
        self.dest_path_var = tk.StringVar(value="")
        dest_label = ttk.Label(dest_frame, textvariable=self.dest_path_var, wraplength=500)
        dest_label.pack(side="left", fill="x", expand=True, padx=5)
        self.dest_button = ttk.Button(dest_frame, text="Selecionar...", command=self.select_dest_folder)
        self.dest_button.pack(side="right")

        # --- Seção de Ação ---
        action_frame = ttk.Frame(main_frame, padding="10")
        action_frame.pack(fill="x", pady=10)
        self.start_button = ttk.Button(action_frame, text="Iniciar Organização", command=self.start_organization_thread)
        self.start_button.pack(pady=5)
        
        # --- Barra de Status ---
        self.status_var = tk.StringVar(value="Pronto.")
        status_bar = ttk.Label(self, textvariable=self.status_var, relief="sunken", anchor="w", padding="5")
        status_bar.pack(side="bottom", fill="x")

        self.process_queue()

    def select_dest_folder(self):
        path = filedialog.askdirectory(title="Selecione a pasta de destino")
        if path:
            self.dest_path_var.set(path)
            self.status_var.set(f"Pasta de destino definida: {path}")

    def start_organization_thread(self):
        selected_sources = [path for path, var in self.source_vars.items() if var.get()]
        dest_path = self.dest_path_var.get()

        if not selected_sources:
            messagebox.showerror("Erro de Validação", "Nenhuma pasta de origem foi selecionada.")
            return
        if not dest_path:
            messagebox.showerror("Erro de Validação", "Nenhuma pasta de destino foi selecionada.")
            return

        self.start_button.config(state="disabled")
        self.dest_button.config(state="disabled")
        self.status_var.set("Iniciando processo...")

        thread = threading.Thread(target=self.organization_worker, args=(selected_sources, dest_path))
        thread.daemon = True
        thread.start()

    def organization_worker(self, source_paths, dest_root):
        try:
            self.queue.put("Mapeando arquivos...")
            files_to_process = []
            for path in source_paths:
                for subdir, _, files in os.walk(path):
                    for file in files:
                        files_to_process.append(os.path.join(subdir, file))
            
            total_files = len(files_to_process)
            self.queue.put(f"Encontrados {total_files} arquivos. Iniciando classificação...")

            for i, original_path in enumerate(files_to_process):
                processed_files = i + 1
                filename = os.path.basename(original_path)
                self.queue.put(f"Processando {processed_files}/{total_files}: {filename}")
                
                categories = list(self.ia_core.deterministic_classifier.rules.keys())
                category = self.ia_core.classify(filename, categories)
                
                dest_category_path = os.path.join(dest_root, category)
                os.makedirs(dest_category_path, exist_ok=True)
                shutil.copy2(original_path, final_dest_path)

            self.queue.put("DONE")
        except Exception as e:
            self.queue.put(f"ERROR: {e}")

    def process_queue(self):
        try:
            message = self.queue.get_nowait()
            if message == "DONE":
                messagebox.showinfo("Sucesso", "Organização concluída com sucesso!")
                self.status_var.set("Pronto.")
                self.start_button.config(state="normal")
                self.dest_button.config(state="normal")
            elif message.startswith("ERROR:"):
                messagebox.showerror("Erro na Execução", message)
                self.status_var.set("Erro. Verifique as permissões e tente novamente.")
                self.start_button.config(state="normal")
                self.dest_button.config(state="normal")
            else:
                self.status_var.set(message)
        except queue.Empty:
            pass
        finally:
            self.after(100, self.process_queue)

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

if __name__ == "__main__":
    app = App()
    app.mainloop()
