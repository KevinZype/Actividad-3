# Problema 1 – Notas

import tkinter as tk
from tkinter import messagebox
import math

# ---------- Colores y fuentes ----------
color_fondo = "white"
color_texto = "#222222"
color_gris = "#777777"
color_linea = "#d9d9d9"
color_panel = "#f6f6f6"

fuente = ("Helvetica", 12)
fuente_negrita = ("Helvetica", 12, "bold")
fuente_entrada = ("Helvetica", 13)


# ---------- Clase Notas ----------
class Notas:
    def __init__(self):
        self.valores = []

    def guardar_notas(self, valores):
        self.valores = valores

    def calcular_promedio(self):
        return sum(self.valores) / len(self.valores)

    def calcular_desviacion(self):
        promedio = self.calcular_promedio()
        suma = 0
        for n in self.valores:
            suma = suma + (n - promedio) ** 2
        return math.sqrt(suma / len(self.valores))

    def calcular_mayor(self):
        return max(self.valores)

    def calcular_menor(self):
        return min(self.valores)


# ---------- Clase Ventana Principal ----------
class VentanaPrincipal:
    def __init__(self):
        self.notas = Notas()

        # ---------- Ventana principal ----------
        self.ventana = tk.Tk()
        self.ventana.title("Notas")
        self.ventana.configure(bg=color_fondo)
        self.ventana.resizable(False, False)

        marco = tk.Frame(self.ventana, bg=color_fondo)
        marco.pack(padx=40, pady=35)

        # ---------- Campos para las notas ----------
        self.entradas = []
        for i in range(5):
            etiqueta = tk.Label(marco, text="Nota " + str(i + 1) + ":", font=fuente, bg=color_fondo, fg=color_gris)
            etiqueta.grid(row=i, column=0, padx=(0, 25), pady=8, sticky="w")

            celda = tk.Frame(marco, bg=color_fondo)
            celda.grid(row=i, column=1, pady=8)

            entrada = tk.Entry(celda, font=fuente_entrada, width=14, relief="flat", bd=0, highlightthickness=0,
                               bg=color_fondo, fg=color_texto, insertbackground=color_texto)
            entrada.pack(ipady=4)

            linea = tk.Frame(celda, bg=color_linea, height=2)
            linea.pack(fill="x")

            entrada.bind("<FocusIn>", lambda evento, l=linea: l.config(bg=color_texto))
            entrada.bind("<FocusOut>", lambda evento, l=linea: l.config(bg=color_linea))

            self.entradas.append(entrada)

        # ---------- Botones ----------
        marco_botones = tk.Frame(marco, bg=color_fondo)
        marco_botones.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(22, 0))
        marco_botones.columnconfigure(0, weight=1, uniform="botones")
        marco_botones.columnconfigure(1, weight=1, uniform="botones")

        btn_calcular = self.crear_boton(marco_botones, "Calcular", self.calcular, "#222222", "#444444", "white")
        btn_calcular.grid(row=0, column=0, sticky="ew", padx=(0, 6))

        btn_limpiar = self.crear_boton(marco_botones, "Limpiar", self.limpiar, "#ececec", "#dedede", color_texto)
        btn_limpiar.grid(row=0, column=1, sticky="ew", padx=(6, 0))

        # ---------- Resultados (parte inferior) ----------
        panel = tk.Frame(marco, bg=color_panel)
        panel.grid(row=6, column=0, columnspan=2, sticky="ew", pady=(25, 0))

        interior = tk.Frame(panel, bg=color_panel)
        interior.pack(anchor="w", padx=22, pady=16)

        nombres = ["Promedio =", "Desviación estándar =", "Valor mayor =", "Valor menor ="]
        resultados = []
        for i in range(4):
            nombre = tk.Label(interior, text=nombres[i], font=fuente, bg=color_panel, fg=color_gris)
            nombre.grid(row=i, column=0, sticky="w", pady=5)

            valor = tk.Label(interior, text="-", font=fuente_negrita, bg=color_panel, fg=color_texto)
            valor.grid(row=i, column=1, sticky="w", padx=(10, 0), pady=5)
            resultados.append(valor)

        self.lbl_promedio = resultados[0]
        self.lbl_desviacion = resultados[1]
        self.lbl_mayor = resultados[2]
        self.lbl_menor = resultados[3]

        self.ventana.bind("<Return>", lambda evento: self.calcular())

        self.entradas[0].focus()

    # ---------- Botones ----------
    def crear_boton(self, padre, texto, comando, color, color_encima, color_letra):
        boton = tk.Label(padre, text=texto, font=fuente_negrita, bg=color, fg=color_letra, pady=9, cursor="hand2")
        boton.bind("<Button-1>", lambda evento: comando())
        boton.bind("<Enter>", lambda evento: boton.config(bg=color_encima))
        boton.bind("<Leave>", lambda evento: boton.config(bg=color))
        return boton

    # ---------- Funciones ----------
    def calcular(self):
        lista = []

        for i in range(5):
            dato = self.entradas[i].get().strip().replace(",", ".")

            # la nota es obligatoria
            if dato == "":
                messagebox.showwarning("Aviso", "Debe ingresar las cinco notas. Falta la nota " + str(i + 1) + ".")
                self.entradas[i].focus()
                return

            # tiene que ser un número
            try:
                nota = float(dato)
            except ValueError:
                messagebox.showwarning("Aviso", "La nota " + str(i + 1) + " no es un número válido.")
                self.entradas[i].focus()
                return

            # tiene que estar entre 0 y 5
            if not (0 <= nota <= 5):
                messagebox.showwarning("Aviso", "La nota " + str(i + 1) + " debe estar entre 0 y 5.")
                self.entradas[i].focus()
                return

            lista.append(nota)

        # se guardan las notas en el objeto y se hacen los cálculos
        self.notas.guardar_notas(lista)

        promedio = self.notas.calcular_promedio()
        desviacion = self.notas.calcular_desviacion()
        mayor = self.notas.calcular_mayor()
        menor = self.notas.calcular_menor()

        # mostrar resultados
        self.lbl_promedio.config(text=("%.2f" % promedio).replace(".", ","))
        self.lbl_desviacion.config(text=("%.2f" % desviacion).replace(".", ","))
        self.lbl_mayor.config(text=str(mayor))
        self.lbl_menor.config(text=str(menor))

    def limpiar(self):
        for entrada in self.entradas:
            entrada.delete(0, tk.END)
        self.lbl_promedio.config(text="-")
        self.lbl_desviacion.config(text="-")
        self.lbl_mayor.config(text="-")
        self.lbl_menor.config(text="-")
        self.entradas[0].focus()


# ---------- Programa principal ----------
miVentanaPrincipal = VentanaPrincipal()
miVentanaPrincipal.ventana.mainloop()