from terminal import *
import random
import csv


CUERPO = "#"
MANZANA = "O"
OBSTACULO = "%"
VELOCIDADMAX = 0.3

ACELERAR = "&"
DESACELERAR = "!"
AGRANDAR = "+"
ACHICAR = "-"
SIMBOLO = "simbolo"
ALTERACION = "alteracion"
CANTIDAD = "cantidad"
TECLA = "tecla"
DESCRIPCION = "descripcion"

ARRIBA = "w"
ABAJO = "s"
DERECHA = "d"
IZQUIERDA = "a"


def main():
	clear_terminal()
	puntuacion_total = 0
	try:
		ruta_nivel = 1
		while True:
			clear_terminal()

			mochila = {}
			serpiente = []
			cabeza_serpiente = ()
			lista_de_especiales = []
			lista_de_obstaculos = []
			movimiento_anterior = ()
			posiciones_de_especiales = []

			longitud_por_nivel,velocidad_por_nivel,dimension_nivel,lista_de_obstaculos,especiales_nivel,lista_de_especiales = leer_archivo(ruta_nivel,lista_de_especiales,lista_de_obstaculos)
			
			mochila = crear_mochila(lista_de_especiales,mochila)

			cabeza_serpiente,pos_inicial_serpienteX,pos_inicial_serpienteY,serpiente = crear_serpiente(dimension_nivel,serpiente,lista_de_obstaculos)

			tablero = armar_tablero(dimension_nivel)

			tablero[pos_inicial_serpienteX][pos_inicial_serpienteY] = CUERPO

			manzanaX,manzanaY,tablero= crear_manzana(dimension_nivel,serpiente,lista_de_obstaculos,tablero)
			
			posiciones_de_especiales = crear_especiales(dimension_nivel,posiciones_de_especiales,especiales_nivel,serpiente,lista_de_obstaculos,(manzanaX,manzanaY))

			especial_aleatorio = alternar_especiales(especiales_nivel)

			actualizar_tablero(tablero,serpiente, lista_de_obstaculos, posiciones_de_especiales,especial_aleatorio,especiales_nivel)

			movimiento_anterior = ""

			serpiente = juego(tablero,serpiente,longitud_por_nivel,dimension_nivel,mochila,lista_de_especiales,cabeza_serpiente,movimiento_anterior,velocidad_por_nivel,manzanaX,manzanaY,lista_de_obstaculos,posiciones_de_especiales,especial_aleatorio,especiales_nivel)

			ruta_nivel += 1
			puntuacion_total += len(serpiente)
		
	except:
		print(f"Gracias por jugar. Llegó hasta el Nivel: {ruta_nivel-1} y su puntuacion total es de: {puntuacion_total}")

def leer_archivo(ruta_nivel,lista_de_especiales,lista_de_obstaculos):
	with open("nivel_" + str(ruta_nivel) + ".txt") as archivo, open("especiales.csv") as especiales:
		especiales_csv = csv.DictReader(especiales)

		longitud_por_nivel = archivo.readline().rstrip("\n")
		velocidad_por_nivel = float(archivo.readline().rstrip("\n"))
		dimension_nivel = archivo.readline().rstrip("\n").split(",")
		obstaculos_nivel = archivo.readline().rstrip("\n").split(";")
		especiales_nivel = archivo.readline().rstrip("\n").split(",")
		
		for especial in especiales_csv:
			if especial[SIMBOLO] in especiales_nivel:
				lista_de_especiales.append(especial)
		
		for i in range(len(obstaculos_nivel)):
			obsX,obsY = obstaculos_nivel[i].split(",")
			lista_de_obstaculos.append((int(obsX),int(obsY)))

	return longitud_por_nivel,velocidad_por_nivel,dimension_nivel,lista_de_obstaculos,especiales_nivel,lista_de_especiales	

#----------Tablero--------------
def armar_tablero(dimensiones):
	"""Recibe una cantidad de filas y columnas y devuelve una matriz fxc de listas de listas"""
	tablero = []

	for fila in range(int(dimensiones[0])):
		nueva_fila = []
		for columna in range(int(dimensiones[1])):
			nueva_fila.append(" ")
		tablero.append(nueva_fila)
	return tablero

