import tkinter as tk
from tkinter import messagebox, ttk
import requests

API_URL = "http://192.168.2.156:3000/produto/"

class TigroPDV:
    def __init__(self, master):
        self.master = master
        self.master.title("Tigro PDV")
        self.master.geometry("500x400")
        self.master.configure(bg="#222")

        self.lista = []

        tk.Label(master, text="Código do produto:", bg="#222", fg="white").pack(pady=5)
        self.codigo_entry = tk.Entry(master, font=("Arial", 14))
        self.codigo_entry.pack(pady=5)
        self.codigo_entry.bind("<Return>", self.buscar_produto)

        tk.Button(master, text="Buscar", command=self.buscar_produto, bg="#ff9800", fg="white").pack(pady=5)

        self.tree = ttk.Treeview(master, columns=("nome", "preco"), show="headings")
        self.tree.heading("nome", text="Produto")
        self.tree.heading("preco", text="Preço (R$)")
        self.tree.pack(pady=10, fill="both", expand=True)

        tk.Button(master, text="Finalizar Compra (F12)", command=self.finalizar, bg="#4CAF50", fg="white").pack(pady=10)

        self.master.bind("<F12>", lambda e: self.finalizar())

    def buscar_produto(self, event=None):
        codigo = self.codigo_entry.get().strip()
        if not codigo:
            return

        try:
            r = requests.get(API_URL + codigo)
            data = r.json()

            if "erro" in data:
                messagebox.showerror("Erro", data["erro"])
                return

            self.lista.append(data)
            self.tree.insert("", "end", values=(data["nome"], f"{data['preco']:.2f}"))

        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao conectar ao servidor:\n{e}")

    def finalizar(self):
        total = sum([p["preco"] for p in self.lista])
        messagebox.showinfo("Compra finalizada", f"Total: R$ {total:.2f}")
        self.lista.clear()
        self.tree.delete(*self.tree.get_children())

root = tk.Tk()
TigroPDV(root)
root.mainloop()
