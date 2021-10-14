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
 """
import time
import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""
def initcatalogo():
    a = model.newcatalog()
    return a
def loaddata(catalogo):
    cargarartistas(catalogo)
    cargarobras(catalogo)
def cargarobras(catalogo):
    obraarchivo = cf.data_dir +"Artworks-utf8-small.csv"
    archivo = csv.DictReader(open(obraarchivo, encoding="utf-8"))
    for obra in archivo:
        model.addobra(catalogo, obra)
    model.mapstructure(catalogo)
def cargarartistas(catalogo):
    obraarchivo = cf.data_dir +"Artists-utf8-small.csv"
    archivo = csv.DictReader(open(obraarchivo, encoding="utf-8"))
    start_time = time.process_time()
    for obra in archivo:
        model.getid(catalogo, obra)
    stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000
    print(elapsed_time_mseg)
def histograma(map):
    a = model.histogram(map)
    return a
def portecnica(tecnica, catalogo):
    a = model.obrasmasantiguas(tecnica, catalogo)
    return a

# Inicialización del Catálogo de libros

# Funciones para la carga de datos

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
