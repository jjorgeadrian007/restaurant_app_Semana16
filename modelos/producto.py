class Producto:
    def __init__(self, id_producto: int, nombre: str, precio: float, categoria: str, stock: int = 0):
        self._validar_datos(id_producto, nombre, precio, categoria, stock)
        self.id_producto = id_producto
        self.nombre = nombre.strip()
        self.precio = float(precio)
        self.categoria = categoria.strip()
        self.stock = stock

    @property
    def codigo(self) -> str:
        return str(self.id_producto)

    def _validar_datos(self, id_producto: int, nombre: str, precio: float, categoria: str, stock: int):
        if not isinstance(id_producto, int) or id_producto <= 0:
            raise ValueError("El ID del producto debe ser un entero positivo.")
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre del producto no puede estar vacío.")
        if float(precio) < 0:
            raise ValueError("El precio del producto no puede ser negativo.")
        if not isinstance(categoria, str) or not categoria.strip():
            raise ValueError("La categoría no puede estar vacía.")
        if not isinstance(stock, int) or isinstance(stock, bool) or stock < 0:
            raise ValueError("El stock debe ser un entero no negativo.")

    def vender(self, cantidad: int):
        if not isinstance(cantidad, int) or isinstance(cantidad, bool) or cantidad <= 0:
            raise ValueError("La cantidad debe ser un entero mayor que cero.")
        if cantidad > self.stock:
            raise ValueError("No hay stock suficiente.")
        self.stock -= cantidad

    def a_diccionario(self) -> dict:
        """Convierte la instancia de Producto a un formato serializable en JSON."""
        return {
            "id_producto": self.id_producto,
            "nombre": self.nombre,
            "precio": self.precio,
            "categoria": self.categoria,
            "stock": self.stock
        }

    @classmethod
    def desde_diccionario(cls, datos: dict):
        """Reconstruye una instancia de Producto a partir de un diccionario."""
        try:
            return cls(
                id_producto=datos["id_producto"],
                nombre=datos["nombre"],
                precio=datos["precio"],
                categoria=datos["categoria"],
                stock=datos.get("stock", 0)
            )
        except KeyError as error:
            raise KeyError(f"El registro carece de la clave requerida: {error}")

    def __str__(self) -> str:
        return f"ID: {self.id_producto} | Nombre: {self.nombre:<18} | Precio: ${self.precio:>6.2f} | Stock: {self.stock} | Categoría: {self.categoria}"