
from math import sin,cos,pi #Librerias necesarias
import copy
import time

global cerrada #Variables globales para el funcionamiento del codigo
global abierta
global pos_init

#Mapas creados para la ejecucion del programa(descomentar para usar)

mapa_objetivos = [[0,0,0,0,0],
				  [0,1,1,1,0],
				  [0,1,1,1,0],
				  [0,1,1,1,0],
				  [0,1,1,1,0],
				  [0,1,1,1,0],
				  [0,0,0,0,0],]
'''
mapa_objetivos=[[0,0,0,0,0,0,0,0,0],
				[0,0,1,1,1,1,0,0,0],
				[0,0,1,1,1,1,0,0,0],
				[0,0,0,0,1,1,0,0,0],
				[0,1,1,1,1,1,1,0,0],
				[0,1,1,1,1,1,1,0,0],
				[0,1,1,1,0,0,0,0,0],
				[0,0,0,1,1,1,0,0,0],
				[0,0,0,1,1,1,0,0,0],
				[0,0,0,0,0,0,0,0,0]]

mapa_objetivos=[[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
				[0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0],
				[0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0],
				[0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0],
				[0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0],
				[0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
				[0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
				[0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
				[0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
				[0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
				[0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
				[0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0],
				[0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0],
				[0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0],
				[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]'''
				
class Estanteria(): #Clase Estanteria con la que se crean los objetos

	def __init__(self,p0,pf):

		self.p0=p0 #Posicion central de la estanteria
		self.pizq = [p0[0] + int(cos(self.p0[2]*(pi/2))),p0[1] + int(sin(self.p0[2]*(pi/2))), self.p0[2]] #Calculo de los lados de la estanteria
		self.pder = [p0[0] - int(cos(self.p0[2]*(pi/2))),p0[1] - int(sin(self.p0[2]*(pi/2))), self.p0[2]]
		self.pf=pf #Posicion de entrega o final

	def actualizar_pos(self,pNuevo): #Metodo para mover la estanteria

		#print('pNuevo:',pNuevo)

		pizq = self.pizq #Guardamos las posiciones anteriores por si tenemos que restaurarlas
		pder = self.pder

		self.pizq = [pNuevo[0] + int(cos(pNuevo[2]*(pi/2))),pNuevo[1] + int(sin(pNuevo[2]*(pi/2))), pNuevo[2]] #Calculamos los nuevos lados de la estanteria
		self.pder = [pNuevo[0] - int(cos(pNuevo[2]*(pi/2))),pNuevo[1] - int(sin(pNuevo[2]*(pi/2))), pNuevo[2]]

		#print('Nuevos lados')
		#print(self.pizq)
		#print(self.pder)

		if mapa_objetivos[self.pizq[0]][self.pizq[1]]!=0 and mapa_objetivos[self.pder[0]][self.pder[1]]!=0 and mapa_objetivos[pNuevo[0]][pNuevo[1]]!=0: #Si la estanteria entra en el lugar al que se mueve
	
			self.p0=pNuevo #Aceptamos esa posicion como nueva y avisamos
			#print('Aceptado:',self.p0)
			return True

		else:

			#print('Fallido') #Rechazamos esa posicion, restauramos los valores antiguos y avisamos
			self.pder= pder
			self.pizq = pizq

			return False
	
	def destino(self): #Comprobamos si estamos en el destino final

		return self.p0==self.pf

	def print(self): #Mostramos la posicion inicial

		print(self.p0)

