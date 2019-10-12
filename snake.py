from terminal import *
import random

FILAS = 10
COLUMNAS =8
CUERPO = "#"
MANZANA = "O"
MAXP = 3

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


	while len(serpiente) < MAXP:


		tablero = armar_tablero(FILAS,COLUMNAS)

#Cree la variable movimiento anterior pero creo que va a haber que sacarla y guardar la tecla de direcciones serpiente en realidad
		movimientoAnterior = ""
		fila_serpiente, columna_serpiente, movimientoAnterior = direcciones_serpiente(fila_serpiente,columna_serpiente,movimientoAnterior)

		#print(movimientoAnterior)


		if fila_serpiente == None and columna_serpiente == None:
			return print("Movimiento invalido")


		#cuerpost =cuerpo_en_manzana(tablero, manzanaY, manzanaX)

		if manzanas in serpiente:


				manzanas = manzana()
				manzanaX,manzanaY = manzanas
				tablero[manzanaY][manzanaX] = MANZANA

				serpiente.append((fila_serpiente, columna_serpiente))

		else:

			tablero[manzanaY][manzanaX] = MANZANA
			serpiente.append((fila_serpiente,columna_serpiente))
			serpiente.pop(0)


		for j in tablero:
			for i in range(len(serpiente)):
				x1,y1 = serpiente[i]
				tablero[y1][x1] = CUERPO



#-----------------Limite del tablero---------------------

		limite = limites(tablero,serpiente)
		if limite == "Pierde":
			return print("Fuera del limite")


		#print(manzanas)
		#print(serpiente)
		clear_terminal()

		imprimir_tablero(tablero)


		print("Puntuación: " + str(len(serpiente)))

	print("Ganaste")


#----------Tablero--------------

def armar_tablero(f,c):
	"""Recibe una cantidad de filas y columnas y devuelve una matriz fxc de listas de listas"""
	tablero = []

	for fila in range(f):
		nueva_fila = []
		for columna in range(c):
			nueva_fila.append(' ')
		tablero.append(nueva_fila)
	return tablero


def imprimir_tablero(tablero):
	for i in tablero:
		print(i)


#----------Manzana---------------

def manzana():
	"""Devuelve una fila y columna aleatorias"""
	fila_manzana = random.randrange(0,FILAS - 2 )
	columna_manzana = random.randrange(0,COLUMNAS - 2 )

	return (fila_manzana, columna_manzana)


def nueva_manzana(tablero, manzanas, manzanaX, manzanaY):

	manzanas = manzana()
	manzanaX,manzanaY = manzanas
	tablero[manzanaY][manzanaX] = MANZANA
	return tablero


#----------Serpiente-------------

def direcciones_serpiente(x, y, movimientoAnterior):
	"""Recibe la posición anterior de la serpiente en filas y columnas y dependiendo de lo que ingrese el usuario, se aumenta o disminuye la fila/columna"""


	print("Ingrese una dirección: [w/a/s/d] ")
	tecla = timed_input(0.4)


	if tecla == "a":
		act_fila = x - 1
		return (act_fila, y, tecla)

	elif tecla == "d":
		act_fila = x + 1
		return (act_fila, y, tecla)

	elif tecla == "w":
		act_columna = y - 1
		return (x, act_columna, tecla)

	elif tecla == "s":
		act_columna = y + 1
		return (x, act_columna, tecla)

#----------------------------Si no se presiona ninguna tecla
	elif tecla == "" or movimientoAnterior == "a":
		act_fila = x - 1
		return (act_fila, y, tecla)

	elif tecla == "" or movimientoAnterior == "d":
		act_fila = x + 1
		return (act_fila, y, tecla)

	elif tecla == "" or movimientoAnterior == "w":
		act_columna = y - 1
		return (x, act_columna, tecla)

	elif tecla == "" or movimientoAnterior == "s":
		act_columna = y + 1
		return (x, act_columna, tecla)
	else:
		return None, None, tecla


#------------Condiciones para perder----------------

def limites(tablero, serpiente):
	for i in range(len(serpiente)):
		for j in range(len(serpiente[i])):
			if serpiente[i][j] < 0 or serpiente[i][j] > len(tablero):
				return "Pierde"

	if serpiente[::-1] in serpiente:
		print("...")
		return "Pierde"





main()
