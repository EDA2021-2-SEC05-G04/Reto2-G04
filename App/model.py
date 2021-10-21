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
import datetime
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
    catalogo["artistsByBegindate"]=mp.newMap(1949,maptype="PROBING",loadfactor=0.5, comparefunction=cmpfunctionmap)
    catalogo["obrabyDateAcquired"]=mp.newMap(300,maptype="PROBING",loadfactor=0.5,comparefunction=cmpfunctionmap) 
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
def requerimiento1(catalog,f1,f2):
    listacompleta= lt.newList('ARRAY_LIST')
    for i in range(int(f1), int(f2)+1):
        if mp.contains (catalog["artistsByBegindate"],str(i)):
            Entryartistasporano=mp.get(catalog["artistsByBegindate"], str(i))
            Artistasporano=me.getValue(Entryartistasporano)["artistas"]
            for j in range(1,lt.size(Artistasporano)+1): 
                Artista= lt.getElement(Artistasporano, j)
                lt.addLast(listacompleta, Artista)
        
    return listacompleta

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
def cargarobraporfecha(catalog,obra):
    fecha_obra=obra["DateAcquired"]
    if(fecha_obra != ""):
        fecha_obra=datetime.datetime.strptime(fecha_obra, "%Y-%m-%d")
        if(mp.contains(catalog["obrabyDateAcquired"],fecha_obra)):
            valor2=mp.get(catalog["obrabyDateAcquired"],fecha_obra)
            valor2=me.getValue(valor2)["obras"]
            lt.addLast(valor2,obra)
        else:
            valor=crear_valor(obra)
            mp.put(catalog["obrabyDateAcquired"],fecha_obra,valor)
def crear_valor(obra):
    dicc={"obras":lt.newList("ARRAY_LIST"),"fecha_adquisicion":obra["DateAcquired"]}
    lt.addLast(dicc["obras"],obra)
    return dicc    
def obrasenrango(inventario,f1,f2):
    map=inventario["obrabyDateAcquired"]
    c=f1
    auxiliar=lt.newList("ARRAY_LIST")
    avance=datetime.timedelta(1,0,0)
    contador=0
    while c<=f2:
        if(mp.contains(map,c)):
            valor=me.getValue(mp.get(map,c))["obras"]
            for i in range(1,lt.size(valor)+1):
                obra=lt.getElement(valor,i)
                lt.addLast(auxiliar,obra)
                if(obra["CreditLine"] =="Purchase"):
                    contador+=1
        c+=avance
    
    return auxiliar,contador   

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
def cargar_artistaporFecha(catalogo,artista):
    mapaartistas= catalogo["artistsByBegindate"]
    anoartista= artista ["BeginDate"]
    cntainartist=mp.contains(mapaartistas, anoartista)
    if cntainartist:
        Entry_ano= mp.get(mapaartistas,anoartista)
        Lista_de_artistas= me.getValue(Entry_ano)
        Valor_lista=Lista_de_artistas ["artistas"]
        lt.addLast(Valor_lista, artista)
    else:
        diccionario_artistas_por_fecha=lista_de_artistas_por_ano(artista)
        mp.put(mapaartistas, anoartista, diccionario_artistas_por_fecha) 
def lista_de_artistas_por_ano(artista):
    
    catalog={"artistas":None, "Fecha_nac":None}
    catalog["artistas"]=lt.newList("ARRAY_LIST", cmpfunctionobras)
    lt.addLast(catalog["artistas"],artista)
    catalog["Fecha_nac"]=artista["BeginDate"]
    return catalog
def cmpfunctionobras(obra1, obra2):
    key= me.getKey(obra2)
    if(obra1 == key):
        return 0
    elif(obra1 >key):
        return 1
    else:
        return -1
# Construccion de modelos

# Funciones para agregar informacion al catalogo

# Funciones para creacion de datos

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista
def compararcid(cid, listacid):
    if (cid in listacid["cid"]):
        return(0)    
    return(-1)
def cmpfunctionmap(key,entry):
    key2=me.getKey(entry)
    if(key > key2):
        return 1
    elif key == key2:
        return 0
    else:
        return -1
def comparardepartamento(departamento, obra):
    if (departamento == obra['departamento']):
        return 0
    elif (departamento > obra['departamento']):
        return 1
    return -1 
def ordenarporcosto(obra1, obra2):
    return(obra1["costo"] > obra2["costo"])