import os
import tkinter as tk
from tkinter import messagebox, ttk

from assets.recursos import ICONO_VENTAS_PIXELES, LOGO_PIXELES


class MainView(ttk.Frame):
    def __init__(self, parent, restaurante, usuario, on_logout):
        super().__init__(parent, padding=20)
        self.restaurante = restaurante
        self.usuario = usuario
        self.on_logout = on_logout
        self.producto_vars = {campo: tk.StringVar() for campo in ("id", "nombre", "precio", "categoria", "stock")}
        self.usuario_vars = {
            campo: tk.StringVar() for campo in ("id", "nombre", "usuario", "telefono", "correo", "rol")
        }
        self.usuario_seleccionado_id = None
        self.venta_usuario_var = tk.StringVar()
        self.venta_producto_var = tk.StringVar()
        self.venta_cantidad_var = tk.StringVar(value="1")
        self.estado_var = tk.StringVar(value="Seleccione una sección para comenzar.")
        self.logo = self._cargar_recurso("logo")
        self.icono_venta = self._cargar_recurso("ventas")
        self._construir()

    def _cargar_recurso(self, nombre):
        pixeles = LOGO_PIXELES if nombre == "logo" else ICONO_VENTAS_PIXELES
        imagen = tk.PhotoImage(width=len(pixeles[0]), height=len(pixeles))
        for fila, valores in enumerate(pixeles):
            imagen.put("{" + " ".join(valores) + "}", to=(0, fila))
        return imagen.zoom(4, 4)

    def _construir(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        encabezado = ttk.Frame(self)
        encabezado.grid(row=0, column=0, sticky="ew", pady=(0, 16))
        encabezado.columnconfigure(0, weight=1)
        ttk.Label(encabezado, image=self.logo).grid(row=0, column=0, rowspan=2, sticky="w", padx=(0, 10))
        ttk.Label(encabezado, text="Panel de gestión", style="Titulo.TLabel").grid(row=0, column=1, sticky="w")
        ttk.Label(encabezado, text=f"Sesión: {self.usuario.nombre}").grid(row=1, column=1, sticky="w", pady=(3, 0))
        ttk.Button(encabezado, text="Cerrar sesión", command=self.on_logout).grid(
            row=0, column=2, rowspan=2, sticky="e"
        )
        encabezado.columnconfigure(1, weight=1)

        cuerpo = ttk.Frame(self)
        cuerpo.grid(row=1, column=0, sticky="nsew")
        cuerpo.columnconfigure(1, weight=1)
        cuerpo.rowconfigure(0, weight=1)

        navegacion = ttk.LabelFrame(cuerpo, text="Navegación", padding=12)
        navegacion.grid(row=0, column=0, sticky="ns", padx=(0, 16))
        ttk.Button(navegacion, text="Productos", command=self._mostrar_productos).pack(fill="x", pady=(0, 8))
        if self.usuario.rol == "Administrador":
            ttk.Button(navegacion, text="Usuarios", command=self._mostrar_usuarios).pack(fill="x", pady=(0, 8))
        ventas_boton = ttk.Button(navegacion, text="Ventas", image=self.icono_venta, compound="left",
                      command=self._mostrar_ventas)
        ventas_boton.pack(fill="x")

        self.contenido = ttk.Frame(cuerpo)
        self.contenido.grid(row=0, column=1, sticky="nsew")
        self.contenido.columnconfigure(0, weight=1)
        self.contenido.rowconfigure(1, weight=1)
        self.estado_label = ttk.Label(self.contenido, textvariable=self.estado_var, foreground="#53606d")
        self.estado_label.grid(
            row=2, column=0, sticky="w", pady=(10, 0)
        )
        self._mostrar_productos()

    def _limpiar_contenido(self):
        for widget in self.contenido.winfo_children():
            if widget is not self.estado_label:
                widget.destroy()

    def _mostrar_productos(self):
        self._limpiar_contenido()
        ttk.Label(self.contenido, text="Productos", style="Seccion.TLabel").grid(row=0, column=0, sticky="w")
        panel = ttk.Frame(self.contenido)
        panel.grid(row=1, column=0, sticky="nsew", pady=(12, 0))
        panel.columnconfigure(1, weight=1)
        panel.rowconfigure(0, weight=1)

        formulario = ttk.LabelFrame(panel, text="Datos del producto", padding=12)
        formulario.grid(row=0, column=0, sticky="ns", padx=(0, 16))
        campos = (("ID", "id"), ("Nombre", "nombre"), ("Precio", "precio"), ("Categoría", "categoria"), ("Stock", "stock"))
        for fila, (etiqueta, clave) in enumerate(campos):
            ttk.Label(formulario, text=f"{etiqueta}:").grid(row=fila, column=0, sticky="w", pady=5)
            ttk.Entry(formulario, textvariable=self.producto_vars[clave], width=24).grid(
                row=fila, column=1, sticky="ew", padx=(10, 0), pady=5
            )
        ttk.Button(formulario, text="Registrar", command=self._registrar_producto).grid(
            row=5, column=0, columnspan=2, sticky="ew", pady=(14, 4)
        )
        ttk.Button(formulario, text="Cargar por ID", command=self._cargar_producto).grid(
            row=6, column=0, columnspan=2, sticky="ew", pady=4
        )
        ttk.Button(formulario, text="Actualizar", command=self._actualizar_producto).grid(
            row=7, column=0, columnspan=2, sticky="ew", pady=4
        )
        ttk.Button(formulario, text="Eliminar", command=self._eliminar_producto).grid(
            row=8, column=0, columnspan=2, sticky="ew", pady=4
        )
        ttk.Button(formulario, text="Limpiar", command=self._limpiar_formulario).grid(
            row=9, column=0, columnspan=2, sticky="ew", pady=(4, 0)
        )

        tabla_frame = ttk.Frame(panel)
        tabla_frame.grid(row=0, column=1, sticky="nsew")
        tabla_frame.columnconfigure(0, weight=1)
        tabla_frame.rowconfigure(0, weight=1)
        columnas = ("id", "nombre", "precio", "categoria", "stock")
        self.productos_tabla = ttk.Treeview(tabla_frame, columns=columnas, show="headings", height=12)
        encabezados = {"id": "ID", "nombre": "Nombre", "precio": "Precio", "categoria": "Categoría", "stock": "Stock"}
        anchos = {"id": 55, "nombre": 150, "precio": 75, "categoria": 110, "stock": 65}
        for columna in columnas:
            self.productos_tabla.heading(columna, text=encabezados[columna])
            self.productos_tabla.column(columna, width=anchos[columna], anchor="w")
        self.productos_tabla.grid(row=0, column=0, sticky="nsew")
        barra = ttk.Scrollbar(tabla_frame, orient="vertical", command=self.productos_tabla.yview)
        barra.grid(row=0, column=1, sticky="ns")
        self.productos_tabla.configure(yscrollcommand=barra.set)
        self._refrescar_productos()

    def _refrescar_productos(self):
        if not hasattr(self, "productos_tabla"):
            return
        for item in self.productos_tabla.get_children():
            self.productos_tabla.delete(item)
        for producto in self.restaurante.listar_productos():
            self.productos_tabla.insert(
                "", "end", values=(producto.id_producto, producto.nombre, f"${producto.precio:.2f}", producto.categoria, producto.stock)
            )

    def _datos_formulario(self):
        return [self.producto_vars[campo].get().strip() for campo in ("id", "nombre", "precio", "categoria", "stock")]

    def _registrar_producto(self):
        try:
            self.restaurante.registrar_producto(*self._datos_formulario())
        except (ValueError, OSError) as error:
            messagebox.showerror("No se pudo registrar", str(error))
            return
        self.estado_var.set("Producto registrado correctamente.")
        self._limpiar_formulario()
        self._refrescar_productos()

    def _cargar_producto(self):
        try:
            producto = self.restaurante.consultar_producto(self.producto_vars["id"].get().strip())
        except ValueError:
            producto = None
        if producto is None:
            messagebox.showwarning("Producto no encontrado", "Ingrese un ID de producto válido.")
            return
        for campo, valor in (
            ("id", producto.id_producto),
            ("nombre", producto.nombre),
            ("precio", producto.precio),
            ("categoria", producto.categoria),
            ("stock", producto.stock),
        ):
            self.producto_vars[campo].set(str(valor))
        self.estado_var.set("Producto cargado para consulta o actualización.")

    def _actualizar_producto(self):
        try:
            actualizado = self.restaurante.actualizar_producto(*self._datos_formulario())
        except (ValueError, OSError) as error:
            messagebox.showerror("No se pudo actualizar", str(error))
            return
        if not actualizado:
            messagebox.showwarning("Producto no encontrado", "No existe un producto con ese ID.")
            return
        self.estado_var.set("Producto actualizado correctamente.")
        self._refrescar_productos()

    def _eliminar_producto(self):
        try:
            eliminado = self.restaurante.eliminar_producto_persistente(self.producto_vars["id"].get().strip())
        except (ValueError, OSError) as error:
            messagebox.showerror("No se pudo eliminar", str(error))
            return
        if not eliminado:
            messagebox.showwarning("Producto no encontrado", "No existe un producto con ese ID.")
            return
        self.estado_var.set("Producto eliminado correctamente.")
        self._limpiar_formulario()
        self._refrescar_productos()

    def _limpiar_formulario(self):
        for variable in self.producto_vars.values():
            variable.set("")

    def _mostrar_usuarios(self):
        if self.usuario.rol != "Administrador":
            self.estado_var.set("Solo un administrador puede gestionar usuarios.")
            return
        self._limpiar_contenido()
        ttk.Label(self.contenido, text="Gestión de usuarios", style="Seccion.TLabel").grid(
            row=0, column=0, sticky="w"
        )
        panel = ttk.Frame(self.contenido)
        panel.grid(row=1, column=0, sticky="nsew", pady=(12, 0))
        panel.columnconfigure(1, weight=1)
        panel.rowconfigure(0, weight=1)

        formulario = ttk.LabelFrame(panel, text="Datos del usuario", padding=12)
        formulario.grid(row=0, column=0, sticky="ns", padx=(0, 16))
        campos = (
            ("Identificador", "id"), ("Nombre", "nombre"), ("Usuario", "usuario"),
            ("Teléfono", "telefono"), ("Correo", "correo"),
        )
        for fila, (etiqueta, clave) in enumerate(campos):
            ttk.Label(formulario, text=f"{etiqueta}:").grid(row=fila, column=0, sticky="w", pady=4)
            entrada = ttk.Entry(formulario, textvariable=self.usuario_vars[clave], width=22)
            entrada.grid(row=fila, column=1, sticky="ew", padx=(8, 0), pady=4)
            self._vincular_atajos_usuario(entrada)
        fila_rol = len(campos)
        ttk.Label(formulario, text="Rol:").grid(row=fila_rol, column=0, sticky="w", pady=4)
        self.usuario_rol_combo = ttk.Combobox(
            formulario, textvariable=self.usuario_vars["rol"], values=("Empleado", "Cliente"),
            state="readonly", width=19,
        )
        self.usuario_rol_combo.grid(row=fila_rol, column=1, sticky="ew", padx=(8, 0), pady=4)
        self.usuario_rol_combo.bind("<<ComboboxSelected>>", self._cambio_rol_usuario)
        self._vincular_atajos_usuario(self.usuario_rol_combo)

        self.usuario_registrar_boton = ttk.Button(
            formulario, text="Registrar", command=self._registrar_usuario
        )
        self.usuario_registrar_boton.grid(row=6, column=0, columnspan=2, sticky="ew", pady=(12, 4))
        self.usuario_actualizar_boton = ttk.Button(
            formulario, text="Actualizar", command=self._actualizar_usuario
        )
        self.usuario_actualizar_boton.grid(row=7, column=0, columnspan=2, sticky="ew", pady=4)
        self.usuario_eliminar_boton = ttk.Button(
            formulario, text="Eliminar", command=self._eliminar_usuario
        )
        self.usuario_eliminar_boton.grid(row=8, column=0, columnspan=2, sticky="ew", pady=4)
        ttk.Button(formulario, text="Limpiar", command=self._limpiar_formulario_usuarios).grid(
            row=9, column=0, columnspan=2, sticky="ew", pady=(4, 0)
        )

        tabla_frame = ttk.Frame(panel)
        tabla_frame.grid(row=0, column=1, sticky="nsew")
        tabla_frame.columnconfigure(0, weight=1)
        tabla_frame.rowconfigure(0, weight=1)
        columnas = ("id", "nombre", "usuario", "rol")
        self.usuarios_tabla = ttk.Treeview(tabla_frame, columns=columnas, show="headings", height=12)
        encabezados = {"id": "Identificador", "nombre": "Nombre", "usuario": "Usuario", "rol": "Rol"}
        anchos = {"id": 105, "nombre": 150, "usuario": 125, "rol": 105}
        for columna in columnas:
            self.usuarios_tabla.heading(columna, text=encabezados[columna])
            self.usuarios_tabla.column(columna, width=anchos[columna], anchor="w")
        self.usuarios_tabla.grid(row=0, column=0, sticky="nsew")
        barra = ttk.Scrollbar(tabla_frame, orient="vertical", command=self.usuarios_tabla.yview)
        barra.grid(row=0, column=1, sticky="ns")
        self.usuarios_tabla.configure(yscrollcommand=barra.set)
        self.usuarios_tabla.bind("<<TreeviewSelect>>", self._seleccionar_usuario)
        self._refrescar_usuarios()

    def _vincular_atajos_usuario(self, widget):
        widget.bind("<Return>", self._atajo_registrar_usuario)
        widget.bind("<Escape>", self._atajo_limpiar_usuarios)

    def _atajo_registrar_usuario(self, _evento):
        self._registrar_usuario()
        return "break"

    def _atajo_limpiar_usuarios(self, _evento):
        self._limpiar_formulario_usuarios()
        return "break"

    def _cambio_rol_usuario(self, _evento):
        rol = self.usuario_vars["rol"].get()
        self.estado_var.set(f"El usuario se registrará con el rol {rol}.")

    def _datos_formulario_usuario(self):
        return [self.usuario_vars[campo].get().strip() for campo in (
            "id", "nombre", "telefono", "correo", "usuario", "rol"
        )]

    def _registrar_usuario(self):
        try:
            self.restaurante.registrar_usuario(*self._datos_formulario_usuario(), self.usuario.identificacion)
        except (ValueError, OSError, PermissionError) as error:
            messagebox.showerror("No se pudo registrar", str(error))
            return
        self._limpiar_formulario_usuarios()
        self._refrescar_usuarios()
        self.estado_var.set("Usuario registrado correctamente.")

    def _seleccionar_usuario(self, _evento):
        seleccion = self.usuarios_tabla.selection()
        if not seleccion:
            return
        identificacion = self.usuarios_tabla.item(seleccion[0], "values")[0]
        try:
            usuario = self.restaurante.consultar_usuario_administrativo(
                identificacion, self.usuario.identificacion
            )
        except PermissionError as error:
            self.estado_var.set(str(error))
            return
        if usuario is None:
            self.estado_var.set("El usuario seleccionado ya no está disponible.")
            return
        self.usuario_seleccionado_id = usuario.identificacion
        for campo, valor in (
            ("id", usuario.identificacion), ("nombre", usuario.nombre),
            ("usuario", usuario.usuario), ("telefono", usuario.telefono),
            ("correo", usuario.correo), ("rol", usuario.rol),
        ):
            self.usuario_vars[campo].set(str(valor))
        estado_boton = "disabled" if usuario.rol == "Administrador" else "normal"
        self.usuario_actualizar_boton.configure(state=estado_boton)
        self.usuario_eliminar_boton.configure(state=estado_boton)
        self.estado_var.set(
            "Las cuentas Administrador no se pueden modificar aquí."
            if usuario.rol == "Administrador" else "Usuario cargado para consulta o actualización."
        )

    def _actualizar_usuario(self):
        if self.usuario_seleccionado_id is None:
            messagebox.showwarning("Seleccione un usuario", "Elija una fila de la tabla para actualizarla.")
            return
        _, nombre, telefono, correo, nombre_usuario, rol = self._datos_formulario_usuario()
        try:
            actualizado = self.restaurante.actualizar_usuario(
                self.usuario_seleccionado_id, nombre, telefono, correo, nombre_usuario, rol,
                self.usuario.identificacion,
            )
        except (ValueError, OSError, PermissionError) as error:
            messagebox.showerror("No se pudo actualizar", str(error))
            return
        if not actualizado:
            messagebox.showwarning("Usuario no encontrado", "No existe el usuario seleccionado.")
            return
        self._limpiar_formulario_usuarios()
        self._refrescar_usuarios()
        self.estado_var.set("Usuario actualizado correctamente.")

    def _eliminar_usuario(self):
        if self.usuario_seleccionado_id is None:
            messagebox.showwarning("Seleccione un usuario", "Elija una fila de la tabla para eliminarla.")
            return
        try:
            eliminado = self.restaurante.eliminar_usuario_administrativo(
                self.usuario_seleccionado_id, self.usuario.identificacion
            )
        except (ValueError, OSError, PermissionError) as error:
            messagebox.showerror("No se pudo eliminar", str(error))
            return
        if not eliminado:
            messagebox.showwarning("Usuario no encontrado", "No existe el usuario seleccionado.")
            return
        self._limpiar_formulario_usuarios()
        self._refrescar_usuarios()
        self.estado_var.set("Usuario eliminado correctamente.")

    def _limpiar_formulario_usuarios(self):
        for variable in self.usuario_vars.values():
            variable.set("")
        self.usuario_seleccionado_id = None
        self.estado_var.set("Formulario de usuario limpio.")
        if hasattr(self, "usuarios_tabla"):
            self.usuarios_tabla.selection_remove(self.usuarios_tabla.selection())
        if hasattr(self, "usuario_actualizar_boton"):
            self.usuario_actualizar_boton.configure(state="normal")
            self.usuario_eliminar_boton.configure(state="normal")

    def _refrescar_usuarios(self):
        if not hasattr(self, "usuarios_tabla"):
            return
        for item in self.usuarios_tabla.get_children():
            self.usuarios_tabla.delete(item)
        usuarios = self.restaurante.listar_usuarios_administrativos(self.usuario.identificacion)
        for usuario in usuarios:
            self.usuarios_tabla.insert(
                "", "end", values=(usuario.identificacion, usuario.nombre, usuario.usuario, usuario.rol)
            )
        self.estado_var.set(f"{len(usuarios)} usuario(s) disponible(s).")

    def _mostrar_ventas(self):
        self._limpiar_contenido()
        ttk.Label(self.contenido, text="Registrar venta", style="Seccion.TLabel").grid(row=0, column=0, sticky="w")
        panel = ttk.Frame(self.contenido)
        panel.grid(row=1, column=0, sticky="nsew", pady=(12, 0))
        panel.columnconfigure(1, weight=1)
        panel.rowconfigure(1, weight=1)

        formulario = ttk.LabelFrame(panel, text="Nueva operación", padding=12)
        formulario.grid(row=0, column=0, sticky="new", padx=(0, 16))
        usuarios = self.restaurante.listar_usuarios()
        productos = self.restaurante.listar_productos()
        usuarios_opciones = [f"{usuario.identificacion} - {usuario.nombre}" for usuario in usuarios]
        productos_opciones = [f"{producto.id_producto} - {producto.nombre} (stock: {producto.stock})" for producto in productos]
        ttk.Label(formulario, text="Usuario:").grid(row=0, column=0, sticky="w", pady=5)
        usuario_combo = ttk.Combobox(formulario, textvariable=self.venta_usuario_var, values=usuarios_opciones,
                                     state="readonly", width=30)
        usuario_combo.grid(row=0, column=1, sticky="ew", padx=(10, 0), pady=5)
        ttk.Label(formulario, text="Producto:").grid(row=1, column=0, sticky="w", pady=5)
        producto_combo = ttk.Combobox(formulario, textvariable=self.venta_producto_var, values=productos_opciones,
                                      state="readonly", width=30)
        producto_combo.grid(row=1, column=1, sticky="ew", padx=(10, 0), pady=5)
        ttk.Label(formulario, text="Cantidad:").grid(row=2, column=0, sticky="w", pady=5)
        ttk.Spinbox(formulario, from_=1, to=999, textvariable=self.venta_cantidad_var, width=8).grid(
            row=2, column=1, sticky="w", padx=(10, 0), pady=5
        )
        ttk.Button(formulario, text="Registrar venta", command=self._registrar_venta).grid(
            row=3, column=0, columnspan=2, sticky="ew", pady=(14, 0)
        )

        tabla_frame = ttk.Frame(panel)
        tabla_frame.grid(row=0, column=1, rowspan=2, sticky="nsew")
        tabla_frame.columnconfigure(0, weight=1)
        tabla_frame.rowconfigure(0, weight=1)
        columnas = ("fecha", "usuario", "producto", "cantidad")
        self.ventas_tabla = ttk.Treeview(tabla_frame, columns=columnas, show="headings", height=12)
        encabezados = {"fecha": "Fecha", "usuario": "Usuario", "producto": "Producto", "cantidad": "Cantidad"}
        for columna in columnas:
            self.ventas_tabla.heading(columna, text=encabezados[columna])
            self.ventas_tabla.column(columna, width=110, anchor="w")
        self.ventas_tabla.grid(row=0, column=0, sticky="nsew")
        barra = ttk.Scrollbar(tabla_frame, orient="vertical", command=self.ventas_tabla.yview)
        barra.grid(row=0, column=1, sticky="ns")
        self.ventas_tabla.configure(yscrollcommand=barra.set)
        self._refrescar_ventas()

    def _registrar_venta(self):
        usuario_id = self.venta_usuario_var.get().split(" - ", 1)[0]
        producto_id = self.venta_producto_var.get().split(" - ", 1)[0]
        try:
            self.restaurante.registrar_venta(usuario_id, producto_id, self.venta_cantidad_var.get())
        except (ValueError, OSError) as error:
            messagebox.showerror("No se pudo registrar la venta", str(error))
            return
        self.estado_var.set("Venta registrada y almacenada correctamente.")
        self.venta_producto_var.set("")
        self.venta_cantidad_var.set("1")
        self._mostrar_ventas()

    def _refrescar_ventas(self):
        for item in self.ventas_tabla.get_children():
            self.ventas_tabla.delete(item)
        nombres_productos = {producto.codigo: producto.nombre for producto in self.restaurante.listar_productos()}
        nombres_usuarios = {usuario.identificacion: usuario.nombre for usuario in self.restaurante.listar_usuarios()}
        for venta in reversed(self.restaurante.listar_ventas()):
            self.ventas_tabla.insert("", "end", values=(
                venta.fecha,
                f"{venta.usuario_id} - {nombres_usuarios.get(venta.usuario_id, 'Desconocido')}",
                f"{venta.producto_codigo} - {nombres_productos.get(venta.producto_codigo, 'Desconocido')}",
                venta.cantidad,
            ))
