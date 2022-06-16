import random as rnd 
import numpy as np
import math
import copy 



'''
Clase que modela la solucion para el problema de las n-reinas a partir
de una representacion genetica, es decir una tupla 
'''

#Conideremos que cada solucion tiene un cromosoma el cual va a ser afectado por la mutacion 

class Solucion: 

    def __init__(self, num_reinas):
        self.__num_reinas = num_reinas
        #El cromosoma es la tupla que representa la posicion de las reinas 
        #Por lo que un gen es una posicion en especifico 
        self.__cromosoma = [-1]*num_reinas
        self.__rep_tablero = [ ["-" for i in range(num_reinas) ] for j in range(num_reinas)] 

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

        # El indice del arreglo es la columna 
        # El valor es el renglon 

        for i in range(len(self.cromosoma)):
            self.rep_tablero[i][self.cromosoma[i]] = "R"


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
            flag = True
            while flag: 
                new_gen = rnd.randint(0,self.__num_reinas-1)
                if new_gen in self.__cromosoma:
                    continue
                else :
                   self.__cromosoma[i] = new_gen
                   flag = False

       
'''
Clase que modela el algortimmo genetico para el problema de las n reinas 
'''
class AG: 

    def __init__(self, num_reinas, num_ind, max_gen, porc_new_ind, porc_mut):
        self.__num_reinas = num_reinas
        self.__num_ind = num_ind
        self.__max_gen = max_gen
        self.__porc_new_ind = porc_new_ind
        self.__num_new_ind = (int)(self.__num_ind*self.__porc_new_ind)
        self.__porc_mut = porc_mut
        self.__actual_pop = self.get_initial_pop()
        self.__objetive_fitness = 0.0 

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

        for i in range(len(sol.cromosoma)):
            for j in range(len(sol.cromosoma)): 
                if(i != j):
                    dx = abs(i-j)
                    dy = abs(sol.cromosoma[i]-sol.cromosoma[j])
                    if(dx ==  dy): 
                        conflictos+=1 

        return (self.__num_reinas*(self.__num_reinas-1))/2 - conflictos


    def two_random_matching(self,population):
        temp = copy.deepcopy(population)
        temp = temp.tolist() 
        matching = []
        while temp != []: 
            #Se escogen dos elementos de forma al azar 
            pair = rnd.sample(temp,2)
            matching.append(pair)
            temp.remove(pair[0])
            temp.remove(pair[1]) 

        return matching
    '''
    Seleccion por torneo, se consideran dos soluciones de forma aleatoria y 
    se selecciona la solucion con el menor valor de valor de fitness, 
    Args : 
        population : poblacion de la cual se hara el torneo 
    Returns : 
        winnners : Un arreglo con los mejores candidatos dado un emparejamiento aleatorio
    Note : Es necesario que la poblacion sea divisible entre dos 
    '''
    def selection_by_tournament(self, population):

        tournament = self.two_random_matching(population)

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
       

        for sol in population: 
            total_fitness += self.fun_fitness(sol)

        for sol in population:
            select_prob.append(self.fun_fitness(sol)/total_fitness) 

        return select_prob

    '''
    Metodo que elige los candidatos a reproduccion dada una probilidad basada en su valor de fitness 
    Args : 
        population : La poblacion de donde se obtienen candidatos 
    Returns : 
        winners : Un arreglo con los mejores candidatos dadas las probabilidades de ser escogidos  
    '''
    def selection_by_roulette(self, population): 
        #num_parents_selected = (int)(self.__num_ind*self.__porc_new_ind)
        num_winners = self.__num_new_ind
        #Se toma un numero par de individuos para hacer el crossover 
        if num_winners%2 != 0: 
            num_winners = num_winners+1
            self.__num_new_ind = num_winners
        probabilities = self.select_probability(population)
        winners = np.random.choice(population,num_winners,replace=False,p=probabilities)
        return winners


    '''
    Implementacion de la operacion crossover entre dos cromosomas que parte aproximadamente a la mitad
    Args : 
        sol_1 : Primer padre 
        sol_2 : Segundo padre 
    Returns : 
        child_1 : Primer hijo generado pro crossover en 2 puntos
        child_2 : Segunddo hijo generado pro crossover en 2 puntos 
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
    
    '''
    Metodo que dada una poblacion, realiza el crossover a esa poblacion regresando los hijos 
    Args: 
    
    Returns:
    '''
    def crossover_all_population(self, population): 
        
        two_matching = self.two_random_matching(population)
        children = []
        for pair in two_matching:
            ch_1, ch_2 = self.crossover_2_points(pair[0],pair[1])
            children.append(ch_1)
            children.append(ch_2)

        return children


    '''
    Metodo que regresa los primeros NUMERO_INIDIVIDUOS - NUEVOS_INDIVIDUOS que tienen
    mejor valor de fitness, este metodo es la representacion de elegir inidividuos de 
    forma elitista 
    Args: 
        population : poblacion a la que se aplica 
    Returns: 
        Mejores best_amount individuos con valor fitness 
    Nota : La lista se regresa en desorden para mantener el factor al azar  
    '''
    def get_first_best(self,population): 
        best_amount = self.__num_ind - self.__num_new_ind
        best_sols = []
        temp_po= sorted(population, key = self.fun_fitness, reverse=True) 
        for i in range(best_amount):
            best_sols.append(temp_po[i])

        best_sols = rnd.sample(best_sols, len(best_sols))
        return best_sols
        #return rnd.shuffle(best_sols)

    #Se escogen padres 
    #Esto se puede hacer por medio del torneo y la ruleta 
    #Despues, se generan los hijos usando los seleccionados 
    #Luego se suma a los hijos con los mejores de la anterior generacion 

    '''
    Metodo que recibe una solucion y la muta 
    Args : 
        sol : Una solucion(individuo) que sera mutada 
    Return : 
        mutate_ind
    '''
    def mutate_individual(self,sol):
        #Probabilidad de que mute cada gen : 
        prob = 1/len(sol.cromosoma)
        
        for i in range(len(sol.cromosoma)): 
            #Condicion para mutar 
            if (rnd.random() < prob):
                new_gen = rnd.randint(0,len(sol.cromosoma)-1)
                sol.set_gen(i, new_gen)

        
      
    '''
    Se recibe una poblacion para mutar 
    Args:
        population : Poblacion a mutar 
    Returns: 
        mutate_pop : Poblacion mutada 
    '''
    def mutate_population(self,population): 
        
        num_mutate_population = (int)(self.__num_ind * self.__porc_mut)
        population = np.random.choice(population,num_mutate_population,replace=False)

        for sol in population: 
            self.mutate_individual(sol)
        

    def new_generation(self): 
        
        #Se seleccionan los padres 
        #Primero se seleccionan por ruleta : 
        selected_by_roulette = self.selection_by_roulette(self.__actual_pop)
        #Segundo se seleccionan por elitismo : 
        selected_by_elitism = self.get_first_best(self.__actual_pop)

        #Se obtienen los hijos de los padres seleccionados por ruleta 
        children_by_roulette = self.crossover_all_population(selected_by_roulette)
        #Se se mutan los hijos 
        self.mutate_population(children_by_roulette) 
        #Se actualiza la poblacion actual 
        self.__actual_pop = selected_by_elitism+children_by_roulette

    def get_best_ind(self): 
        #print(sorted(self.__actual_pop, key = self.fun_fitness))
        #print(type(self.__actual_pop))
        return sorted(self.__actual_pop, key = self.fun_fitness)[0]


    def AG_execution(self):
        i = 0 
        while(i < self.__max_gen):
            self.new_generation()
            i += 1

        print(str(self.fun_fitness(self.get_best_ind())))
        print(str(self.get_best_ind().generar_tablero()))
        

    #ELIMINAR 

    



    def elitismo(self):
        pop = self.__actual_pop 
        self.mostrar_global_fitness(pop)
        print("####################")
        self.mostrar_global_fitness(self.get_first_best(pop))


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


'''
Funcion auxiliar para regresar el porcentaje de un numero 
'''
def percentage(part, whole):
  percentage = 100 * float(part)/float(whole)
  return percentage


def ejecucion(): 

    #sol_1 = Solucion(8)
    #print(sol_1)
    #print(sol_1)
    #sol_1.genes_randomization()
    #print(sol_1)
    #print(sol_1.generar_tablero())
    #def __init__(self, num_reinas, num_ind, max_gen, porc_new_ind, porc_mut):
    genetic = AG(10,50,250,0.70,0.1)
    genetic.AG_execution()
    #so_1 = Solucion(10)
    #so_1.set_cromosoma([4,0,7,9,6,3,1,8,5,2])
    #print(str(so_1.generar_tablero()))
    #print(genetic.fun_fitness(so_1))
    #genetic.elitismo()
    #genetic.mostrar_sols()
    #genetic.selection_tournament()
    #genetic.mostrar_ruleta()
    #print(percentage(5,50))
    #genetic.mostrar_torneo()
    #genetic.mostrar_fitness()

if __name__ == '__main__': 
    ejecucion()