def actualizar_tablero(tablero, serpiente, obstaculo,posiciones_de_especiales,especial_aleatorio,especiales_nivel):
	"""Actualiza el tablero actual con la posicion de la serpiente, los obstaculos y los especiales en el"""
	for j in tablero:
		for i in range(len(serpiente)):
			x1,y1 = serpiente[i]
			tablero[x1][y1] = CUERPO
		
		for i in range(0,len(obstaculo)):
			obstaculo_x, obstaculo_y = obstaculo[i]
			tablero[obstaculo_x][obstaculo_y] = OBSTACULO
		
		for i in range(len(posiciones_de_especiales)):			
			especialx,especialy = posiciones_de_especiales[i]			
			tablero[especialx][especialy] = especiales_nivel[especial_aleatorio[i]]

		print(j)	
	return tablero			
	
#----------Mochila---------------
def crear_mochila(lista_de_especiales,mochila):
	"""Devuelve una mochila con los especiales que contiene el nivel"""
	for i in range(len(lista_de_especiales)):
	
		lista_de_especiales[i].update({CANTIDAD : 0})

		if mochila.get(lista_de_especiales[i][TECLA]) == None: 
		
			 mochila[lista_de_especiales[i][TECLA]] = lista_de_especiales[i]
	return mochila

def imprimir_mochila(mochila,lista_de_especiales):
	print("Mochila: ")
	print("Simbolo		||Tecla		||Cantidad		||Descripcion")
	claves = list(mochila.keys())
	
	for i in range(len(lista_de_especiales)):
		if lista_de_especiales[i][TECLA] in claves:
			print(f"{mochila[claves[i]][SIMBOLO]}		||{mochila[claves[i]][TECLA]}		||{mochila[claves[i]][CANTIDAD]}			||{mochila[claves[i]][DESCRIPCION]}")

#----------Especiales------------
def crear_especiales(dimension_del_tablero,posiciones,cantidad_de_especiales,serpiente,lista_de_obstaculos,manzana):
	"""Crea una coordenada para poner un especial en el tablero, teniendo en cuenta que el especial no puede ocupar el lugar de un obstaculo, la manzana, o la serpiente"""
	for i in range(0,len(cantidad_de_especiales)-1):
		pos_especialX,pos_especialY = coord_XY(dimension_del_tablero)
		
		while (pos_especialX,pos_especialY) in serpiente or (pos_especialX,pos_especialY) in lista_de_obstaculos or (pos_especialX,pos_especialY) == manzana:
			pos_especialX,pos_especialY = coord_XY(dimension_del_tablero)

		posiciones.append((pos_especialX,pos_especialY))
	return posiciones

def come_un_especial(posiciones_de_especiales,mochila,lista_de_especiales,tablero,dimension_del_tablero,especiales_nivel,serpiente,lista_de_obstaculos,especial_aleatorio,manzana):
	"""Si la serpiente come un especial aumenta la cantidad de ese tipo en la mochila, y a su vez genera otro especial"""
	cabeza_serpiente_x,cabeza_serpiente_y = serpiente[-1]
	
	claves = list(mochila.keys())
	for i in range(len(mochila)):
		if mochila[claves[i]][SIMBOLO] == lista_de_especiales[i][SIMBOLO] and	tablero[cabeza_serpiente_x][cabeza_serpiente_y] == lista_de_especiales[i][SIMBOLO]:
			mochila[claves[i]][CANTIDAD] += 1
	
	for i in range(len(posiciones_de_especiales)):
		while posiciones_de_especiales[0] in serpiente or posiciones_de_especiales[0] in lista_de_obstaculos:
			posiciones_de_especiales = crear_especiales(dimension_del_tablero,posiciones_de_especiales,lista_de_especiales,serpiente,lista_de_obstaculos,(manzana))
			especial_aleatorio = alternar_especiales(especiales_nivel)
			posiciones_de_especiales.remove(serpiente[-1])	

	return especial_aleatorio,mochila

