from random import randint
import copy

# Auxiliary Function for rotating the DNA in each cycle.
def rotate(l,n):
    return l[n:] + l[:n]

# History is the object responsible for accounting all the organisms.
class History:
    def __init__(self):
        self.orgs = []
    def addOrganism(self, org):
        self.orgs.append(org)
    def getGenepool(self):
        genepool = []
        genepooldetail = []
        for organism in self.orgs:
            if not organism.dna in genepool:
                genepool.append(organism.dna)
                genepooldetail.append([[organism.name], organism.dna, 1])
            else:
                for unit in genepooldetail:
                    if unit[1] == organism.dna:
                        unit[0].append(organism.name)
                        unit[2] += 1
        return genepooldetail

# Organism is the structure for the living organisms.
class Organism:
    def __init__(self, name, dna, energy):
        self.memory = 0
        self.name = name
        self.dna = dna
        self.energy = energy
        self.size = len(dna)
        self.age = 0
        self.sons = 0
        self.parent = ""
    def __repr__(self):
        return self.name + " E:" + str(self.energy) + "Y:" +  str(self.age) 
    def toAge(self):
        self.age += 1
    def reportStatus(self):
        print("Name: ", self.name)
        print("DNA: ", self.dna)
        print("Energy: ", self.energy)
        print("Size: ", self.size)
        print("Age: ", self.age)
    def divide(self):
        self.sons += 1
        son = copy.deepcopy(self)
        son.sons = 0
        son.parent = self.name
        son.name = son.name +  "-" + str(self.sons)
        son.age = 0
        son.energy = 5
        self.energy += -5
        for x in range(randint(0,10)):
            if randint(1,100) > 95:
                print("MUTACION!")
                if randint(0,1) == 0:
                    # ADD GEN
                    son.dna.insert(randint(0,len(son.dna)-1), randint(0,12))
                else:
                    # REMOVE GEN
                    son.dna.pop(randint(0, len(son.dna)-1))
        print(son.dna)
        return son
    def decreaseEnergy(self):
        print("Bajando de ", self.energy)
        self.energy = self.energy - 1
    def increaseEnergy(self, energy):
        self.energy = energy + energy

# QuantumPackages are the "food" of this simulation. The name comes from the concept used in operative systems.
class QuantumPackage:
    def __init__(self, quantums):
        self.quantums = quantums
    def __repr__(self):
        return 'QP'

# Enviroment is the class responsible for holding all the living organisms. 
class Enviroment: 
    def __init__(self, size):
        self.size = size
        self.landscape = [[0 for x in range(size)] for x in range(size)]
    def reportStatus(self):
        print("LANDSCAPE:")
        for row in self.landscape:
            print(row)
    def getOrganismsCoor(self):
        organisms = []
        fila = 0
        columna = 0
        for row in self.landscape:
            columna = 0
            for element in row:
                if isinstance(element,Organism):
                   organisms.append((fila, columna))
                columna += 1
            fila += 1
        print("FOUND ", len(organisms))
        return organisms
    def getOrganisms(self):
        orgs = []
        for row in self.landscape:
            for element in row:
                if isinstance(element,Organism):
                    orgs.append(element)
        return orgs
    def countOrgs(self):
                cont = 0
                for row in self.landscape:
                        for element in row:
                                if isinstance(element, Organism):
                                        cont += 1
                return cont
    
# Time is the class responsible for aging the living organisms.
class Time:
    def aging(self, enviroment):
        for row in enviroment.landscape:
            for element in row:
                if isinstance(element, Organism):
                    element.toAge()

# Death is the class responsible for killing old or starving organisms.
class Death:
    def __init__(self):
        self.killed = []
    def kill(self, enviroment):
        fila=0
        for row in enviroment.landscape:
            columna = 0
            for element in row:
                if isinstance(element, Organism):
                    if element.energy <= 0 or element.age > 20:
                        self.killed.append(element)
                        print("Killing ", fila, columna)
                        enviroment.landscape[fila][columna] = 0
                columna +=1
            fila +=1

