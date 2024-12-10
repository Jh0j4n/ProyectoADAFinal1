def generar_combinaciones(A, oferentes, B, gobierno):
    def Combinacion_recursiva(OferActual, ActualSuma, ActualCombinacion):
        if ActualSuma == A: 
            combinations.append(ActualCombinacion[:])
            return
        if OferActual == len(oferentes) or ActualSuma > A:
            return
        
        minival = oferentes[OferActual][1]
        maxival = oferentes[OferActual][2]
        
        for value in range(minival, maxival + 1):
            if ActualSuma + value <= A:  
                ActualCombinacion.append(value)
                Combinacion_recursiva(OferActual + 1, ActualSuma + value, ActualCombinacion)
                ActualCombinacion.pop()
    
    def calcular_ingreso(combinacion):
        ingreso = 0
        for i in range(len(combinacion)):
            ingreso += combinacion[i] * oferentes[i][0]
        Acciones_Sobrantes = A - sum(combinacion) 
        ingreso += Acciones_Sobrantes * B 
        return ingreso
    
    oferentes.append(gobierno)  
    
    combinations = []
    Combinacion_recursiva(0, 0, [])  

    ingresos = []
    for combinacion in combinations:
        ingresos.append(calcular_ingreso(combinacion))
    
    MaxIngreso = 0
    MejorCombinacion = []
    for combinacion, ingreso in zip(combinations, ingresos):
        if ingreso > MaxIngreso:
            MaxIngreso = ingreso
            MejorCombinacion = combinacion
    
    return MejorCombinacion, MaxIngreso

def recopilar_datos():
    A = int(input("Ingrese el total de acciones (A): "))
    B = int(input("Ingrese el precio mínimo por acción (B): "))
    
    NumOferentes = int(input("Ingrese la cantidad de oferentes: "))
    oferentes = []
    
    for i in range(NumOferentes):
        print(f"\nOferente {i + 1}:")
        pi = int(input("  Ingrese el precio por acción (pi): "))
        mi = int(input("  Ingrese el número mínimo de acciones a comprar (mi): "))
        Mi = int(input("  Ingrese el número máximo de acciones a comprar (Mi): "))
        oferentes.append((pi, mi, Mi))
    
    gobierno = (B, 0, A) 
    return A, B, oferentes, gobierno

if __name__ == "__main__":
    A, B, oferentes, gobierno = recopilar_datos()
    MejorCombinacion, MaxIngreso = generar_combinaciones(A, oferentes, B, gobierno)
    print(f"\nMejor Combinación: {MejorCombinacion}")
    print(f"Máximo Ingreso: {MaxIngreso}")
