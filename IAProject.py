# Elias Rodriguez Chimal - Computer engineering programmer.

from random import randint, uniform,random
import numpy as np

matrizAdy = [[0,1,1,0,0,0,0,0,0,0],
             [1,0,0,1,0,0,0,1,1,0],
             [1,0,0,1,0,0,1,0,0,1],
             [0,1,1,0,1,1,0,0,0,0],
             [0,0,0,1,0,0,0,0,0,0],
             [0,0,0,1,0,0,0,0,0,0],
             [0,0,1,0,0,0,0,0,0,1],
             [0,1,0,0,0,0,0,0,1,0],
             [0,1,0,0,0,0,0,1,0,0],
             [0,0,1,0,0,0,1,0,0,0]]

vectorRV = []
vectorCV = []

probabilidadMutacion = 30
probabilidadCruce = 99
umbralAptitud = 0
solucionCorrecta = False
cromosomaSolucion = []

# chromosome[((NodeA, NodeB),(colorA, colorB))]
listaCromosomas = []
listaAptitud = []
listaPrometedores = []
coloresNodos = []
listaCromosomasNueva = []
n = 12
m = 10
muestraPob = 80
nodo1Existe = False
nodo2Existe = False

for i in range(muestraPob):
    j=i
    vectorCV.append([i,j])

# I populated the generation using random, but respecting connections.
# I made tests using 40 chromosomes for the population, but the amount of times that generate a
# solution was less than the initial set, a population of 80 or more chromosomes works better.

for h in range(muestraPob):
    coloresNodos = []
    cromosoma = []
    for i in range(m):
        j=i
        while j<10:
            if matrizAdy[i][j] == 1:
                nodo1Existe=False
                nodo2Existe=False
                colorA = randint(1,3)
                colorB = randint(1,3)
                cromosoma.append([[i,j],[colorA,colorB]])
                for k in range(len(coloresNodos)):
                    if coloresNodos[k][0] == i:
                        nodo1Existe = True
                    if coloresNodos[k][0] == j:
                        nodo2Existe = True
                if nodo1Existe == False:
                    coloresNodos.append([i,colorA])
                if nodo2Existe == False:
                    coloresNodos.append([j,colorB])
            j=j+1
    vectorRV.append(coloresNodos)
    listaCromosomas.append(cromosoma)    

# Regulation of SV (vector) elements (in this case, called "listaCromosomas")
# based on the RV vector elements, taking into consideration the connections within CV vector.

for i in range(len(vectorCV)):
    for h in range(m):
        for j in range(n):
            if listaCromosomas[vectorCV[i][0]][j][0][0] == vectorRV[vectorCV[i][1]][h][0]:
                listaCromosomas[vectorCV[i][0]][j][1][0] = vectorRV[vectorCV[i][1]][h][1]
            if listaCromosomas[vectorCV[i][0]][j][0][1] == vectorRV[vectorCV[i][1]][h][0]:
                listaCromosomas[vectorCV[i][0]][j][1][1] = vectorRV[vectorCV[i][1]][h][1]

# Fitness function applied to every chromosome. 
    
def fitnessFunc(posCromosoma):
    aptitudTotal = 0
    color1 = 0
    color2 = 0
    color3 = 0
    for h in range(m):
        
        for i in range(n):
            color1=0
            color2=0
            color3=0
            if listaCromosomas[posCromosoma][i][0][0] == h:
                if listaCromosomas[posCromosoma][i][1][0] == 1:
                    color1 = color1+1
                if listaCromosomas[posCromosoma][i][1][0] == 2:
                    color2 = color2+1
                if listaCromosomas[posCromosoma][i][1][0] == 3:
                    color3 = color3+1
            if listaCromosomas[posCromosoma][i][0][1] == h:
                if listaCromosomas[posCromosoma][i][1][1] == 1:
                    color1 = color1+1
                if listaCromosomas[posCromosoma][i][1][1] == 2:
                    color2 = color2+1
                if listaCromosomas[posCromosoma][i][1][1] == 3:
                    color3 = color3+1

        # The next condition check if our node has more than one color assigned to the same 
        # chromosome, if so, increment 1 to its total fitness, called "aptitudTotal". The same
        # happens with the condition below, where if one color is repeated in one connection, also it is 
        # incremented by 1 to its total fitness. 

        if (color1 and color2 > 0) or (color1 and color3 > 0) or (color2 and color3 > 0) or (color1 and color2 and color3 > 0):
            aptitudTotal = aptitudTotal+1
    repColor = 0
    aptitudResta = 0
    for i in range(n):
        if listaCromosomas[posCromosoma][i][1][0] == listaCromosomas[posCromosoma][i][1][1]:
            repColor = repColor + 1
    aptitudTotal = aptitudTotal + repColor

    # The generation of "listaAptitud" will help us in the function below (getPrometedores())
    # since it will allow us to set a fitness limit to this list, so we can check more easily
    # and then get the more useful chromosomes.

    listaAptitud.append([posCromosoma,aptitudTotal])
    return aptitudTotal

# Function to get chromosomes that are more useful for the next generation.

