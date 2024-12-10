def generar_combinacionesDP(A, oferentes, B):
    num_oferentes = len(oferentes)
    dp = [[0] * (A + 1) for _ in range(num_oferentes + 1)]
    
    for i in range(1, num_oferentes + 1):
        pi, mi, Mi = oferentes[i - 1]
        for j in range(A + 1):
            dp[i][j] = dp[i - 1][j]
            for k in range(mi, min(Mi, j) + 1):
                dp[i][j] = max(dp[i][j], dp[i - 1][j - k] + k * pi)

    max_ingreso = dp[num_oferentes][A]
    
    mejor_combinacion = [0] * num_oferentes
    j = A
    for i in range(num_oferentes, 0, -1):
        pi, mi, Mi = oferentes[i - 1]
        for k in range(mi, min(Mi, j) + 1):
            if dp[i][j] == dp[i - 1][j - k] + k * pi:
                mejor_combinacion[i - 1] = k
                j -= k
                break

    acciones_gobierno = A - sum(mejor_combinacion)
    max_ingreso += acciones_gobierno * B

    # Solo añadir acciones del gobierno si hay sobrantes
    if acciones_gobierno > 0:
        mejor_combinacion.append(acciones_gobierno)

    return mejor_combinacion, acciones_gobierno, max_ingreso



def recopilar_datos():
    A = int(input("Ingrese el total de acciones (A): "))
    B = int(input("Ingrese el precio mínimo por acción (B): "))
    
    num_oferentes = int(input("Ingrese la cantidad de oferentes: "))
    oferentes = []
    
    for i in range(num_oferentes):
        print(f"\nOferente {i + 1}:")
        pi = int(input("  Ingrese el precio por acción (pi): "))
        mi = int(input("  Ingrese el número mínimo de acciones a comprar (mi): "))
        Mi = int(input("  Ingrese el número máximo de acciones a comprar (Mi): "))
        oferentes.append((pi, mi, Mi))
    
    return A, B, oferentes,

if __name__ == "__main__":
    A, B, oferentes = recopilar_datos()
    mejor_combinacion, acciones_gobierno, max_ingreso = generar_combinacionesDP(A, oferentes, B)

    # Imprimir los resultados
    print(f"\nMejor Combinación (Cantidad de acciones por oferente y gobierno): {mejor_combinacion}")
    print(f"Acciones compradas por el gobierno: {acciones_gobierno}")
    print(f"Máximo Ingreso: {max_ingreso}")
