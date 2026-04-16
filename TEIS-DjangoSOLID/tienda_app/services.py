from django.shortcuts import get_object_or_404

from .domain.builders import OrdenBuilder
from .domain.logic import CalculadorImpuestos
from .models import Inventario, Libro


class CompraService:
    def __init__(self, procesador_pago):
        self.procesador = procesador_pago
        self.builder = OrdenBuilder()

    def obtener_detalle_producto(self, libro_id):
        libro = get_object_or_404(Libro, id=libro_id)
        total = CalculadorImpuestos.obtener_total_con_iva(libro.precio)
        return {"libro": libro, "total": total}

    def ejecutar_compra(self, libro_id, cantidad=1, direccion="", usuario=None):
        libro = get_object_or_404(Libro, id=libro_id)
        inventario = get_object_or_404(Inventario, libro=libro)

        if inventario.cantidad < cantidad:
            raise ValueError("No hay suficiente stock para completar la compra.")

        orden = (
            self.builder
            .con_usuario(usuario)
            .con_productos([libro])
            .para_envio(direccion)
            .build()
        )

        if self.procesador.pagar(orden.total, usuario=usuario):
            inventario.cantidad -= cantidad
            inventario.save()
            return orden.total

        orden.delete()
        raise Exception("Error en la pasarela de pagos.")

    def ejecutar_proceso_compra(self, usuario, lista_productos, direccion):
        # Uso del Builder : Semantica clara y validacion interna
        orden = (
            self.builder
            .con_usuario(usuario)
            .con_productos(lista_productos)
            .para_envio(direccion)
            .build()
        )

        # Uso del Factory ( inyectado ) : Cambio de comportamiento sin cambio de codigo
        if self.procesador.pagar(orden.total):
            return f"Orden {orden.id} procesada exitosamente."

        orden.delete()
        raise Exception("Error en la pasarela de pagos.")
