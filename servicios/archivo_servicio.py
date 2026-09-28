import json
import os

from modelos import Producto, Usuario, Venta


class ArchivoServicio:
    def __init__(self, directorio: str = "datos", ruta_archivo: str | None = None):
        self.directorio = os.path.dirname(ruta_archivo) if ruta_archivo else directorio
        self.rutas = {
            "productos": os.path.join(self.directorio, "productos.json"),
            "usuarios": os.path.join(self.directorio, "usuarios.json"),
            "ventas": os.path.join(self.directorio, "ventas.json")
        }
        if ruta_archivo:
            self.rutas["productos"] = ruta_archivo
        os.makedirs(self.directorio or ".", exist_ok=True)

    def _cargar(self, clave: str, constructor):
        try:
            with open(self.rutas[clave], "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
            if not isinstance(datos, list):
                print(f"[Aviso] {clave}.json no contiene una lista válida.")
                return []
            objetos = []
            for registro in datos:
                try:
                    objetos.append(constructor.desde_diccionario(registro))
                except (KeyError, ValueError) as error:
                    print(f"[Advertencia] Registro omitido: {error}")
            return objetos
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            print(f"[Error] {clave}.json contiene JSON inválido. Se usará una colección vacía.")
            return []
        except PermissionError:
            print(f"[Error] Sin permisos para leer {clave}.json.")
            return []

    def _guardar(self, clave: str, objetos) -> bool:
        try:
            with open(self.rutas[clave], "w", encoding="utf-8") as archivo:
                json.dump([objeto.a_diccionario() for objeto in objetos], archivo, indent=4, ensure_ascii=False)
            return True
        except PermissionError:
            print(f"[Error] Sin permisos para guardar {clave}.json.")
            return False
        except OSError as error:
            print(f"[Error] No se pudo guardar {clave}.json: {error}")
            return False

    def cargar_productos(self):
        return self._cargar("productos", Producto)

    def guardar_productos(self, productos):
        return self._guardar("productos", productos)

    def cargar_usuarios(self):
        return self._cargar("usuarios", Usuario)

    def guardar_usuarios(self, usuarios):
        return self._guardar("usuarios", usuarios)

    def cargar_ventas(self):
        return self._cargar("ventas", Venta)

    def guardar_ventas(self, ventas):
        return self._guardar("ventas", ventas)
