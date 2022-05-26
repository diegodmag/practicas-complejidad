'''
Clase que modela el algoritmo de aproximacion para el problema de optimizacion de Set Covering 
initial_set : Es el conjunto de elementos inicial 
family : Es la familia de subconjuntos de X 
'''
import sre_compile
from turtle import st


class  SetCovering:
    def __init__(self, initial_set, family ):
        self.initial_set = initial_set 
        self.family = family
        self.temp_set = initial_set
        self.constructed_set = []

    def __str__(self):

        best = self.get_max_card_sets() 

        tab = "\n---------------------------------------- \n"
        init_info = "Conjunto inicial X:"+str(self.initial_set)+"\n"
        fam_info = "Familia de subconjuntos F:"+str(self.family)+"\n"+"Cardinalidad:"+str(len(self.family))
        solution_info = "Subconjunto solucion S:"+str(self.constructed_set)+"\n"+"Cardinalidad:"+str(len(self.constructed_set))
        approximation_info = "El subconjunto con mayor cardinalidad del subconjunto solucion S es: "+str(best)+"\ncon cardinalidad : "+str(len(best))
        conclution_info = "Por lo que este es un algoritmo :"+str(len(best))+"- Aproximable"
        return tab+init_info+tab+fam_info+tab+solution_info+tab+approximation_info+tab+conclution_info

    
    def subset_maximizes_solution(self):
        max_of_set = set()
        for s in self.family:
            if len(s & self.temp_set) > len(max_of_set):
                max_of_set = s
        

        return max_of_set

    def get_max_card_sets(self): 
        max_card = set()
        
        for s in self.constructed_set:
            if len(s) >= len(max_card): 
                max_card = s 
        
        return max_card

    #   Importante, para que esto funcione para cada elemento del conjunto original debe 
    #   haber al menos un subconjunto en la coleccion que lo contenga 
    def algorithm_execution(self):
        #Mientras U sea distinto del vacio 
        while(len(self.temp_set)!=0):
            #Encontramos el subconjunto s de la familia que maximiza la interseccion con U
            s = self.subset_maximizes_solution()
            #Quitamos a s de U
            self.temp_set = self.temp_set - s 
            #Agregamos s a la solucion 
            self.constructed_set.append(s)


def tests():
    tab = "\n---------------------------------------- \n"
    print("Ejemplo 1 :")
    initial_set = {'a','b', 'c','d','f','g','r','x','w'}
    family = [{'a','c','g'}, {'d','f'}, {'d','c'},{'b','c','a','g'},{'a','c','f','r'},{'w','x'}]
    instance = SetCovering(initial_set,family)
    instance.algorithm_execution()
    print(instance)
    print(tab+"\n")
    
    print("Ejemplo 2 :")
    initial_set = {1,2,3,4,5,6,7,8,9,10,11,12}
    family = [{1,3,5,7}, {7,9,11,2,5}, {2,4,12},{12,5,8,10},{1,10,8},{5,6,9}]
    instance = SetCovering(initial_set,family)
    instance.algorithm_execution()
    print(instance)
    print(tab+"\n")

    print("Ejemplo 3 :")
    initial_set = {20,40,60,80,90,120,150,180}
    family = [{20,60,120,180}, {40,80,90,150}, {120,180,40,60}]
    instance = SetCovering(initial_set,family)
    instance.algorithm_execution()
    print(instance)
    print(tab+"\n")

    print("Ejemplo 4 :")
    initial_set = {'a','b','c','d'}
    family = [{'c','a','d'}, {'b'}]
    instance = SetCovering(initial_set,family)
    instance.algorithm_execution()
    print(instance)
    print(tab+"\n")

    print("Ejemplo 5 :")
    initial_set = {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,20,21}
    family = [{13},{14},{1,21,12}, {2,1,21}, {3,2,4,5,21}, {6,21,1,2,4}, {16,18,20,15,6}, {7,8,9,10,11}, {1,2,3,17,18,20,21}]
    instance = SetCovering(initial_set,family)
    instance.algorithm_execution()
    print(instance)
    print(tab+"\n")


if __name__=='__main__':
    tests()