def usa_especial(lista_de_especiales,serpiente,velocidad,mochila,tecla):
	"""Activa un especial de la mochila cuando el jugador presiona la tecla correspondiente a ese especial"""
	
	if mochila[tecla][CANTIDAD]>0:
		if mochila[tecla][SIMBOLO] == ACELERAR and velocidad > VELOCIDADMAX and float(mochila[tecla][ALTERACION]) < velocidad:
			velocidad -= float(mochila[tecla][ALTERACION])
			mochila[tecla][CANTIDAD] -=1

		if 	mochila[tecla][SIMBOLO] == DESACELERAR:
			velocidad += float(mochila[tecla][ALTERACION])
			mochila[tecla][CANTIDAD] -=1

		if mochila[tecla][SIMBOLO] == AGRANDAR:	
			for i in range(int(mochila[tecla][ALTERACION])):
				serpiente.append(serpiente[-1])
			mochila[tecla][CANTIDAD] -=1	

		if mochila[tecla][SIMBOLO] == ACHICAR and len(serpiente) > 1:
			for i in range(0,int(mochila[tecla][ALTERACION])):
				serpiente.remove(serpiente[0])
			mochila[tecla][CANTIDAD] -=1	

						
	return serpiente, velocidad, mochila

def alternar_especiales(cantidad_especiales):
	"""Genera una lista con elementos aleatorios que van de 0 a la cantidad de especiales"""
	res = []
	for i in range(0,len(cantidad_especiales)):
		especial_aleatorio = random.randrange(0,len(cantidad_especiales))
		res.append(especial_aleatorio)
	return res

#----------Serpiente-------------
def crear_serpiente(dimension_nivel,serpiente,lista_de_obstaculos):
	"""Crea a la serpiente por primera vez, verificando que no se genera en un obstaculo"""
	
	pos_inicial_serpienteX,pos_inicial_serpienteY = coord_XY(dimension_nivel)

	while choca_un_obstaculo((pos_inicial_serpienteX,pos_inicial_serpienteY),lista_de_obstaculos):
		pos_inicial_serpienteX,pos_inicial_serpienteY = coord_XY(dimension_nivel)
	
	cabeza_serpiente = (pos_inicial_serpienteX,pos_inicial_serpienteY)	
	serpiente.append((pos_inicial_serpienteX,pos_inicial_serpienteY))

	return cabeza_serpiente,pos_inicial_serpienteX,pos_inicial_serpienteY,serpiente

#----------Manzana---------------
def crear_manzana(dimension_del_tablero,serpiente,lista_de_obstaculos,tablero):
	"""Devuelve una fila y columna aleatorias que definen la posición de una manzana"""
	 
	pos_manzanaX,pos_manzanaY = coord_XY(dimension_del_tablero)
	while (pos_manzanaX,pos_manzanaY) in serpiente or (pos_manzanaX,pos_manzanaY) in lista_de_obstaculos:
		pos_manzanaX,pos_manzanaY = coord_XY(dimension_del_tablero)
		
	tablero[pos_manzanaX][pos_manzanaY] = MANZANA

	return pos_manzanaX, pos_manzanaY,tablero

def la_serpiente_comio(posiciones_XY_manzana,tablero,serpiente,cabeza,dimension_nivel,obstaculo):
	"""Recibe la posición de una manzana y si la serpiente pasa por esa posición se genera otra manzana aleatoriamente, sino la manzana se mantiene en su posición"""
	
	if posiciones_XY_manzana in serpiente:
		manzanaX,manzanaY,tablero = crear_manzana(dimension_nivel,serpiente,obstaculo,tablero)	
		serpiente.append(cabeza)
		return tablero, serpiente, (manzanaX, manzanaY)

	else:
		manzanaX,manzanaY = posiciones_XY_manzana
		tablero[manzanaX][manzanaY] = MANZANA
		serpiente.append(cabeza)
		serpiente.pop(0)
		return tablero, serpiente, (manzanaX,manzanaY)

