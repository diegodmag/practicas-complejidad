from importlib.resources import path
import random as rnd 

"""
Clase que modela una grafica cuyos vertices solo pueden ser numeros enteros 
"""
class Grafica :

    '''
    param : vertices, una lista de enteros que representan a los vertices 
    param : aristas, una de aristas, cada arist es un conjunto de dos elementos, 
            lo cual nos ayuda a que {x,y}={y,x},como es una grafica no direccionada es indistinto 
            el orden de los vertices en la arista 
    '''
    def __init__(self, vertices, aristas):
        self.__vertices = vertices 
        self.__aristas = aristas  

    def __str__(self):
        return "V = "+str(self.vertices)+"\n"+"E = "+str(self.aristas) 

    @property 
    def vertices(self):
        return self.__vertices
    
    @property 
    def aristas(self):
        return self.__aristas


"""
Metodo que genera una grafica a partir de una lista de vertices 
"""
def generador_de_ejemplar(vertices):
    aristas = []
    for v in vertices: 
        for u in vertices: 
            if v != u:
                #Generando aristas de forma aleatorea  
                cota = 4
                if(rnd.randint(0,cota)==cota): 
                    temp = {v,u}
                    if temp not in aristas:
                        aristas.append({v,u})

    return Grafica(vertices,aristas)



"""
Algoritmo que determina si dado dos vertices existe al menos un camino entre ellos 
"""
def algo_alcanzabilidad(G,s,t):
    
    #/*Fase Adivinadora*/
    S = []
    S.append(s)
    S.append(t)
    for v in G.vertices:
        # /*nd-choice*/ 
        if v!= s and v != t: 
            if(rnd.randint(0,1)==1):
                S.append(v)

    
    #/*Fase Verificadora */
    # Verificamos que s y t existan en G.vertices 
    if s not in G.vertices or t not in G.vertices: 
        print("AQUI ENTRO")
        return False
  

    #Generamos una subgrafica con el subconjunto de vertices S obtenido
    E_s = []
    for s in S: 
        for e in G.aristas: 
            if s in e:
                if e not in E_s:
                    #print(str(s) + "|"+ str(e))
                    E_s.append(e) 


    temp = Grafica(S,E_s)
    ##Corremos dfs 
    path = dfs(temp,s,set())

    #path = dfs(G,s,set())
    
    print("Solucion candidata"+str(S))



    if t in path:
        return True


    return False    


'''
Implementacion recursiva de DFS 
'''
def dfs(G,s,visitados): 
    
    if s not in visitados:
        visitados.add(s)
        for e in G.aristas: 
            if s in e:
                for v in e:
                    if v != s:
                        dfs(G,v,visitados)
    
    return visitados




def ejecucion_ejemplar_random():
    #Generando un ejemplar de grafica 
    g = generador_de_ejemplar([1,2,3,4,5,6,7,8,9,10])
    print(g)
    s = 4
    t = 5
    print(f'Hay un camino entre {s} y {t} ?  '+str(algo_alcanzabilidad(g,s,t)))

def ejecucion_ejemplar_fijo(): 
    v = [1,2,3,4,5,6,7,8,9,10,11,12]
    e = [ {1,5}, {5,3}, {5,7}, {5,9}, {9,10}, {11,12}, {6,12}, {4,2}]
    g_fija = Grafica(v,e)
    
    print(g_fija)
    print("#########################################")
    print(f'Hay un camino entre {6} y {11} ?  '+str(algo_alcanzabilidad(g_fija,6,11)))
    print(f'Hay un camino entre {1} y {10} ?  '+str(algo_alcanzabilidad(g_fija,1,10)))
    print(f'Hay un camino entre {2} y {4} ?  '+str(algo_alcanzabilidad(g_fija,2,4)))
    print(f'Hay un camino entre {11} y {3} ?  '+str(algo_alcanzabilidad(g_fija,11,3)))
    print(f'Hay un camino entre {10} y {3} ?  '+str(algo_alcanzabilidad(g_fija,10,3)))


def ejecucion(): 

    #ejecucion_ejemplar_random()
    
    print("#########################################")

    #Usando un ejemplar fijo 
    ejecucion_ejemplar_fijo()
    





if __name__ == '__main__': 
    ejecucion()




