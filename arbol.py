global cerrada
global abierta
from math import sin,cos,pi

#clase estantería, con atributos de posiciones iniciales y finales

'''mapa_objetivos=[[0,0,0,0,0,0,0,0,0],
				[0,0,1,1,1,1,0,0,0],
				[0,0,1,1,1,1,0,0,0],
				[0,0,0,0,1,1,0,0,0],
				[0,1,1,1,1,1,1,0,0],
				[0,1,1,1,1,1,1,0,0],
				[0,1,1,1,0,0,0,0,0],
				[0,0,0,1,1,1,0,0,0],
				[0,0,0,1,1,1,0,0,0],
				[0,0,0,0,0,0,0,0,0]]'''

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
				[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
				
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

		else:

			#print('Fallido')
			self.pder= pder
			self.pizq = pizq
	
	def destino(self):

		return self.p0==self.pf

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

		distancia=[]
		for p in estante:
			distancia.append(abs((p.pf[0]-novo_nodo.pos[0]))+abs((p.pf[1]-novo_nodo.pos[1])))

		novo_nodo.g=novo_nodo.pai.g+g
		novo_nodo.f=novo_nodo.g+min(distancia)

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

			if nodo.pos==actual.pos:

				actual=self.comprobar(abierta.pop(0))
			
		return actual

	def run(self):

		exito=False

		while not exito and len(abierta)!=0:

			actual=self.comprobar(abierta.pop(0))

			tmp = [Estanteria(actual.estante[0].p0,actual.estante[0].pf)]


			#al tener varias estanterías trabajamos con una lista de las mismas, cada vez que una de ellas llega al destino la eliminamos de la lista para trabajar con la siguiente
			if len(estanterias)==0:
				exito=True

			if tmp[0].destino():

				estanterias.pop(0)

			else:

				self.elevador_subir(actual,[Estanteria(actual.estante[0].p0,actual.estante[0].pf)])
				self.elevador_bajar(actual,[Estanteria(actual.estante[0].p0,actual.estante[0].pf)])
				self.mover(actual,[Estanteria(actual.estante[0].p0,actual.estante[0].pf)])
				self.girar_izquierda(actual,[Estanteria(actual.estante[0].p0,actual.estante[0].pf)])
				self.girar_derecha(actual,[Estanteria(actual.estante[0].p0,actual.estante[0].pf)])

				cerrada.append(actual)

		print("Terminamos pibe")

		plan=[]
		while actual.pai!=None:

			plan.append(actual.pos)
			actual=actual.pai
	
		plan=plan[::-1]
  
		print(plan)
  
	def elevador_subir(self,actual,tmp):
     
		pos_temp=actual.pos.copy()
		nuevo_mapa=actual.mapa.copy()

		if pos_temp[0]==tmp[0].p0[0] and pos_temp[1]==tmp[0].p0[1] and not tmp[0].destino() and not actual.pos[3]:
			pos_temp[3]=True

			actual.addNodo(nuevo_mapa,pos_temp,1,tmp)

	def elevador_bajar(self,actual,tmp):

		pos_temp=actual.pos.copy()
		nuevo_mapa=actual.mapa.copy()

		if pos_temp[3]:

			pos_temp[3]=False
			actual.addNodo(nuevo_mapa,pos_temp,1,tmp)

	def mover(self,actual,tmp):

		pos_temp=actual.pos.copy()
		nuevo_mapa=actual.mapa.copy()

		if pos_temp[2]==0:

			pos_temp[0]-=1

		elif pos_temp[2]==-1:

			pos_temp[1]-=1

		elif pos_temp[2]==1:

			pos_temp[1]+=1

		elif pos_temp[2]==-2:

			pos_temp[0]+=1

		if mapa_objetivos[pos_temp[0]][pos_temp[1]]!=0:

			if actual.pos[3]:

				tmp[0].actualizar_pos([pos_temp[0],pos_temp[1],tmp[0].p0[2]])
			
			actual.addNodo(nuevo_mapa,pos_temp,1,tmp)

	def girar_izquierda(self,actual,tmp):

		pos_temp=actual.pos.copy()

		if pos_temp[2]==0:

			pos_temp[2]=-1

		elif pos_temp[2]==-1:

			pos_temp[2]=-2

		elif pos_temp[2]==-2:

			pos_temp[2]=1

		elif pos_temp[2]==1:

			pos_temp[2]=0

		if pos_temp[3]:

			giro = tmp[0].p0[2]
			giro-=1
			if giro<-2:
				giro=1

			tmp[0].actualizar_pos([pos_temp[0],pos_temp[1],giro])

		actual.addNodo(mapa_objetivos,pos_temp,3,tmp)

	def girar_derecha(self,actual,tmp):

		pos_temp=actual.pos.copy()

		if pos_temp[2]==0:

			pos_temp[2]=1

		elif pos_temp[2]==1:

			pos_temp[2]=-2

		elif pos_temp[2]==-2:

			pos_temp[2]=-1

		elif pos_temp[2]==-1:

			pos_temp[2]=0

		if pos_temp[3]:

			giro = tmp[0].p0[2]
			giro+=1
			if giro>1:
				giro=-2

			tmp[0].actualizar_pos([pos_temp[0],pos_temp[1],giro])

		actual.addNodo(mapa_objetivos,pos_temp,3,tmp)

estanterias=[Estanteria([8,3,0],[2,8,0]),Estanteria([9,3,0],[3,7,0]),Estanteria([10,13,0],[3,9,0])]
root=Nodo(None,mapa_objetivos,[12,8,0,False],estanterias)

cerrada=[]
abierta=[root]

root.run()