class Nodo():
	
	def __init__(self,pai,mapa,pos,estante): #Valores internos de los nodos
	
		self.pos=pos #Posicion del robot
		self.f=0 #Funcion de evaluación
		self.g=0 #Coste heuristico de cada nodo
		self.pai=pai #Cada nodo garda os seus nodos relacionados
		self.fillo=None
		self.mapa=mapa #E unha copia do mapa

		self.estante = estante #Vector de estanterias
		
	def addNodo(self,mapa,pos,g,estante): #Metodo para crear nodos
		
		novo_nodo=Nodo(self,mapa,pos,estante) #Creamos o nodo

		distancia=0 #Calculamos a sua heuristica
		for p in estante:

			if not p.destino():

				distancia += (abs(p.pf[0]-p.p0[0]) + abs(p.p0[0]-novo_nodo.pos[0]) + abs(p.pf[1]-p.p0[1]) + abs(p.p0[1]-novo_nodo.pos[1]) + abs((p.pf[2]-p.p0[2])*(2+int(novo_nodo.pos[3]))) + abs((p.p0[2]-novo_nodo.pos[2])*(2+int(novo_nodo.pos[3]))))

		euclideo = distancia + (abs(pos_init[0]-novo_nodo.pos[0]) + abs(pos_init[1]-novo_nodo.pos[1]) + abs((pos_init[2]-novo_nodo.pos[2])*(2+int(novo_nodo.pos[3]))))

		novo_nodo.g=novo_nodo.pai.g+g #Añadimos el coste da accion al coste del nodo anterior
		novo_nodo.f=novo_nodo.g+euclideo #Calculamos la funcion de transferencia con la heuristica

		if abierta == []: #Ordenamos abierta, si no tiene elementos, se añade sin mas

			abierta.append(novo_nodo)

		else: #Si tiene elementos
			
			for i in range(len(abierta)):

				if abierta[i].f>novo_nodo.f: #Comprueba las funciones heuristicas y lo mete en su posicion

					abierta.insert(i,novo_nodo)
					break

				if i==len(abierta)-1: #Si es la ultima posicion, lo añade al final

					abierta.append(novo_nodo)

		return novo_nodo #Devuelve el nodo final

	def comprobar(self,actual): #Metodo de comprobacion de nodos repetidos sobre cerrada

		for nodo in cerrada: #Comprobamos cada nodo

			final = 0 

			for i in range(len(nodo.estante)): #Para cada estanteria

				if nodo.estante[i].p0 == actual.estante[i].p0: #Comprobamos cada una y si son iguales sumamos a la variable de control

					final +=1

			if nodo.pos==actual.pos and final == len(nodo.estante): #Si la posicion del robot y la posicion de las estanterias son las mismas, sacamos un nuevo nodo de abierta

				actual=self.comprobar(abierta.pop(0))
			
		return actual

	def cercania(self,actual,est): #Comprobamos bajo que estanteria estamos

		#print('Actual:',actual.pos)

		for element in est: #Para cada estanteria, comprobamos si estamos debajo y no esta entregada

			#print('Pos estanterias:',element.p0)

			if actual.pos[:2] == element.p0[:2] and not element.destino():

				return est.index(element) #Devolvemos el indice

		return -1 #Si no hay, devolvemos un fallo

	def run(self): #Ejecucion principal del programa

		g = open('plan.txt','w') #Ficheros de escritura
		f = open('stadistics.txt','w')

		exito=False #Exito del programa

		start = time.time() #Inicio del tiempo de ejecucion

		while not exito and len(abierta)!=0: #Mientras tengamos elementos y no tengamos solucion

			actual=self.comprobar(abierta.pop(0)) #Sacamos un nodo de abierta

			tmp = copy.deepcopy(actual.estante) #Copiamos las estanterias

			#if tmp[0].destino():
			#
			#	print('Actual:',actual.pos)
			#	print(tmp[0].p0)
			#	print(tmp[1].p0)

			final = 0

			for element in tmp: #Si todas las estanterias estan entregadas

				if element.destino():

					final += 1

			if final == len(tmp) and actual.pos == pos_init: #Y el robot esta en el inicio, finalizamos la ejecucion

				exito = True

			else:

				est = self.cercania(actual,tmp) #Comprobamos cual es la estanteria que tengo encima

				self.elevador_subir(actual,copy.deepcopy(tmp),est) #Todos los operadores programados en base a esa estanteria
				self.elevador_bajar(actual,copy.deepcopy(tmp),est)
				self.mover(actual,copy.deepcopy(tmp),est)
				self.girar_izquierda(actual,copy.deepcopy(tmp),est)
				self.girar_derecha(actual,copy.deepcopy(tmp),est)

				cerrada.append(actual) #Metemos el nodo en cerrada

				#input()

		f.write('Tiempo de ejecucion: {0}\n'.format(time.time() - start)) #Añadimos datos al fichero de estadisticas
		f.write('Coste total: {0}\n'.format(actual.g))
		f.write('Nodos expandidos: {0}\n'.format(len(cerrada)+1))

		print("Terminamos pibe") #Mensaje de finalizacion

		plan=[]
		while actual.pai!=None: #Recuperamos el plan

			plan.append(actual.pos)
			actual=actual.pai
	
		plan=plan[::-1] #Y le damos la vuelta para verlo
  
		#print(plan)
		g.write(str(plan)) #Guardamos los datos en los ficheros
		f.write('Longitud del plan: {0}\n'.format(len(plan)))
  
	def elevador_subir(self,actual,tmp,est): #Metodo de elevacion de las estanterias
     
		pos_temp=actual.pos.copy()
		nuevo_mapa=actual.mapa.copy()

		if actual.pos[:2] == tmp[est].p0[:2] and not tmp[est].destino() and not actual.pos[3]: #Si estamos debajo de una, no esta entregada y no esta levantado ya, lo levanta
			
			pos_temp[3]=True
			actual.addNodo(nuevo_mapa,pos_temp,3,tmp)

	def elevador_bajar(self,actual,tmp,est): #Metodo de bajada de estanterias

		pos_temp=actual.pos.copy()
		nuevo_mapa=actual.mapa.copy()

		if pos_temp[3]: #Si esta subido, lo bajass

			pos_temp[3]=False
			actual.addNodo(nuevo_mapa,pos_temp,3,tmp)

	def mover(self,actual,tmp,est): #Metodo de movimiento del robot y las estanterias

		pos_temp=actual.pos.copy()
		nuevo_mapa=actual.mapa.copy()
		valor = True #Valor de verificacion de las estanterias

		if pos_temp[2]==0: #Comprobacion de movimiento por angulo 

			pos_temp[0]-=1

		elif pos_temp[2]==-1:

			pos_temp[1]-=1

		elif pos_temp[2]==1:

			pos_temp[1]+=1

		elif pos_temp[2]==-2:

			pos_temp[0]+=1

		z=1 #Coste del operador

		if mapa_objetivos[pos_temp[0]][pos_temp[1]]!=0: #Si el espacio al que se mueve no es una pared

			if actual.pos[3] and est!=-1: #Si el elevador esta subido y no tenemos una señal de fallo

				z+=1 #Aumentamos el coste del operador

				valor = tmp[est].actualizar_pos([pos_temp[0],pos_temp[1],tmp[est].p0[2]]) #Actualizamos la estanteria y esperamos el valor de verificacion de que se puede mover
			
			if valor: #Si la estanteria puede ir a esa posicion

				actual.addNodo(nuevo_mapa,pos_temp,z,tmp) #Añadimos el nodo

	def girar_izquierda(self,actual,tmp,est): #Metodo para girar a la izquierda

		pos_temp=actual.pos.copy()
		valor = True #Valor de verificacion de las estanterias

		if pos_temp[2]==0: #Giro respecto al angulo anterior

			pos_temp[2]=-1

		elif pos_temp[2]==-1:

			pos_temp[2]=-2

		elif pos_temp[2]==-2:

			pos_temp[2]=1

		elif pos_temp[2]==1:

			pos_temp[2]=0

		z=2 #Coste del operador

		if pos_temp[3] and est!=-1: #Elevador subido y no es un fallo

			giro = tmp[est].p0[2] #Cambiamos el giro de la estanteria
			giro-=1
			if giro<-2:
				giro=1

			z+=1 #Aumentamos el coste del operador

			valor = tmp[est].actualizar_pos([tmp[est].p0[0],tmp[est].p0[1],giro]) #Giramos la estanteria y esperamos verificacion

		if valor: #Si la estanteria verifica, creamos el nodo

			actual.addNodo(mapa_objetivos,pos_temp,z,tmp)

	def girar_derecha(self,actual,tmp,est): #Metodo para girar a la derecha

		pos_temp=actual.pos.copy()
		valor = True #Valor de verificacion de la estanteria

		if pos_temp[2]==0: #Giro respecto al angulo

			pos_temp[2]=1

		elif pos_temp[2]==1:

			pos_temp[2]=-2

		elif pos_temp[2]==-2:

			pos_temp[2]=-1

		elif pos_temp[2]==-1:

			pos_temp[2]=0

		z=2 #Coste del operador

		if pos_temp[3] and est!=-1: #Elevador subido y no es un fallo

			giro = tmp[est].p0[2] #Giramos la estanteria
			giro+=1
			if giro>1:
				giro=-2

			z+=1 #Aumentamos el coste del operador

			valor = tmp[est].actualizar_pos([tmp[est].p0[0],tmp[est].p0[1],giro]) #Giramos estanteria y esperamos verificacion

		if valor: #Si esta verificado, creamos el nodo

			actual.addNodo(mapa_objetivos,pos_temp,z,tmp)

if __name__ == "__main__":

	#Posicion inicial del robot(descomentar para probar)
	
	pos_init = [1,2,0,False] #Posicion inicial para el primer mapa
	#pos_init = [8,4,0,False] #Posicion inicial para los dos siguientes

	#Estanterias con las que trabaja(descomentar para probar)

	estanterias = [Estanteria([2,3,0],[4,3,0])] #Estanteria para el primer mapa
	#estanterias = [Estanteria([2,3,0],[4,3,0]),Estanteria([2,1,0],[4,1,0])] #Estanterias para el primer mapa
	#estanterias = [Estanteria([5,2,0],[2,4,0])] #Estanterias para el segundo mapa
	#estanterias = [Estanteria([8,3,0],[3,7,0]),Estanteria([9,13,0],[3,9,0])] #Estanterias para el tercer mapa

	root=Nodo(None,mapa_objetivos,pos_init,estanterias) #Nodo inicial

	cerrada=[] #Lista de cerrada de A*
	abierta=[root] #Lista de abierta de A*

	root.run() #Ejecucion del algoritmo A*