from datetime import date


class Venta:
    def __init__(self, usuario_id: str, producto_codigo: str, cantidad: int, fecha: str | None = None):
        if not isinstance(usuario_id, str) or not usuario_id.strip():
            raise ValueError("La identificación del usuario no puede estar vacía.")
        if not isinstance(producto_codigo, str) or not producto_codigo.strip():
            raise ValueError("El código del producto no puede estar vacío.")
        if not isinstance(cantidad, int) or isinstance(cantidad, bool) or cantidad <= 0:
            raise ValueError("La cantidad debe ser un entero mayor que cero.")
        self.usuario_id = usuario_id.strip()
        self.producto_codigo = producto_codigo.strip()
        self.cantidad = cantidad
        self.fecha = (fecha or date.today().isoformat()).strip()
        if not self.fecha:
            raise ValueError("La fecha de la venta no puede estar vacía.")

    def a_diccionario(self) -> dict:
        return {
            "usuario_id": self.usuario_id,
            "producto_codigo": self.producto_codigo,
            "cantidad": self.cantidad,
            "fecha": self.fecha,
        }

    @classmethod
    def desde_diccionario(cls, datos: dict):
        try:
            return cls(datos["usuario_id"], datos["producto_codigo"], datos["cantidad"], datos.get("fecha"))
        except KeyError as error:
            raise KeyError(f"El registro carece de la clave requerida: {error}")