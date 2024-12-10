A = 1000
B = 100
#           (precio por acción, mínimo de acciones, máximo de acciones)
ofertas = [(500, 100, 600), (450, 400, 800)]#2 oferentes, n = 2
gobierno = (100, 0, 1000)

#asignacion es la lista de acciones asignadas a cada oferente,ejemplo:[500,400] o [600,400]
def calcular_valor(asignacion, ofertas, gobierno, A):
    vr = 0 #inicializamos el valor recibido en 0
    #i es el indice de la lista, xi el valor que esta tomando de la lista
    #ejemplo:[500,400] i = 0, xi = 500 - i = 1, xi = 400
    for i, xi in enumerate(asignacion):
    #pi = precio por acción del oferente i
    #mi = mínimo de acciones del oferente i
    #Mi = máximo de acciones del oferente i
        #desempaquetamos la tupla, si ofertas[0] = (500, 100, 600) entonces pi = 500, mi = 100, Mi = 600
        pi, mi, Mi = ofertas[i]
        #multiplicamos el precio por acción(pi) por el número de acciones asignadas(xi)
        vr += xi * pi

    acciones_restantes = A - sum(asignacion)
    vr += acciones_restantes * gobierno[0]#las acciones restantes se asignan al gobierno
    return vr


def asignar_acciones(A, oferentes):
    asignacion = []
    acciones_disponibles = A
# key = lambda define una funcione anonima, key es el criterio de ordenamiento
#sorted ordena de forma ascendente, -x lo hace de forma descendente, es decir que tenemos:
#orden ascendente:
#(500, 100, 600), (450, 400, 800), (600, 200, 700) = (450, 400, 800), (500, 100, 600), (600, 200, 700)
#orden descendente:
#(600, 200, 700), (500, 100, 600), (450, 400, 800)
    ofertas_ordenadas = sorted(oferentes, key = lambda x: -x[0])#x[0] es el precio por acción(primera posicion de la tupla)
    #extraemos los valores de la tupla
    #pi = precio por acción del oferente i, mi = mínimo de acciones del oferente i, Mi = máximo de acciones del oferente i
    for pi, mi , Mi in ofertas_ordenadas:#Python me obliga a pone pi :b, tuki
    #condicion de asignacion de acciones #1: si se puede asignar el minimo,como?
    #revisamosel minimo que pide el oferente mi con las disponiles
        if acciones_disponibles >= mi:
        #asignamos el maximo entre el minimo y el maximo permitido
            asignar = min(Mi, acciones_disponibles)
            asignacion.append(asignar)
            acciones_disponibles -= asignar#solo restamos las acciones asignadas a las disponibles
             # Si no se pueden asignar las acciones mínimas, no se asigna ninguna a ese oferente.        
        else:
            asignacion.append(0)
    #retornamos la lista de asignaciones
    return asignacion

if __name__ == "__main__":
    asignacion = asignar_acciones(A, ofertas)
    valor = calcular_valor(asignacion, ofertas, gobierno, A)
    print(f'Asignación: {asignacion}')
    print(f'Valor recibido: {valor}')