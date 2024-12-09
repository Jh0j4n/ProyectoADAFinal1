def costo_min_din(cadena_inicial, cadena_destino, costo_insertar, costo_borrar, costo_reemplazar, costo_avanzar, costo_reemplazo_total):
    len_inicial, len_destino = len(cadena_inicial), len(cadena_destino)

    # Tabla para almacenar los costos mínimos y las operaciones
    costo = [[float('inf')] * (len_destino + 1) for _ in range(len_inicial + 1)]
    historial_operaciones = [[[] for _ in range(len_destino + 1)] for _ in range(len_inicial + 1)]
    
    uso_reemplazo_total = False

    # Caso base (cuando no hay ninguna operación realizada)
    costo[0][0] = 0
    historial_operaciones[0][0] = [(cadena_inicial, "Sin cambios")]

    for i in range(1, len_inicial + 1):
        costo[i][0] = costo[i - 1][0] + costo_borrar
        cadena_parcial = cadena_inicial[:i - 1]
        historial_operaciones[i][0] = historial_operaciones[i - 1][0] + [(cadena_parcial, f"Eliminar '{cadena_inicial[i - 1]}'")]

    for j in range(1, len_destino + 1):
        costo[0][j] = costo[0][j - 1] + costo_insertar
        cadena_parcial = historial_operaciones[0][j - 1][-1][0] + cadena_destino[j - 1]
        historial_operaciones[0][j] = historial_operaciones[0][j - 1] + [(cadena_parcial, f"Agregar '{cadena_destino[j - 1]}'")]

    for i in range(1, len_inicial + 1):
        for j in range(1, len_destino + 1):
            if cadena_inicial[i - 1] == cadena_destino[j - 1]:
                costo_avance_op = costo[i - 1][j - 1] + costo_avanzar
                nueva_cadena_avance = historial_operaciones[i - 1][j - 1][-1][0][:i - 1] + cadena_destino[j - 1] + historial_operaciones[i - 1][j - 1][-1][0][i:]
                tipo_operacion = "Avanzar"
            else:
                costo_reemplazo_op = costo[i - 1][j - 1] + costo_reemplazar
                nueva_cadena_reemplazo = historial_operaciones[i - 1][j - 1][-1][0][:i - 1] + cadena_destino[j - 1] + historial_operaciones[i - 1][j - 1][-1][0][i:]
                tipo_operacion = f"Reemplazar '{cadena_inicial[i - 1]}' por '{cadena_destino[j - 1]}'"

            costo_borrar_op = costo[i - 1][j] + costo_borrar
            nueva_cadena_borrar = historial_operaciones[i - 1][j][-1][0][:i - 1] + historial_operaciones[i - 1][j][-1][0][i:]

            costo_insertar_op = costo[i][j - 1] + costo_insertar
            nueva_cadena_insertar = historial_operaciones[i][j - 1][-1][0][:i] + cadena_destino[j - 1] + historial_operaciones[i][j - 1][-1][0][i:]

            costos_posibles = [costo_avance_op if cadena_inicial[i - 1] == cadena_destino[j - 1] else costo_reemplazo_op,
                               costo_borrar_op,
                               costo_insertar_op]

            operaciones_posibles = [(tipo_operacion if cadena_inicial[i - 1] == cadena_destino[j - 1] else f"Reemplazar '{cadena_inicial[i - 1]}' por '{cadena_destino[j - 1]}'", nueva_cadena_avance if cadena_inicial[i - 1] == cadena_destino[j - 1] else nueva_cadena_reemplazo),
                    (f"Eliminar '{cadena_inicial[i - 1]}'", nueva_cadena_borrar),
                    (f"Agregar '{cadena_destino[j - 1]}'", nueva_cadena_insertar)]

            # Aplicar operación "Reemplazo Total" si es necesario
            if j == len_destino and i > len_destino and not uso_reemplazo_total:
                costo_reemplazo_total_op = costo[i - 1][j] + costo_reemplazo_total
                nueva_cadena_reemplazo_total = cadena_destino
                costos_posibles.append(costo_reemplazo_total_op)
                operaciones_posibles.append(('Reemplazo total', nueva_cadena_reemplazo_total))
                uso_reemplazo_total = True

            # Elegir la operación con el menor costo
            costo_minimo = min(costos_posibles)
            indice_minimo = costos_posibles.index(costo_minimo)
            costo[i][j] = costo_minimo
            operacion_final, nueva_cadena = operaciones_posibles[indice_minimo]

            if "Reemplazar" in operacion_final or operacion_final == 'Avanzar':
                historial_operaciones[i][j] = historial_operaciones[i - 1][j - 1] + [(nueva_cadena, operacion_final)]
            elif "Agregar" in operacion_final:
                historial_operaciones[i][j] = historial_operaciones[i][j - 1] + [(nueva_cadena, operacion_final)]
            else:
                historial_operaciones[i][j] = historial_operaciones[i - 1][j] + [(nueva_cadena, operacion_final)]

            if nueva_cadena == cadena_destino:
                historial_operaciones[i][j].append((nueva_cadena, "Transformación completa"))
                return costo[i][j], historial_operaciones[i][j]

    return costo[len_inicial][len_destino], historial_operaciones[len_inicial][len_destino]


def mostrar_transformacion(cadena_inicial, pasos):
    estado_actual = list(cadena_inicial)
    print(f"{''.join(estado_actual):15} -> Sin cambios")
    indice_destino = 0  

    for paso in pasos[1:]:
        operacion = paso[1]
        
        if "Eliminar" in operacion:
            char_a_eliminar = operacion.split("'")[1]
            del estado_actual[indice_destino]
        
        elif "Agregar" in operacion:
            char_a_agregar = operacion.split("'")[1]
            estado_actual.insert(indice_destino, char_a_agregar)
            indice_destino += 1
        
        elif "Reemplazar" in operacion:
            nuevo_char = operacion.split("'")[3]
            estado_actual[indice_destino] = nuevo_char
            indice_destino += 1  
        
        elif "Avanzar" in operacion:
            estado_actual[indice_destino] = cadena_destino[indice_destino]
            indice_destino += 1
        
        elif "Reemplazo total" in operacion:
            estado_actual = list(cadena_destino)
            indice_destino = len(cadena_destino)  
        
        print(f"{''.join(estado_actual):15} -> {operacion}")


# Definición de costos
costo_insertar = 2
costo_borrar = 2
costo_reemplazar = 3
costo_avanzar = 1
costo_reemplazo_total = 1

cadena_inicial = ""
cadena_destino = ""

costo_final, pasos_transformacion = costo_min_din(cadena_inicial, cadena_destino, costo_insertar, costo_borrar, costo_reemplazar, costo_avanzar, costo_reemplazo_total)
