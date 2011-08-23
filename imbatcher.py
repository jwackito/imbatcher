#!/usr/bin/python
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

def msd(im1path, im2path, thrsh, verbose):
	from PIL import Image
	import numpy
	'''Devuelve True si la Mean Square Difference es entre im1 e im2 es menor que el umbral thrsh'''
	im1 = Image.open(im1path)
	im2 = Image.open(im2path)
	if im1.size != im2.size:
		return False
	else:
		(w,h)= im1.size
	im1 = numpy.asarray(im1)
	im2 = numpy.asarray(im2)
	im1 = im1.astype(int)
	im2 = im2.astype(int)
	
	diff = abs(im1 - im2)
	#print im1path + ' ' + ' ' + im2path + ' ' + str(sqrt((diff * diff).sum() / float(800*600)))
	if verbose:
		print im1path + ' ' + ' ' + im2path + ' ' + str(numpy.sqrt(abs((diff * diff).sum() / float(w*h))))
	return numpy.sqrt(abs((diff * diff).sum() / float(w*h))) < thrsh

def findthrsh(files, index, verbose):
	from PIL import Image
	import numpy
	(w,h)=Image.open(files[index]).size
	partial = 0
	for i in range(index, index + 10):
		im1 = numpy.asarray(Image.open(files[i])).astype(int)
		im2 = numpy.asarray(Image.open(files[i+1])).astype(int)
		diff = abs(im1 - im2)
		partial+=(numpy.sqrt(abs((diff * diff).sum() / float(w*h))))*1.3
	if verbose:
		print 'Using threshold = ' + str(int((partial/10)+5))
	return int((partial/10)+5)

def process(basepath, thrsh, fformat, prefix, verbose):
	import os
	import glob
	import natsorted
	import io

	if basepath[-1] != '/':
		basepath += '/'
	files = natsorted.natsorted((glob.glob(basepath + '*.' + fformat)), cmp=natsorted.natcmp)
	print 'Processing the directory ' + basepath
	print str(len(files)) + ' files found...'
	batched = []
	filerfl = 1 
	adaptive = False
	if thrsh == 0:
		#Using addaptive threshold
		adaptive = True
		thrsh = findthrsh(files, 0, verbose)
	for i in range(0, len(files)-1):
		if not msd(files[i], files[i+1], thrsh, verbose):
			batched.append(files[i])
			f = io.open(basepath + prefix + str(filerfl) + '.rfl', 'wb')
			for fi in batched:
				f.write(fi+'\n')
			filerfl+=1
			print '***********END BATCH*****' + files [i+1] + '******'
			batched = []
			if adaptive:
				thrsh = findthrsh(files, i+1, verbose)
		else:
			batched.append(files[i])
	batched.append(files[i])
	f = io.open(basepath + prefix + str(filerfl) + '.rfl', 'wb')
	for fi in batched:
		f.write(fi+'\n')
	filerfl+=1
	print '***********END BATCH*****' + files [i+1] + '******'

def __Main__():
	import argparse
	
	parser = argparse.ArgumentParser(description='Mean Square Difference based image batcher. The program generate a set of Registax 6 frame list (.rfl) files, one for each batch of images.')	
	parser.add_argument('-t', '--threshold', dest='thrsh', type=int, default=0, help='El umbral para las diferencias. Por defecto es 0, para umbral adaptativo.')
	parser.add_argument('-f', '--format', dest='fformat', choices=['jpg', 'png', 'bmp'], default='png', help='El formato de los archivos a tratar.')
	parser.add_argument('-p', '--list-prefix', dest='prefix', default='list', help='El prefijo para los nombres de los .rfl')
	parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', default=False, help='Mucha mucha salida. Puede hacer más lento el proceso. Util para setear el umbral.')
	parser.add_argument('-d', '--dir', dest='basepath', required=True, help='El directorio donde están las fotos.')
	args = parser.parse_args()
	#must be one of the formats provided here http://www.pythonware.com/library/pil/handbook/index.htm
	process(args.basepath, args.thrsh, args.fformat, args.prefix, args.verbose)

__Main__()
