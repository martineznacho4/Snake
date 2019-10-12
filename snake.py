from terminal import *
import random

FILAS = 10
COLUMNAS =8
CUERPO = "#"
MANZANA = "O"
MAXP = 4

def main():
	clear_terminal()

	serpiente = []
	fila_serpiente = random.randrange(0,FILAS -2)
	columna_serpiente = random.randrange(0,COLUMNAS -2)
	serpiente.append((fila_serpiente,columna_serpiente))

	tablero = armar_tablero(FILAS,COLUMNAS)

	tablero[columna_serpiente][fila_serpiente] = CUERPO

	movimientoAnterior = ()

	manzanas = manzana()
	manzanaX,manzanaY = manzanas
	tablero[manzanaY][manzanaX] = MANZANA

	imprimir_tablero(tablero)

	movimientoAnterior = ""

	while len(serpiente) < MAXP:

		tablero = armar_tablero(FILAS,COLUMNAS)
		
		fila_serpiente, columna_serpiente, movimientoAnterior = direcciones_serpiente(fila_serpiente,columna_serpiente,movimientoAnterior)

		comerse = comerseASiMisma(fila_serpiente,columna_serpiente,serpiente)

		if fila_serpiente == None and columna_serpiente == None:
			return print("Movimiento invalido")

		manzanas,tablero,serpiente,manzanaY,manzanaX = manzanaEnSerpiente(manzanas,manzanaX,manzanaY,tablero,serpiente,fila_serpiente,columna_serpiente)	

		tablero = agregarSerpienteAlTablero(tablero,serpiente)

		#-----------------Limite del tablero---------------------

		limite = limites(tablero,serpiente, fila_serpiente, columna_serpiente)
		if limite == "Pierde":
			return print("Fuera del limite")

		if comerse == "Pierde":
			return print("La serpiente se comio a si misma")

		clear_terminal()

		imprimir_tablero(tablero)

		print("Puntuación: " + str(len(serpiente)))

	print("Victoria")

#----------Tablero--------------

def armar_tablero(f,c):
	"""Recibe una cantidad de filas y columnas y devuelve una matriz fxc de listas de listas"""
	tablero = []

	for fila in range(f):
		nueva_fila = []
		for columna in range(c):
			nueva_fila.append("'")
		tablero.append(nueva_fila)
	return tablero

def imprimir_tablero(tablero):
	for i in tablero:
		print(i)

def agregarSerpienteAlTablero(tablero, serpiente):
	"""Agrega la posicion actual de la serpiente al tablero"""
	for j in tablero:
			for i in range(len(serpiente)):
				x1,y1 = serpiente[i]
				tablero[y1][x1] = CUERPO
	return tablero			

#----------Manzana---------------

def manzana():
	"""Devuelve una fila y columna aleatorias que definen la posición de una manzana"""
	fila_manzana = random.randrange(0,FILAS - 2 )
	columna_manzana = random.randrange(0,COLUMNAS - 2 )

	return (fila_manzana, columna_manzana)

def manzanaEnSerpiente(manzanas,manzanaX,manzanaY,tablero,serpiente,fila_serpiente,columna_serpiente):
	"""Recibe la posición de una manzana y si la serpiente pasa por esa posición se genera otra manzana aleatoriamente, sino la manzana se mantiene en su posición"""
	if manzanas in serpiente:
		manzanas = manzana()
		manzanaX,manzanaY = manzanas
		tablero[manzanaY][manzanaX] = MANZANA
		serpiente.append((fila_serpiente, columna_serpiente))
		return manzanas, tablero, serpiente,manzanaY,manzanaX
	else:
		tablero[manzanaY][manzanaX] = MANZANA
		serpiente.append((fila_serpiente,columna_serpiente))
		serpiente.pop(0)
		return manzanas, tablero, serpiente,manzanaY,manzanaX

#----------Serpiente-------------

def direcciones_serpiente(x, y, movimientoAnterior):
	"""Recibe la posicion anterior de la serpiente y su ultimo movimiento, y dependiendo de lo que ingrese el usuario se aumenta o disminuye una fila/columna. Si el usuario no ingresa nada el movimiento continua en la direccion anterior"""

	print("Ingrese una dirección: [w/a/s/d]:")
	tecla = timed_input(0.4)

	if tecla == "a" or tecla == "aa":
		act_fila = x - 1
		return (act_fila, y, tecla)

	elif tecla == "d" or tecla == "dd":
		act_fila = x + 1
		return (act_fila, y, tecla)

	elif tecla == "w" or tecla == "ww":
		act_columna = y - 1
		return (x, act_columna, tecla)

	elif tecla == "s" or tecla == "ss":
		act_columna = y + 1
		return (x, act_columna, tecla)

	#----------------------------Si no se presiona ninguna tecla----------
	
	elif tecla == "":
		if movimientoAnterior == "a":
			act_fila = x - 1
			return (act_fila, y, movimientoAnterior)

		elif movimientoAnterior == "d":
			act_fila = x + 1
			return (act_fila, y, movimientoAnterior)

		elif movimientoAnterior == "w":
			act_columna = y - 1
			return (x, act_columna, movimientoAnterior)

		elif movimientoAnterior == "s":
			act_columna = y + 1
			return (x, act_columna, movimientoAnterior)
		else:
			return (x,y,movimientoAnterior)

	else:
		return None, None, tecla

#------------Condiciones para perder----------------

def limites(tablero, serpiente,fila_serpiente,columna_serpiente):
	"""Devuelve la cadena "Pierde" si la serpiente llega a uno de los bordes del tablero"""
	for i in range(len(serpiente)):
		for j in range(len(serpiente[i])):
			if serpiente[i][j] < 0 or serpiente[i][j] > len(tablero):
				return "Pierde"

def comerseASiMisma(fila_serpiente,columna_serpiente,serpiente):
	"""Devuelve la cadena "Pierde" si la siguiente posición de la serpiente ya se encuentra en el cuerpo de la serpiente"""
	if (fila_serpiente,columna_serpiente) in serpiente:
		return "Pierde"


main()
