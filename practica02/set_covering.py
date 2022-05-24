'''
Clase que modela el algoritmo de aproximacion para el problema de optimizacion de Set Covering 
initial_set : Es el conjunto de elementos inicial 
family : Es la familia de subconjuntos de X 
'''
class  SetCovering:
    def __init__(self, initial_set, family ):
        self.initial_set = initial_set 
        self.family = family
        self.temp_set = initial_set
        self.constructed_set = []

    def __str__(self):
        return "Conjunto inicial X:"+str(self.initial_set)+"\n"+"Familia de subconjuntos F:"+str(self.family)+"\n"+"Subconjunto solucion S:"+str(self.constructed_set)+"\n"+"Cardinalidad del subconjunto solucion :"+str(len(self.constructed_set))

    
    def subset_maximizes_solution(self):
        max_of_set = set()
        for s in self.family:
            if len(s & self.temp_set) > len(max_of_set):
                max_of_set = s
        

        return max_of_set

        
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

def ejecucion():

    initial_set = {'a','b', 'c','d','f','g','r','x','w'}
    family = [{'a','c','g'}, {'d','f'}, {'d','c'},{'b','c','a','g'},{'a','c','f','d','r','x'},{'w'}]
    instance = SetCovering(initial_set,family)
    instance.algorithm_execution()
    print(instance)


if __name__=='__main__':
    ejecucion()