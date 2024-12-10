def costo_min_din(cadena_inicial, cadena_destino, costo_insertar, costo_borrar, costo_reemplazar, costo_avanzar, costo_reemplazo_total):
    len_inicial, len_destino = len(cadena_inicial), len(cadena_destino)

    # Tabla para almacenar los costos mínimos y las operaciones
    costo = [[float('inf')] * (len_destino + 1) for _ in range(len_inicial + 1)]
    historial_operaciones = [[[] for _ in range(len_destino + 1)] for _ in range(len_inicial + 1)]

    # Caso base (cuando no hay ninguna operación realizada)
    costo[0][0] = 0
    historial_operaciones[0][0] = [(cadena_inicial, "Sin cambios")]

    for i in range(1, len_inicial + 1):
        costo[i][0] = costo[i - 1][0] + costo_borrar
        cadena_parcial = cadena_inicial[:i - 1]
        historial_operaciones[i][0] = historial_operaciones[i - 1][0] + [(cadena_parcial, f"Eliminar '{cadena_inicial[i - 1]}'")]

    for j in range(1, len_destino + 1):
        costo[0][j] = costo[0][j - 1] + costo_insertar
        cadena_parcial = cadena_destino[:j]
        historial_operaciones[0][j] = historial_operaciones[0][j - 1] + [(cadena_parcial, f"Agregar '{cadena_destino[j - 1]}'")]

    for i in range(1, len_inicial + 1):
        for j in range(1, len_destino + 1):
            if cadena_inicial[i - 1] == cadena_destino[j - 1]:
                costo_avance_op = costo[i - 1][j - 1] + costo_avanzar
                historial_avance = historial_operaciones[i - 1][j - 1] + [(cadena_destino[:j], "Avanzar")]
                opciones = [(costo_avance_op, historial_avance)]
            else:
                costo_reemplazo_op = costo[i - 1][j - 1] + costo_reemplazar
                historial_reemplazo = historial_operaciones[i - 1][j - 1] + [
                    (cadena_destino[:j], f"Reemplazar '{cadena_inicial[i - 1]}' por '{cadena_destino[j - 1]}'")
                ]
                opciones = [(costo_reemplazo_op, historial_reemplazo)]

            costo_borrar_op = costo[i - 1][j] + costo_borrar
            historial_borrar = historial_operaciones[i - 1][j] + [
                (cadena_inicial[:i - 1], f"Eliminar '{cadena_inicial[i - 1]}'")
            ]
            opciones.append((costo_borrar_op, historial_borrar))

            costo_insertar_op = costo[i][j - 1] + costo_insertar
            historial_insertar = historial_operaciones[i][j - 1] + [
                (cadena_destino[:j], f"Agregar '{cadena_destino[j - 1]}'")
            ]
            opciones.append((costo_insertar_op, historial_insertar))

            if i == len_inicial and j == len_destino:
                costo_reemplazo_total_op = costo[i - 1][j] + costo_reemplazo_total
                historial_reemplazo_total = historial_operaciones[i - 1][j] + [
                    (cadena_destino, "Reemplazo total")
                ]
                opciones.append((costo_reemplazo_total_op, historial_reemplazo_total))

            # Elegir la operación con el menor costo
            costo[i][j], historial_operaciones[i][j] = min(opciones, key=lambda x: x[0])

    return costo[len_inicial][len_destino], historial_operaciones[len_inicial][len_destino]


def mostrar_transformacion(cadena_inicial, pasos):
    print(f"{cadena_inicial:15} -> Sin cambios")
    for paso in pasos[1:]:
        cadena, operacion = paso
        print(f"{cadena:15} -> {operacion}")


# Definición de costos
costo_insertar = 2
costo_borrar = 2
costo_reemplazar = 3
costo_avanzar = 1
costo_reemplazo_total = 5

# Prueba del código
cadena_inicial = ""
cadena_destino = ""

costo_final, pasos_transformacion = costo_min_din(
    cadena_inicial, cadena_destino, costo_insertar, costo_borrar, costo_reemplazar, costo_avanzar, costo_reemplazo_total
)


