#!/usr/bin/env python

import componentes
#import errores
import flujo
import string
import sys
import os
from sys import argv

class Analex():
    #############################################################################
    ##  Conjunto de palabras reservadas para comprobar si un identificador es PR
    #############################################################################
    PR = frozenset(["PROGRAMA", "VAR", "ENTERO", "REAL", "BOOLEANO", "INICIO", "FIN", "SI", "ENTONCES", "SINO", "MIENTRAS", "HACER", "LEE", "ESCRIBE", "Y", "O", "NO", "CIERTO","FALSO"])

    ############################################################################
    #
    #  Funcion: __init__
    #  Tarea:  Constructor de la clase
    #  Prametros:  flujo:  flujo de caracteres de entrada
    #  Devuelve: --
    #
    ############################################################################
    def __init__(self, flujo):
        self.flujo= flujo
        self.poserror= 0
        self.nlinea=1

        self.numeros = frozenset(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"])
        self.letras = frozenset(["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "ñ", "o", "p", 
        "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G","H", "I", "J", 
        "K", "L", "M", "N", "Ñ", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"])
        self.relacionales = frozenset(["=", "<>" "<", "<=", ">=", ">"])


    ############################################################################
    #
    #  Funcion: TrataNum
    #  Tarea:  Lee un numero del flujo
    #  Prametros:  flujo:  flujo de caracteres de entrada
    #              ch: primera caractera tratar
    #  Devuelve: El valor numerico de la cadena leida
    #
    ############################################################################
    def TrataNum(self, flujo, ch):
        l = ch
        real = False
        ch = flujo.siguiente()
        
        while isinstance(ch, self.numeros):
            l += ch
            ch = flujo.siguiente()

            if ch == "." and real == False:
                aux = ch
                ch = flujo.siguiente()

                if self.EsNumero(ch):
                    real = True
                    l += aux
                    l += ch
                    ch = flujo.siguiente()

        # TODO (EN EL FUTURO)
        # detectar si hay un punto y coma o un espacio en blanco
        # si no es un punto y como o un espacio, entonces no es un componente válido (ej: 2345A)

        ch = flujo.devuelve(ch)

        # convertir l en numero y devolverlo
        if real == False:
            l = int(l)
            l = componentes.Numero("int", l, self.nlinea)
        else:
            l = float(l)
            l = componentes.Numero("float", l, self.nlinea)
        return l


    ############################################################################
    #
    #  Funcion: TrataIdent
    #  Tarea:  Lee identificadores
    #  Prametros:  flujo:  flujo de caracteres de entrada
    #              ch: Primer caracter a tratar
    #  Devuelve: Devuelve una cadena de caracteres que representa un identificador
    #
    ############################################################################
    def TrataIdent(self,flujo, ch):
        l = ch
        ch = flujo.siguiente()
        
        while self.EsNumero(ch) or isinstance(ch, self.letras):
            l += ch
            ch = flujo.siguiente()
      
        ch = flujo.devuelve(ch)

        # por comodidad, hemos decidido incluir el tratamiento de una palabra reservada dentro de la función TrataIdent
        if isinstance(l, self.PR):
            return componentes.PR(l, self.nlinea)
        else:
            return componentes.Identif(l, self.nlinea)

    ############################################################################
    #
    #  Funcion: TrataComent
    #  Tarea:  ignora todos los caractéres presentes en el comentario
    #  Prametros:  flujo:  flujo de caracteres de entrada
    #
    ############################################################################
    def TrataComent(self, flujo):
        
        while flujo.siguiente() != "%":
            continue

        return

    ############################################################################
    #
    #  Funcion: EliminaBlancos
    #  Tarea:  Descarta todos los caracteres blancos que hay en el flujo de entrada
    #  Prametros:  flujo:  flujo de caracteres de entrada
    #  Devuelve: --
    #
    ############################################################################
    def EliminaBlancos(self, flujo):

        while flujo.siguiente() == " ":
            continue

        flujo.devuelve()

        return

    ############################################################################
    #
    #  Funcion: Analiza
    #  Tarea:  Identifica los diferentes componentes lexicos
    #  Prametros:  --
    #  Devuelve: Devuelve un componente lexico
    #
    ############################################################################
    def Analiza(self):
        l = ""
        ch = self.flujo.siguiente();
        if ch == " ":
            # acciones si hemos encontrado un blanco
            self.EliminaBlancos(self.flujo)
            return self.Analiza()
        elif ch == "\r":
            # TODO: duda, que hace la \r
            return self.Analiza()
        elif isinstance(ch, self.letras):
            # completar aqui para todas las categorias lexicasw
            return self.TrataIdent(self.flujo, ch)
        elif isinstance(ch, self.numeros):
            # completar aqui para todas las categorias lexicasw
            return self.TrataNum(self.flujo, ch)
        elif ch == ":":
            l += ch
            ch = self.flujo.siguiente()
            if ch == "=":
                l += ch
                l = componentes.OpAsigna(self.nlinea)
                return l

            print ("ERROR LEXICO  Linea " + str(self.nlinea) + " ::  Caracter " + ch + " invalido ")
            return self.Analiza()
        elif ch == "+":
            return componentes.OpAdd(self.nlinea)
        elif ch == "-":
            return componentes.OpResta(self.nlinea)
        elif ch == "*":
            return componentes.OpMult(self.nlinea)
        elif ch == "/":
            return componentes.OpDiv(self.nlinea)
        elif ch == "%":
            l += ch
            ch = self.flujo.siguiente()
            if ch == "%":
                return self.TrataComent()
            else:
                return componentes.OpResto(self.nlinea)
        elif isinstance(ch, self.relacionales):
            l += ch
            ch = self.flujo.siguiente()
            if isinstance(ch, self.relacionales) and ch != l:
                l += ch
                l = componentes.OpRel(self.nlinea, l)
                return l
            elif ch == l:
                # se ha encontrado un caracter no permitido
                print ("ERROR LEXICO  Linea " + str(self.nlinea) + " ::  Caracter " + ch + " invalido ")
                return self.Analiza()
            else:
                self.flujo.devuelve()
                return componentes.OpRel(self.nlinea, ch)
        elif ch == "\n":
            # acciones al encontrar un salto de linea
            self.nlinea = self.nlinea + 1
            return self.Analiza()
        elif ch:
            # se ha encontrado un caracter no permitido
            print ("ERROR LEXICO  Linea " + str(self.nlinea) + " ::  Caracter " + ch + " invalido ")
            return self.Analiza()
        else:
            # el final de fichero
            return componentes.EOF()

############################################################################
#
#  Funcion: __main__
#  Tarea:  Programa principal de prueba del analizador lexico
#  Prametros:  --
#  Devuelve: --
#
############################################################################
if __name__=="__main__":
    script, filename = argv
    txt = open(filename)
    print ("PROGRAMA FUENTE %r"  % filename)
    i = 0
    fl = flujo.Flujo(txt)
    analex = Analex(fl)
    c = analex.Analiza()

    while c.cat != "EOF":
        print (c)
        c = analex.Analiza()

    i = i + 1