def getPrometedores():
    for i in range(len(listaAptitud)):

        # Set a limit for the max fitness = 8, this value gives better results.
        # You could encode data as you like, this limit could be modified with different values 
        # (getting the best elements despite having reduced quantity in result) 

        if listaAptitud[i][1] <= 8:
            listaPrometedores.append(listaCromosomas[listaAptitud[i][0]])

# Mutation operator. Will act on RV, performing a random mutation.

def mutacion(probMutacion):

    # Set a probability of 30% for this method and 'cruce(probCruce)' which has a 99%.
    # Randomize a number between 0 and 100, in case that this number is less than the probability
    # assigned before (i.e. for the mutation, less than 30), the process runs.

    exitoMutacion = randint(0,100)
    if listaCromosomas:

        # In case that the mutation runs, this works as follows:
        # We choose one random gene of a random chromosome and assign a new color to the
        # first element in the gene (in this case, following the gene format previously described, which 
        # goes: ((nodeA, nodeB), (colorA, colorB)), and the value that we modified would be 'colorA') 

        # P.S: to avoid confusions and program crashings, we always use as execution range 
        # for the cycle (length of the list we are working with) since this will be changing 
        # their length regularly.

        rango = len(listaCromosomas)-1
        if exitoMutacion <= probMutacion:
            cromosomaMutado = randint(0,rango)
            genMutado = randint(0,11)
            valorSV = randint(1,3)
            nodoMutado = listaCromosomas[cromosomaMutado][genMutado][0][0]
            for i in range(n):

                # Modification of the color for all nodes that matched
                # with the one who has been mutated, it avoids setting two colors 
                # to the same node.

                if listaCromosomas[cromosomaMutado][i][0][0] == nodoMutado:
                    listaCromosomas[cromosomaMutado][i][1][0] = valorSV
                if listaCromosomas[cromosomaMutado][i][0][1] == nodoMutado:
                    listaCromosomas[cromosomaMutado][i][1][1] = valorSV

# Crossover operator.

def cruce(probCruce):

    # With 'global', we indicate to the function that the lists that are using this reserved word, 
    # exist previously, else, an error will appear telling us that we are trying to
    # reference a list despite they have not been declared.

    global listaCromosomas
    global listaPrometedores
    listaCromosomasNueva = []
    
    # Also, we use the same probability validation of crossover as we did with mutation.

    exitoCruce = randint(0,100)
    if exitoCruce < probCruce:        
        p = 0
        h = 0
        
        # In case that crossover runs, this works as follows:
        # cromosomaAux1 in its first element, assign first gene of the first progenitor chromosome,
        # at the same time, to the second element assign the second gene of the second progenitor chromosome,
        # and so on, until it finishes with all the existing genes of those parents.
        
        # For the cromosomaAux2, we use the same parents, but using the inverse genes. i.e, as first element, 
        # cromosomaAux2 will contain the first gene of the second progenitor, and the second gen of the first
        # progenitor, and so on until it finishes with all the genes.

        # Both children are added to the next generation of chromosomes.

        while p<len(listaPrometedores):
            cromosomaAux1 = []
            cromosomaAux2 = []
            while h < n:
                if(p+1<len(listaPrometedores)):
                    cromosomaAux1.append(listaPrometedores[p][h])
                    cromosomaAux1.append(listaPrometedores[p+1][h+1])
                h=h+2
            h = 0
            while h < n:
                if(p+1<len(listaPrometedores)):
                    cromosomaAux2.append(listaPrometedores[p+1][h])
                    cromosomaAux2.append(listaPrometedores[p][h+1])
                h=h+2
                
            if cromosomaAux1 and cromosomaAux2:
                listaCromosomasNueva.append(cromosomaAux2)
                listaCromosomasNueva.append(cromosomaAux1)
            p = p+2
        listaCromosomas = []
        listaCromosomas = listaCromosomasNueva

# Main section of the program (executions).

        # At this point, the only thing left is the execution of the functions previously described,
        # besides that from this point on, we will see the execution of the program.

while solucionCorrecta!=True:
    listaAptitud = []
    listaPrometedores = []
    for i in range(len(listaCromosomas)):
        aptitudAux = fitnessFunc(i)

        # After evaluating the fitness of every chromosome, if one of them has 0
        # (which means that the program couldn't find any repetead color and no nodes with different colors 
        # assigned to same chromosome), it is labelled as the right answer, and therefore, the program ends.

        # This validation is made twice since the first generation could contain the solution to the problem,
        # and the next one could too.

        if aptitudAux == 0:
                solucionCorrecta = True
                cromosomaSolucion = listaCromosomas[i]
                print("Solución Correcta: ", cromosomaSolucion)
                break
                
    getPrometedores()
    cruce(probabilidadCruce)
    mutacion(probabilidadMutacion)
    for i in range(len(listaCromosomas)):
        aptitudAux = fitnessFunc(i)
        if aptitudAux == 0:
                solucionCorrecta = True
                cromosomaSolucion = listaCromosomas[i]
                print("Solución Correcta: ", cromosomaSolucion)  