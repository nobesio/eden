from random import randint
import copy

def rotate(l,n):
    return l[n:] + l[:n]
class history:
    def __init__(self):
        self.orgs = []
    def addOrg(self, org):
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

class organism:
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
        print("NAME: ", self.name)
        print("DNA: ", self.dna)
        print("ENERGY: ", self.energy)
        print("SIZE: ", self.size)
        print("AGE: ", self.age)
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

class quantumPackage:
    def __init__(self, quantums):
        self.quantums = quantums
    def __repr__(self):
        return 'QP'

class enviroment: 
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
                if isinstance(element,organism):
                   organisms.append((fila, columna))
                columna += 1
            fila += 1
        print("FOUND ", len(organisms))
        return organisms
    def getOrganisms(self):
        orgs = []
        for row in self.landscape:
            for element in row:
                if isinstance(element,organism):
                    orgs.append(element)
        return orgs
    def countOrgs(self):
                cont = 0
                for row in self.landscape:
                        for element in row:
                                if isinstance(element, organism):
                                        cont += 1
                return cont
    
            
        
        
class time:
    def aging(self, enviroment):
        for row in enviroment.landscape:
            for element in row:
                if isinstance(element, organism):
                    element.toAge()
class death:
    def __init__(self):
        self.killed = []
    def kill(self, enviroment):
        fila=0
        for row in enviroment.landscape:
            columna = 0
            for element in row:
                if isinstance(element, organism):
                    if element.energy <= 0 or element.age > 20:
                        self.killed.append(element)
                        print("Killing ", fila, columna)
                        enviroment.landscape[fila][columna] = 0
                columna +=1
            fila +=1
class interpreter:
    def interprete(self, enviroment):
        def up():
            enviroment.landscape[x][y].decreaseEnergy()
            print("Move Up" , x, y)
            if x > 0:
                if enviroment.landscape[x-1][y] == 0:
                    enviroment.landscape[x-1][y] = enviroment.landscape[x][y]
                    enviroment.landscape[x][y] = 0
                elif isinstance(enviroment.landscape[x-1][y],quantumPackage):
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
                elif isinstance(enviroment.landscape[x+1][y],quantumPackage):
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
                elif isinstance(enviroment.landscape[x][y+1],quantumPackage):
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
                elif isinstance(enviroment.landscape[x][y-1],quantumPackage):
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
            

book = history()
earth = enviroment(30)
earth.reportStatus()

earth.landscape[0][0] = quantumPackage(10)
#Poblemos Tierra
for i in range(0,15):
    x = randint(0, earth.size-1)
    y = randint(0, earth.size-1)
    if earth.landscape[x][y] == 0:
        dna = []
        for a in range(1,11):
            dna.append(randint(0,12))
        earth.landscape[x][y] = organism("Eva"+str(i), dna, 15)
earth.reportStatus()

chronos = time()
parca = death()

god = interpreter()

for i in range(0,200):
        if earth.countOrgs() > 0:
                print("ciclo: ", i)
                god.interprete((earth))
                chronos.aging(earth)
                parca.kill(earth)
                earth.reportStatus()
                for i in range(1,4):
                        x = randint(0,29)
                        y = randint(0,29)
                        if earth.landscape[x][y] == 0:
                                earth.landscape[x][y] = quantumPackage(randint(5,10))
                for org in earth.getOrganisms():
                        if not org in book.orgs:
                                book.addOrg(org)
        else:
                print("SE MURIERON TODOS EN EL CICLO: ", i)
                break


print("Living:", len(earth.getOrganisms()))
print("GENEPOOL:", book.getGenepool())


