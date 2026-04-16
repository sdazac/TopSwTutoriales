import datetime
from ..domain.interfaces import ProcesadorPago

class BancoNacionalProcesador(ProcesadorPago):
    """
    Implementación concreta de la infraestructura.
    Simula un banco local escribiendo en un log.
    """
    def pagar(self, monto: float, usuario=None) -> bool:
        # Simulamos una operación de red o persistencia externa
        # Genera un archivo log por usuario
        nombre_usuario = usuario.username if usuario else "anonimo"
        archivo_log = f"pagos_locales_{nombre_usuario}.log"
        
        with open(archivo_log, "a") as f:
            f.write(f"[{datetime.datetime.now()}] BANCO NACIONAL - Cobro procesado: ${monto}\n")
        return True