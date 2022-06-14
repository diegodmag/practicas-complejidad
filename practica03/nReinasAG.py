import random as rnd 
import numpy as np
import math


'''
Clase que modela la solucion para el problema de las n-reinas a partir
de una representacion genetica, es decir una tupla 
'''

#Conideremos que cada solucion tiene un cromosoma el cual va a ser afectado por la mutacion 

from sympy import false, re, true


class Solucion: 

    def __init__(self, num_reinas):
        self.__num_reinas = num_reinas
        #El cromosoma es la tupla que representa la posicion de las reinas 
        #Por lo que un gen es una posicion en especifico 
        self.__cromosoma = [-1]*num_reinas
        self.__rep_tablero = [ [-1 for i in range(num_reinas) ] for j in range(num_reinas)] 

    def __str__(self): 
        return "Cromosoma :"+str(self.__cromosoma)+"\n"+"Tablero :"+str(self.__rep_tablero)


    @property
    def cromosoma(self):
        return self.__cromosoma
    
    @property
    def rep_tablero(self): 
        return self.__rep_tablero

    def set_cromosoma(self, cromosoma):
        self.__cromosoma = cromosoma

    '''
    Metodo que modifica un gen del cromosoma dado un indice 
    Args : 
        i : indice del gene en el cromosoma a modificar 
        gen : nuevo valor del gen 
    '''
    def set_gen(self, i, gen): 
        self.cromosoma[i] = gen 

    '''
    Metodo que genera el tablero  
    '''
    #FALRA IMPLEMENTAR IMPORTANTE  
    def generar_tablero(self):

        tablero = ""

        for fila in self.__rep_tablero:
            tablero = tablero+str(fila)+"\n"
    
        return tablero
    '''
    Metodo que asigna de forma aleatoria los genes del cromosoma del la solucion 
    '''
    def randomizar_genes(self): 
        #Debo de generar una distribucion aleatoria de los numeros de 0 a num_reinas 
        #Cuando se genera un numero se revisa que no este en la lista 
        for i in range(len(self.__cromosoma)): 
            flag = true
            while flag: 
                new_gen = rnd.randint(0,self.__num_reinas-1)
                if new_gen in self.__cromosoma:
                    continue
                else :
                   self.__cromosoma[i] = new_gen
                   flag = false

       
