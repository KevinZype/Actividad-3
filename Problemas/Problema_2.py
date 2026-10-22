# Problema 2 – Figuras geométricas

import tkinter as tk
from tkinter import messagebox
import math

# ---------- Colores y fuentes ----------
color_fondo = "white"
color_texto = "#222222"
color_gris = "#777777"
color_linea = "#d9d9d9"
color_panel = "#f6f6f6"
color_trazo = "#222222"
color_oculto = "#aaaaaa"

fuente = ("Helvetica", 12)
fuente_negrita = ("Helvetica", 12, "bold")
fuente_entrada = ("Helvetica", 13)


# ---------- Jerarquía de clases ----------
class Figura:
    def calcular_volumen(self):
        return 0

    def calcular_superficie(self):
        return 0


class Cilindro(Figura):
    def __init__(self, radio, altura):
        self.radio = radio
        self.altura = altura

    def calcular_volumen(self):
        return math.pi * self.radio ** 2 * self.altura

    def calcular_superficie(self):
        return 2 * math.pi * self.radio * (self.radio + self.altura)


class Esfera(Figura):
    def __init__(self, radio):
        self.radio = radio

    def calcular_volumen(self):
        return 4 / 3 * math.pi * self.radio ** 3

    def calcular_superficie(self):
        return 4 * math.pi * self.radio ** 2


class Piramide(Figura):
    # pirámide de base cuadrada
    def __init__(self, base, altura, apotema):
        self.base = base
        self.altura = altura
        self.apotema = apotema

    def calcular_volumen(self):
        return self.base ** 2 * self.altura / 3

    def calcular_superficie(self):
        # base + cuatro triángulos laterales
        return self.base ** 2 + 2 * self.base * self.apotema


class Cubo(Figura):
    def __init__(self, lado):
        self.lado = lado

    def calcular_volumen(self):
        return self.lado ** 3

    def calcular_superficie(self):
        return 6 * self.lado ** 2


class Prisma(Figura):
    # prisma rectangular
    def __init__(self, largo, ancho, altura):
        self.largo = largo
        self.ancho = ancho
        self.altura = altura

    def calcular_volumen(self):
        return self.largo * self.ancho * self.altura

    def calcular_superficie(self):
        return 2 * (self.largo * self.ancho + self.largo * self.altura + self.ancho * self.altura)


# ---------- Dibujos de las figuras ----------
def trazo(c, x0, y0, x1, y1):
    c.create_line(x0, y0, x1, y1, fill=color_trazo, width=2, capstyle="round")


def oculto(c, x0, y0, x1, y1):
    c.create_line(x0, y0, x1, y1, fill=color_oculto, width=1, dash=(4, 3))


def dibujar_cilindro(c):
    # tapa de arriba
    c.create_oval(65, 25, 155, 49, outline=color_trazo, width=2)
    # lados
    trazo(c, 65, 37, 65, 103)
    trazo(c, 155, 37, 155, 103)
    # base: parte de adelante sólida y parte de atrás punteada
    c.create_arc(65, 91, 155, 115, start=180, extent=180, style="arc", outline=color_trazo, width=2)
    c.create_arc(65, 91, 155, 115, start=0, extent=180, style="arc", outline=color_oculto, dash=(4, 3))


def dibujar_esfera(c):
    c.create_oval(65, 25, 155, 115, outline=color_trazo, width=2)
    # línea del ecuador
    c.create_arc(65, 58, 155, 82, start=180, extent=180, style="arc", outline=color_trazo, width=1)
    c.create_arc(65, 58, 155, 82, start=0, extent=180, style="arc", outline=color_oculto, dash=(4, 3))


def dibujar_piramide(c):
    cima = (115, 20)
    izq_ad = (55, 108)
    der_ad = (150, 108)
    der_at = (175, 88)
    izq_at = (80, 88)

    trazo(c, cima[0], cima[1], izq_ad[0], izq_ad[1])
    trazo(c, cima[0], cima[1], der_ad[0], der_ad[1])
    trazo(c, cima[0], cima[1], der_at[0], der_at[1])
    trazo(c, izq_ad[0], izq_ad[1], der_ad[0], der_ad[1])
    trazo(c, der_ad[0], der_ad[1], der_at[0], der_at[1])

    oculto(c, cima[0], cima[1], izq_at[0], izq_at[1])
    oculto(c, izq_ad[0], izq_ad[1], izq_at[0], izq_at[1])
    oculto(c, izq_at[0], izq_at[1], der_at[0], der_at[1])


