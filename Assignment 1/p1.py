
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

checkTreeClass = True
if checkTreeClass:
    A = Tree("diminuto")
    A.Add("pequeno")
    A.Add("abaco")
    A.Add("grande")
    A.Add("diminuto")
    print(A)
    #print (A.Exists(["ínfimo"]))
    print (A.Exists("grande"))