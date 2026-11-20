"""
Proyecto: sistema-reservas-grupo-213023_535 (Software FJ)
Curso: Programación 213023 - Fase 4 - Grupo 213023_535

Partes 5 y 6 - Yesica Mendoza Torres:
Clase Reserva, clase SistemaGestion y simulación de operaciones.

Nota: esta parte usa las clases de las demás partes (logger, excepciones,
Entidad, Cliente, Servicio y los tres servicios), por lo que se debe
ejecutar junto con ellas. El archivo completo del proyecto es
sistema-reservas-grupo-213023_535.py
"""

# Clase Reserva y sistema de gestión

class Reserva(Entidad):
    """Une un cliente con un servicio y controla el estado de la reserva."""

    # Estados posibles de una reserva
    PENDIENTE = "Pendiente"
    CONFIRMADA = "Confirmada"
    CANCELADA = "Cancelada"

    def __init__(self, cliente, servicio):
        # Se revisa que el cliente sea un objeto Cliente (si no, es una reserva incorrecta)
        if not isinstance(cliente, Cliente):
            raise ReservaError("La reserva necesita un cliente valido.")
        # Se revisa que el servicio sea un objeto Servicio
        if not isinstance(servicio, Servicio):
            raise ReservaError("La reserva necesita un servicio valido.")
        super().__init__()                      # Se crea la entidad base (con su id)
        self._cliente = cliente                 # Cliente que reserva
        self._servicio = servicio               # Servicio reservado
        self._duracion = servicio._horas        # La duración (en horas) es la del servicio
        self._estado = Reserva.PENDIENTE        # Toda reserva nueva empieza pendiente
        self._costo_total = None                # Todavía no se ha calculado el costo
        logger.info(
            f"Reserva #{self.id} creada: {cliente.nombre} -> {servicio.nombre}"
        )

    # Propiedades de solo lectura (encapsulación)
    @property
    def cliente(self):
        return self._cliente

    @property
    def servicio(self):
        return self._servicio

    @property
    def duracion(self):
        return self._duracion

    @property
    def estado(self):
        return self._estado

    @property
    def costo_total(self):
        return self._costo_total

    # Procesamiento: calcula el costo de la reserva
    def procesar(self, impuesto=0, descuento=0):
        """
        Calcula el costo de la reserva. Se puede usar de varias formas:
        procesar()
        procesar(impuesto=0.19)
        procesar(impuesto=0.19, descuento=0.10)
        """
        try:
            # Solo se puede procesar una reserva que esté pendiente
            if self._estado != Reserva.PENDIENTE:
                raise ReservaError(
                    f"No se puede procesar una reserva en estado {self._estado}."
                )
            # El servicio revisa su disponibilidad y sus parámetros, y calcula el costo
            costo = self._servicio.calcular_costo_total(impuesto, descuento)
        except ReservaError:
            # Es un error propio de la reserva: se envía tal cual hacia afuera
            raise
        except SoftwareFJError as error:
            # Error del servicio (no disponible, parámetros inválidos, cálculo raro):
            # se encadena con "from" para conservar la causa original
            raise ReservaError(
                f"La reserva #{self.id} no pudo procesarse."
            ) from error
        except Exception as error:
            # Cualquier error inesperado también se convierte en ReservaError
            raise ReservaError(
                f"Error inesperado al procesar la reserva #{self.id}."
            ) from error
        else:
            # Este bloque solo se ejecuta si NO hubo ningún error
            self._costo_total = costo
            logger.info(f"Reserva #{self.id} procesada. Costo: ${costo:,.2f}")
            return costo
        finally:
            # Este bloque se ejecuta siempre, haya o no haya error
            logger.info(f"Reserva #{self.id}: intento de procesamiento terminado.")

    # Confirmación: procesa la reserva y cambia su estado
    def confirmar(self, impuesto=0, descuento=0):
        costo = self.procesar(impuesto, descuento)  # Si algo falla, el error sale aquí
        self._estado = Reserva.CONFIRMADA           # Si todo salió bien, queda confirmada
        logger.info(f"Reserva #{self.id} confirmada para {self._cliente.nombre}.")
        return costo

    # Cancelación: no se puede cancelar dos veces
    def cancelar(self):
        if self._estado == Reserva.CANCELADA:
            raise ReservaError(f"La reserva #{self.id} ya esta cancelada.")
        self._estado = Reserva.CANCELADA
        logger.info(f"Reserva #{self.id} cancelada.")

    def describir(self):
        costo = (
            f"${self._costo_total:,.2f}" if self._costo_total is not None
            else "sin calcular"
        )
        return (
            f"Reserva #{self.id} | Cliente: {self._cliente.nombre} | "
            f"Servicio: {self._servicio.nombre} | "
            f"Duración: {self._duracion} horas | "
            f"Estado: {self._estado} | Costo: {costo}"
        )