def dibujar_caja(c, x, y, ancho, alto, d):

    c.create_rectangle(x, y, x + ancho, y + alto, outline=color_trazo, width=2)

    trazo(c, x + d, y - d, x + ancho + d, y - d)
    trazo(c, x + ancho + d, y - d, x + ancho + d, y + alto - d)
    trazo(c, x, y, x + d, y - d)
    trazo(c, x + ancho, y, x + ancho + d, y - d)
    trazo(c, x + ancho, y + alto, x + ancho + d, y + alto - d)

    oculto(c, x + d, y - d, x + d, y + alto - d)
    oculto(c, x + d, y + alto - d, x + ancho + d, y + alto - d)
    oculto(c, x, y + alto, x + d, y + alto - d)


def dibujar_cubo(c):
    dibujar_caja(c, 60, 50, 70, 70, 30)


def dibujar_prisma(c):
    dibujar_caja(c, 45, 55, 90, 60, 30)


# ---------- Datos de cada figura ----------
# nombre: (datos que se piden, clase, función que dibuja)
figuras = {
    "Cilindro": (["Radio", "Altura"], Cilindro, dibujar_cilindro),
    "Esfera": (["Radio"], Esfera, dibujar_esfera),
    "Pirámide": (["Base", "Altura", "Apotema"], Piramide, dibujar_piramide),
    "Cubo": (["Lado"], Cubo, dibujar_cubo),
    "Prisma": (["Largo", "Ancho", "Altura"], Prisma, dibujar_prisma),
}

# ventanas de figuras que están abiertas
abiertas = {}


# ---------- Botones ----------
def crear_boton(padre, texto, comando, color, color_encima, color_letra):
    boton = tk.Label(padre, text=texto, font=fuente_negrita, bg=color, fg=color_letra, pady=9, cursor="hand2")
    boton.bind("<Button-1>", lambda evento: comando())
    boton.bind("<Enter>", lambda evento: boton.config(bg=color_encima))
    boton.bind("<Leave>", lambda evento: boton.config(bg=color))
    return boton


