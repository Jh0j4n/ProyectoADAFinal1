from typing import List, Tuple

class TransformationResult:
    def __init__(self, cost: int, steps: List[Tuple[str, str]]):
        self.cost = cost
        self.steps = steps
 
class interfaz_voraz:
    def __init__(self, source: str, objetivo: str, costs: dict = None):
        #Asignacion de datos para hacer la transformacion
        self.source = source
        self.objetivo = objetivo
        self.costs = costs
    
    def transform(self):
        # Index actual de la palabra de origen a la objetivo
        i, j = 0, 0  
        #Estado actual de la lista source
        estado_actual = self.source
        #Costo total
        costo_total = 0
        #Lista de operaciones
        operaciones = []
        #Booleano para ver si killed se a usado
        kill_used = False
        
        while i < len(estado_actual) and j < len(self.objetivo):
            #En caso de que las 2 letras en las posiciones i,j sean iguales:
            if estado_actual[i] == self.objetivo[j]:
                #Avanzar
                operaciones.append((estado_actual, "advance"))
                i, j = i + 1, j + 1
                costo_total += self.costs['advance']
                #Si no son iguales se envia a la mejor opcion posible 
            else:
                operacion, new_state, new_x, new_y, cost = self.mejor_opcion(
                    estado_actual, i, j, kill_used
                )
                
                if operacion.startswith("kill"):
                    kill_used = True
                
                estado_actual = new_state
                i, j = new_x, new_y
                costo_total += cost
                operaciones.append((estado_actual, operacion))
                
                if kill_used:
                    break
        
        # Continuar con las letras que no se han actualizado
        costo_total, operaciones = self.letras_faltantes(
            estado_actual, i, j, costo_total, operaciones, kill_used
        )
        
        return costo_total, operaciones
    
    def mejor_opcion(self, actual, i, j, kill_used):
        chars_remaining = len(actual) - i
        kill_cost = self.costs['kill']
        
        #Mira si kill es mejor opcion
        if not kill_used and kill_cost <= chars_remaining * self.costs['delete']:
            return (
                "kill",
                actual[:i],
                i,
                j,
                kill_cost
            )
        
        #Comparacion de costos donde se tomara la desicion
        operaciones = {
            'replace': (
                f"replace '{actual[i]}' with '{self.objetivo[j]}'",
                actual[:i] + self.objetivo[j] + actual[i+1:],
                i + 1,
                j + 1,
                self.costs['replace']
            ),
            'delete': (
                f"delete '{actual[i]}'",
                actual[:i] + actual[i+1:],
                i,
                j,
                self.costs['delete']
            ),
            'insert': (
                f"insert '{self.objetivo[j]}'",
                actual[:i] + self.objetivo[j] + actual[i:],
                i,
                j + 1,
                self.costs['insert']
            )
        }
        
        '''
        Con esta funcion de lambda encontramos las operaciones con menor costo 
        basado en lo que se elijio arriba por metodo voraz
        '''
        mejor_operacion = min(operaciones.values(), key=lambda x: x[4])
        
        return mejor_operacion
    
    def letras_faltantes(self, actual, i, j, costo_total, operaciones, kill_used):
        
        #Si ya se alcanzo el maximo lo unico que queda es insertar
        while j < len(self.objetivo):
            actual += self.objetivo[j]
            operaciones.append((actual, f"insert '{self.objetivo[j]}'"))
            costo_total += self.costs['insert']
            j += 1
        
        #Matar si ya se tiene lo mismo pero aun hay letras de sobra
        if i < len(actual) and not kill_used:
            actual = actual[:i]  
            operaciones.append((actual, "kill from cursor to end"))
            costo_total += self.costs['kill']
        
        return costo_total, operaciones


def main():
    # Example usage
    original = "hambre"
    objetivo = "hola"
    
    costos = {
        'advance': 1,  # a
        'delete': 2,   # d
        'replace': 3,  # r
        'insert': 2,   # i
        'kill': 10    # k
    }
    
    transformer = interfaz_voraz(original, objetivo, costos)
    min_cost, steps = transformer.transform()
    
    print(f"El costo mínimo para transformar '{original}' en '{objetivo}' es: {min_cost}")
    print("\nPasos de la transformación:")
    for state, operacion in steps:
        print(f"{state:<15} -> {operacion}")

if __name__ == "__main__":
    main()