#----------Movimiento-------------
def direcciones_serpiente(cabeza, movimiento_anterior,velocidad,lista_de_especiales,mochila,serpiente):
	"""Recibe la posicion de la cabeza de la serpiente y su ultimo movimiento, y dependiendo de lo que ingrese el usuario se activa un especial o aumenta/disminuye una fila/columna. Si el usuario no ingresa nada el movimiento continua en la direccion anterior"""

	print("Ingrese una dirección: [w/a/s/d]:")
	tecla = timed_input(velocidad)

	act_fila,act_columna = cabeza
	if tecla in mochila:
		serpiente,velocidad,mochila = usa_especial(lista_de_especiales,serpiente,velocidad,mochila,tecla)
		tecla = movimiento_anterior	
	
	if tecla == ARRIBA or tecla == "" and movimiento_anterior == ARRIBA:
		tecla = ARRIBA
		act_fila -= 1

	elif tecla == ABAJO or tecla == "" and movimiento_anterior == ABAJO:
		tecla = ABAJO
		act_fila += 1

	elif tecla == IZQUIERDA or tecla == "" and movimiento_anterior == IZQUIERDA:
		tecla = IZQUIERDA
		act_columna -= 1

	elif tecla == DERECHA or tecla == "" and movimiento_anterior == DERECHA:
		tecla = DERECHA
		act_columna += 1
	
	elif tecla == "" and movimiento_anterior == "":
		return (act_fila, act_columna), tecla,serpiente,velocidad,mochila

	else:
		return (None, None), tecla,serpiente,velocidad,mochila

	return (act_fila, act_columna), tecla,serpiente,velocidad,mochila	

#----------Condiciones para perder----------------
def choca_un_obstaculo(cabeza,obstaculo):
	"""Valida si la cabeza de la serpiente choca contra un obstaculo"""
	for i in range(0,len(obstaculo)):
		obstaculo_x, obstaculo_y = obstaculo[i]
		if (int(obstaculo_x),int(obstaculo_y)) == cabeza:
			return True

def serpiente_en_el_borde(serpiente,dimension):
	"""Devuelve True si la serpiente llega a uno de los bordes del tablero"""	
	return serpiente[-1][0] < 0 or serpiente[-1][1] < 0  or serpiente[-1][0] > int(dimension[0]) -1 or serpiente[-1][1] > int(dimension[1]) -1
	

def se_comio_a_si_misma(cabeza, serpiente, movimiento_anterior):
	"""Devuelve True si la siguiente posición de la cabeza de la serpiente ya se encuentra ocupada por su cuerpo"""
	return cabeza in serpiente and movimiento_anterior is not ""

def coord_XY(dimension_del_tablero):
	coordx = random.randrange(0,int(dimension_del_tablero[0]))
	coordy = random.randrange(0,int(dimension_del_tablero[1]))
	return coordx,coordy

def juego(tablero,serpiente,longitud_por_nivel,dimension_nivel,mochila,lista_de_especiales,cabeza_serpiente,movimiento_anterior,velocidad_por_nivel,manzanaX,manzanaY,lista_de_obstaculos,posiciones_de_especiales,especial_aleatorio,especiales_nivel):
	while len(serpiente) < int(longitud_por_nivel):
		tablero = armar_tablero(dimension_nivel)
		imprimir_mochila(mochila,lista_de_especiales)
	
		cabeza_serpiente, movimiento_anterior,serpiente,velocidad_por_nivel,mochila = direcciones_serpiente(cabeza_serpiente,movimiento_anterior,velocidad_por_nivel,lista_de_especiales,mochila,serpiente)
			
		comerse = se_comio_a_si_misma(cabeza_serpiente, serpiente, movimiento_anterior)
	
		if None in cabeza_serpiente: 
			return print("Movimiento invalido")
	
		tablero,serpiente,(manzanaX,manzanaY) = la_serpiente_comio((manzanaX,manzanaY),tablero,serpiente,cabeza_serpiente,dimension_nivel,lista_de_obstaculos)			
		
		if serpiente_en_el_borde(serpiente, dimension_nivel):
			print("Fuera del limite")
			return 

		if comerse:
			print("La serpiente se comio a si misma")
			return 
			
		if choca_un_obstaculo(cabeza_serpiente,lista_de_obstaculos):
			print("La serpiente choco contra un obstaculo")
			return						

		clear_terminal()									
		
		actualizar_tablero(tablero,serpiente, lista_de_obstaculos, posiciones_de_especiales,especial_aleatorio,especiales_nivel)
		
		if serpiente[-1] in posiciones_de_especiales:
			especial_aleatorio,mochila = come_un_especial(posiciones_de_especiales,mochila,lista_de_especiales,tablero,dimension_nivel,especiales_nivel,serpiente,lista_de_obstaculos,especial_aleatorio,(manzanaX,manzanaY))

		print("Puntuación en este nivel: " + str(len(serpiente)))

	return serpiente	

main()
