global cerrada
global abierta
'''
mapa_objetivos=[[0,0,0,0,0,0,0,0],
				[0,0,1,1,3,1,0,0],
				[0,0,1,1,1,1,0,0],
				[0,0,0,0,1,1,0,0],
				[0,1,1,1,1,1,1,0],
				[0,1,2,1,1,1,1,0],
				[0,1,1,1,0,0,0,0],
				[0,0,0,1,1,1,0,0],
				[0,0,0,1,1,1,0,0],
				[0,0,0,0,0,0,0,0]]'''

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
				[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

pos_entrega=[]

for i in range(0,len(mapa_objetivos)):
	for j in range(0,len(mapa_objetivos[0])):
		if mapa_objetivos[i][j]==3:

			pos_entrega.append([i,j])

class Nodo(object):
	
	def __init__(self,pai,mapa,pos):
	
		self.pos=pos
		self.f=0
		self.g=0
		self.pai=pai
		self.fillo=None
		self.mapa=mapa
		
	def addNodo(self,mapa,pos,g):
		
		novo_nodo=Nodo(self,mapa,pos)

		if mapa_objetivos[novo_nodo.pos[0]][novo_nodo.pos[1]]==2:

			novo_nodo.pos[3]=True
			novo_nodo.mapa[novo_nodo.pos[0]][novo_nodo.pos[1]]=1
		
  
		if mapa_objetivos[novo_nodo.pos[0]][novo_nodo.pos[1]]==4:

			novo_nodo.pos[3]=False

		distancia=[]
		for p in pos_entrega:
			distancia.append(abs((p[0]-novo_nodo.pos[0]))+abs((p[1]-novo_nodo.pos[1])))

		novo_nodo.g=novo_nodo.pai.g+g
		novo_nodo.f=novo_nodo.g+min(distancia)

		if abierta == []:

			abierta.append(novo_nodo)

		else:

			#ordenamiento por heurística
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
   
			if actual.pos==[pos_entrega[0][0],pos_entrega[0][1],0,True]: #or actual.pos==[pos_entrega[1][0],pos_entrega[1][1],0,True] or actual.pos==[pos_entrega[2][0],pos_entrega[2][1],0,True]:
				actual.mapa[actual.pos[0]][actual.pos[1]]=4
    
			if actual.mapa[pos_entrega[0][0]][pos_entrega[0][1]]==4: #and actual.mapa[pos_entrega[1][0]][pos_entrega[1][1]]==4 and actual.mapa[3][9]==4:
				for a in mapa_objetivos:
					print(a)
				exito=True



			else:

				self.mover(actual)
				self.girar_izquierda(actual)
				self.girar_derecha(actual)
				cerrada.append(actual)
				
			#print(actual.pos)
			#input('')

		
		print("Terminamos pibe")
		print(exito)
		plan=[]
		while actual.pai!=None:

			plan.append(actual.pos)
			actual=actual.pai

		plan=plan[::-1]
		print(plan)


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

		if actual.pos[3]:
		#	if pos_temp[2]==1 or pos_temp==-1:
		#		if mapa_objetivos[pos_temp[0]+1][pos_temp[1]]==0 and mapa_objetivos[pos_temp[0]-1][pos_temp[1]]==0:
		#
		#			cabe=False
     
		#	if pos_temp[2]==0 or pos_temp==-2:
		#		if mapa_objetivos[pos_temp[0]][pos_temp[1]-1]==0 and mapa_objetivos[pos_temp[0]][pos_temp[1]+1]==0:
		#
		#			cabe=False
  
			pass

		if mapa_objetivos[pos_temp[0]][pos_temp[1]]!=0 and cabe:
      
			if actual.pos[3]:

				nuevo_mapa[pos_temp[0]][pos_temp[1]]=2
				nuevo_mapa[actual.pos[0]][actual.pos[1]]=2

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

		#print("Posicion actual: {}".format(pos_temp))

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

		#print("Posicion actual: {}".format(pos_temp))

		actual.addNodo(mapa_objetivos,pos_temp,3)

root=Nodo(None,mapa_objetivos,[8,4,0,False])

cerrada=[]
abierta=[root]

root.run()