# ---------- Ventana de cada figura ----------
def abrir_figura(nombre):
    if nombre in abiertas:
        abiertas[nombre].lift()
        return

    campos, clase, dibujar = figuras[nombre]

    v = tk.Toplevel(ventana)
    v.title(nombre)
    v.configure(bg=color_fondo)
    v.resizable(False, False)
    abiertas[nombre] = v

    def cerrar():
        del abiertas[nombre]
        v.destroy()

    v.protocol("WM_DELETE_WINDOW", cerrar)

    marco = tk.Frame(v, bg=color_fondo)
    marco.pack(padx=40, pady=30)

    # dibujo de la figura
    lienzo = tk.Canvas(marco, width=220, height=140, bg=color_fondo, highlightthickness=0)
    lienzo.grid(row=0, column=0, columnspan=2, pady=(0, 10))
    dibujar(lienzo)

    # campos para los datos
    entradas = []
    for i in range(len(campos)):
        etiqueta = tk.Label(marco, text=campos[i] + " (cm):", font=fuente, bg=color_fondo, fg=color_gris)
        etiqueta.grid(row=i + 1, column=0, padx=(0, 25), pady=6, sticky="w")

        # cada casilla lleva una línea debajo (en vez de un recuadro)
        celda = tk.Frame(marco, bg=color_fondo)
        celda.grid(row=i + 1, column=1, pady=6)

        entrada = tk.Entry(celda, font=fuente_entrada, width=12, relief="flat", bd=0, highlightthickness=0,
                           bg=color_fondo, fg=color_texto, insertbackground=color_texto)
        entrada.pack(ipady=4)

        linea = tk.Frame(celda, bg=color_linea, height=2)
        linea.pack(fill="x")

        # la línea se oscurece cuando la casilla está seleccionada
        entrada.bind("<FocusIn>", lambda evento, l=linea: l.config(bg=color_texto))
        entrada.bind("<FocusOut>", lambda evento, l=linea: l.config(bg=color_linea))

        entradas.append(entrada)

    def calcular():
        datos = []

        for i in range(len(campos)):
            dato = entradas[i].get().strip().replace(",", ".")

            # el dato es obligatorio
            if dato == "":
                messagebox.showwarning("Aviso", "Debe ingresar todos los datos. Falta: " + campos[i] + ".")
                entradas[i].focus()
                return

            # tiene que ser un número
            try:
                valor = float(dato)
            except ValueError:
                messagebox.showwarning("Aviso", campos[i] + " no es un número válido.")
                entradas[i].focus()
                return

            # tiene que ser mayor que 0
            if not math.isfinite(valor) or valor <= 0:
                messagebox.showwarning("Aviso", campos[i] + " debe ser un número mayor que 0.")
                entradas[i].focus()
                return

            datos.append(valor)

        # se crea la figura con los datos y se calculan los resultados
        figura = clase(*datos)
        volumen = figura.calcular_volumen()
        superficie = figura.calcular_superficie()

        lbl_volumen.config(text=("%.2f" % volumen).replace(".", ","))
        lbl_superficie.config(text=("%.2f" % superficie).replace(".", ","))

    def limpiar():
        for entrada in entradas:
            entrada.delete(0, tk.END)
        lbl_volumen.config(text="-")
        lbl_superficie.config(text="-")
        entradas[0].focus()

    # botones
    marco_botones = tk.Frame(marco, bg=color_fondo)
    marco_botones.grid(row=len(campos) + 1, column=0, columnspan=2, sticky="ew", pady=(18, 0))
    marco_botones.columnconfigure(0, weight=1, uniform="botones")
    marco_botones.columnconfigure(1, weight=1, uniform="botones")

    btn_calcular = crear_boton(marco_botones, "Calcular", calcular, "#222222", "#444444", "white")
    btn_calcular.grid(row=0, column=0, sticky="ew", padx=(0, 6))

    btn_limpiar = crear_boton(marco_botones, "Limpiar", limpiar, "#ececec", "#dedede", color_texto)
    btn_limpiar.grid(row=0, column=1, sticky="ew", padx=(6, 0))

    # resultados 
    panel = tk.Frame(marco, bg=color_panel)
    panel.grid(row=len(campos) + 2, column=0, columnspan=2, sticky="ew", pady=(22, 0))

    interior = tk.Frame(panel, bg=color_panel)
    interior.pack(anchor="w", padx=22, pady=16)

    nombre_volumen = tk.Label(interior, text="Volumen (cm³):", font=fuente, bg=color_panel, fg=color_gris)
    nombre_volumen.grid(row=0, column=0, sticky="w", pady=5)
    lbl_volumen = tk.Label(interior, text="-", font=fuente_negrita, bg=color_panel, fg=color_texto)
    lbl_volumen.grid(row=0, column=1, sticky="w", padx=(10, 0), pady=5)

    nombre_superficie = tk.Label(interior, text="Superficie (cm²):", font=fuente, bg=color_panel, fg=color_gris)
    nombre_superficie.grid(row=1, column=0, sticky="w", pady=5)
    lbl_superficie = tk.Label(interior, text="-", font=fuente_negrita, bg=color_panel, fg=color_texto)
    lbl_superficie.grid(row=1, column=1, sticky="w", padx=(10, 0), pady=5)

    v.bind("<Return>", lambda evento: calcular())

    entradas[0].focus_force()


# ---------- Ventana principal ----------
ventana = tk.Tk()
ventana.title("Figuras")
ventana.configure(bg=color_fondo)
ventana.resizable(False, False)

menu = tk.Frame(ventana, bg=color_fondo)
menu.pack(padx=40, pady=35)

texto_menu = tk.Label(menu, text="Seleccione una figura", font=fuente, bg=color_fondo, fg=color_gris, width=22)
texto_menu.pack(pady=(0, 18))

for nombre in figuras:
    boton = crear_boton(menu, nombre, lambda n=nombre: abrir_figura(n), "#ececec", "#dedede", color_texto)
    boton.pack(fill="x", pady=5)

ventana.mainloop()
