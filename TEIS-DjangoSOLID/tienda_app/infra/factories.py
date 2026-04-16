import os

from .gateways import BancoNacionalProcesador


class MockPaymentProcessor:
    def pagar(self, monto: float, usuario=None) -> bool:
        nombre_usuario = usuario.username if usuario else "anonimo"
        print(f"[DEBUG] Mock Payment ({nombre_usuario}): Procesando pago de ${monto} sin cargo real.")
        return True


class PaymentFactory:
    @staticmethod
    def get_processor():
        provider = os.getenv('PAYMENT_PROVIDER', 'BANCO')

        if provider == 'MOCK':
            return MockPaymentProcessor()

        return BancoNacionalProcesador()