# Interpreter is the class that gives life to the organism. It executes the code in their DNA.
class Interpreter:
    def interprete(self, enviroment):
        def up():
            enviroment.landscape[x][y].decreaseEnergy()
            print("Move Up" , x, y)
            if x > 0:
                if enviroment.landscape[x-1][y] == 0:
                    enviroment.landscape[x-1][y] = enviroment.landscape[x][y]
                    enviroment.landscape[x][y] = 0
                elif isinstance(enviroment.landscape[x-1][y],QuantumPackage):
                    enviroment.landscape[x][y].increaseEnergy(enviroment.landscape[x-1][y].quantums)
                    enviroment.landscape[x-1][y] = enviroment.landscape[x][y]
                    enviroment.landscape[x][y] = 0
        def down():
            enviroment.landscape[x][y].decreaseEnergy()
            print("Move Down", x, y)
            if x < enviroment.size-1:
                if enviroment.landscape[x+1][y] == 0:
                    enviroment.landscape[x+1][y] = enviroment.landscape[x][y]
                    enviroment.landscape[x][y] = 0
                elif isinstance(enviroment.landscape[x+1][y],QuantumPackage):
                    enviroment.landscape[x][y].increaseEnergy(enviroment.landscape[x+1][y].quantums)
                    enviroment.landscape[x+1][y] = enviroment.landscape[x][y]
                    enviroment.landscape[x][y] = 0
        def right():
            enviroment.landscape[x][y].decreaseEnergy()
            print("Move Right", x, y)
            if y < enviroment.size-1:
                if enviroment.landscape[x][y+1] == 0:
                    enviroment.landscape[x][y+1] = enviroment.landscape[x][y]
                    enviroment.landscape[x][y] = 0
                elif isinstance(enviroment.landscape[x][y+1],QuantumPackage):
                    enviroment.landscape[x][y].increaseEnergy(enviroment.landscape[x][y+1].quantums)
                    enviroment.landscape[x][y+1] = enviroment.landscape[x][y]
                    enviroment.landscape[x][y] = 0
        def left():
            enviroment.landscape[x][y].decreaseEnergy()
            print("Move Left", x, y)
            if y > 0:
                if enviroment.landscape[x][y-1] == 0:
                    enviroment.landscape[x][y-1] = enviroment.landscape[x][y]
                    enviroment.landscape[x][y] = 0
                elif isinstance(enviroment.landscape[x][y-1],QuantumPackage):
                    enviroment.landscape[x][y].increaseEnergy(enviroment.landscape[x][y-1].quantums)
                    enviroment.landscape[x][y-1] = enviroment.landscape[x][y]
                    enviroment.landscape[x][y] = 0

        def divide():
            if enviroment.landscape[x][y].energy > 7:
                enviroment.landscape[x][y].decreaseEnergy()
                sonX = randint(-1,1)
                sonY = randint(-1,1)
                if sonX != 0 or sonY != 0:
                    if x + sonX > 0 and x + sonX < enviroment.size-1:
                        if y + sonY > 0 and y + sonY < enviroment.size-1:
                            if enviroment.landscape[x + sonX][y + sonY] == 0:
                                enviroment.landscape[x + sonX][y + sonY] = enviroment.landscape[x][y].divide()
            else:
               enviroment.landscape[x][y].decreaseEnergy() 

        def writeOne():
            print("WRITE 1")
            enviroment.landscape[x][y].memory = 1
        def writeCero():
            print("WRITE 0")
            enviroment.landscape[x][y].memory = 0
        def ifTrue():
            print("CHECKING iF TRUE")
            if enviroment.landscape[x][y].memory != 1:
                enviroment.landscape[x][y].dna = rotate(enviroment.landscape[x][y].dna, 1)
        def checkUp():
            print("CHECKING UP")
            if x > 0:
                if enviroment.landscape[x-1][y] != 0:
                    enviroment.landscape[x][y].memory = 1
                else:
                    enviroment.landscape[x][y].memory = 0
            else:
                enviroment.landscape[x][y].memory = 0
        def checkDown():
            print("CHECKING DOWN")
            if x < enviroment.size-1:
                if enviroment.landscape[x+1][y] != 0:
                    enviroment.landscape[x][y].memory = 1
                else:
                    enviroment.landscape[x][y].memory = 0
            else:
                enviroment.landscape[x][y].memory = 0
        def checkRight():
            print("CHECKING RIGHT")
            if y < enviroment.size-1:
                if enviroment.landscape[x][y+1] != 0:
                    enviroment.landscape[x][y].memory = 1
                else:
                    enviroment.landscape[x][y].memory = 0
            else:
                enviroment.landscape[x][y].memory = 0
        def checkLeft():
            print("CHECKING LEFT")
            if y > 0:
                if enviroment.landscape[x][y-1] != 0:
                    enviroment.landscape[x][y].memory = 1
                else:
                    enviroment.landscape[x][y].memory = 0
            else:
                enviroment.landscape[x][y].memory = 0
        def checkEnergyDivide():
            if enviroment.landscape[x][y].energy > 7:
                enviroment.landscape[x][y].memory = 1
            else:
                enviroment.landscape[x][y].memory = 0

            
                
            
        options = {0 : up,
           1 : down,
           2 : right,
           3 : left,
           4 : divide,
           5 : writeOne,
           6 : writeCero,
           7 : ifTrue,
           8 : checkUp,
           9 : checkDown,
           10 : checkRight,
           11 : checkLeft,
           12: checkEnergyDivide
                   
        }

        for organismCoordinates in enviroment.getOrganismsCoor():
            x = organismCoordinates[0]
            y = organismCoordinates[1]
            gen = enviroment.landscape[x][y].dna[0]
            enviroment.landscape[x][y].dna = rotate(enviroment.landscape[x][y].dna, 1)
            print("ejecutando en ", x, y, "gen ", gen)
            
            options[gen]()
            



if __name__ == '__main__':
	book = History()
	earth = Enviroment(10)
	earth.reportStatus()

	earth.landscape[0][0] = QuantumPackage(10)
	earth.landscape[1][1] = Organism("Eva", [8,7,0,9,7,1,10,7,2,11,7,3,12,7,4], 15)
	#Poblemos Tierra
	for i in range(0,4):
	    x = randint(0, earth.size-1)
	    y = randint(0, earth.size-1)
	    if earth.landscape[x][y] == 0:
	        dna = []
	        for a in range(1,11):
	            dna.append(randint(0,12))
	        earth.landscape[x][y] = Organism("Eva"+str(i), dna, 15)
	earth.reportStatus()

	chronos = Time()
	parca = Death()

	god = Interpreter()

	for i in range(0,200):
	        if earth.countOrgs() > 0:
	                print("ciclo: ", i)
	                god.interprete((earth))
	                chronos.aging(earth)
	                parca.kill(earth)
	                earth.reportStatus()
	                for i in range(1,4):
	                        x = randint(0,9)
	                        y = randint(0,9)
	                        if earth.landscape[x][y] == 0:
	                                earth.landscape[x][y] = QuantumPackage(randint(5,10))
	                for org in earth.getOrganisms():
	                        if not org in book.orgs:
	                                book.addOrganism(org)
	        else:
	                print("SE MURIERON TODOS EN EL CICLO: ", i)
	                break


	print("Living:", len(earth.getOrganisms()))
	print("GENEPOOL:", book.getGenepool())


