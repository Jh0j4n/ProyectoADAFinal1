def advance(word1, word2, i, j):
    if i < len(word1) and j < len(word2) and word1[i] == word2[j]:
        return word1, word2, i + 1, j + 1
    return word1, word2, i, j
def delete(word1,word2,i,j):
    word1.pop(i)
    return word1,word2,i,j
def replace(word1,word2,i,j):
    word1[i] = word2[j]
    return word1,word2,i+1,j+1
def insert(word1,word2,i,j):
    word1.insert(i, word2[j])
    return word1,word2,i+1,j+1
def kill(word1,word2,i,j):
    word1 = word1[:i]
    return word1,word2,i,j
#
advance_Cost = 1
delete_Cost = 12
replace_Cost = 1
insert_Cost = 1
kill_Cost = 16
#
# Python
def calcular_mejor_coste(word1, word2, i, j, advance_Cost, delete_Cost, replace_Cost, insert_Cost, kill_Cost, operaciones, costos):
    if i == len(word1) and j == len(word2):
        return [(costos, operaciones)]
    results = []
    if i == len(word1):  
        word1, word2, i, j = insert(word1[:], word2[:], i, j)
        new_operaciones = operaciones + ['insert '+ ''.join(word1)]
        new_costos = costos + [insert_Cost]
        results.extend(calcular_mejor_coste(word1, word2, i, j, advance_Cost, delete_Cost, replace_Cost, insert_Cost, kill_Cost, new_operaciones, new_costos))
    
    elif j == len(word2):  
        to_delete = len(word1[i:])
        if to_delete * delete_Cost < kill_Cost:
            word1, word2, i, j = delete(word1[:], word2[:], i, j)
            new_operaciones = operaciones + ['delete '+ ''.join(word1[:])]
            new_costos = costos + [delete_Cost]
            results.extend(calcular_mejor_coste(word1, word2, i, j, advance_Cost, delete_Cost, replace_Cost, insert_Cost, kill_Cost, new_operaciones, new_costos))
        else:
            word1, word2, i, j = kill(word1[:], word2[:], i, j)
            new_operaciones = operaciones + ['kill '+ ''.join(word1[:])]
            new_costos = costos + [kill_Cost]
            results.extend(calcular_mejor_coste(word1, word2, i, j, advance_Cost, delete_Cost, replace_Cost, insert_Cost, kill_Cost, new_operaciones, new_costos))
    
    else:
        if word1[i] == word2[j]:  # Advance if characters are equal
            word1, word2, i, j = advance(word1[:], word2[:], i, j)
            new_operaciones = operaciones + ['advance '+ ''.join(word1[:])]
            new_costos = costos + [advance_Cost]
            results.extend(calcular_mejor_coste(word1, word2, i, j, advance_Cost, delete_Cost, replace_Cost, insert_Cost, kill_Cost, new_operaciones, new_costos))
       
        else:

            word1_ins, word2_ins, i_ins, j_ins = insert(word1[:], word2[:], i, j)
            new_operaciones_ins = operaciones + ['insert '+ ''.join(word1[:])]
            new_costos_ins = costos + [insert_Cost]
            results.extend(calcular_mejor_coste(word1_ins, word2_ins, i_ins, j_ins, advance_Cost, delete_Cost, replace_Cost, insert_Cost, kill_Cost, new_operaciones_ins, new_costos_ins))
            
            # Delete
            word1_del, word2_del, i_del, j_del = delete(word1[:], word2[:], i, j)
            new_operaciones_del = operaciones + ['delete '+ ''.join(word1[:])]
            new_costos_del = costos + [delete_Cost]
            results.extend(calcular_mejor_coste(word1_del, word2_del, i_del, j_del, advance_Cost, delete_Cost, replace_Cost, insert_Cost, kill_Cost, new_operaciones_del, new_costos_del))
            
            # Replace
            word1_rep, word2_rep, i_rep, j_rep = replace(word1[:], word2[:], i, j)
            new_operaciones_rep = operaciones + ['replace '+ ''.join(word1[:])]
            new_costos_rep = costos + [replace_Cost]
            results.extend(calcular_mejor_coste(word1_rep, word2_rep, i_rep, j_rep, advance_Cost, delete_Cost, replace_Cost, insert_Cost, kill_Cost, new_operaciones_rep, new_costos_rep))
            
            # Kill
            word1_kill, word2_kill, i_kill, j_kill = kill(word1[:], word2[:], i, j)
            new_operaciones_kill = operaciones + ['kill ' + ''.join(word1[:])]
            new_costos_kill = costos + [kill_Cost]
            results.extend(calcular_mejor_coste(word1_kill, word2_kill, i_kill, j_kill, advance_Cost, delete_Cost, replace_Cost, insert_Cost, kill_Cost, new_operaciones_kill, new_costos_kill))
    
    return results
def tupla_con_menor_suma(lista_de_tuplas):
    return min(lista_de_tuplas, key=lambda tupla: sum(tupla[0]))

def main():
    costos1 = []
    operaciones = []
    string = "abcdf"
    word1 = list(string)
    string2 = "abcd"
    word2 = list(string2)

    results = tupla_con_menor_suma(calcular_mejor_coste(word1[:], word2[:], 0, 0, advance_Cost, delete_Cost, replace_Cost, insert_Cost, kill_Cost, operaciones, costos1))
    for a in results:
        print(a)

if __name__ == "__main__":
    main()
   