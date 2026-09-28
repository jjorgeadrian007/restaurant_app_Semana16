import os
import tkinter as tk
from tkinter import ttk

from servicios import ArchivoServicio, RestauranteServicio
from ui import LoginView, MainView


def main():
    directorio = os.path.dirname(os.path.abspath(__file__))
    archivos = ArchivoServicio(directorio=os.path.join(directorio, "datos"))
    restaurante = RestauranteServicio(
        archivos.cargar_productos(),
        archivos.cargar_usuarios(),
        archivo_servicio=archivos,
        ventas=archivos.cargar_ventas(),
    )

    ventana = tk.Tk()
    ventana.title("El Buen Sabor")
    ventana.geometry("1080x650")
    ventana.minsize(900, 560)
    estilos = ttk.Style(ventana)
    estilos.configure("Titulo.TLabel", font=("Segoe UI", 20, "bold"), foreground="#17324d")
    estilos.configure("Seccion.TLabel", font=("Segoe UI", 16, "bold"), foreground="#17324d")
    vista_actual = None

    def mostrar_login():
        nonlocal vista_actual
        if vista_actual is not None:
            vista_actual.destroy()
        vista_actual = LoginView(ventana, restaurante, mostrar_principal)
        vista_actual.pack(fill="both", expand=True)

    def mostrar_principal(usuario):
        nonlocal vista_actual
        if vista_actual is not None:
            vista_actual.destroy()
        vista_actual = MainView(ventana, restaurante, usuario, mostrar_login)
        vista_actual.pack(fill="both", expand=True)

    mostrar_login()
    ventana.mainloop()


if __name__ == "__main__":
    main()
