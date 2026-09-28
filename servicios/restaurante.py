from modelos import Producto, Usuario, Venta


class Restaurante:
    def __init__(self, nombre: str):
        self.nombre = nombre
        self._productos: list[Producto] = []
        self._usuarios: list[Usuario] = []
        self._ventas: list[Venta] = []
        self._productos_por_codigo: dict[str, Producto] = {}
        self._usuarios_por_identificacion: dict[str, Usuario] = {}
        self._ventas_por_usuario: dict[str, list[Venta]] = {}

    def _normalizar_codigo_producto(self, codigo_producto) -> str:
        if codigo_producto is None:
            return ""
        return str(codigo_producto).strip()

    def _normalizar_identificacion(self, identificacion: str) -> str:
        return str(identificacion).strip()

    def _reconstruir_indices_productos(self):
        self._productos_por_codigo = {}
        for producto in self._productos:
            self._productos_por_codigo[str(producto.id_producto)] = producto
            self._productos_por_codigo[producto.codigo] = producto

    def _reconstruir_indices_usuarios(self):
        self._usuarios_por_identificacion = {}
        for usuario in self._usuarios:
            self._usuarios_por_identificacion[usuario.identificacion] = usuario

    def _reconstruir_indices_ventas(self):
        self._ventas_por_usuario = {}
        for venta in self._ventas:
            usuario_id = venta.usuario_id
            self._ventas_por_usuario.setdefault(usuario_id, []).append(venta)

    def _reconstruir_indices(self):
        self._reconstruir_indices_productos()
        self._reconstruir_indices_usuarios()
        self._reconstruir_indices_ventas()

    def inicializar_productos(self, productos: list[Producto]):
        self._productos = list(productos)
        self._reconstruir_indices_productos()

    def obtener_productos(self) -> list[Producto]:
        return list(self._productos)

    def buscar_producto(self, codigo_producto) -> Producto | None:
        clave = self._normalizar_codigo_producto(codigo_producto)
        if not clave:
            return None
        return self._productos_por_codigo.get(clave)

    def buscar_producto_por_id(self, id_producto: int) -> Producto | None:
        return self.buscar_producto(id_producto)

    def agregar_producto(self, producto: Producto) -> bool:
        clave = self._normalizar_codigo_producto(producto.id_producto)
        if self._productos_por_codigo.get(clave) is not None:
            raise ValueError(f"Ya existe un producto registrado con el ID {producto.id_producto}.")
        self._productos.append(producto)
        self._productos_por_codigo[producto.codigo] = producto
        return True

    def actualizar_producto(self, id_producto: int, nuevo_nombre: str, nuevo_precio: float,
                           nueva_categoria: str, nuevo_stock: int | None = None) -> bool:
        producto = self.buscar_producto(id_producto)
        if producto is None:
            return False
        stock = producto.stock if nuevo_stock is None else nuevo_stock
        producto._validar_datos(id_producto, nuevo_nombre, nuevo_precio, nueva_categoria, stock)
        producto.nombre = nuevo_nombre.strip()
        producto.precio = float(nuevo_precio)
        producto.categoria = nueva_categoria.strip()
        producto.stock = stock
        return True

    def eliminar_producto(self, id_producto: int) -> bool:
        producto = self.buscar_producto(id_producto)
        if producto is None:
            return False
        self._productos.remove(producto)
        self._productos_por_codigo.pop(producto.codigo, None)
        return True

    def inicializar_usuarios(self, usuarios: list[Usuario]):
        self._usuarios = list(usuarios)
        self._reconstruir_indices_usuarios()

    def obtener_usuarios(self) -> list[Usuario]:
        return list(self._usuarios)

    def buscar_usuario(self, identificacion: str) -> Usuario | None:
        clave = self._normalizar_identificacion(identificacion)
        if not clave:
            return None
        return self._usuarios_por_identificacion.get(clave)

    def agregar_usuario(self, usuario: Usuario) -> bool:
        clave = self._normalizar_identificacion(usuario.identificacion)
        if self._usuarios_por_identificacion.get(clave) is not None:
            raise ValueError(f"Ya existe un usuario con identificación {usuario.identificacion}.")
        self._usuarios.append(usuario)
        self._usuarios_por_identificacion[usuario.identificacion] = usuario
        return True

    def actualizar_usuario(self, identificacion: str, nuevo_nombre: str, nuevo_telefono: str,
                           nuevo_correo: str, nuevo_usuario: str | None = None,
                           nuevo_rol: str | None = None) -> bool:
        usuario = self.buscar_usuario(identificacion)
        if usuario is None:
            return False
        actualizado = Usuario(
            usuario.identificacion, nuevo_nombre, nuevo_telefono, nuevo_correo,
            usuario.usuario if nuevo_usuario is None else nuevo_usuario,
            usuario.rol if nuevo_rol is None else nuevo_rol,
        )
        usuario.nombre = actualizado.nombre
        usuario.telefono = actualizado.telefono
        usuario.correo = actualizado.correo
        usuario.usuario = actualizado.usuario
        usuario.rol = actualizado.rol
        return True

    def eliminar_usuario(self, identificacion: str) -> bool:
        usuario = self.buscar_usuario(identificacion)
        if usuario is None:
            return False
        self._usuarios.remove(usuario)
        self._usuarios_por_identificacion.pop(usuario.identificacion, None)
        return True

    def inicializar_ventas(self, ventas: list[Venta]):
        self._ventas = list(ventas)
        self._reconstruir_indices_ventas()

    def obtener_ventas(self) -> list[Venta]:
        return list(self._ventas)

    def vender_producto(self, codigo_producto, identificacion_usuario: str, cantidad: int) -> bool:
        usuario = self.buscar_usuario(identificacion_usuario)
        producto = self.buscar_producto(codigo_producto)
        if usuario is None or producto is None:
            return False
        if not isinstance(cantidad, int) or isinstance(cantidad, bool) or cantidad <= 0:
            return False
        if producto.stock < cantidad:
            return False
        venta = Venta(usuario.identificacion, producto.codigo, cantidad)
        producto.vender(cantidad)
        self._ventas.append(venta)
        self._ventas_por_usuario.setdefault(usuario.identificacion, []).append(venta)
        return True

    def consultar_ventas_usuario(self, identificacion_usuario: str) -> list[Venta]:
        clave = self._normalizar_identificacion(identificacion_usuario)
        return list(self._ventas_por_usuario.get(clave, []))
