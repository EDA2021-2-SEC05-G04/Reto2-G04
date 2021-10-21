"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf
from DISClib.ADT.map import get
import config as cf
import sys
import controller
import datetime
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2-  listar cronológicamente los artistas")
    print("4-  casificar las obras de un artista por técnica ")
    print("5-  clasificar las obras por la nacionalidad de sus creadores ")
    print("6-  transportar obras de un departamento ")

catalog = None
def initcatalogo():
    return controller.initcatalogo()
def cargardatos(catalogo):
    controller.loaddata(catalogo)

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        catalogo = initcatalogo()
        cargardatos(catalogo)


    elif int(inputs[0]) == 2:
        print("listando cronológicamente los artistas.")
        f1 = input("Fecha 1: ")
        f2 = input("Fecha 2: ")
        lista_ordenada = controller.obtenerartistasfechas(catalogo, f1,f2)
        print(lt.size(lista_ordenada))
        for i in range( 1, 4) : 
            print(lt.getElement(lista_ordenada, i)["DisplayName"] +"   " +  lt.getElement(lista_ordenada, i)["Nationality"] + "  " +  lt.getElement(lista_ordenada, i)["BeginDate"] +"  " + lt.getElement(lista_ordenada, i)["EndDate"]+ "  " +lt.getElement(lista_ordenada, i)["Gender"])
        print( "\n")
        for i in range(lt.size(lista_ordenada)- 2, lt.size(lista_ordenada)+1) : 
            print(lt.getElement(lista_ordenada, i)["DisplayName"] +"   " +  lt.getElement(lista_ordenada, i)["Nationality"] + "  " +  lt.getElement(lista_ordenada, i)["BeginDate"] +"  " + lt.getElement(lista_ordenada, i)["EndDate"]+ "  " +lt.getElement(lista_ordenada, i)["Gender"])
    elif  int(inputs[0]) == 3:
        print("listando cronológicamente las adquisiciones")
        fi = input("fecha 1 : ")
        fo = input("fecha 2 : ")
        fechai = datetime.datetime.strptime(fi, "%Y-%m-%d")
        fechao = datetime.datetime.strptime(fo, "%Y-%m-%d")

        lista = controller.fechas(catalogo,fechai,fechao)
        print("Números de obras en el rango:",lt.size(lista[0]))
        print("Números de obras adquiridas por compra:",lista[1])
        for i in range( 1, 4) : 
            print(lt.getElement(lista[0], i)["Title"] +"   " +  lt.getElement(lista[0], i)["ConstituentID"] + "  " +  lt.getElement(lista[0], i)["DateAcquired"] +"  " + lt.getElement(lista[0], i)["Medium"]+ "  " +lt.getElement(lista[0], i)["Dimensions"])
        print( "\n")
        for i in range(lt.size(lista[0])- 2, lt.size(lista[0])+1) : 
            print(lt.getElement(lista[0], i)["Title"] +"   " +  lt.getElement(lista[0], i)["ConstituentID"] + "  " +  lt.getElement(lista[0], i)["DateAcquired"] +"  " + lt.getElement(lista[0], i)["Medium"]+ "  " +lt.getElement(lista[0], i)["Dimensions"])
    elif  int(inputs[0]) == 4:
        controller.has(catalogo)
        artist = input("Nombre del artista: ")
        ans = controller.req3(catalogo, artist)
        print("numero de obras de  " + artist+  " es : " + str(ans[0]))
        print("las tecnicas utilizadas de   " + artist+  " son: " + str(ans[1]))
        print("la tecnica mas usada de  " + artist+  " es: " + str(ans[2]))
        for ob in lt.iterator(ans[3]):
            print("Titulo " +  str(ob["Title"]))
            print("Fecha de la obra " +  str(ob["Date"]))
            print("Medio " +  str(ob["Medium"]))
            print("Dimensiones " +  str(ob["Dimensions"]))
    elif  int(inputs[0]) == 5:
         a = controller.req4(catalogo)
         print(a) 
         for l in range(1,4):
             print((lt.getElement(a[1], l)))
         for k in range(lt.size(a[1])-3, lt.size(a[1])+1 ):
             print((lt.getElement(a[1], k)))
    elif  int(inputs[0]) == 6:
         departamento = input("Ingrese departamento a transportar:  ")
         costo = controller.req5(catalogo, departamento)
         print("Costo total de transporte" + str(costo[0]))
         print("Peso neto de transporte" + str(costo[1]))
         for i in lt.iterator(costo[2]):
             print("Titulo: " , i["obra"]["Title"])
             print("Artistas: " ,i["obra"]["ConstituentID"])   
             print("fecha : " , i["obra"]["Date"])
             print("medio: ", i["obra"]["Medium"])
             print("Dimenciones: " , i["obra"]["Dimensions"])
    else:
        sys.exit(0)
sys.exit(0)
