import logging
import re
import math
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



# Clase abstracta Servicio
class Servicio(Entidad):

    def __init__(self, nombre, precio_base, disponible=True):

        # Valida el nombre del servicio
        if not isinstance(nombre, str) or len(nombre.strip()) < 3:
            raise ServicioInvalidoError(
                "El nombre del servicio debe tener al menos 3 caracteres."
            )

        # Valida el precio base
        if (
            isinstance(precio_base, bool)
            or not isinstance(precio_base, (int, float))
            or not math.isfinite(precio_base)
            or precio_base < 0
        ):
            raise ServicioInvalidoError(
                "El precio base debe ser un numero valido y no negativo."
            )

        # Valida la disponibilidad
        if not isinstance(disponible, bool):
            raise ServicioInvalidoError(
                "La disponibilidad debe ser True o False."
            )

        super().__init__()
        self._nombre = nombre.strip()
        self._precio_base = float(precio_base)
        self._disponible = disponible

    @property
    def nombre(self):
        return self._nombre

    @property
    def precio_base(self):
        return self._precio_base

    @property
    def disponible(self):
        return self._disponible

    # Metodo abstracto para calcular el costo
    @abstractmethod
    def calcular_costo(self):
        pass

    # Metodo abstracto para describir el servicio
    @abstractmethod
    def describir(self):
        pass

    # Metodo abstracto para validar los parametros
    @abstractmethod
    def validar_parametros(self):
        pass

    # Metodo para calcular el costo total
    def calcular_costo_total(self, impuesto=0, descuento=0):
        """
        Permite calcular el costo de diferentes maneras:

        calcular_costo_total()
        calcular_costo_total(impuesto=0.19)
        calcular_costo_total(impuesto=0.19, descuento=0.10)
        """

        try:
            # Valida el impuesto y el descuento
            for nombre, valor in [
                ("Impuesto", impuesto),
                ("Descuento", descuento)
            ]:

                if (
                    isinstance(valor, bool)
                    or not isinstance(valor, (int, float))
                    or not math.isfinite(valor)
                    or not 0 <= valor <= 1
                ):
                    raise ServicioInvalidoError(
                        f"{nombre} debe estar entre 0 y 1."
                    )

            # Comprueba la disponibilidad del servicio
            if not self.disponible:
                raise ServicioNoDisponibleError(
                    f"El servicio {self.nombre} no esta disponible."
                )

            # Valida los parametros del servicio especializado
            self.validar_parametros()

            # Calcula el costo propio del servicio
            costo = self.calcular_costo()

            if (
                isinstance(costo, bool)
                or not isinstance(costo, (int, float))
                or not math.isfinite(costo)
                or costo < 0
            ):
                raise CalculoInconsistenteError(
                    "El costo calculado no es valido."
                )

            # Aplica el descuento y despues el impuesto
            subtotal = costo * (1 - descuento)
            total = subtotal * (1 + impuesto)

            if not math.isfinite(total) or total < 0:
                raise CalculoInconsistenteError(
                    "El resultado del calculo es inconsistente."
                )

            logger.info(
                f"Costo calculado para {self.nombre}: "
                f"${total:.2f}"
            )

            return round(total, 2)

        except SoftwareFJError:
            logger.exception(
                f"Error al calcular el costo del servicio {self.nombre}."
            )
            raise

        except Exception as error:
            logger.exception(
                f"Error inesperado al calcular el servicio {self.nombre}."
            )

            raise CalculoInconsistenteError(
                "No fue posible calcular el costo del servicio."
            ) from error
            
# SERVICIO 1: RESERVA DE SALAS


class ReservaSala(Servicio):

    def __init__(self, nombre, precio_base, capacidad, horas, disponible=True):
        super().__init__(nombre, precio_base, disponible)
        self._capacidad = capacidad
        self._horas = horas
        self.validar_parametros()

        logger.info(f"Servicio de reserva de sala creado: {self.nombre}")

    def validar_parametros(self):
        if (
            isinstance(self._capacidad, bool)
            or not isinstance(self._capacidad, int)
            or self._capacidad <= 0
        ):
            raise ServicioInvalidoError(
                "La capacidad de la sala debe ser un entero mayor que cero."
            )

        if (
            isinstance(self._horas, bool)
            or not isinstance(self._horas, (int, float))
            or not math.isfinite(self._horas)
            or self._horas <= 0
        ):
            raise ServicioInvalidoError(
                "Las horas de reserva deben ser mayores que cero."
            )

    def calcular_costo(self):
        return self.precio_base * self._horas

    def describir(self):
        return (
            f"Reserva de sala: {self.nombre} | "
            f"Capacidad: {self._capacidad} personas | "
            f"Duración: {self._horas} horas"
        )


# SERVICIO 2: ALQUILER DE EQUIPOS


class AlquilerEquipo(Servicio):

    def __init__(
        self, nombre, precio_base, tipo_equipo, horas,
        cantidad=1, disponible=True
    ):
        super().__init__(nombre, precio_base, disponible)
        self._tipo_equipo = tipo_equipo
        self._horas = horas
        self._cantidad = cantidad
        self.validar_parametros()

        logger.info(f"Servicio de alquiler de equipos creado: {self.nombre}")

    def validar_parametros(self):
        if (
            not isinstance(self._tipo_equipo, str)
            or len(self._tipo_equipo.strip()) < 2
        ):
            raise ServicioInvalidoError(
                "Debe indicar un tipo de equipo válido."
            )

        if (
            isinstance(self._horas, bool)
            or not isinstance(self._horas, (int, float))
            or not math.isfinite(self._horas)
            or self._horas <= 0
        ):
            raise ServicioInvalidoError(
                "Las horas de alquiler deben ser mayores que cero."
            )

        if (
            isinstance(self._cantidad, bool)
            or not isinstance(self._cantidad, int)
            or self._cantidad <= 0
        ):
            raise ServicioInvalidoError(
                "La cantidad de equipos debe ser un entero mayor que cero."
            )

    def calcular_costo(self):
        return self.precio_base * self._horas * self._cantidad

    def describir(self):
        return (
            f"Alquiler de equipo: {self.nombre} | "
            f"Tipo: {self._tipo_equipo} | "
            f"Cantidad: {self._cantidad} | "
            f"Duración: {self._horas} horas"
        )

# SERVICIO 3: ASESORÍA ESPECIALIZADA

class AsesoriaEspecializada(Servicio):

    def __init__(
        self, nombre, precio_base, especialidad, horas,
        disponible=True
    ):
        super().__init__(nombre, precio_base, disponible)
        self._especialidad = especialidad
        self._horas = horas
        self.validar_parametros()

        logger.info(f"Servicio de asesoría creado: {self.nombre}")

    def validar_parametros(self):
        if (
            not isinstance(self._especialidad, str)
            or len(self._especialidad.strip()) < 3
        ):
            raise ServicioInvalidoError(
                "Debe indicar una especialidad válida."
            )

        if (
            isinstance(self._horas, bool)
            or not isinstance(self._horas, (int, float))
            or not math.isfinite(self._horas)
            or self._horas <= 0
        ):
            raise ServicioInvalidoError(
                "Las horas de asesoría deben ser mayores que cero."
            )

    def calcular_costo(self):
        return self.precio_base * self._horas

    def describir(self):
        return (
            f"Asesoría especializada: {self.nombre} | "
            f"Especialidad: {self._especialidad} | "
            f"Duración: {self._horas} horas"
        )


