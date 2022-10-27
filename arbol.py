global cerrada
global abierta

mapa_objetivos=[[0,0,0,0,0,0,0,0],
				[0,0,1,1,1,3,0,0],
				[0,0,1,1,1,1,0,0],
				[0,0,0,0,1,1,0,0],
				[0,1,1,1,1,1,1,0],
				[0,1,2,1,1,1,1,0],
				[0,1,1,1,0,0,0,0],
				[0,0,0,1,1,1,0,0],
				[0,0,0,1,1,1,0,0],
				[0,0,0,0,0,0,0,0]]


class Nodo(object):
	
	def __init__(self,pai,mapa,pos):
	
		self.pos=pos
		self.h=0
		self.pai=pai
		self.fillo=None
		self.mapa=mapa
		
	def addNodo(self,mapa,pos):
		
		novo_nodo=Nodo(self,mapa,pos)

		if mapa_objetivos[novo_nodo.pos[0]][novo_nodo.pos[1]]==2:

			novo_nodo.pos[3]=True

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
			#print("Actual {}".format(actual.pos))

			if actual.pos==[1,5,0,True]:
				exito=True

			else:

				self.mover(actual)
				self.girar_izquierda(actual)
				self.girar_derecha(actual)
				cerrada.append(actual)
		
		print("Terminamos pibe")


	def mover(self,actual):

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

				print("Posicion actual: {}".format(actual.pos))
				nuevo_mapa[pos_temp[0]][pos_temp[1]]=2
				nuevo_mapa[actual.pos[0]][actual.pos[1]]=2

			actual.addNodo(nuevo_mapa,pos_temp)

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

		actual.addNodo(mapa_objetivos,pos_temp)

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
		#print(pos_temp)

		actual.addNodo(mapa_objetivos,pos_temp)
#		input("ñakjsdñ")

root=Nodo(None,mapa_objetivos,[8,4,0,False])

cerrada=[]
abierta=[root]

root.run()

