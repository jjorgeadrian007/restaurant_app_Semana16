import tempfile

from modelos import Producto, Usuario, Venta
from servicios import ArchivoServicio, Restaurante, RestauranteServicio


def test_indices_y_busquedas_rapidas():
    restaurante = Restaurante("Test")
    producto = Producto(10, "Cafe", 2.5, "Bebidas", 7)
    usuario = Usuario("u-001", "Ana", "099999999", "ana@test.com")

    restaurante.inicializar_productos([producto])
    restaurante.inicializar_usuarios([usuario])
    restaurante.inicializar_ventas([Venta("u-001", "10", 2)])

    assert restaurante.buscar_producto(10) is producto
    assert restaurante.buscar_producto("10") is producto
    assert restaurante.buscar_usuario("u-001") is usuario
    assert len(restaurante.consultar_ventas_usuario("u-001")) == 1
    assert "10" in restaurante._productos_por_codigo
    assert "u-001" in restaurante._usuarios_por_identificacion
    assert "u-001" in restaurante._ventas_por_usuario


def test_venta_actualiza_stock_y_indices():
    restaurante = Restaurante("Test")
    restaurante.inicializar_productos([Producto(5, "Pan", 1.5, "Panaderia", 3)])
    restaurante.inicializar_usuarios([Usuario("u-002", "Luis", "098888888", "luis@test.com")])
    restaurante.inicializar_ventas([])

    assert restaurante.vender_producto(5, "u-002", 2) is True
    assert restaurante.buscar_producto(5).stock == 1
    assert len(restaurante.consultar_ventas_usuario("u-002")) == 1
    assert restaurante._ventas_por_usuario["u-002"][0].producto_codigo == "5"


def test_gestion_usuarios_persistencia_y_autorizacion():
    with tempfile.TemporaryDirectory() as directorio:
        archivos = ArchivoServicio(directorio=directorio)
        administrador = Usuario("admin-1", "Admin", "091111111", "admin@test.com", "admin", "Administrador")
        servicio = RestauranteServicio([], [administrador], archivo_servicio=archivos)
        empleado = servicio.registrar_usuario(
            "emp-1", "Ana", "092222222", "ana@test.com", "ana", "Empleado", "admin-1"
        )

        assert servicio.validar_acceso("ana", "emp-1") is empleado
        assert archivos.cargar_usuarios()[1].rol == "Empleado"
        assert servicio.actualizar_usuario(
            "emp-1", "Ana Ruiz", "092222222", "ana@test.com", "ana.r", "Cliente", "admin-1"
        )
        assert archivos.cargar_usuarios()[1].usuario == "ana.r"

        try:
            servicio.eliminar_usuario_administrativo("emp-1", "emp-1")
        except PermissionError:
            pass
        else:
            raise AssertionError("Un usuario no administrador pudo eliminar usuarios")

        assert servicio.eliminar_usuario_administrativo("emp-1", "admin-1")
        assert len(archivos.cargar_usuarios()) == 1
