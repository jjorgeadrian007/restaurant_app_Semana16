import os
import tkinter as tk
from tkinter import messagebox, ttk

from assets.recursos import LOGO_PIXELES


class LoginView(ttk.Frame):
    def __init__(self, parent, restaurante, on_login):
        super().__init__(parent, padding=32)
        self.restaurante = restaurante
        self.on_login = on_login
        self.logo = self._cargar_logo()
        self._construir()

    def _cargar_logo(self):
        imagen = tk.PhotoImage(width=len(LOGO_PIXELES[0]), height=len(LOGO_PIXELES))
        for fila, pixeles in enumerate(LOGO_PIXELES):
            imagen.put("{" + " ".join(pixeles) + "}", to=(0, fila))
        return imagen.zoom(4, 4)

    def _construir(self):
        self.columnconfigure(1, weight=1)
        ttk.Label(self, image=self.logo).grid(row=0, column=0, columnspan=2, pady=(0, 8))
        ttk.Label(self, text="El Buen Sabor", font=("Segoe UI", 20, "bold")).grid(
            row=1, column=0, columnspan=2, pady=(0, 24)
        )
        ttk.Label(self, text="Acceso a la aplicación").grid(row=2, column=0, columnspan=2, pady=(0, 16))
        ttk.Label(self, text="Usuario:").grid(row=3, column=0, sticky="w", padx=(0, 12), pady=6)
        self.usuario_var = tk.StringVar()
        usuario_entry = ttk.Entry(self, textvariable=self.usuario_var)
        usuario_entry.grid(row=3, column=1, sticky="ew", pady=6)
        ttk.Label(self, text="Contraseña:").grid(row=4, column=0, sticky="w", padx=(0, 12), pady=6)
        self.contrasena_var = tk.StringVar()
        contrasena_entry = ttk.Entry(self, textvariable=self.contrasena_var, show="*")
        contrasena_entry.grid(row=4, column=1, sticky="ew", pady=6)
        ttk.Button(self, text="Ingresar", command=self._ingresar).grid(
            row=5, column=0, columnspan=2, pady=(20, 0), ipadx=16
        )
        usuario_entry.focus_set()
        contrasena_entry.bind("<Return>", lambda _event: self._ingresar())

    def _ingresar(self):
        identificacion = self.usuario_var.get().strip()
        contrasena = self.contrasena_var.get()
        if not identificacion or not contrasena.strip():
            messagebox.showwarning("Datos incompletos", "Ingrese usuario y contrasena.")
            return
        usuario = self.restaurante.validar_acceso(identificacion, contrasena)
        if usuario is None:
            messagebox.showerror("Acceso denegado", "El usuario o la contrasena no son validos.")
            return
        self.on_login(usuario)