from random import *
from math import *

class kromosom:
	def __init__(self, nilai,down,up):
		self.nilai = nilai
		self.down = down
		self.up = up
		self.fitness = 0
		self.function = 0
		self.setfunction()
		self.setfitness()

	def decoding(self):
		x = self.down+(self.up-self.down)*(int(''.join(map(str,self.nilai[:5])))*10**-5)
		y = self.down+(self.up-self.down)*(int(''.join(map(str,self.nilai[5:])))*10**-5)
		return [x,y]

	def setfunction(self):
		x = self.decoding()[0]
		y = self.decoding()[1]
		self.function = -1*(abs(sin(x)*cos(y)*exp(abs(1-((sqrt(x**2+y**2))/pi)))))

	def setfitness(self):
		self.fitness = self.function*-1
		
class GA:
	def __init__(self, populasi,jmlkromosom,generasi):
		self.populasi = populasi
		self.jmlkromosom = jmlkromosom
		self.generasi = generasi
		self.individu = []
		self.parent = []
		self.initial()
		self.mutationrate = 0.4
		self.newindividu = []

	def initial(self):
		for i in range(self.populasi):
			a = [randint(0,9) for j in range(self.jmlkromosom)]
			self.individu.append(kromosom(a,-10,10))

	def parentselection(self):
		self.parent=[]
		jml = 0
		for i in range(self.populasi):
			jml += self.individu[i].fitness

		for x in range(self.populasi/2):
			parent = []
			for j in range(2):
				roll = uniform(0,jml)
				pos = 0
				for i in range(self.populasi):
					pos += self.individu[i].fitness
					if(roll<=pos):
						parent.append(self.individu[i])
						break
			self.parent.append(parent)

	def recombination(self):
		awal = randint(0,self.jmlkromosom-2)
		akhir = randint(0,self.jmlkromosom-2)
		if(awal>akhir):
			awal,akhir = akhir,awal
		for i in self.parent:
			self.newindividu.append(kromosom(i[0].nilai[:awal]+i[1].nilai[awal:akhir]+i[0].nilai[akhir:],-10,10))
			self.newindividu.append(kromosom(i[1].nilai[:awal]+i[0].nilai[awal:akhir]+i[1].nilai[akhir:],-10,10))

	def mutation(self):
		for i in range(len(self.newindividu)):
			gen = []
			for j in self.newindividu[i].nilai:
				bit = j
				rate = random()
				if rate<=self.mutationrate:
					bit = randint(0,9)
				gen.append(bit)
			self.newindividu[i] = kromosom(gen,-10,10)

	def survivorselection(self):
		self.individu = self.individu + self.newindividu
		self.individu = sorted(self.individu, key = lambda x:x.fitness,reverse=True)
		newindividu = []
		for i in range(self.populasi):
			newindividu.append(self.individu[i])
		self.individu = newindividu[:]
		self.newindividu = []

	def run(self):
		i = 0
		while(round(self.individu[0].fitness,4)!=19.2085):
			print "generasi ke-",i
			i+=1
			self.parentselection()
			self.recombination()
			self.mutation()
			self.survivorselection()
			print self.individu[0].decoding(),":",round(self.individu[0].fitness,4)

class __main__:
	holdertable = GA(20,10,5000)
	holdertable.run()