'''
Clase que modela el algortimmo genetico para el problema de las n reinas 
'''
class AG: 

    def __init__(self, num_reinas, num_ind, max_gen, porc_new_ind, porc_mut):
        self.__num_reinas = num_reinas
        self.__num_ind = num_ind
        self.__max_gen = max_gen
        self.__porc_new_ind = porc_new_ind
        self.__porc_mut = porc_mut
        self.__actual_pop = self.get_initial_pop()

    '''
    Genera una poblacion de soluciones con cromosomas 
    generados de manera aleatoria  
    '''
    def get_initial_pop(self):
        init_pop = []
        for i in range(self.__num_ind):
            sol = Solucion(self.__num_reinas)
            sol.randomizar_genes()
            init_pop.append(sol) 
        return init_pop

    '''
    Funcion fitness basada en la diferencia ||q_{i} - q_{j} || == ? ||i - j||
    Args : 
        sol : La solucion a evaluar 
    Return : 
        conflictos : Numero de conflictos encontrados (Una solucion optima tiene 0 conflictos )
    '''
    def fun_fitness(self, sol): 
        conflictos = 0 
        for gen in sol.cromosoma:
            for gen_2 in sol.cromosoma:
                if gen != gen_2 : 
                    diff_filas = abs(gen - gen_2)
                    diff_colums = abs(sol.cromosoma.index(gen)-sol.cromosoma.index(gen_2))
                    if diff_filas == diff_colums:
                        conflictos = conflictos + 1
        
        return conflictos
    '''
    Seleccion por torneo, se consideran dos soluciones de forma aleatoria y 
    se selecciona la solucion con el menor valor de valor de fitness  
    Args : 
        population : poblacion de la cual se hara el torneo 
    Returns : 
        winnners : Un arreglo con los mejores candidatos dado un emparejamiento aleatorio
    '''
    def selection_by_tournament(self, population):

        temp = population 
        tournament = []
        while temp != []: 
            #Se escogen dos elementos de forma al azar 
            pair = rnd.sample(temp,2)
            tournament.append(pair)
            temp.remove(pair[0])
            temp.remove(pair[1])

        winners = []
        for pair in tournament: 
            #Se considera el minimo por que la funcion fitness es mas optima mientras mas cercana al 0 sea 
            winer_value = min(self.fun_fitness(pair[0]), self.fun_fitness(pair[1]))
            if winer_value == self.fun_fitness(pair[0]):
                winners.append(pair[0])
            else : 
                winners.append(pair[1])
        
        
        return winners
    
    '''
    Metodo que le asigna a cada individuo de una poblacion dada la probalidad de ser seleccionado 
    Args:
        population : La poblacion de donde se obtienen las probabilidades  
    Returns: 
        select_prob : Un arreglo que contiene la probabilidad de cada individuo de ser selccionado 

    Notes : Buscamos que mientras mas cercano sea  0 el valor de fitness de una solucion mas probable 
            es que sea considerada, las probabilidades no pueden ser fitness/total_fitness, ya que esto
            produciria que los que tienen mayor fitness puedan ser seleccionados con mayor probabilidad,
            por lo que para evitar esto generamos un valor temporar de fitness en donde calculmaos el 
            total de finess y le sustremos el valor original de la solucion, obteniendo un valor "inverso"
            de fitness el cual ahora si nos sirve para calcular la probabilidad basandonos en que mientras 
            mayor sea el valor de fitness de una solucion, menor sera la probabilidad de ser seleccionado
    '''
    def select_probability(self, population):

        total_fitness = 0 
        select_prob = []
        temp_fitness = 0

        for sol in population: 
            total_fitness += self.fun_fitness(sol)

        for sol in population: 
            temp_fitness += abs(total_fitness-self.fun_fitness(sol)) 


        for sol in population:
            #La probabilidad es 1 - fitness/total_fitness por que mientras menor sea 
            #el valor de fitness, mejor candidata es la solucion 
            select_prob.append((abs(total_fitness-self.fun_fitness(sol)) / temp_fitness)) 

        return select_prob

    '''
    Metodo que elige los candidatos a reproduccion dada una probilidad basada en su valor de fitness 
    Args : 
        population : La poblacion de donde se obtienen candidatos 
    Returns : 
        winners : Un arreglo con los mejores candidatos dadas las probabilidades de ser escogidos  
    '''
    def selection_by_roulette(self, population): 
        
        probabilities = self.select_probability(population)
        winners = np.random.choice(population,2,replace=False,p=probabilities)
        return winners


    '''
    Implementacion de la operacion crossover entre dos cromosomas que parte aproximadamente a la mitad
    '''
    def crossover_2_points(self, sol_1, sol_2): 
        c = math.floor(self.__num_reinas/2)
        new_cromosome_1 = sol_1.cromosoma[0:c] + sol_2.cromosoma[c:len(sol_2.cromosoma)]
        new_cromosome_2 = sol_2.cromosoma[0:c] + sol_1.cromosoma[c:len(sol_1.cromosoma)]
        child_1 = Solucion(self.__num_reinas)
        child_1.set_cromosoma(new_cromosome_1)
        child_2 = Solucion(self.__num_reinas)
        child_2.set_cromosoma(new_cromosome_2)

        return child_1, child_2
    
    


    #ELIMINAR 

    def mostrar_global_fitness(self, pop): 
        for sol in pop: 
            print(str(sol.cromosoma) + " fitness :"+str(self.fun_fitness(sol)))


    def mostrar_ruleta(self): 
        self.mostrar_global_fitness(self.__actual_pop)
        print("#########")
        winners = self.selection_by_roulette(self.__actual_pop)
        for sol in winners: 
            print(sol.cromosoma)

        child_1, child_2 = self.crossover_2_points(winners[0],winners[1])
        print("#########")
        print(str(child_1.cromosoma))
        print(str(child_2.cromosoma))


    def mostrar_torneo(self): 
        self.mostrar_sols()
        print("#####")
        tour,win = self.selection_tournament()
        
        for x in tour : 
            print(str(x[0].cromosoma) + " fitnes: "+str(self.fun_fitness(x[0]))+" VS " + str(x[1].cromosoma)+" fitnes: "+str(self.fun_fitness(x[1])))

        print("#####")
        print("WINNERS")
        for w in win: 
            print(str(w.cromosoma))

    #ELIMINAR
    def mostrar_fitness(self):
        init_pop = self.get_initial_pop()
        for x in init_pop:
            print(self.fun_fitness(x))

    #ELIMINAR 
    def mostrar_sols(self): 
        #init_pop = self.get_initial_pop()
        for x in self.__actual_pop: 
            print(x.cromosoma)


def ejecucion(): 

    #sol_1 = Solucion(8)
    #print(sol_1)
    #print(sol_1)
    #sol_1.genes_randomization()
    #print(sol_1)
    #print(sol_1.generar_tablero())
    genetic = AG(8,10,250,0.96,.15)
    #genetic.mostrar_sols()
    #genetic.selection_tournament()
    genetic.mostrar_ruleta()
    #genetic.mostrar_torneo()
    #genetic.mostrar_fitness()

if __name__ == '__main__': 
    ejecucion()