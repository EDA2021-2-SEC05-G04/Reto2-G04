"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """

import time
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import mergesort as mg
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""
def newcatalog ():
    catalogo = {
        "obras" :  None,
        "obra" : None,
        "medium" : None,
        "contiid": None,
        "nation" : None
    }
    catalogo["contiid"] = mp.newMap(
       100, 
        maptype = "PROBING",
        loadfactor = 0.8

    )
    catalogo["nation"]= mp.newMap(
        200, 
        maptype = "CHAINING",
        loadfactor = 3.0
    )
    catalogo["national"] = lt.newList("ARRAY_LIST",compararnacionalidad) 
    catalogo["medium"] = lt.newList("ARRAY_LIST", comparartenica)
    catalogo["obras"] = mp.newMap(
        200, 
        maptype = "CHAINING",
        loadfactor = 3.0
    )
    catalogo["obra"] = lt.newList("SINGLE_LINKED")
    return(catalogo)



# Construccion de modelos

# Funciones para agregar informacion al catalogo
def getid(catalogo, artist):
    id = artist["ConstituentID"]
    addartist(catalogo, id, artist)
def addartist(catalogo, id, artist):
    mp.put(catalogo["contiid"], id , artist["Nationality"])


def addobra(catalogo, obra):
    #lt.addLast(catalogo["obra"], obra)
    obr = lt.newList(datastructure='SINGLE_LINKED')
    tecnica = obra["Medium"]
    ides = obra["ConstituentID"].split(", ")
    lt.addLast(obr, obra)
    for id in ides:
        idx = id.strip("[]' ")
        element = mp.get(catalogo["contiid"], idx)
        mp.put(catalogo["nation"], element["value"], obra["Title"])
    addtecnica(catalogo, tecnica, obra)
    
def addtecnica(catalogo, tecnica, obra):
    a = lt.isPresent(catalogo["medium"], tecnica)
    if a > 0:
        el = lt.getElement(catalogo["medium"], a)
    else:
        el = addtec(tecnica)
        lt.addLast(catalogo["medium"], el)
    lt.addLast(el["obras"],obra)
def addtec(tecnica):
    dir = {
        "tecnica" : None,
        "obras" : None
    }
    dir["tecnica"]  = tecnica
    dir["obras"] = lt.newList("SINGLE_LINKED")
    return(dir)

def mapstructure(catalogo):
    obras = catalogo["medium"]
    for i in lt.iterator(obras):

        mp.put(catalogo["obras"], i["tecnica"], i["obras"])
# Funciones para creacion de datos

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista
def comparartenica(tecnica, obra):
    if (tecnica == obra['tecnica']):
        return 0
    elif (tecnica > obra['tecnica']):
        return 1
    return -1 
def compararnacionalidad(tecnica, obra):
    if (tecnica == obra['nacionalidad']):
        return 0
    elif (tecnica > obra['nacionalidad']):
        return 1
    return -1 
def obrasmasantiguas(tecnica, catalogo):
    g = mp.get(catalogo["obras"], tecnica)
    ordenado = mg.sort(g["value"],cmpfecha)
    a = lt.subList(ordenado, lt.size(ordenado) - 3,lt.size(ordenado) - (lt.size(ordenado) - 3 ))
    return a
# Funciones de ordenamiento

def cmpfecha (obra1, obra2):
    return(obra1["Date"] > obra2["Date"])

def histogram (elements):
    elist = mp.valueSet(elements)
    histo = {}
    for i in lt.iterator(elist):
        if i in histo.keys():
            histo[i] += 1
        else:
            histo[i] = 1
    return histo