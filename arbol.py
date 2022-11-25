
from math import sin,cos,pi
import copy
import time

global cerrada
global abierta
global pos_init

#clase estantería, con atributos de posiciones iniciales y finales


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
				
class Estanteria():

	def __init__(self,p0,pf):

		self.p0=p0
		self.pizq = [p0[0] + int(cos(self.p0[2]*(pi/2))),p0[1] + int(sin(self.p0[2]*(pi/2))), self.p0[2]]
		self.pder = [p0[0] - int(cos(self.p0[2]*(pi/2))),p0[1] - int(sin(self.p0[2]*(pi/2))), self.p0[2]]
		self.pf=pf

	def actualizar_pos(self,pNuevo):

		#print('pNuevo:',pNuevo)

		pizq = self.pizq
		pder = self.pder

		self.pizq = [pNuevo[0] + int(cos(pNuevo[2]*(pi/2))),pNuevo[1] + int(sin(pNuevo[2]*(pi/2))), pNuevo[2]]
		self.pder = [pNuevo[0] - int(cos(pNuevo[2]*(pi/2))),pNuevo[1] - int(sin(pNuevo[2]*(pi/2))), pNuevo[2]]

		#print('Nuevos lados')
		#print(self.pizq)
		#print(self.pder)

		if mapa_objetivos[self.pizq[0]][self.pizq[1]]!=0 and mapa_objetivos[self.pder[0]][self.pder[1]]!=0 and mapa_objetivos[pNuevo[0]][pNuevo[1]]!=0:
	
			self.p0=pNuevo
			#print('Aceptado:',self.p0)
			return True

		else:

			#print('Fallido')
			self.pder= pder
			self.pizq = pizq

			return False
	
	def destino(self):

		return self.p0==self.pf

	def print(self):

		print(self.p0)

