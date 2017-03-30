#!/usr/bin/env python
# -*- coding: utf-8 -*-
from crccheck.crc import Crc16Buypass		#Libreria para calcular CRC
import array								#Libreria para almacenar array
import rfm22b_demod							#Programa generado en GRC
import datetime								#Libreria para almacenar la hora
from gnuradio import gr				
from time import sleep
from binascii import hexlify, unhexlify
import sys

#colores para diferenciar las partes de la trama
def pink(t):	return '\033[95m' + t + '\033[0m'
def blue(t):	return '\033[94m' + t + '\033[0m'
def yellow(t):	return '\033[93m' + t + '\033[0m'
def green(t):	return '\033[92m' + t + '\033[0m'
def red(t):		return '\033[91m' + t + '\033[0m'

#Llamamos al programa en GRC
tb = rfm22b_demod.rfm22b_demod()
tb.start() 														#Inicializamos

while True:
    if tb.msg_sink.count(): 									# Si existe un dato 

	current_time	= datetime.datetime.now().time() 
	current_time	= current_time.isoformat() 					#Almacenamos la hora
	
	frame		= tb.msg_sink.delete_head_nowait().to_string() 	#Convertimos el dato a string
	#print hexlify(frame)
	from_id		= hexlify(frame[0:1])							#De donde viene
	to_id		= hexlify(frame[1:2])   						#Hacia donde va
	ID			= hexlify(frame[2:3])   						#Identificacion
	flag		= hexlify(frame[3:4])   						#Bandera
	pkt_len		= hexlify(frame[4:5])   						#Tamanio del frame en Hex
	length		= int(pkt_len,16)								#Tamanio del frame en Int
	data		= frame[5:5+length]								#frame en ASCII
	crc			= hexlify(frame[5+length:5+length+2]) 			#CRC (Cyclic Redundancy Check)
	
	arrayD=array.array('B',frame[0:5+length]) 					#almacenamos el frame en un array
	CRCFinal = Crc16Buypass.calc(arrayD) 						#Calculamos el CRC para el frame obtenido
	a = CRCFinal 												#Almacenamos el CRC calculado en 'a'
	b = '%x' % a 												#Almacenamos el hexadecimal sin '0x'
	#print b
	#print crc

	if crc==b: 													#Si el CRC calculado es igual al CRC obtenido se confirma el dato
	    print "[%s] %s %s %s %s %s %s %s" %(current_time,yellow(from_id),blue(to_id),green(ID),flag,red(pkt_len),data,yellow(crc)) #Se imprime el dato correcto
