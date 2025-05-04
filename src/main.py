import customtkinter as ctk
from tkinter import messagebox

# Inicializar a interface
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


# Funções de callback para cada erro
def erro_1045():
    messagebox.showerror(
        "Erro 1045", "Erro 1045: Access denied for user (usuário ou senha incorretos)."
    )


def erro_1064():
    messagebox.showerror(
        "Erro 1064", "Erro 1064: Erro de sintaxe SQL. Verifique a consulta."
    )


def erro_1146():
    messagebox.showerror(
        "Erro 1146", "Erro 1146: A tabela especificada não existe no banco de dados."
    )


def erro_2002():
    messagebox.showerror(
        "Erro 2002",
        "Erro 2002: Não foi possível conectar ao servidor MySQL (host errado ou servidor inativo).",
    )


# Criar janela principal
app = ctk.CTk()
app.title("Erros no MySQL")
app.geometry("400x400")

# Logo (pode ser uma imagem futuramente)
label_logo = ctk.CTkLabel(
    app, text="🛑 Erros no MySQL", font=ctk.CTkFont(size=24, weight="bold")
)
label_logo.pack(pady=20)

# Botões para erros
btn_1045 = ctk.CTkButton(app, text="Erro 1045", command=erro_1045)
btn_1045.pack(pady=5)

btn_1064 = ctk.CTkButton(app, text="Erro 1064", command=erro_1064)
btn_1064.pack(pady=5)

btn_1146 = ctk.CTkButton(app, text="Erro 1146", command=erro_1146)
btn_1146.pack(pady=5)

btn_2002 = ctk.CTkButton(app, text="Erro 2002", command=erro_2002)
btn_2002.pack(pady=5)

# Rodar a interface
app.mainloop()
