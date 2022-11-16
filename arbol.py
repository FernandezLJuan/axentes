global cerrada
global abierta
from math import sin,cos,pi

#clase estantería, con atributos de posiciones iniciales y finales

mapa_objetivos=[[0,0,0,0,0,0,0,0],
				[0,0,1,1,1,1,0,0],
				[0,0,1,1,1,1,0,0],
				[0,0,0,0,1,1,0,0],
				[0,1,1,1,1,1,1,0],
				[0,1,1,1,1,1,1,0],
				[0,1,1,1,0,0,0,0],
				[0,0,0,1,1,1,0,0],
				[0,0,0,1,1,1,0,0],
				[0,0,0,0,0,0,0,0]]
'''
mapa_objetivos=[[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
				[0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0],
				[0,0,0,0,0,0,1,1,3,1,1,0,0,0,0,0,0],
				[0,0,0,0,0,0,1,3,1,3,1,0,0,0,0,0,0],
				[0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0],
				[0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
				[0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
				[0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
				[0,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,0],
				[0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
				[0,1,1,2,1,1,1,1,1,1,1,1,1,2,1,1,0],
				[0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0],
				[0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0],
				[0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0],
				[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],]'''
class Estanteria():

	def __init__(self,p0,pf):

		self.p0=p0
		self.pf=pf

	def actualizar_pos(self,pNuevo):
		
		self.p0=pNuevo
	
	def destino(self):

		return self.p0==self.pf

class Nodo():
	
	def __init__(self,pai,mapa,pos):
	
		self.pos=pos
		self.f=0
		self.g=0
		self.pai=pai
		self.fillo=None
		self.mapa=mapa
		
	def addNodo(self,mapa,pos,g):
		
		novo_nodo=Nodo(self,mapa,pos)

		distancia=[]
		for p in estanterias:
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

			if estanterias[0].destino():
				
				exito=True

			else:

				self.elevador_subir(actual)
				self.mover(actual)
				self.girar_izquierda(actual)
				self.girar_derecha(actual)

				cerrada.append(actual)

		print("Terminamos pibe")
		plan=[]

		while actual.pai!=None:
      
			plan.append(actual.pos)
			actual=actual.pai
   
		plan=plan[::-1]
  
		print(plan)
  
	def elevador_subir(self,actual):
     
		pos_temp=actual.pos.copy()
		nuevo_mapa=actual.mapa.copy()

		if pos_temp[0]==estanterias[0].p0[0] and pos_temp[1]==estanterias[0].p0[1] and not estanterias[0].destino():
			pos_temp[3]=True

			actual.addNodo(nuevo_mapa,pos_temp,1)

	def elevador_bajar(self,actual):

		pos_temp=actual.pos.copy()
		nuevo_mapa=actual.mapa.copy()

		if pos_temp[3]:

			pos_temp[3]=False
			actual.addNodo(nuevo_mapa,pos_temp,1)

	def mover(self,actual):

		pos_temp=actual.pos.copy()
		nuevo_mapa=actual.mapa.copy()
		cabe=True

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

				estanterias[0].actualizar_pos([pos_temp[0],pos_temp[1],0])
    
			actual.addNodo(nuevo_mapa,pos_temp,1)

	def girar_izquierda(self,actual):

		pos_temp=actual.pos.copy()

		if pos_temp[2]==0:

			pos_temp[2]=-1

		elif pos_temp[2]==-1:

			pos_temp[2]=-2

		elif pos_temp[2]==-2:

			pos_temp[2]=1

		elif pos_temp[2]==1:

			pos_temp[2]=0

		actual.addNodo(mapa_objetivos,pos_temp,3)

	def girar_derecha(self,actual):

		pos_temp=actual.pos.copy()

		if pos_temp[2]==0:

			pos_temp[2]=1

		elif pos_temp[2]==1:

			pos_temp[2]=-2

		elif pos_temp[2]==-2:

			pos_temp[2]=-1

		elif pos_temp[2]==-1:

			pos_temp[2]=0

		actual.addNodo(mapa_objetivos,pos_temp,3)

root=Nodo(None,mapa_objetivos,[8,4,0,False])

cerrada=[]
abierta=[root]

estanterias=[Estanteria([5,2,0],[1,4,0])]

root.run()

