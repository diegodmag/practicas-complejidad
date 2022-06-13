
#Primero vamos a modelar una solucinon y su representacion grafica 
#Recordemos que una solucion tiene una representacion genetica 
# y una representacion grafica 
# La representacion genetica es rep_gen = (q_1, ...., q_2), donde indexOf(q_i) = columna de la reina 
#   
#                                                        donde rep_gen[i] = posicion de la fila de la reina 
'''
Clase que modela la solucion para el problema de las n-reinas a partir
de una representacion genetica, es decir una tupla 
'''

#Conideremos que cada solucion tiene un cromosoma el cual va a ser afectado por la mutacion 

from sympy import re


class Solucion: 

    def __init__(self, num_reinas):
        self.__num_reinas = num_reinas
        self.__cromosoma = [0]*num_reinas
        self.__rep_tablero = [ [0 for i in range(num_reinas) ] for j in range(num_reinas)] 

    def __str__(self): 
        return "Cromosoma :"+str(self.__cromosoma)+"\n"+"Tablero :"+str(self.__rep_tablero)


    @property
    def cromosoma(self):
        return self.__cromosoma
    
    @property
    def rep_tablero(self): 
        return self.__rep_tablero

    #Notemos que cromosoma es un arreglo entonces hay que tener cuidado con este metodo
    #Tal vez sea pertinente un metodo que modifique un gen del cromosoma 
    def set_cromosoma(self, cromosoma):
        self.__cromosoma = cromosoma

    #Revisar la forma en la que se presenta 
    def generar_tablero(self):

        tablero = ""

        for fila in self.__rep_tablero:
            tablero = tablero+str(fila)+"\n"
    
        return tablero

def ejecucion(): 

    sol_1 = Solucion(8)
    #print(sol_1)
    print(sol_1.generar_tablero())

if __name__ == '__main__': 
    ejecucion()