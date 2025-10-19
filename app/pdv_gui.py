import tkinter as tk
from tkinter import simpledialog, messagebox
import requests

# IP do PC
URL_PRODUTOS = 'http://192.168.2.156:3000/produtos'

class TigroPDV:
    def __init__(self, root):
        self.root = root
        self.root.title("Tigro PDV")
        self.root.geometry("500x600")
        self.root.configure(bg="#1e1e1e")
        
        self.produtos = []
        self.produtos_venda = []  # apenas os produtos adicionados na venda
        self.quantidade_proximo = 1
        self.total_venda = 0

        # Título
        self.titulo = tk.Label(root, text="Tigro PDV", font=("Helvetica", 24, "bold"), bg="#1e1e1e", fg="#ffffff")
        self.titulo.pack(pady=20)

        # Lista de produtos adicionados
        self.lista_frame = tk.Frame(root, bg="#2e2e2e")
        self.lista_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        self.lista_scroll = tk.Scrollbar(self.lista_frame)
        self.lista_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.lista = tk.Listbox(self.lista_frame, width=50, height=15, font=("Helvetica", 14), bg="#2e2e2e", fg="#ffffff", yscrollcommand=self.lista_scroll.set, bd=0, highlightthickness=0)
        self.lista.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.lista_scroll.config(command=self.lista.yview)

        # Total da venda
        self.label_total = tk.Label(root, text="Total: R$0", font=("Helvetica", 18, "bold"), bg="#1e1e1e", fg="#00ff00")
        self.label_total.pack(pady=10)

        # Instruções
        self.label_info = tk.Label(root, text="F11 → Alterar quantidade  |  F12 → Finalizar venda", font=("Helvetica", 12), bg="#1e1e1e", fg="#cccccc")
        self.label_info.pack(pady=5)

        # Atualização automática
        self.root.after(1000, self.loop_atualizar)

        # Atalhos de teclado
        root.bind("<F12>", self.finalizar_venda)
        root.bind("<F11>", self.mudar_quantidade)

    def loop_atualizar(self):
        self.atualizar_produtos()
        self.root.after(1000, self.loop_atualizar)

    def atualizar_produtos(self):
        try:
            res = requests.get(URL_PRODUTOS)
            self.produtos = res.json()
            self.lista.delete(0, tk.END)
            self.total_venda = 0
            for p in self.produtos:
                qtd = p.get('quantidade',0)
                if qtd > 0:  # mostrar apenas produtos adicionados
                    linha = f"{p['nome']} - Qtd: {qtd} - R${p['preco']*qtd}"
                    self.lista.insert(tk.END, linha)
                    self.total_venda += p['preco'] * qtd
            self.label_total.config(text=f"Total: R${self.total_venda}")
        except:
            messagebox.showerror("Erro", "Não foi possível conectar ao backend.")

    def finalizar_venda(self, event=None):
        if self.total_venda == 0:
            messagebox.showinfo("PDV", "Nenhum produto adicionado!")
            return
        messagebox.showinfo("Venda finalizada", f"Total da venda: R${self.total_venda}")
        # Zerar produtos
        for p in self.produtos:
            p['quantidade'] = 0
        # Atualizar backend
        for p in self.produtos:
            requests.post('http://192.168.2.156:3000/adicionar-produto', json={"codigo": p['codigo'], "zerar": True})
        self.atualizar_produtos()

    def mudar_quantidade(self, event=None):
        q = simpledialog.askinteger("Quantidade", "Quantidade do próximo produto:", minvalue=1)
        if q:
            self.quantidade_proximo = q

if __name__ == "__main__":
    root = tk.Tk()
    app = TigroPDV(root)
    root.mainloop()
