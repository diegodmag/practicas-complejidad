###Clase variable 
import random as rnd 

'''
Clase que modela una variable booleana 
'''
class Variable: 
    def __init__(self,nombre,valor): 
        self.__nombre = nombre 
        self.__valor = valor 

    def __str__(self):
        return "["+self.__nombre+": "+str(self.__valor)+"]" 

    @property
    def nombre(self):
        return self.__nombre
    @property
    def valor(self):
        return self.__valor

    def set_valor(self, new_value):
        self.__valor=new_value

    """
    Regresa una instancia de la variable pero negada 
    """
    def negar(self):
        temp = Variable(self.nombre, self.valor)
        if temp.valor == True:
            temp.set_valor(False)
        else :
            temp.set_valor(True)

        return temp 


'''
Clase que modela una clausula 
'''
class Clausula:
    def __init__(self, nombre, variables):
        self.__nombre = nombre 
        self.__variables = variables
    
    def __str__(self):
        varstr = "" 
        for v in self.__variables: 
            varstr += str(v)+", "    
        
        return self.__nombre+" : ("+varstr+")"

    @property
    def nombre(self):
        return self.__nombre
    
    @property 
    def variables(self):
        return self.__variables

    """
    El valor de una clausula es 1 si al menos una de sus variables tiene valor 1 
    """
    def get_valor(self):
        for v in self.__variables: 
            if v.valor==True:
                return True 
        
        return False 
 

"""
Clase que modela una expresion hecha en clausulas 
"""
class ExpresionFNC: 

    def __init__(self,nombre,clausulas): 
        self.__nombre = nombre 
        self.__clausulas = clausulas

    def __str__(self): 
        string = "Expresion : "+self.nombre+" = \n"
        for c in self.clausulas: 
            string += str(c) + "\n"

        return string 

    @property
    def nombre(self): 
        return self.__nombre

    @property 
    def clausulas(self):
        return self.__clausulas

    """
    Una clausula se satisface si los valores de todas sus clausulas es 1 
    """
    def se_satisface(self):
        for c in self.clausulas: 
            if c.get_valor()==False: 
                return False; 
            
        return True


#### IMPLEMENTACION DEL ALGORITMO 3-SAT CON ESPECIFICACIONES DE LA PRACTICA  

###CONSTRUCCION DEL EJEMPLAR JUNTO A LA FASE ADIVINADORA 
"""
Metodo que construye de forma determinista un ejemplar para el problema del 3 sat 
Recibe una lista de variables de tamanio 10 
Regresa una expresion en FNC 
param : U , una lista de variables 
"""
def constructor_de_ejemplar(U):
    
    #Lista de clausulas 
    clausulas = []

    #Se declara una bandera, nos servira para saber si el candidato a ejemplar se 
    #encuentra en FNC y sus clausulas son correctas 
    cont = 0  
    #Seran 5 clausulas de tamanio 3 
    while(cont < 5): 
        #Generamos los indices aleatorios de las variables a considerar
        i_1 = rnd.randint(0,len(U)-1)
        i_2 = rnd.randint(0,len(U)-1)
        i_3 = rnd.randint(0,len(U)-1)
        #Verificamos que sean indices distintos para que no este la misma variable negada en la clausula 
        if (i_1 != i_2 and i_2 != i_3 and i_1!=i_3):
            #Inicializamos la lista de variables 
            variables = []
            #/*nd-choice*/ 
            for i in [i_1,i_2,i_3]:
                moneda = rnd.randint(0,1)
                if moneda == 0:
                    variables.append(U[i].negar())
                else:
                    variables.append(U[i])
            
            temp_clausula  = Clausula("C"+str(cont),variables)
            clausulas.append(temp_clausula)
            #Aumentamos el contador ya que logramos generar una clausula que cumple con la FNC 
            cont+=1

            
    return ExpresionFNC("E"+str(rnd.randint(0,100)), clausulas)


###FASE VERIFICADORA 
"""
El algoritmo que verifica en tiempo polinomial si la solucion es candidata o no 
Cabe resaltar que la construccion y fase adivinadora ocurren en el metodo constructor_de_ejemplar
Para determinar si se satisface o no se utiliza el metodo "se_satisface" de la clase EjemplarFNC
param : U -> Lista de variables 
"""
def algo_3_SAT(U): 

    #El algoritmo solo imprime pero facilmente podria regresar un booleano 
    
    E = E = constructor_de_ejemplar(U)
    print(E)
    print("La expresion se satisface ? :"+ str(E.se_satisface()))
  

def ejecucion(): 

    U = [Variable('A',True),Variable('B',True),Variable('C',True),Variable('D',True),Variable('E',True),Variable('F',True),Variable('G',True),Variable('H',True),Variable('I',True),Variable('J',True)]
    algo_3_SAT(U)

if __name__ == '__main__': 
    ejecucion()



