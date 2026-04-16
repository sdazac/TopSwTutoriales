from django.shortcuts import render
from django.views import View
from django.views.generic import ListView

from .infra.factories import PaymentFactory
from .models import Libro
from .services import CompraService


class ListaLibrosView(ListView):
    """
    Vista para listar todos los libros disponibles.
    """
    model = Libro
    template_name = 'tienda_app/lista_libros.html'
    context_object_name = 'libros'


class CompraView(View):
    """Vista delgada que delega toda la lógica al servicio."""
    template_name = 'tienda_app/compra.html'

    def get(self, request, libro_id):
        servicio = CompraService(PaymentFactory.get_processor())
        return render(request, self.template_name, servicio.obtener_detalle_producto(libro_id))

    def post(self, request, libro_id):
        servicio = CompraService(PaymentFactory.get_processor())
        usuario = request.user if request.user.is_authenticated else None
        try:
            total = servicio.ejecutar_compra(libro_id, cantidad=1, usuario=usuario)
            return render(request, self.template_name, {'mensaje_exito': f"¡Compra completada! Total: ${total}", 'total': total})
        except Exception as e:
            return render(request, self.template_name, {'error': str(e)}, status=400)
