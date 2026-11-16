import logging
import re
from abc import ABC, abstractmethod


# Configuración de logs
logger = logging.getLogger("SoftwareFJ")
logger.setLevel(logging.INFO)
logger.handlers.clear()

manejador = logging.FileHandler("software_fj.log", mode="w", encoding="utf-8")
manejador.setFormatter(
    logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
)
logger.addHandler(manejador)

logger.info("Sistema Software FJ iniciado")


# Excepciones personalizadas
class SoftwareFJError(Exception):
    """Excepción base del sistema."""


class ClienteInvalidoError(SoftwareFJError):
    """Datos del cliente inválidos."""


class ServicioInvalidoError(SoftwareFJError):
    """Parámetros del servicio inválidos."""


class ServicioNoDisponibleError(SoftwareFJError):
    """Servicio no disponible."""


class ReservaError(SoftwareFJError):
    """Error relacionado con una reserva."""


class CalculoInconsistenteError(SoftwareFJError):
    """Resultado de cálculo inconsistente."""


# Entidad y Cliente
class Entidad(ABC):
    _contador = 0

    def __init__(self):
        Entidad._contador += 1
        self._id = Entidad._contador

    @property
    def id(self):
        return self._id

    @abstractmethod
    def describir(self):
        pass


class Cliente(Entidad):
    def __init__(self, nombre, documento, correo, telefono):
        super().__init__()
        self.nombre = nombre
        self.documento = documento
        self.correo = correo
        self.telefono = telefono

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise ClienteInvalidoError(
                "El nombre debe tener al menos 3 caracteres."
            )
        self.__nombre = valor.strip()

    @property
    def documento(self):
        return self.__documento

    @documento.setter
    def documento(self, valor):
        documento = str(valor)
        if not documento.isdigit() or not 6 <= len(documento) <= 10:
            raise ClienteInvalidoError(
                "El documento debe tener entre 6 y 10 dígitos."
            )
        self.__documento = documento

    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        if not isinstance(valor, str) or not re.fullmatch(
            r"[^@\s]+@[^@\s]+\.[^@\s]+", valor
        ):
            raise ClienteInvalidoError(
                "El correo electrónico no tiene un formato válido."
            )
        self.__correo = valor

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        telefono = str(valor)
        if not telefono.isdigit() or len(telefono) != 10:
            raise ClienteInvalidoError(
                "El teléfono debe tener exactamente 10 dígitos."
            )
        self.__telefono = telefono

    def describir(self):
        return (
            f"Cliente #{self.id}: {self.nombre} | "
            f"Doc: {self.documento} | {self.correo} | "
            f"Tel: {self.telefono}"
        )
