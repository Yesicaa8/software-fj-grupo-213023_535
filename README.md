Software fj – Sistema de reservas

Sistema orientado a objetos en **Python**, sin bases de datos, para gestionar **clientes, servicios y reservas** de la empresa Software FJ, con **manejo avanzado de excepciones** y archivo de logs.
Proyecto de la **Fase 4 – Programación (213023)**, UNAD – Ingeniería de Sistemas · **Grupo 213023_535**.

## ¿De qué trata?
Software FJ es una empresa que atiende **clientes** y ofrece **servicios**: reserva de salas, alquiler de equipos y asesorías especializadas. Un cliente puede hacer una **reserva** de un servicio por unas horas, y el sistema debe seguir funcionando aunque ocurran errores (datos inválidos, servicios no disponibles, reservas incorrectas). Cada evento y cada error quedan anotados en el archivo `software_fj.log`.

## Qué incluye
- Clase abstracta `Entidad` y clase `Cliente` con validaciones y datos encapsulados
- Clase abstracta `Servicio` y tres servicios especializados: `ReservaSala`, `AlquilerEquipo` y `AsesoriaEspecializada` (polimorfismo y métodos sobrescritos)
- Método sobrecargado de cálculo de costos: `calcular_costo_total()` con impuesto y descuento opcionales
- Clase `Reserva` (procesar, confirmar y cancelar) y clase `SistemaGestion`
- Excepciones personalizadas, `try/except/else/finally` y encadenamiento de excepciones
- Archivo de logs y simulación de 20 operaciones válidas e inválidas

## Reparto del trabajo

| Parte | Integrante | Qué desarrolla | Estado |
|---|---|---|---|
| 1 y 2 | Brayan Stiven Casas Cardenas | Logs, excepciones personalizadas, `Entidad` y `Cliente` | ✅ |
| 3 | Kelly Nathalia Mejia Narvaez | Clase `Servicio` y método sobrecargado `calcular_costo_total` | ✅ |
| 4 | María Alejandra Castillo Montenegro | `ReservaSala`, `AlquilerEquipo` y `AsesoriaEspecializada` | ✅ |
| 5 y 6 | Yesica Mendoza Torres | `Reserva`, `SistemaGestion` y simulación de operaciones | ✅ |

## Archivos
- `sistema-reservas-grupo-213023_535.ipynb`: proyecto completo (producto de entrega)
- `Fase 4.py`: el mismo código en un solo archivo de Python
- `software_fj.log`: archivo de logs generado al ejecutar

## Cómo ejecutarlo
1. Abrir el notebook con el botón **Abrir en Colab** de arriba.
2. Ejecutar las celdas en orden (*Entorno de ejecución → Ejecutar todo*).
3. Revisar el archivo `software_fj.log` que se genera.

**Curso:** Programación 213023 · **Grupo:** 213023_535
