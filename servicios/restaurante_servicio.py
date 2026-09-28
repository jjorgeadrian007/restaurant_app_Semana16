from modelos import Producto, Usuario, Venta

from .restaurante import Restaurante


class RestauranteServicio(Restaurante):
    """Coordina los datos que necesitan las vistas de la aplicacion."""

    def __init__(self, productos: list[Producto], usuarios: list[Usuario], nombre: str = "El Buen Sabor",
                 archivo_servicio=None, ventas: list[Venta] | None = None):
        super().__init__(nombre)
        self.archivo_servicio = archivo_servicio
        self.inicializar_productos(productos)
        self.inicializar_usuarios(usuarios)
        self.inicializar_ventas(ventas or [])

    def validar_acceso(self, identificacion: str, contrasena: str) -> Usuario | None:
        """Valida el nombre de usuario; la identificación se conserva como clave simulada."""
        clave = identificacion.strip()
        usuario = next(
            (registro for registro in self.obtener_usuarios()
             if registro.usuario == clave or registro.identificacion == clave),
            None,
        )
        if usuario is None or not contrasena.strip() or contrasena.strip() != usuario.identificacion:
            return None
        return usuario

    def listar_productos(self) -> list[Producto]:
        return self.obtener_productos()

    def listar_usuarios(self) -> list[Usuario]:
        return self.obtener_usuarios()

    def _exigir_administrador(self, identificacion_administrador: str):
        administrador = self.buscar_usuario(identificacion_administrador)
        if administrador is None or administrador.rol != "Administrador":
            raise PermissionError("Solo un administrador puede gestionar usuarios.")

    def _validar_usuario_administrable(self, usuario: Usuario, rol_nuevo: str | None = None):
        if usuario.rol == "Administrador" or rol_nuevo == "Administrador":
            raise ValueError("La gestión administrativa solo permite usuarios Empleado o Cliente.")

    def listar_usuarios_administrativos(self, identificacion_administrador: str) -> list[Usuario]:
        self._exigir_administrador(identificacion_administrador)
        return self.listar_usuarios()

    def consultar_usuario_administrativo(self, identificacion: str,
                                         identificacion_administrador: str) -> Usuario | None:
        self._exigir_administrador(identificacion_administrador)
        return self.buscar_usuario(identificacion)

    def _guardar_usuarios(self):
        if self.archivo_servicio is not None and not self.archivo_servicio.guardar_usuarios(self.obtener_usuarios()):
            raise OSError("No se pudo guardar usuarios.json.")

    def _validar_nombre_usuario_unico(self, nombre_usuario: str, identificacion: str | None = None):
        clave = nombre_usuario.strip().casefold()
        if any(
            usuario.identificacion != identificacion and usuario.usuario.casefold() == clave
            for usuario in self.obtener_usuarios()
        ):
            raise ValueError(f"El nombre de usuario '{nombre_usuario}' ya está registrado.")

    def registrar_usuario(self, identificacion: str, nombre: str, telefono: str, correo: str,
                          nombre_usuario: str, rol: str, identificacion_administrador: str) -> Usuario:
        self._exigir_administrador(identificacion_administrador)
        usuario = Usuario(identificacion, nombre, telefono, correo, nombre_usuario, rol)
        self._validar_usuario_administrable(usuario)
        self._validar_nombre_usuario_unico(usuario.usuario)
        self.agregar_usuario(usuario)
        try:
            self._guardar_usuarios()
        except OSError:
            self.eliminar_usuario(usuario.identificacion)
            raise
        return usuario

    def actualizar_usuario(self, identificacion: str, nombre: str, telefono: str, correo: str,
                           nombre_usuario: str, rol: str,
                           identificacion_administrador: str) -> bool:
        self._exigir_administrador(identificacion_administrador)
        usuario = self.buscar_usuario(identificacion)
        if usuario is None:
            return False
        self._validar_usuario_administrable(usuario, rol)
        self._validar_nombre_usuario_unico(nombre_usuario, identificacion)
        valores_anteriores = (usuario.nombre, usuario.telefono, usuario.correo, usuario.usuario, usuario.rol)
        actualizado = super().actualizar_usuario(
            identificacion, nombre, telefono, correo, nombre_usuario, rol
        )
        if actualizado:
            try:
                self._guardar_usuarios()
            except OSError:
                super().actualizar_usuario(identificacion, *valores_anteriores[:3],
                                           valores_anteriores[3], valores_anteriores[4])
                raise
        return actualizado

    def eliminar_usuario_administrativo(self, identificacion: str,
                                        identificacion_administrador: str) -> bool:
        self._exigir_administrador(identificacion_administrador)
        usuario = self.buscar_usuario(identificacion)
        if usuario is None:
            return False
        self._validar_usuario_administrable(usuario)
        eliminado = super().eliminar_usuario(identificacion)
        if eliminado:
            try:
                self._guardar_usuarios()
            except OSError:
                self._usuarios.append(usuario)
                self._reconstruir_indices_usuarios()
                raise
        return eliminado

    def _guardar_productos(self):
        if self.archivo_servicio is not None and not self.archivo_servicio.guardar_productos(self.obtener_productos()):
            raise OSError("No se pudo guardar productos.json.")

    def _guardar_ventas(self):
        if self.archivo_servicio is not None and not self.archivo_servicio.guardar_ventas(self.obtener_ventas()):
            raise OSError("No se pudo guardar ventas.json.")

    def registrar_producto(self, id_producto, nombre: str, precio, categoria: str, stock=0) -> Producto:
        producto = Producto(int(id_producto), nombre, float(precio), categoria, int(stock))
        self.agregar_producto(producto)
        try:
            self._guardar_productos()
        except OSError:
            self.eliminar_producto(producto.id_producto)
            raise
        return producto

    def consultar_producto(self, id_producto) -> Producto | None:
        return self.buscar_producto_por_id(int(id_producto))

    def actualizar_producto(self, id_producto, nombre: str, precio, categoria: str, stock) -> bool:
        producto = self.consultar_producto(id_producto)
        if producto is None:
            return False
        valores_anteriores = (producto.nombre, producto.precio, producto.categoria, producto.stock)
        actualizado = super().actualizar_producto(
            producto.id_producto, nombre, float(precio), categoria, int(stock)
        )
        if actualizado:
            try:
                self._guardar_productos()
            except OSError:
                producto.nombre, producto.precio, producto.categoria, producto.stock = valores_anteriores
                raise
        return actualizado

    def eliminar_producto_persistente(self, id_producto) -> bool:
        producto = self.consultar_producto(id_producto)
        if producto is None:
            return False
        eliminado = super().eliminar_producto(producto.id_producto)
        if eliminado:
            try:
                self._guardar_productos()
            except OSError:
                self._productos.append(producto)
                self._reconstruir_indices_productos()
                raise
        return eliminado

    def cantidad_productos(self) -> int:
        return len(self.obtener_productos())

    def cantidad_usuarios(self) -> int:
        return len(self.obtener_usuarios())

    def listar_ventas(self) -> list[Venta]:
        return self.obtener_ventas()

    def registrar_venta(self, identificacion_usuario: str, id_producto, cantidad) -> Venta:
        try:
            cantidad_entera = int(cantidad)
        except (TypeError, ValueError) as error:
            raise ValueError("La cantidad debe ser un entero mayor que cero.") from error
        usuario = self.buscar_usuario(identificacion_usuario)
        producto = self.consultar_producto(id_producto)
        if usuario is None:
            raise ValueError("Seleccione un usuario registrado.")
        if producto is None:
            raise ValueError("Seleccione un producto registrado.")
        if cantidad_entera <= 0:
            raise ValueError("La cantidad debe ser un entero mayor que cero.")
        if producto.stock < cantidad_entera:
            raise ValueError("No hay stock suficiente para registrar la venta.")

        venta = Venta(usuario.identificacion, producto.codigo, cantidad_entera)
        producto.vender(cantidad_entera)
        self._ventas.append(venta)
        self._ventas_por_usuario.setdefault(usuario.identificacion, []).append(venta)
        try:
            self._guardar_productos()
            self._guardar_ventas()
        except OSError:
            producto.stock += cantidad_entera
            self._ventas.pop()
            self._reconstruir_indices_ventas()
            raise
        return venta