class Nodo():
	
	def __init__(self,pai,mapa,pos,estante):
	
		self.pos=pos
		self.f=0
		self.g=0
		self.pai=pai
		self.fillo=None
		self.mapa=mapa

		self.estante = estante
		
	def addNodo(self,mapa,pos,g,estante):
		
		novo_nodo=Nodo(self,mapa,pos,estante)

		distancia=0
		for p in estante:

			if not p.destino():

				distancia += (abs(p.pf[0]-p.p0[0]) + abs(p.p0[0]-novo_nodo.pos[0]) + abs(p.pf[1]-p.p0[1]) + abs(p.p0[1]-novo_nodo.pos[1]) + abs((p.pf[2]-p.p0[2])*(2+int(novo_nodo.pos[3]))) + abs((p.p0[2]-novo_nodo.pos[2])*(2+int(novo_nodo.pos[3]))))

		euclideo = distancia + (abs(pos_init[0]-novo_nodo.pos[0]) + abs(pos_init[1]-novo_nodo.pos[1]) + abs((pos_init[2]-novo_nodo.pos[2])*(2+int(novo_nodo.pos[3]))))

		novo_nodo.g=novo_nodo.pai.g+g
		novo_nodo.f=novo_nodo.g+euclideo

		if abierta == []:

			abierta.append(novo_nodo)

		else:
			
			for i in range(len(abierta)):

				if abierta[i].f>novo_nodo.f:

					abierta.insert(i,novo_nodo)
					break

				if i==len(abierta)-1:

					abierta.append(novo_nodo)

		return novo_nodo

	def comprobar(self,actual):

		for nodo in cerrada:

			final = 0

			for i in range(len(nodo.estante)):

				if nodo.estante[i].p0 == actual.estante[i].p0:

					final +=1

			if nodo.pos==actual.pos and final == len(nodo.estante):

				actual=self.comprobar(abierta.pop(0))
			
		return actual

	def cercania(self,actual,est):

		#print('Actual:',actual.pos)

		for element in est:

			#print('Pos estanterias:',element.p0)

			if actual.pos[:2] == element.p0[:2] and not element.destino():

				return est.index(element)

		return -1

	def run(self):

		exito=False

		while not exito and len(abierta)!=0:

			actual=self.comprobar(abierta.pop(0))

			tmp = copy.deepcopy(actual.estante)

			#if tmp[0].destino():
			#
			#	print('Actual:',actual.pos)
			#	print(tmp[0].p0)
			#	print(tmp[1].p0)

			final = 0

			for element in tmp:

				if element.destino():

					final += 1

			if final == len(tmp) and actual.pos == pos_init:

				exito = True

			else:

				est = self.cercania(actual,tmp)

				self.elevador_subir(actual,copy.deepcopy(tmp),est)
				self.elevador_bajar(actual,copy.deepcopy(tmp),est)
				self.mover(actual,copy.deepcopy(tmp),est)
				self.girar_izquierda(actual,copy.deepcopy(tmp),est)
				self.girar_derecha(actual,copy.deepcopy(tmp),est)

				cerrada.append(actual)

				#input()

		print("Terminamos pibe")

		plan=[]
		while actual.pai!=None:

			plan.append(actual.pos)
			actual=actual.pai
	
		plan=plan[::-1]
  
		print(plan)
  
	def elevador_subir(self,actual,tmp,est):
     
		pos_temp=actual.pos.copy()
		nuevo_mapa=actual.mapa.copy()

		if actual.pos[:2] == tmp[est].p0[:2] and not tmp[est].destino() and not actual.pos[3]:
			
			pos_temp[3]=True
			actual.addNodo(nuevo_mapa,pos_temp,3,tmp)

	def elevador_bajar(self,actual,tmp,est):

		pos_temp=actual.pos.copy()
		nuevo_mapa=actual.mapa.copy()

		if pos_temp[3]:

			pos_temp[3]=False
			actual.addNodo(nuevo_mapa,pos_temp,3,tmp)

	def mover(self,actual,tmp,est):

		pos_temp=actual.pos.copy()
		nuevo_mapa=actual.mapa.copy()
		valor = True

		if pos_temp[2]==0:

			pos_temp[0]-=1

		elif pos_temp[2]==-1:

			pos_temp[1]-=1

		elif pos_temp[2]==1:

			pos_temp[1]+=1

		elif pos_temp[2]==-2:

			pos_temp[0]+=1

		z=1

		if mapa_objetivos[pos_temp[0]][pos_temp[1]]!=0:

			if actual.pos[3] and est!=-1:

				z+=1

				valor = tmp[est].actualizar_pos([pos_temp[0],pos_temp[1],tmp[est].p0[2]])
			
			if valor:

				actual.addNodo(nuevo_mapa,pos_temp,z,tmp)

	def girar_izquierda(self,actual,tmp,est):

		pos_temp=actual.pos.copy()
		valor = True

		if pos_temp[2]==0:

			pos_temp[2]=-1

		elif pos_temp[2]==-1:

			pos_temp[2]=-2

		elif pos_temp[2]==-2:

			pos_temp[2]=1

		elif pos_temp[2]==1:

			pos_temp[2]=0

		z=2

		if pos_temp[3] and est!=-1:

			giro = tmp[est].p0[2]
			giro-=1
			if giro<-2:
				giro=1

			z+=1

			valor = tmp[est].actualizar_pos([tmp[est].p0[0],tmp[est].p0[1],giro])

		if valor:

			actual.addNodo(mapa_objetivos,pos_temp,z,tmp)

	def girar_derecha(self,actual,tmp,est):

		pos_temp=actual.pos.copy()
		valor = True

		if pos_temp[2]==0:

			pos_temp[2]=1

		elif pos_temp[2]==1:

			pos_temp[2]=-2

		elif pos_temp[2]==-2:

			pos_temp[2]=-1

		elif pos_temp[2]==-1:

			pos_temp[2]=0

		z=2

		if pos_temp[3] and est!=-1:

			giro = tmp[est].p0[2]
			giro+=1
			if giro>1:
				giro=-2

			z+=1

			valor = tmp[est].actualizar_pos([tmp[est].p0[0],tmp[est].p0[1],giro])

		if valor:

			actual.addNodo(mapa_objetivos,pos_temp,z,tmp)

start = time.time()

pos_init = [1,2,0,False]

estanterias = [Estanteria([2,3,0],[4,3,0]),Estanteria([2,1,0],[4,1,0])] #[Estanteria([8,3,0],[3,7,0]),Estanteria([9,13,0],[3,9,0])] #[Estanteria([2,3,0],[4,3,0]),Estanteria([2,1,0],[4,1,0])]

root=Nodo(None,mapa_objetivos,pos_init,estanterias)

cerrada=[]
abierta=[root]

root.run()

print(time.time() - start)