class SistemaGestion:
    """Guarda las listas de clientes, servicios y reservas, y evita que un error detenga el programa."""

    def __init__(self):
        self.clientes = []                      # Lista interna de clientes
        self.servicios = []                     # Lista interna de servicios
        self.reservas = []                      # Lista interna de reservas

    def registrar_cliente(self, *datos):
        cliente = Cliente(*datos)               # Si los datos son inválidos, Cliente lanza el error
        self.clientes.append(cliente)           # Solo se guarda si se creó bien
        return cliente

    def registrar_servicio(self, clase, *datos):
        servicio = clase(*datos)                # clase puede ser ReservaSala, AlquilerEquipo o AsesoriaEspecializada
        self.servicios.append(servicio)
        return servicio

    def crear_reserva(self, cliente, servicio, impuesto=0, descuento=0):
        reserva = Reserva(cliente, servicio)    # Se crea la reserva (pendiente)
        reserva.confirmar(impuesto, descuento)  # Se confirma (calcula el costo)
        self.reservas.append(reserva)           # Solo se guarda si se confirmó
        return reserva

    def ejecutar(self, descripcion, funcion, *args, **kwargs):
        """Ejecuta una operación y, si falla, registra el error y sigue funcionando."""
        try:
            resultado = funcion(*args, **kwargs)
        except SoftwareFJError as error:
            # Error controlado del sistema; si tiene causa encadenada, también se muestra
            causa = f" | Causa: {error.__cause__}" if error.__cause__ else ""
            logger.error(f"{descripcion} FALLO: {error}{causa}")
            print(f"[ERROR] {descripcion}: {error}{causa}")
            return None
        except Exception as error:
            # Error inesperado (por ejemplo, un dato que falta): el programa tampoco se detiene
            logger.error(f"{descripcion} FALLO por error inesperado: {error!r}")
            print(f"[ERROR INESPERADO] {descripcion}: {error!r}")
            return None
        else:
            logger.info(f"{descripcion} OK")
            print(f"[OK] {descripcion}")
            return resultado


# Simulación de operaciones (válidas e inválidas)

sistema = SistemaGestion()
ejecutar = sistema.ejecutar

print("=== SIMULACIÓN DE OPERACIONES - SOFTWARE FJ ===")

# --- Clientes: dos válidos y tres inválidos ---
laura = ejecutar("Op 1: registrar cliente válido (Laura)", sistema.registrar_cliente,
                 "Laura Gómez", "1012345678", "laura@correo.com", "3001234567")
carlos = ejecutar("Op 2: registrar cliente válido (Carlos)", sistema.registrar_cliente,
                  "Carlos Pérez", "79456123", "carlos@correo.com", "3109876543")
ejecutar("Op 3: registrar cliente con correo inválido", sistema.registrar_cliente,
         "Ana Ruiz", "52123456", "ana-correo", "3201112233")
ejecutar("Op 4: registrar cliente con documento inválido", sistema.registrar_cliente,
         "Pedro Díaz", "12AB", "pedro@correo.com", "3015556677")
ejecutar("Op 5: registrar cliente con parámetros faltantes", sistema.registrar_cliente,
         "Sofía Mora")

# --- Servicios: tres válidos, uno no disponible y dos inválidos ---
sala = ejecutar("Op 6: crear sala de reuniones (4 h)", sistema.registrar_servicio,
                ReservaSala, "Sala Ejecutiva", 80000, 10, 4)
equipo = ejecutar("Op 7: crear alquiler de portátiles (24 h)", sistema.registrar_servicio,
                  AlquilerEquipo, "Portátiles Pro", 15000, "Portátil i7", 24, 2)
asesoria = ejecutar("Op 8: crear asesoría en ciberseguridad (6 h)", sistema.registrar_servicio,
                    AsesoriaEspecializada, "Asesoría Ciberseguridad", 120000, "Ciberseguridad", 6)
proyector = ejecutar("Op 9: crear proyector no disponible", sistema.registrar_servicio,
                     AlquilerEquipo, "Proyector HD", 20000, "Proyector", 5, 1, False)
ejecutar("Op 10: crear sala con precio negativo", sistema.registrar_servicio,
         ReservaSala, "Sala Express", -5000, 8, 2)
ejecutar("Op 11: crear asesoría con 0 horas", sistema.registrar_servicio,
         AsesoriaEspecializada, "Asesoría Datos", 90000, "Analítica de datos", 0)

# --- Reservas: exitosas y fallidas ---
r1 = ejecutar("Op 12: reserva de sala con IVA 19 %", sistema.crear_reserva,
              laura, sala, 0.19)
ejecutar("Op 13: reserva de asesoría con IVA 19 % y descuento 10 %", sistema.crear_reserva,
         carlos, asesoria, 0.19, 0.10)
ejecutar("Op 14: reserva de equipo sin impuestos", sistema.crear_reserva,
         laura, equipo)
ejecutar("Op 15: reserva de un servicio no disponible", sistema.crear_reserva,
         carlos, proyector)
ejecutar("Op 16: reserva con impuesto inválido (150 %)", sistema.crear_reserva,
         laura, sala, 1.5)
ejecutar("Op 17: reserva sin cliente (parámetro faltante)", sistema.crear_reserva,
         None, sala)

# --- Operaciones no permitidas sobre reservas ya creadas ---
ejecutar("Op 18: confirmar una reserva que ya estaba confirmada", r1.confirmar)
ejecutar("Op 19: cancelar una reserva", r1.cancelar)
ejecutar("Op 20: cancelar de nuevo la misma reserva", r1.cancelar)

# --- Resumen final ---
print("\n--- CLIENTES REGISTRADOS ---")
for c in sistema.clientes:
    print(c.describir())

print("\n--- SERVICIOS REGISTRADOS ---")
for s in sistema.servicios:
    print(s.describir())                        # Polimorfismo: cada servicio se describe distinto

print("\n--- RESERVAS ---")
for r in sistema.reservas:
    print(r.describir())

print("\n--- ARCHIVO software_fj.log ---")
with open("software_fj.log", encoding="utf-8") as archivo:
    print(archivo.read())
