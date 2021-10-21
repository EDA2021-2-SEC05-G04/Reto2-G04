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
        "obras" : None,
        "ConstiID" :None,
        "hasid": None,
        "names": None,
        "jid" : None,
        "nations": None,
        "diccnations" : None,
        "departamento": None,
        "hasdep" : None
     }
    catalogo["diccnations"] = {} 
    catalogo["obras"] = lt.newList("ARRAY_LIST")
    catalogo["ConstiID"] = lt.newList("ARRAY_LIST",compararcid)
    catalogo["departamento"] =  lt.newList("ARRAY_LIST", comparardepartamento)
    catalogo["hasdep"] = catalogo["jid"] = mp.newMap(
        200, 
        maptype = "CHAINING",
        loadfactor = 3.0
    )
    catalogo["jid"] = mp.newMap(
        200, 
        maptype = "CHAINING",
        loadfactor = 3.0
    )
    catalogo["hasid"] = mp.newMap(
        200, 
        maptype = "CHAINING",
        loadfactor = 3.0
    )
    catalogo["nations"] = mp.newMap(
        200, 
        maptype = "CHAINING",
        loadfactor = 3.0
    )
    catalogo["names"] = mp.newMap(
        200, 
        maptype = "CHAINING",
        loadfactor = 3.0
    )
    return(catalogo)

def addartist(catalogo, artist):
    name = artist["DisplayName"]
    id = artist["ConstituentID"]
    mp.put(catalogo["names"], name, artist)
    mp.put(catalogo["jid"], id, artist)

def addobra(catalogo, obra):
    lt.addLast(catalogo["obras"],obra)
    ides = obra["ConstituentID"].split(", ")
    for id in ides:
        idx = id.strip("[]' ")
        addid(catalogo,idx,obra)
    dep = obra["Department"]
    adddepartamento(catalogo,dep, obra)
def adddepartamento(catalogo,dep, departamento):
    cat = catalogo["departamento"]
    posicion = lt.isPresent(cat, dep)
    if posicion > 0:
        depa = lt.getElement(cat, posicion)
    else:
        depa = nuevodepa(dep)
        lt.addLast(cat, depa)
    lt.addLast(depa["obras"], departamento)


def nuevodepa(depa):
    reto= {
        "departamento" : None,
        "obras" : None
    }
    reto["departamento"] = depa
    reto["obras"] = lt.newList("ARRAY_LIST")
    return(reto)
def addid(catalog, cid, obra):
    cat = catalog["ConstiID"]
    posicion = lt.isPresent(cat, cid)
    if posicion > 0:
        artista = lt.getElement(cat, posicion)
    else:
        artista = nuevoide(cid)
        lt.addLast(cat, artista)
    lt.addLast(artista["obras"], obra)

def nuevoide(coid):
     ide = {"cid": None,
    "obras": None}
     ide["cid"] = coid 
     ide["obras"] = lt.newList("ARRAY_LIST") 
     return(ide)

def hasid(catalogo):
    dict = catalogo["ConstiID"]
    for i in lt.iterator(dict):
        mp.put(catalogo["hasid"], i["cid"], i["obras"])

def  req3(catalogo, artist):
    consti = mp.get(catalogo["names"], artist)
    obras = mp.get(catalogo["hasid"], consti["value"]["ConstituentID"])
    numobras = lt.size(obras["value"])
    obraslist = lt.newList("SINGLE_LINKED")
    mayor = 0
    tecmasusada = None
    histo = {}
    for i in lt.iterator(obras["value"]):
        if i["Medium"] not in histo.keys():
            histo[i["Medium"]] = 1 
        else:
            histo[i["Medium"]] += 1 
    for llave in histo:
        if histo[llave] > mayor:
            mayor = histo[llave]
            tecmasusada = llave
    for o in lt.iterator(obras["value"]):
        if  o["Medium"] == tecmasusada:
            lt.addLast(obraslist,o)
    return (numobras, histo, tecmasusada, obraslist)


def grupo(catalogo):
    dicc = {}
    hasid(catalogo)
    keys = mp.keySet(catalogo["hasid"])
    for i in lt.iterator(keys):
        obras = mp.get(catalogo["hasid"], i)
        nation = mp.get(catalogo["jid"], i)
        if nation["value"]["Nationality"] in dicc.keys():
            lt.addLast(dicc[nation["value"]["Nationality"]], obras["value"])
        else:
            dicc[nation["value"]["Nationality"]] = lt.newList("ARRAY_LIST")
    return(dicc)
def hasdep(catalogo):
    for i in lt.iterator(catalogo["departamento"]):
        mp.put(catalogo["hasdep"], i["departamento"], i["obras"])

def req4 (catalogo):
    histo = {}
    mayor = 0
    mnacional = None
    dicc = grupo(catalogo)
    for i in dicc.keys():
        mp.put(catalogo["nations"], i ,dicc[i])
    nati = mp.keySet(catalogo["nations"])
    for k in lt.iterator(nati):
        m = mp.get(catalogo["nations"], k)
        if k in histo.keys():
             histo[k] += lt.size(m["value"])
        else:
             histo[k] = lt.size(m["value"])
    for llave in histo:
        if histo[llave] > mayor:
            mayor = histo[llave]
            mnacional = llave
    obrasmnacional = mp.get(catalogo["nations"],mnacional)
    return(histo, obrasmnacional["value"])

def req5 (catalogo, departamento):
    hasdep(catalogo)
    dicc = lt.newList("ARRAY_LIST")
    costo = 0
    pesoneto =0
    obras = mp.get(catalogo["hasdep"], departamento)
    obr = obras["value"]
    for i in lt.iterator(obr):
        if (i["Height (cm)"] != "" and i["Width (cm)"] != ""):
            area = (float(i["Height (cm)"]) / 100) * (float(i["Width (cm)"])/ 100)
            costo += area * 72.00
        elif (i["Height (cm)"] != "" and i["Width (cm)"] != "" and i["Length (cm)"] != ""  ):
            area = (float(i["Height (cm)"]) / 100) * (float(i["Width (cm)"])/ 100) * (float(catalogo["Length (cm)"])/ 100)
            costo += area * 72.00
        elif (i["Weight (kg)"] != ""):
            area = (i["Weight (kg)"] )
            costo += area * 72.00
            pesoneto += int(area)
        else:
            costo +=  48.00
        dop = {"obra" : i, "costo": costo}
        lt.addLast(dicc, dop)
    ord = mg.sort(dicc, ordenarporcosto)
    a = lt.subList(ord, 1, 5)
    return(round(costo, 2), pesoneto, a)
    
  
# Construccion de modelos

# Funciones para agregar informacion al catalogo

# Funciones para creacion de datos

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista
def compararcid(cid, listacid):
    if (cid in listacid["cid"]):
        return(0)    
    return(-1)
def comparardepartamento(departamento, obra):
    if (departamento == obra['departamento']):
        return 0
    elif (departamento > obra['departamento']):
        return 1
    return -1 
def ordenarporcosto(obra1, obra2):
    return(obra1["costo"] > obra2["costo"])