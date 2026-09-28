# Sistema de Gestión de Restaurante

**Estudiante:** Jorge Adrián Santamaría Muñoz  
**Asignatura:** Programación Orientada a Objetos

Aplicación de escritorio en Python que usa Tkinter para gestionar el acceso, productos, usuarios y ventas. La interfaz separa navegación y formularios; los modelos representan los registros y los servicios concentran validaciones y persistencia JSON.

## Estructura

```text
restaurante_app/
├── datos/
│   ├── productos.json
│   ├── usuarios.json
│   └── ventas.json
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   ├── usuario.py
│   └── venta.py
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   ├── restaurante.py
│   └── restaurante_servicio.py
├── ui/
│   ├── __init__.py
│   ├── login_view.py
│   └── main_view.py
├── assets/
│   ├── __init__.py
│   └── recursos.py
├── main.py
└── README.md
```

## Responsabilidades

- `Producto`, `Usuario` y `Venta` representan las entidades del sistema. `Usuario` incluye un identificador, nombre de usuario y rol (`Administrador`, `Empleado` o `Cliente`).
- `ArchivoServicio` centraliza la lectura y escritura de los archivos JSON.
- `RestauranteServicio` valida el acceso, aplica las reglas de usuarios y coordina las operaciones con persistencia.
- `LoginView` muestra el formulario de acceso y comunica el resultado al punto de entrada.
- `MainView` ofrece navegación y gestión de productos y ventas. La sección Usuarios está disponible solo para administradores e implementa registro, consulta, actualización y eliminación.
- `main.py` prepara las dependencias, crea una sola ventana Tkinter y cambia las vistas sin abrir otra ventana.

## Persistencia y ventas

Los archivos se cargan al iniciar. Si no existen, se inicia con una colección vacía. JSON inválido, claves faltantes y registros con valores inválidos se informan sin detener la carga de los registros válidos. Las ventas incluyen usuario, producto, cantidad y fecha; los registros antiguos sin fecha reciben la fecha actual al cargarse.

El acceso es simulado: se ingresa con el nombre de usuario y la identificación funciona como contraseña. La cuenta inicial incluida es usuario `33`, contraseña `33`, con rol `Administrador`. Para mantener compatibilidad, los registros antiguos que no incluyan un nombre de usuario usan su identificación como nombre de usuario; los registros antiguos sin rol se consideran `Cliente`.

Desde Productos se puede registrar, cargar por ID, actualizar y eliminar. La vista solicita estas operaciones a `RestauranteServicio`; `ArchivoServicio` conserva los cambios en `datos/productos.json`.

Desde Usuarios, un administrador puede gestionar cuentas Empleado y Cliente. El Treeview solo muestra identificador, nombre, usuario y rol. Al seleccionar una fila, la vista consulta el registro por identificador a través de `RestauranteServicio`; los controles de administrador no se pueden modificar ni eliminar. Los eventos `<<TreeviewSelect>>`, `<<ComboboxSelected>>`, `<Return>` y `<Escape>` coordinan la interacción con el formulario.

Desde Ventas se seleccionan un usuario y un producto existentes mediante `ttk.Combobox`, se indica la cantidad y se usa **Registrar venta**. `RestauranteServicio` valida la operación, descuenta el stock, guarda `datos/productos.json` y `datos/ventas.json`, y la vista actualiza el `Treeview` inmediatamente. La carpeta `assets/` contiene las matrices de píxeles del logotipo y del ícono utilizados por las vistas.

## Ejecución

Desde la carpeta raíz del proyecto:

```bash
python main.py
```

Se puede comprobar la sintaxis con:

```bash
python -m compileall modelos servicios main.py
```

También se puede ejecutar la validación automatizada con:

```bash
python -m pytest -q
```