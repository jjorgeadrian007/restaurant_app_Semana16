class Usuario:
    ROLES = ("Administrador", "Empleado", "Cliente")

    def __init__(self, identificacion: str, nombre: str, telefono: str, correo: str,
                 usuario: str | None = None, rol: str = "Cliente"):
        if not isinstance(identificacion, str) or not identificacion.strip():
            raise ValueError("La identificación del usuario no puede estar vacía.")
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre del usuario no puede estar vacío.")
        if not isinstance(telefono, str) or not telefono.strip():
            raise ValueError("El teléfono del usuario no puede estar vacío.")
        if not isinstance(correo, str) or not correo.strip() or "@" not in correo:
            raise ValueError("El correo del usuario no es válido.")
        nombre_usuario = identificacion if usuario is None else usuario
        if not isinstance(nombre_usuario, str) or not nombre_usuario.strip():
            raise ValueError("El nombre de usuario no puede estar vacío.")
        if rol not in self.ROLES:
            raise ValueError("Seleccione un rol válido.")
        self.identificacion = identificacion.strip()
        self.nombre = nombre.strip()
        self.telefono = telefono.strip()
        self.correo = correo.strip()
        self.usuario = nombre_usuario.strip()
        self.rol = rol

    def a_diccionario(self) -> dict:
        return {"identificacion": self.identificacion, "nombre": self.nombre,
            "telefono": self.telefono, "correo": self.correo,
            "usuario": self.usuario, "rol": self.rol}

    @classmethod
    def desde_diccionario(cls, datos: dict):
        try:
            return cls(datos["identificacion"], datos["nombre"], datos["telefono"], datos["correo"],
                       datos.get("usuario", datos["identificacion"]), datos.get("rol", "Cliente"))
        except KeyError as error:
            raise KeyError(f"El registro carece de la clave requerida: {error}")

    def __str__(self) -> str:
        return (f"ID: {self.identificacion} | Nombre: {self.nombre} | Usuario: {self.usuario} "
            f"| Rol: {self.rol} | Teléfono: {self.telefono} | Correo: {self.correo}")