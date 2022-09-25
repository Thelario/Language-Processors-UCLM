
# -------------------------------------------------------------------------

class SymbolsTable:

    def __init__(self):
        self.dictionary = {}

    def AddSymbol(self, sName, sValue, sType):
        self.dictionary[sName] = [sValue, sType]

    def AddSymbol(self, sName, sValue, sType):
        self.dictionary[sName] = [sValue, sType]

    # Attribute is a parameter that will indicate the element to change in the 
    # list that representes the symbol. Attribute can be 0(for value) and 1(for type).
    def Modify(self, sName, attribute, newValue):
        if (not self.Exists(sName)):
            print("The symbol with id " + str(sName) + "doesn't exist.")
            return;

        self.dictionary[sName][attribute] = newValue

    def Exists(self, sName):
        return sName in self.dictionary

    def Value(self, sName):
        if (not self.Exists(sName)):
            print("The symbol with id " + str(sName) + "doesn't exist.")
            return;

        return self.dictionary[sName]

    def PrintDictionary(self):
        print(self.dictionary)

# -------------------------------------------------------------------------

# Checking the class works well

checkSymbolClass = False
if checkSymbolClass:
    table = SymbolsTable()
    table.PrintDictionary()
    table.AddSymbol("a", 10, "int")
    table.PrintDictionary()
    print(str(table.Exists("a")))
    print(str(table.Exists("b")))

# -------------------------------------------------------------------------

class Tree:
    def __init__(self, elto):
        self.elto= elto # elto is a list with [name, value, type]
        self.izdo= None
        self.dcho= None

    def Add(self, newElem):
        if (self.elto[0] == newElem[0]):
            return

        if (newElem[0] > self.elto[0]):
            self.dcho = newElem
        else:
            self.izdo = newElem

    def Exists(self, elem):
        if (self.elto[0] == elem[0]):
            return True

        if (self.izdo == None and self.dcho == None):
            return False
        elif(self.izdo == None):
            return self.dcho.Exists(elem)
        else:
            return self.izdo.Exists(elem)

    def __str__(self):
        return "root: " + str(self.elto) + " (izdo: " + str(self.izdo) + "), (dcho: " + str(self.dcho) + ")"

    # Attribute is a parameter that will indicate the element to change in the 
    # list that representes the symbol. Attribute can be 0(for value) and 1(for type).
    def Modify(self, sName, attribute, newValue):
        if (self.elto[0] == sName):
            self.elto[attribute] = newValue
            return

        if (self.izdo == None and self.dcho == None):
            return
        
        self.izdo.Modify(sName, attribute, newValue)
        self.dcho.Modify(sName, attribute, newValue)

    def Value(self, sName, attribute):
        if (self.elto[0] == sName):
            return self.elto[attribute]

        if (self.izdo == None and self.dcho == None):
            return None

        return self.izdo.Value(sName, attribute) or self.dcho.Value(sName, attribute)

# -------------------------------------------------------------------------

# Checking the class works well

checkTreeClass = False
if checkTreeClass:
    A = Tree("diminuto")
    A.Add("pequeno")
    A.Add("abaco")
    A.Add("grande")
    A.Add("diminuto")
    print(A)
    print (A.Exists(["ínfimo"]))
    print (A.Exists("grande"))

# -------------------------------------------------------------------------

class EXP:
    def __init__(self): 
        pass

    # muestra la expresión utilizando paréntesis
    def mostrar(self): 
        pass 

    # muestra el número de operaciones de la expresión
    def numero_operaciones(self): 
        pass 

    # evalua la expresión
    def interpreta(self): 
        pass 

class Numero(EXP):
    # p.e. para crear una hoja con el d´ıgito 7 har´ıamos Numero(7)
    def __init__(self, valor):
        self.valor= valor

    def mostrar(self):
        return str(self.valor)

    def numero_operaciones(self):
        return 0

    def interpreta(self):
        return self.valor

class Operacion(EXP):
# p.e. para crear un nodo con la expresi´on 5*3 har´ıamos
# Operacion(’*’,Numero(5),Numero(3))
    def __init__(self, op, izda, dcha):
        self.op= op
        self.izda= izda
        self.dcha= dcha

    def mostrar(self):
        return "(" + self.izda.mostrar() + self.op + self.dcha.mostrar() + ")"

    def numero_operaciones(self):
        return 1 + self.izda.numero_operaciones() + self.dcha.numero_operaciones()

    def interpreta(self):
        if self.op== "+":
            return self.izda.interpreta() + self.dcha.interpreta()
        elif self.op=="*": 
            return self.izda.interpreta() * self.dcha.interpreta()
        elif self.op=="-":
            return self.izda.interpreta() - self.dcha.interpreta()
        elif self.op=="/":
            return self.izda.interpreta() / self.dcha.interpreta()

# -------------------------------------------------------------------------

checkEXP = False
if checkEXP:
    # Introducimos el ´arbol de la expresi´on 4*5+3*2
    num1=Numero(4)
    num2=Numero(5)
    num3=Numero(3)
    num4=Numero(2)
    arbol1=Operacion("*",num1,num2) # 4*5
    arbol2=Operacion("*",num3,num4) # 4*5
    arbol_final=Operacion("+",arbol1,arbol2) # arbol1+arbol2

    # Accedemos al ´arbol de tres formas diferentes mediante funciones miembro
    print ("El arbol contiene la expresion:", arbol_final.mostrar())
    print ("El arbol contiene en total %d operaciones" % arbol_final.numero_operaciones())
    print ("La expresion se evalua como:", arbol_final.interpreta())
