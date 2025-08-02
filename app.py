import customtkinter as ctk
import tkinter

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class DataDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Configuração da Janela Principal ---
        self.title("Painel de Visualização de Dados")
        self.geometry("800x600")
        self.configure(fg_color="#f0f0f0")

        # --- Frame Superior para os Controlos ---
        top_frame = ctk.CTkFrame(self, fg_color="transparent")
        top_frame.pack(pady=20, padx=20, fill="x")

        title_label = ctk.CTkLabel(top_frame, text="Análise de Vendas Mensais", font=ctk.CTkFont(
            size=24, weight="bold"), text_color="#333")
        title_label.pack(side="left")

        self.load_button = ctk.CTkButton(
            top_frame, text="Carregar Dados", command=self.carregar_e_exibir_dados)
        self.load_button.pack(side="right")

        # --- Frame Principal para o Gráfico ---
        self.chart_frame = ctk.CTkFrame(
            self, fg_color="white", corner_radius=10)
        self.chart_frame.pack(pady=(0, 20), padx=20, expand=True, fill="both")

        # --- LÓGICA CORRIGIDA: Criamos a "tela" do gráfico UMA ÚNICA VEZ ---
        # A 'fig' é a tela inteira, e o 'ax' é a área de desenho (o nosso "pincel")
        self.fig, self.ax = plt.subplots(figsize=(7, 5), dpi=100)
        # Define o fundo da "tela" como branco
        self.fig.patch.set_facecolor('white')

        # A "ponte" entre o Matplotlib e o Tkinter também é criada uma única vez
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.chart_frame)
        self.canvas.get_tk_widget().pack(expand=True, fill="both", padx=10, pady=10)

    def carregar_e_exibir_dados(self):
        try:
            # 1. Limpa qualquer desenho anterior que estivesse na nossa tela
            self.ax.clear()

            # 2. Usa o Pandas para ler o nosso ficheiro .csv
            df_vendas = pd.read_csv('vendas.csv')

            # 3. Desenha o novo gráfico de barras na nossa tela já existente
            self.ax.bar(df_vendas['Mes'], df_vendas['Vendas'], color="#5E95FF")

            # 4. Adiciona títulos e etiquetas
            self.ax.set_title(
                "Desempenho de Vendas ao Longo do Ano", fontsize=16)
            self.ax.set_ylabel("Valor das Vendas (€)", fontsize=12)
            # A linha abaixo precisa de ser ajustada para usar o 'ax'
            self.ax.tick_params(axis='x', rotation=45)

            self.ax.spines['top'].set_visible(False)
            self.ax.spines['right'].set_visible(False)
            self.ax.set_facecolor('white')

            self.fig.tight_layout()

            # 5. Manda a "ponte" redesenhar-se para mostrar as alterações
            self.canvas.draw()

        except FileNotFoundError:
            self.ax.clear()
            self.ax.text(0.5, 0.5, "Erro: Ficheiro 'vendas.csv' não encontrado.",
                         ha='center', va='center', color='red', fontsize=14)
            self.canvas.draw()
        except Exception as e:
            self.ax.clear()
            self.ax.text(0.5, 0.5, f"Ocorreu um erro: {e}",
                         ha='center', va='center', color='red', fontsize=14)
            self.canvas.draw()


# --- Ponto de Entrada da Aplicação ---
if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    app = DataDashboard()
    app.mainloop()
