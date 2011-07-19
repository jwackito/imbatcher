#-*-coding:utf-8-*-
###############################################################################
#	imbatcher - Programa para separar lotes de fotos similares
#		Compara imágenes de a dos
#	Copyright (C) 2011  Joaquín Bogado <joaquinbogado en gmail.com>
#
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with this program.  If not, see <http://www.gnu.org/licenses/>.
###############################################################################

from PIL import Image
from numpy import *
from sys import *
from os import *
from glob import *
from natsorted import *

#TODO: mejorar el manejo de parametros al programa principal
#	basepath es obligatorio
#	thrsh opcional (por defecto 30)
#TODO: Manejar diferentes tamaños de imagen.

def ayuda():
	print 'MODO DE USO: '
	print '\t' + argv[0] + ' -h'
	print '\t\tImprime esta ayuda'
	print '\t' + argv[0] + ' directorio_de_imagenes [umbral]'
	print '\t\tSi umbral no está seteada, utiliza 10 que generalmente funciona bien.'
	print '\t\tValores muy bajos para umbral pueden detectar fotos como diferentes sin serlo'
	print '\t\ty valores muy altos pueden de detectar fotos diferentes como iguales.'
	exit()

def msd(im1path, im2path, thrsh):
	'''Devuelve True si la Mean Square Difference es entre im1 e im2 es menor que el umbral thrsh'''
	im1 = asarray(Image.open(im1path))
	im2 = asarray(Image.open(im2path))
	im1 = im1.astype(int)
	im2 = im2.astype(int)
	
	diff = abs(im1 - im2)
	#print im1path + ' ' + ' ' + im2path + ' ' + str(sqrt((diff * diff).sum() / float(800*600)))
	return sqrt((diff * diff).sum() / float(800*600)) < thrsh

if len(argv) >= 2:
	if argv[1] == '-h':
		ayuda()
	else:
		basepath = argv[1]
if len(argv) >= 3:
	try:thrsh = int(argv[2])
	except: ayuda()

files = natsorted((glob(basepath + '*.png')), cmp=natcmp)
print 'Procesando el directorio ' + basepath
print str(len(files)) + ' archivos encontrados...'
batched = []
filerfl = 1 
for i in range(0, len(files)-1):
#for i in range(9090,9095):
	if not msd(files[i], files[i+1], thrsh):
		import io
		batched.append(files[i])
		f = io.open(basepath + str(filerfl) + '.rfl', 'wb')
		for fi in batched:
			f.write(fi+'\n')
		filerfl+=1
		print '***********END BATCH*****' + files [i+1] + '******'
		batched = []
	else:
		batched.append(files[i])

import io
batched.append(files[i])
f = io.open(basepath + str(filerfl) + '.rfl', 'wb')
for fi in batched:
	f.write(fi+'\n')
filerfl+=1
print '***********END BATCH*****' + files [i+1] + '******'
