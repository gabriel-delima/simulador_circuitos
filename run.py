################################################
#        Projeto  de Circuitos Elétricos       #
################################################
import getData
import functions

print("-----------------------------------------------")
storage = getData.setComponentsInStorage()
print("-----------------------------------------------")


firstMatrix = functions.buildMainMatrix(storage)
print(firstMatrix)
print("x")
secondMatrix = functions.buildSecondMatrix(storage)
print(secondMatrix)
print("=")
thirdMatrix = functions.buildthirdMatrix(storage)
print(thirdMatrix)
functions.solveSystem(firstMatrix,secondMatrix,thirdMatrix,storage)
print("---------- DONE ----------")
print("--------------------------")


