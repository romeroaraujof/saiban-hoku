# -*- coding: utf-8 -*-
# UFPk - Useful Functions Pack - V. 1.0 RC2
# 11/05/2009 - 08/06/2010
# Romero Gomes da Silva Araujo Filho
# Marvin Dalkiri - Monkey's Translations

import os.path, os, sys, array, shutil

try:
    import psyco
    psyco.full()
except: pass

# -------------------------------------------------------------------------------------------------------
#
#                                               TODO
#
# -------------------------------------------------------------------------------------------------------

#TODO:

# -------------------------------------------------------------------------------------------------------
#
#                                               Funções Úteis
#
# -------------------------------------------------------------------------------------------------------

def choice(minNumber, maxNumber, userInput):
    condition=False
    if userInput not in range(minNumber, maxNumber):
        print "\nValor incorreto! Os valores possíveis estão entre %d e %d!\n" % (minNumber, maxNumber)
    else:
        condition=True
    return userInput, condition

def filesFolder(directory):
    files=os.listdir(directory)
    return files

##def superListFolder(directory, option):
##    if option == "dump":
##        try:
##            os.mkdir("Dumped Scripts")
##        except: pass
##        filesList = []
##        for root, dirs, files in os.walk('BMG'):
##            if files:
##                for i in range(len(files)):
##                    filesList.append(os.path.join(root[4:], files[i]))
##                    try:
##                        os.makedirs(os.path.join("Dumped Scripts", root[4:]))
##                    except: pass
##        dumpBMG(filesList)
##        try:
##            os.makedirs(os.path.join("Dumped Scripts", root[4:]))
##        except: pass
##    elif option == "create":
##        try:
##            os.mkdir("New BMG")
##        except: pass
##        filesList = []
##        for root, dirs, files in os.walk('Dumped Scripts'):
##            if files:
##                for i in range(len(files)):
##                    filesList.append(os.path.join(root[15:], files[i]))
##                    try:
##                        os.makedirs(os.path.join('New BMG', root[15:]))
##                    except: pass
##        insertBMG(filesList)
##        try:
##            os.makedirs(os.path.join('New BMG', root[15:]))
##        except: pass

def removeChars(textData, chars):
    chars = list(chars)
##    newText=""
    for i in range(len(chars)):
        textData = textData.replace(chars[i], "")
    return textData
##    for element in range(len(textData)):
##        if textData[element] not in chars:
##            newText += textData[element]
##    return newText

def reverseList(someList):
    """
    UFPk.reverseList(someList) ->
    Recebe uma lista de chaves, devolve a lista ordenada por tamanho decrescente
    Pode também ser utilizado com qualquer tipo de lista.
    """
    ind2=len(someList)-1
    troquei=True
    while troquei != False:
        troquei=False
        for ind1 in range((ind2)):
            if someList[ind1]<someList[ind1+1]:
                temp=someList[ind1]
                someList[ind1]=someList[ind1+1]
                someList[ind1+1]=temp
                troquei=True
        ind2=ind2-1
    return someList

def orderList(someList):
    """
    UFPk.orderList(someList) ->
    Recebe uma lista de chaves, devolve a lista ordenada por tamanho decrescente
    Pode também ser utilizado com qualquer tipo de lista.
    """
    ind2=len(someList)-1
    troquei=True
    while troquei != False:
        troquei=False
        for ind1 in range((ind2)):
            if someList[ind1]>someList[ind1+1]:
                temp=someList[ind1]
                someList[ind1]=someList[ind1+1]
                someList[ind1+1]=temp
                troquei=True
        ind2=ind2-1
    return someList

# -------------------------------------------------------------------------------------------------------
#
#                                               ROMHack
#
# -------------------------------------------------------------------------------------------------------

def doubleBitsTable(tableFile, secondByte = "00"):
    """
    UFPk.doubleBitsTable(tableFile[, secondByte])
    Retorna uma tabela de 16 bits.
    Caso o byte secundário não seja fornecido, se usa 00.
    """
    f=open(tableFile, "r+")
    lines = []
    for line in f:
        if len(removeChars(line, "\n\r")) >= 3:
            if line.find("=") == 4:
                lines.append(line)
            elif "=" not in line:
                lines.append(line)
            else:
                lines.append(line[:2] + secondByte + line[2:])
        else:
            lines.append(line)
    f.close()
    os.remove(tableFile)
    f=open(tableFile, "w")
    f.writelines(lines)
    return None

def numberString(string, hexform = None):
    """
    UFPk.numberString(string[, hexform]) -> "abcd" = 0x61626364
    Retorna o valor de uma string de qualquer tamanho.
    Caso se queira o valor hexadecimal, o parâmetro hexform deve ser fixado como True
    """
    if hexform == None:
        totalValue = 0
        for element in string:
            totalValue = (totalValue<<8) + ord(element)
        return totalValue
    elif hexform == True:
        totalValue = ""
        for element in string:
            if element == "\x00":
                totalValue += "00"
            else:
                totalValue += hex(ord(element))[2:]
        return totalValue

def invertString(string):
    """
    UFPk.invertString(string) -> "abcd" = "dcba"
    Retorna uma string invertida de uma string.
    """
    invertedString=""
    for i in range(len(string)-1, -1, -1):
        invertedString=invertedString+string[i]
    return invertedString

def stringLenght(romFile, scriptStart, scriptEnd, tableDictionary):
    """
    UFPk.stringLenght(romFile, scriptStart, scriptEnd, tableDictionary)
    Devolve uma lista com o tamanho de cada String do script.
    Usado em jogos onde o ponteiro é, na verdade, o tamanho de cada string.
    """
    f1=open(romFile, "rb")

    stringLenghts = []

    i = scriptStart
    size = 0

    EOPCheck = invertTable(tableDictionary).get("<p>") #EOPCheck is the end of pointer check. In other words: the endstring, <p>.
    while True:
        if len(EOPCheck) == 1:
            char = f1.read(1)
            size += 1
            i+=1
            while char is not EOPCheck:
                size += 1
                i+=1
                char = f1.read(1)
            stringLenghts.append(size)
            size = 0
            if i == scriptEnd:
                break
        elif len(EOPCheck) == 2: #By other means: the table value for <p> is a 16-bits one.
            f2bytes = EOPCheck[0]
            l2bytes = EOPCheck[1]
            pointerDefine = False
            while pointerDefine != True:
                char = f1.read(1)
                size += 1
                i += 1
                if char == f2bytes:
                    if f1.read(1) == l2bytes:
                        size += 1
                        i += 1
                        pointerDefine = True
            stringLenghts.append(size)
            size = 0
            pointerDefine = False
            if i == scriptEnd:
                break

    for lenght in range(len(stringLenghts)):
        stringLenghts[lenght] = createPointer(stringLenghts[lenght], pointerSize, pointerDiff)
    return stringLenghts



def invertPointers(pointer):
    """
    UFPk.invertPointers(pointer)
    Retorna o valor numérico de um ponteiro, recebido como string.
    DEVE SER RECEBIDO COMO STRING!
    """
    invertedPointer=0
    for i in range(len(pointer)-1, -1, -1):
        invertedPointer=(invertedPointer<<8)+ord(pointer[i])
    return invertedPointer

def createPointer(pointer, pointerSize, pointerDiff = 0):
    """
    UFPk.createPointer(pointer, pointerSize[, pointerDiff])
    Função para calcular os ponteiros. Recebe o valor calculado pelo programa
    para os ponteiros, o tamanho em bytes do mesmo, e a diferença
    de cálculo entre os ponteiros.
    """
    createdPointer=""
    pointer = hex(pointer - pointerDiff)[2:]
    if "L" in pointer:
        pointer = pointer[:-1]
    if len(pointer)%2 == 1:
        pointer = "0" + pointer
    if len(pointer)/2 < pointerSize:
        pointer = "00"*(pointerSize-len(pointer)/2) + pointer
    for i in range(pointerSize, 0, -1):
        createdPointer += chr(int("0x" + pointer[(2*i-2):(2*i)],16))
    return createdPointer

def dumpPointers(romFile, pointerStart, pointerEnd, pointerSize, pointerDiff = 0):
    """
    UFPk.dumpPointers(pointerStart, pointerEnd, pointerSize, pointerDiff)
    Recebe os offsets de início e fim dos ponteiros, o tamanho e a diferença de ponteiro.
    Retorna uma lista.
    """
    f1=open(romFile, "rb")
    pointers = []
    for element in range((pointerEnd-pointerStart)/pointerSize + 1):
        temp=invertPointers(f1.read(pointerSize))
        pointers.append(temp + pointerDiff)
    return pointers

def pointerParser(pointerTable):
    """
    UFPk.pointerParser(pointerTable) ->
    Recebe uma tabela de ponteiros, e a devolve
    sem os ponteiros repetidos.
    Funciona em conjunto com a função
    UFPk.pointerLinker()
    """
    nonRepeated=[]
    for pointer in pointerTable:
        if pointer not in nonRepeated:
            nonRepeated.append(pointer)
    return nonRepeated

def pointerLinker(originalPointers, parsedPointers):
    """
    UFPk.pointerLinker(originalPointers, parsedPointers) ->
    Recebe uma tabela de ponteiros sem os ponteiros repetidos
    e a devolve com os ponteiros repetidos.
    Funciona em conjunto com a função
    UFPk.pointerLinker()
    """
    repeats=[]
    nonRepeated = []
    i=0
    for pointer in originalPointers:
        if pointer not in nonRepeated:
            nonRepeated.append(pointer)
        else:
            repeats.append((originalPointers.index(pointer), i))
        i+=1
    for pointer in repeats:
        parsedPointers.insert(pointer[1], parsedPointers[pointer[0]])
    return parsedPointers

def getChars(numberString):
    if len(numberString)%2 == 1:
        numberString = "0" + numberString
    string = ""
    while len(numberString) > 0:
        string += chr(int(numberString[:2], 16))
        numberString = numberString[2:]
    return string

def importTable(tableName):
    """
    UFPk.importTable(tableName)
    Importa uma tabela Thingy modificada, e retorna seus valores em formato de um dicionário
    """
    newTable = {}
    tableFile=open(tableName, "rb")
    if numberString(tableFile.read(3), True).upper() == "EFBBBF":
        pass
    else:
        tableFile.seek(0)
    for line in tableFile:
        line=line.strip("\r\n")
        if "=" and "=<" and ":(" not in line:
            try:
                equal=line.index("=")
                if line[equal+1:] == "\\n" or line[equal+1:] == "\n":
                    newTable[getChars(line[:equal])] = "\n"
                else:
                    newTable[getChars(line[:equal])]=line[equal+1:]
            except:
                if line == "":
                    pass
                elif "=" not in line: # Dado: Essa parte foi feita para compatibilidade com as pessoas que usam "/" como fim de diálogo, e "*" como fim de texto.
                    if line[0] == "/":
                        newTable[getChars(line[1:])]="<p>"
                    elif line[0] == "*":
                        newTable[getChars(line[1:])]="\n"
                else: # Condição para eventuais bookmarks
                    pass
    tableFile.close()
    return newTable

def invertTable(tableDictionary):
    """
    UFPk.invertTable(tableDictionary)
    Recebe uma tabela já em formato de dicionário, e inverte, do formato FF=a para a=FF
    """
    newDictionary={}
    a=0
    for i in tableDictionary.iterkeys():
        if type(tableDictionary[i]) is list:
            newDictionary[tableDictionary[i][0]]=[i, tableDictionary[i][1]]
        else:
            newDictionary[tableDictionary[i]]=i
    return newDictionary

def importVariableTable(tableName):
    """
    UFPk.variableTable(tableName) -> Dicionário com Tabela
    Função para importação de valores variáveis de tabelas, onde importa uma tabela Thingy modificada,
    e retorna seus valores que aceitam variáveis em formato de um dicionário.
    """
    newTable={}
    tableFile=open(tableName, "rb")
    if numberString(tableFile.read(3), True).upper() == "EFBBBF":
        pass
    else:
        tableFile.seek(0)
    for line in tableFile:
        line=line.strip("\r\n")
        if "=" and "=<" and ":(" in line:
            equal = line.index("=")
            variable = line.index("(")
            variableSize = int(line[variable+1:-1])
            newTable[getChars(line[:equal])]=[line[equal+1:variable], variableSize]
    tableFile.close()
    return newTable

def asciiTable():
    """
    UFPk.asciiTable() -> Retorna uma tabela ASCII básica
    """
    return {0: '<p>', 13: '\n', 32: ' ', 33: '!', 34: '"', 35: '#', 36: '$',
            37: '%', 38: '&', 39: '\'', 40: '(', 41: ')', 44: ',', 45: '-',
            46: '.', 48: '0', 49: '1', 50: '2', 51: '3', 52: '4', 53: '5',
            54: '6', 55: '7', 56: '8', 57: '9', 58: ':', 63: '?', 65: 'A',
            66: 'B', 67: 'C', 68: 'D', 69: 'E', 70: 'F', 71: 'G', 72: 'H',
            73: 'I', 74: 'J', 75: 'K', 76: 'L', 77: 'M', 78: 'N', 79: 'O',
            80: 'P', 81: 'Q', 82: 'R', 83: 'S', 84: 'T', 85: 'U', 86: 'V',
            87: 'W', 88: 'X', 89: 'Y', 90: 'Z', 97: 'a', 98: 'b', 99: 'c',
            100: 'd', 101: 'e', 102: 'f', 103: 'g', 104: 'h', 105: 'i',
            106: 'j', 107: 'k', 108: 'l', 109: 'm', 110: 'n', 111: 'o',
            112: 'p', 113: 'q', 114: 'r', 115: 's', 116: 't', 117: 'u',
            118: 'v', 119: 'w', 120: 'x', 121: 'y', 122: 'z'}

def fullASCII():
    """
    UFPk.fullASCII() -> Retorna uma tabela ASCII completa, com acentos
    """
    print "Not implemented yet"

def shiftJIS():
    """
    UFPk.shiftJIS() -> Retorna uma tabela de codificação japonesa shift-JIS
    """
    print "Not implemented yet"

def eucJIS():
    """
    UFPk.eucJIS() -> Retorna uma tabela de codificação japonesa euc-JIS
    """
    print "Not implemented yet"

def optimizeScript(scriptArchive, tableDictionary, variableTable = {}, scriptFile = True):
    """
    UFPk.optimizeScript(scriptArchive, tableDictionary[, scriptFile = True])
    Retorna uma string RAW do script dado.
    Caso scriptFile seja ignorado, abre a partir de um arquivo, que esteja na pasta
    padrão "Dumped Scripts". Caso seja dado outro valor, scriptArchive deverá ser passado
    como uma string.
    """

    invertedTable=invertTable(tableDictionary)
    invertedVariableTable = invertTable(variableTable)
    extraChars=["<", ">", "[", "]"]
    newScript=""
    if scriptFile == True:
        f1 = open(os.path.join("Dumped Scripts", scriptArchive), "rb")
        wholeThing = f1.read()
        f1.close()
    else:
        wholeThing = scriptArchive
    wholeThing = wholeThing.replace("---------------------------------", "<p>")
    wholeThing = wholeThing.replace("#################################", "<new_page>")
    wholeThing = wholeThing.replace("#\r\n", "<n>")
    wholeThing = wholeThing.replace("*\r\n", "<n>")
    if "<n>" not in invertedTable.keys() and "\n" in invertedTable:
        invertedTable["<n>"] = invertedTable.get("\n")
    wholeThing = wholeThing.replace("\r\n", "")
    tableKeys=orderLenKeys(invertedTable.keys())
    charTable, longTable=stripTable(tableKeys)

    for element in invertedVariableTable.keys():
        if element in wholeThing:
            variable = invertedVariableTable.get(element)[1]
            wholeThing = wholeThing.split(element)
            for i in range(1, len(wholeThing)):
                variables = wholeThing[i][:wholeThing[i].find(">")]
                wholeThing[i] = wholeThing[i][wholeThing[i].find(">")+1:]
                variables = variables.split(",")
                variableString = ""
                for j in range(len(variables)):
                    variableString += "[$" + hex(int(variables[j]))[2:] + "]"
                wholeThing[i] = variableString + wholeThing[i]
                if len(invertedVariableTable.get(element)[0]) == 2:
                    f2bytes=invertedVariableTable.get(element)[0][0]
                    l2bytes=invertedVariableTable.get(element)[0][1]
                    wholeThing[i] = "[$" + hex(ord(f2bytes))[2:] + "]" + "[$" + hex(ord(l2bytes))[2:] + "]" + wholeThing[i]
                else:
                    wholeThing[i] = "[$" + hex(ord(invertedVariableTable.get(element)[0]))[2:] + "]" + wholeThing[i]
            wholeThing = "".join(wholeThing)

    for element in longTable:
        if element in wholeThing:
            if len(invertedTable.get(element)) == 2:
                f2bytes=invertedTable.get(element)[0]
                l2bytes=invertedTable.get(element)[1]
                wholeThing=wholeThing.replace(element, "[$" + hex(ord(f2bytes))[2:] + "]" + "[$" + hex(ord(l2bytes))[2:] + "]")
            else:
                wholeThing=wholeThing.replace(element, "[$" + hex(ord(invertedTable.get(element)))[2:] + "]")
    char = 0
    size = len(wholeThing)

    while True:
        temp = ""
        if char == size:
            break
        if wholeThing[char] == "[" and wholeThing[char+1] == "$":
            while wholeThing[char] != "]":
                temp+=wholeThing[char]
                char += 1
            char += 1
            newScript+=chr(int("0x" + temp[2:],16))
            temp = ""
        elif wholeThing[char] in charTable:
            if len(invertedTable.get(wholeThing[char])) == 2:
                newScript = newScript + invertedTable.get(wholeThing[char])[0] + invertedTable.get(wholeThing[char])[1]
                char += 1
            else:
                newScript+=invertedTable.get(wholeThing[char])
                char += 1
        else:
            if wholeThing[char] not in extraChars:
                extraChars.append(wholeThing[char])
            char += 1
    if len(extraChars) > 4:
        j=open("Caracteres Fora da Tabela.txt", "w+b")
        for k in range(4, len(extraChars)):
            j.write(extraChars[k] + "\r\n")
        j.close()
    return newScript

def checkScriptLenght(wholeScript, scriptStart, scriptEnd):
    return len(wholeScript) - (scriptEnd - scriptStart)




##def checkScriptLenght(scriptStart, scriptEnd, newScript, scriptName, tableDictionary):
##    scriptSize=scriptEnd-scriptStart
##    spaceChar=chr(invertTable(tableDictionary).get(" "))
##    if len(newScript)>scriptSize:
##        print "Script " + scriptName + " e' maior que o original! A diferenca e' de %d bytes." % (len(newScript)-scriptSize)
##    else:
##        newScript+=(len(newScript)-scriptSize)*spaceChar
##    return newScript

def orderLenKeys(tableKeys):
    """
    UFPk.orderLenKeys(tableKeys) -> recebe uma lista de chaves, devolve a lista ordenada por tamanho decrescente
    Pode também ser utilizado com qualquer tipo de lista.
    """
    ind2=len(tableKeys)-1
    troquei=True
    while troquei != False:
        troquei=False
        for ind1 in range((ind2)):
            if len(tableKeys[ind1])<len(tableKeys[ind1+1]):
                temp=tableKeys[ind1]
                tableKeys[ind1]=tableKeys[ind1+1]
                tableKeys[ind1+1]=temp
                troquei=True
        ind2=ind2-1
    return tableKeys

def orderSizeKeys(tableKeys):
    """
    UFPk.orderSizeKeys(tableKeys) -> recebe uma lista de chaves, devolve a lista ordenada por valor decrescente
    Pode também ser utilizado com qualquer tipo de lista de valores.
    """
    ind2=len(tableKeys)-1
    troquei=True
    while troquei != False:
        troquei=False
        for ind1 in range((ind2)):
            if tableKeys[ind1]<tableKeys[ind1+1]:
                temp=tableKeys[ind1]
                tableKeys[ind1]=tableKeys[ind1+1]
                tableKeys[ind1+1]=temp
                troquei=True
        ind2=ind2-1
    return tableKeys

def stripTable(tableKeys):
    charTable=[]
    longTable=[]
    for element in tableKeys:
        if len(element)==1:
            position=tableKeys.index(element)
            longTable=tableKeys[:position]
            charTable=tableKeys[position:]
            break
    return charTable, longTable

def stripTableSize(tableDictionary): #lembrar que essa é a função para as tabelas de 16 bytes!!!
##    tableKeys=orderSizeKeys(tableDictionary.keys())
##    charTable=[]
##    longTable=[]
    tableKeys = tableDictionary.keys()
    sixteenBitsTable=[]
    eightBitsTable=[]
    for element in tableKeys:
        if len(element) == 1 and element not in eightBitsTable:
            eightBitsTable.append(element)
        elif len(element) == 2 and element not in sixteenBitsTable:
            sixteenBitsTable.append(element[0])
    return eightBitsTable, sixteenBitsTable

def endOfFile(f1):
    #TODO: tenho que refazer isso tudo...s
    f1.seek(0, 2)
    temp = f1.read(1)
    while temp == 0x00:
        f1.seek(-2,1)
        temp=f1.read()
    return f1.tell()

def getChar(char, tableDictionary):
    if char in tableDictionary:
        char=tableDictionary.get(char)
        if char == "\n" or char == "<n>":
            return "#\r\n"
        elif char == "<p>":
            return "\r\n\r\n---------------------------------\r\n\r\n"
        elif char == "<new_page>":
            return "\r\n\r\n#################################\r\n\r\n"
        else:
            return char
    else:
        return "[$" + hex(ord(char))[2:] + "]"

def dumpScriptPointersFull(romFile, pointerStart, pointerEnd, pointerSize, tableDictionary, i, pointerDiff = 0):
    """
    UFPk.dumpScriptPointersFull(romFile, pointerStart, pointerEnd, pointerSize, tableDictionary, i, pointerDiff = 0)
    Função para dumpar um script.
    Não permite interferências do usuário, só é recomendada quando o script for regular.
    """
    try:
        os.mkdir("Dumped Scripts")
    except:
        pass
    pointers=[]
    tempf=[]
    scriptName="script-%03d.txt" %i
    i=i+1
    f1=open(romFile, "rb")
    f2=open(os.path.join("Dumped Scripts", scriptName), "wb")
    f1.seek(pointerStart)

    for element in range((pointerEnd-pointerStart)/pointerSize + 1):
        temp=invertPointers(f1.read(pointerSize))
        pointers.append(temp + pointerDiff)

    pointers = pointerParser(pointers)

    eightBitsTable, sixteenBitsTable=stripTableSize(tableDictionary)

    if pointerDiff is not 0:
        for pointer in pointers:
#            print hex(pointer)
#            raw_input()
            try:
                f1.seek(pointer)
            except:
                break
            endOfPointer = False
            while endOfPointer is False:
                char=f1.read(1)
                if char in sixteenBitsTable:
                    try: char += f1.read(1)
                    except: break
                    if char in tableDictionary:
                        f2.write(getChar(char, tableDictionary))
                    else:
                        if (char[0]) in eightBitsTable:
                            f2.write(getChar((char[0]), tableDictionary))
                            f1.seek(-1, 1)
                        else:
                            f2.write("[$" + hex(ord(char[0]))[2:] + "]")
                            f1.seek(-1, 1)
                            char = char[0]
                elif char in eightBitsTable:
                    f2.write(getChar(char, tableDictionary))
                elif char not in tableDictionary:
                    f2.write("[$" + hex(ord(char))[2:] + "]")
                if tableDictionary.get(char) == "<p>":
                    endOfPointer = True
        f2.close()

    elif pointerDiff == 0:
        i = i-1
        dumpScriptFull(romFile, f1.tell() + min(pointers), f1.tell() + max(pointers), tableDictionary, i)
    f1.close()

def dumpScriptFull(romFile, scriptStart, scriptEnd, tableDictionary, i):
    """
    UFPk.dumpScriptFull(romFile, scriptStart, scriptEnd, tableDictionary, i)
    Dumpa um script que comece em scriptStart, até scriptEnd, usando os
    valores da tabela tableDictionary, na ROM romFile, com o índice i.
    Recomendado quando o jogo não possuir ponteiros, e o script seja regular.
    Pode ser ainda usado em caso de tabelas de ponteiros relativas.
    """
    try:
        os.mkdir("Dumped Scripts")
    except:
        pass
    scriptName="script-%03d.txt" %i
    i=i+1

    eightBitsTable, sixteenBitsTable=stripTableSize(tableDictionary)

    f1=open(romFile, "rb")
    f2=open(os.path.join("Dumped Scripts", scriptName), "wb")
    f1.seek(scriptStart)
    scriptSize = 0
    while scriptSize < (scriptEnd - scriptStart + 1):
        char = f1.read(1)
        scriptSize += 1
        if char in sixteenBitsTable:
            try: char += f1.read(1)
            except: break
            scriptSize += 1
            if char in tableDictionary:
                f2.write(getChar(char, tableDictionary))
            else:
                if char[0] in eightBitsTable:
                    f2.write(getChar(char[0], tableDictionary))
                    f1.seek(-1, 1)
                    scriptSize -= 1
                else:
                    f2.write("[$" + hex(ord(char[0]))[2:] + "]")
                    f1.seek(-1, 1)
                    char = char[0]
                    scriptSize -= 1
        elif char in eightBitsTable:
            f2.write(getChar(char, tableDictionary))
        elif char not in tableDictionary:
            f2.write("[$" + hex(ord(char))[2:] + "]")
    f1.close()
    f2.close()

def dumpScriptSimple(rawInput, tableDictionary, i, saveFile = True, nameFile = None):
    """
    UFPk.dumpScriptSimple(rawInput, tableDictionary, i[, saveFile = False, nameFile = None])
    Insere os valores da tabela no script que esteja em formato RAW.
    Usado quando o script passou por etapas anteriores, ou o mesmo não é regular
    e precisa de modificações antes de ser dumpado.
    Caso seja dado um valor a saveFile, o script não será salvo em um arquivo.
    Caso seja dado um valor a nameFile, o arquivo será salvo com esse nome.
    """
    try:
        os.mkdir("Dumped Scripts")
    except:
        pass
    if nameFile == None:
        scriptName="script-%03d.txt" %i
    else:
        scriptName=nameFile

    f1=open("dumptemp.dat", "w+b")
    f1.write(rawInput)
    f1.seek(0)

    eightBitsTable, sixteenBitsTable=stripTableSize(tableDictionary)

    f2 = ""

    scriptSize = 0

    while scriptSize < len(rawInput):
        char = f1.read(1)
        scriptSize += 1
        if char in sixteenBitsTable:
            try: char += f1.read(1)
            except: break
            scriptSize += 1
            if char in tableDictionary:
                f2 += getChar(char, tableDictionary)
            else:
                if char[0] in eightBitsTable:
                    f2 += getChar((char[0]), tableDictionary)
                    f1.seek(-1, 1)
                    scriptSize -= 1
                else:
                    f2 += ("[$" + hex(ord(char[0]))[2:] + "]")
                    f1.seek(-1, 1)
                    char = char[0]
                    scriptSize -= 1
        elif char in eightBitsTable:
            f2 += getChar(char, tableDictionary)
        elif char not in tableDictionary:
            f2 += ("[$" + hex(ord(char))[2:] + "]")
    f1.close()
    if saveFile == True:
        try:
            os.unlink("dumptemp.dat")
        except:
            pass
        endFile=open(os.path.join("Dumped Scripts", scriptName), "wb")
        endFile.write(f2)
        endFile.close()
        return True
    else:
        try:
            os.unlink("dumptemp.dat")
        except:
            pass
        return f2

def dumpScriptPointersSimple(romFile, pointersTable, pointerSize, tableDictionary, i, pointerDiff = 0):
    """
    UFPk.dumpScriptPointersSimple(romFile, pointersTable, pointerSize, tableDictionary, i, pointerDiff = 0)
    Função para dumpar um script.
    Permite que o usuário altere informações, e trate o script como quiser.
    Os ponteiros devem ser passados como uma lista de strings.
    """
    try:
        os.mkdir("Dumped Scripts")
    except:
        pass
#    pointers=[]
#    tempf=[]
    scriptName="script-%03d.txt" %i
    i=i+1
    f1=open(romFile, "rb")
    f2=open(os.path.join("Dumped Scripts", scriptName), "wb")
    f1.seek(pointerStart)
    for i in range(len(pointersTable)):
        temp=invertPointers(pointersTable[i])
        pointersTable[i] = temp + pointerDiff
        #TODO: end this

    pointers = pointerParser(pointers)

    eightBitsTable, sixteenBitsTable=stripTableSize(tableDictionary)

    if pointerDiff is not 0:
        for pointer in pointers:
            try:
                f1.seek(pointer)
            except:
                break
            endOfPointer = False
            while endOfPointer is False:
                char=ord(f1.read(1))
                if tableDictionary.get(char) == "<p>":
                    endOfPointer = True
                if char == 0x00:
                    if len(tableDictionary["exceptions"]) != 0:
                        try: char = ord(f1.read(1))
                        except: break
                        if char in tableDictionary["exceptions"]:
                            f2.write(getChar(char, tableDictionary))
                            char = ord(f1.read(1))
                            scriptSize += 1
                        else:
                            f2.write(getChar(0x00, tableDictionary))
                            #f2.write("[$0]")
                        if tableDictionary.get(char) == "<p>":
                            endOfPointer = True
                if char in sixteenBitsTable and char is not 0x00:
                    try: char = (char<<8) + ord(f1.read(1))
                    except: break
                    if char in tableDictionary:
                        f2.write(getChar(char, tableDictionary))
                    else:
                        if (char>>8) in eightBitsTable:
                            f2.write(getChar((char>>8), tableDictionary))
                            f1.seek(-1, 1)
                        else:
                            f2.write("[$" + hex(char/256)[2:] + "]")
                            f1.seek(-1, 1)
                            char = char/256
                    if tableDictionary.get(char) == "<p>":
                        endOfPointer = True
                elif char in eightBitsTable:
                    f2.write(getChar(char, tableDictionary))
                elif char is not 0x00:
                    f2.write("[$" + hex(char)[2:] + "]")
                elif char == 0x00 and char not in tableDictionary:
                    f2.write("[$" + hex(char)[2:] + "]")
        f2.close()

    elif pointerDiff == 0:
        i = i-1
        dumpScriptFull(romFile, f1.tell() + min(pointers), f1.tell() + max(pointers), tableDictionary, i)
    f1.close()


def updatePointers(romFile, scriptStart, scriptEnd, pointerStart, pointerEnd, tableDictionary, pointerSize, pointerDiff = 0):
    f1=open(romfile, "r+b")
    newPointers=[]
    f1.seek(scriptStart)
    size = 0
    print "\n\n" + "Calculando Ponteiros... Espere...".center(79) + "\n\n"
    EOPCheck = invertTable(tableDictionary).get("<p>") #EOPCheck is the end of pointer check. In other words: the endstring, <p>.
    while True:
        if EOPCheck < 0x100:
            char = f1.read(1)
            size += 1
            while ord(char) is not EOPCheck:
                size += 1
                char = f1.read(1)
            newPointers.append(size + min(pointers))
            if len(newPointers) == ((pointerEnd-pointerStart)/poiterSize):
                break
        elif EOPCheck > 0xFF: #By other means: the table value for <p> is a 16-bits one.
            EOPStart = EOPCheck/256
            EOPEnd = EOPCheck%256
            char = f1.read(1)
            size += 1
            while True:
                if ord(char) == EOPStart:
                    endchar = ord(f1.read(1))
                    size += 1
                    if endchar == EOPEnd:
                        break
                    else:
                        char = f1.read(1)
                        size += 1
                        break
            newPointers.append(size + min(pointers))
            if len(newPointers) == len(pointers):
                break

    for pointer in range(len(newPointers)):
        newPointers[pointer] = createPointer(newPointers[pointer], pointerSize, pointerDiff)
    newPointers = "".join(newPointers)
    f1.seek(pointerStart)
    f1.write(newPointers)


def insertScript(romFile, scriptStart, scriptEnd, tableDictionary):
    shutil.copy(romFile, "[NEW] " + romFile)
    romFile = "[NEW] " + romFile
    f1=open(romFile, "r+b")

    files = filesFolder("Dumped Scripts")
    for scriptArchive in range(len(files)):
        f1.seek(scriptStart[scriptArchive])
        wholeScript = optimizeScript(files[scriptArchive], tableDictionary)
        if len(wholeScript) > (scriptEnd[scriptArchive] - scriptStart[scriptArchive] + 1):
            raw_input("\n\nO script " + files[scriptArchive] + " nao podera ser adicionado, por ser maior que o original.\n\
A diferenca e de " + str(len(wholeScript) - (scriptEnd[scriptArchive] - scriptStart[scriptArchive])) + " bytes. Aperte ENTER para continuar.\n\n")
        else:
            f1.seek(scriptStart[scriptArchive] + len(wholeScript) + 1)
            if len(invertTable(tableDictionary).get(" ")) == 1:
                for extraBytes in range((scriptEnd[scriptArchive] - scriptStart[scriptArchive]) - len(wholeScript)):
                    f1.write(invertTable(tableDictionary).get(" "))
                f1.seek(scriptStart[scriptArchive])
            else:
                for extraBytes in range(((scriptEnd[scriptArchive] - scriptStart[scriptArchive]) - len(wholeScript))/2):
                    f1.write(invertTable(tableDictionary).get(" ")[0])
                    f1.write(invertTable(tableDictionary).get(" ")[1])
                f1.seek(scriptStart[scriptArchive])
            for element in range(len(wholeScript)):
                f1.write(wholeScript[element])
            print "Script localizado na posicao " + hex(scriptStart[scriptArchive]) + " e de nome " + files[scriptArchive] + " adicionado com sucesso!"

def insertScriptPointers(romFile, pointerStart, pointerEnd, pointerSize, tableDictionary, pointerDiff = 0):

#TODO arrumar espaço do script

    shutil.copy(romFile, "[NEW] " + romFile)
    romFile = "[NEW] " + romFile

    files = filesFolder("Dumped Scripts")

    for scriptArchive in range(len(files)):
        f1=open(romFile, "r+b")
        f1.seek(pointerStart[scriptArchive])
        pointers=[]
        for element in range((pointerEnd[scriptArchive]-pointerStart[scriptArchive])/pointerSize + 1):
            temp=invertPointers(f1.read(pointerSize))
            pointers.append(temp + pointerDiff)
        sizeOfLastPointer=0
        endOfScript=[""]

        wholeScript = optimizeScript(files[scriptArchive], tableDictionary)
        f1.seek(max(pointers))
        try: char = f1.read(1)
        except: char = invertTable(tableDictionary).get("<p>")
        sizeOfLastPointer+=1
        if len(invertTable(tableDictionary).get("<p>")) == 1:
            while char != invertTable(tableDictionary).get("<p>"):
                sizeOfLastPointer+=1
                char = f1.read(1)
        elif len(invertTable(tableDictionary).get("<p>")) == 2:
            f2bytes = invertTable(tableDictionary).get("<p>")[0]
            l2bytes = invertTable(tableDictionary).get("<p>")[1]
            pointerDefine = False
            while pointerDefine != True:
                while char != f2bytes:
                    sizeOfLastPointer+=1
                    char = f1.read(1)
                char2 = f1.read(1)
                if char2 == l2bytes:
                    pointerDefine = True
                else:
                    char = char2
                    sizeOfLastPointer+=1
        spaceOnROM = max(pointers) + sizeOfLastPointer - min(pointers)
##        print max(pointers)
##        print min(pointers)
##        print sizeOfLastPointer
##        print len(wholeScript)
##        print spaceOnROM
##        raw_input()
        if spaceOnROM < len(wholeScript):
            print "\n\nO tamanho do script %s e' maior do que o espaço atual." %(files[scriptArchive])
            print "A diferenca e' de %d bytes." %(len(wholeScript) - spaceOnROM)
            choice = raw_input("Deseja continuar? (S)im, (N)ão ou (C)ortar Script?\n>>> ")
            if choice.lower() == "n":
                print "O programa ira' ignorar a insercao do script %s\n\n" %(files[scriptArchive])
                thisScript = False
            elif choice.lower() == "s":
                wholeScript += invertTable(tableDictionary).get("<p>")
                thisScript = True
            elif choice.lower() == "c":
                wholeScript = wholeScript[:-(len(wholeScript) - spaceOnROM)-len(invertTable(tableDictionary).get("<p>"))]
                wholeScript += invertTable(tableDictionary).get("<p>")
                thisScript = True
            else:
                print "Escolha errada. O programa ira' ignorar a insercao do script %s\n\n" %(files[scriptArchive])
                thisScript = False

                ## Isso aqui abaixo seria uma tentativa, digamos que frustrada, de se colocar o script que faltasse no final do arquivo. Vou pensar isso melhor depois. Ou nunca, talvez...
                # endOfScript = wholeScript[spaceOnROM:]
                # wholeScript = wholeScript[:spaceOnROM]
                # f1.seek(spaceOnROM + 1)
                # for char in range(len(endOfScript)):
                    # byte=f1.read(1)
                    # if ord(byte) in (0x00, 0xff):
                        # wholeScript=wholeScript+endOfScript[0]
                        # endOfScript=endOfScript[1:]
                    # else:
                        # endOfScript=wholeScript[-2] + endOfScript
                        # wholeScript=wholeScript[:-2] + chr(invertTable(tableDictionary).get("<p>")/256) + chr(invertTable(tableDictionary).get("<p>")%256)
                # f1.seek(spaceOnROM + 1)

        elif spaceOnROM >= len(wholeScript):   #wholeScript = o arquivo de texto
                                                #spaceOnROM = o espaço vazio
            # Nesse caso, o script é menor que o espaço disponível...
            numberOfSpaces = spaceOnROM - len(wholeScript)
            wholeScript = wholeScript + (numberOfSpaces/len(invertTable(tableDictionary).get(" "))) * invertTable(tableDictionary).get(" ")
            thisScript = True

        if thisScript == True:
            f1.seek(pointerEnd[scriptArchive] - pointerSize + 1)
            a=invertPointers(f1.read(pointerSize))
            lastOffset = a + pointerDiff
            f1.seek(min(pointers))
            f1.write(wholeScript)
            newPointers=[min(pointers)]
            f1.seek(min(pointers))
            size = 0
#            print hex(min(pointers))
#            raw_input()
            print "Arquivo %s" %(files[scriptArchive])
            print "\n\n" + "Calculando Ponteiros... Espere...".center(79) + "\n\n"
            EOPCheck = invertTable(tableDictionary).get("<p>") #EOPCheck is the end of pointer check. In other words: the endstring, <p>.
            while (len(newPointers)<len(pointers)):
                if len(EOPCheck) == 1:
                    char = f1.read(1)
                    size += 1
                    while char != EOPCheck:
                        size += 1
                        char = f1.read(1)
                    newPointers.append(size + min(pointers))
                elif len(EOPCheck) == 2: #By other means: the table value for <p> is a 16-bits one.
                    f2bytes = EOPCheck[0]
                    l2bytes = EOPCheck[1]
                    pointerDefine = False
                    while pointerDefine != True:
                        char = f1.read(1)
                        size += 1
                        if char == f2bytes:
                            if f1.read(1) == l2bytes:
                                size += 1
                                pointerDefine = True
                    newPointers.append(size + min(pointers))
                    pointerDefine = False
                if f1.tell() > lastOffset:
                    for j in range(len(pointers) - len(newPointers)):
                        newPointers.append(newPointers[-1])
            for pointer in range(len(newPointers)):
                newPointers[pointer] = createPointer(newPointers[pointer], pointerSize, pointerDiff)
            newPointers = "".join(newPointers)
            f1.seek(pointerStart[scriptArchive])
            f1.write(newPointers)
        f1.close()

def binMSBF(number):
    newNumber=""
    bit=1
    while bit is not 0:
        bit=number >> 1
        newNumber = newNumber + str(number - (bit<<1))
        number = number >> 1
    return newNumber + "0"*(8-len(newNumber))

def bin(number):
    newNumber=""
    bit=1
    while bit is not 0:
        bit=number >> 1
        newNumber = str(number - (bit<<1)) + newNumber
        number = number >> 1
#    return newNumber
    return "0"*(8-len(newNumber)) + newNumber

def lzssUncompress(compressed):
    f=open("lztemp.dat", "w+b")
    f.write(compressed)
    f.seek(0)
    if ord(f.read(1)) != 0x10:
#        print("Impossivel descomprimir! Aperte enter para sair.")
        return compressed
    else:
        compressionSize=invertPointers(f.read(3))
#        print hex(compressionSize)[2:]
        uncompressed=""
        while len(uncompressed) < compressionSize:
            try:
                flag = bin(ord(f.read(1)))
            except:
                break
            for bit in flag:
                if bit == "0":
                    uncompressed+=f.read(1)
                else:
                    compression=bin(ord(f.read(1))) + bin(ord(f.read(1)))
                    bytesToCopy = int(compression[:4],2)
                    disp=int(compression[4:], 2)+1
                    for i in range(bytesToCopy+3):
                        uncompressed+=uncompressed[len(uncompressed)-int(compression[4:], 2)-1]
    f.close()
    try:
        os.unlink("lztemp.dat")
    except:
        pass
    return uncompressed


def endStrings(romFile, startScript, endScript, tableDictionary, nameFile = "endStrings.dat"):
    """
endStrings(romFile, startScript, endScript, endString[, nameFile = "endStrings.dat"])
Função para localizar os fins de linha de um determinado bloco de textos.
"""

    f=open(romFile, "rb")
    f.seek(startScript)

    endStrings = []
    endOfLine = invertTable(tableDictionary).get("<p>")

    i = 0
    currentByte = f.read(1)
#    i+=1

    while (i + startScript) < (endScript):
        if len(endOfLine == 1):
            while currentByte is not endOfLine:
                i+=1
                currentByte = f.read(1)
            endStrings.append(hex(f.tell()) + "\r\n")
            currentByte = f.read(1)
            i+=1
        elif len(endOfLine == 2):
            f2bytes = endOfLine[0]
            l2bytes = endOfLine[1]
            pointerDefine = False
            while pointerDefine != True:
                while currentByte is not f2bytes:
                    i+=1
                    currentByte = f.read(1)
                if f.read(1) == l2bytes:
                    i+=1
                    if f.read(1) == l2bytes:
                        i+=1
                    pointerDefine = True
                else:
                    i+=1
                    currentByte = f.read(1)
            endStrings.append(hex(f.tell()) + "\r\n")
            currentByte = f.read(1)
            i+=1

    f.close()

    g=open(nameFile, "wb")
    g.writelines(endStrings)
    g.close()

    return None

def bruteForcePointerSearch(romFile, endPointers, startPointers = 0, pointerDiff = 0, endStringsFile = "endStrings.dat", pointersFile = "pointers.dat"):
    """
bruteForcePointerSearch(romFile, endPointers[, startPointers = 0, pointerDiff = 0, endStringsFile = "endStrings.dat", pointersFile = "pointers.dat"])
Como o nome sugere, é uma função para localização de ponteiros em todo a ROM.
Não é recomendada para ROMs muito grandes, tendo em vista que, em um Pentium D 3000ghz, 1gb RAM,
localizar os ponteiros demora em média 10 minutos para cada 20000 ponteiros.
Entretanto, em muitas situações, é a ÚNICA solução viável... Infelizmente.
Otimizações desse código são (muito) bem vindas.
    """
    f=open(romFile, "rb")
    g=open(endStringsFile, "rb")
    endStrings = []
    pointers = []

    for line in g:
        endStrings.append(createPointer(pointerDiff + int(removeChars(line, ['L', '\r', '\n']), 16), 4))
    g.close()

    f.seek(startPointers)
    if endPointers == 0:
        search = f.read()
    else:
        search = f.read(endPointers-startPointers)
    f.close()

#    k=open("search.dat", "wb")
#    k.write(search)
#    k.close()

    i = 0
    print "*****************************"
    for endString in endStrings:
        repet = search.count(endString)
        if repet == 0:
            pointers.append("-0x1\r\n")
        elif repet == 1:
            pointers.append(hex(search.find(endString) + startPointers) + "\r\n")
        else:
            split = search.split(endString)
            a = ""
            lenSplit = 0
            for j in range(len(split) - 1):
                lenSplit += len(split[j])
                a += hex(lenSplit + startPointers) + ", "
                lenSplit += 0x04
            pointers.append(a + "\r\n")
        i+=1
        if i%5 == 0:
            print "* %05d * %05d * %9.5f *" %(i, len(endStrings), float(i)*100/len(endStrings))
    print "*****************************"
    g=open(pointersFile, "wb")
    g.writelines(pointers)
    g.close()

def bruteForcePointersUpdate(romFile, tableDictionary, startScript, endScript, pointerDiff = 0, pointerSize = 4, endStringsFile = "endStrings.dat", newEndStringsFile = "newEndStrings.dat", pointersFile = "pointers.dat"):
    """
bruteForcePointersUpdate(romFile, tableDictionary, startScript, endScript[, pointerDiff = 0, pointerSize = 4, endStringsFile = "endStrings.dat", newEndStringsFile = "newEndStrings.dat", pointersFile = "pointers.dat"])
Devendo ser usada em conjunto com a função 'bruteForcePointerSearch', essa função apenas
atualiza os scripts espalhados pela ROM.
    """
    endString = []
    newString = []
    eachPointer = []
    endStrings(romFile, startScript, endScript, tableDictionary, newEndStringsFile)
    f=open(endStringsFile, "rb")
    g=open(newEndStringsFile, "rb")
    h=open(pointersFile, "rb")
    for line in f:
        endString.append(line.strip())
    for line in g:
        newString.append(line.strip())
    for line in h:
        eachPointer.append(line.strip())
    f.close()
    g.close()
    h.close()

    f=open(romFile, "r+b")
    i = 0
    lenEachPointer = len(eachPointer)
    for pointer in eachPointer:
        if pointer != "-0x1":
            if "," in pointer:
#                pointer = UFPk.removeChars(" ")
                pointerList = pointer.split(",")[:-1]
                for j in pointerList:
                    f.seek(int(j, 16))
                    f.write(createPointer(int(newString[i].strip("L"), 16), pointerSize, pointerDiff))
                i+=1
            else:
                f.seek(int(pointer, 16))
                f.write(createPointer(int(newString[i].strip("L"), 16), pointerSize, pointerDiff))
                i+=1
        else:
            i+=1
            pass
        if i%100 == 0:
            print "Calculando ponteiros. Aguarde...\n"
            print "Ponteiro %d de %d pronto. %.4f porcento concluido." %(i, lenEachPointer, float(i)*100/lenEachPointer)
    f.close()

if __name__ == "__main__":
    raw_input("Isso... Muito bom, agora so' falta importar o mo'dulo, ao inve's de abri'-lo.\nAperte ENTER para sair, e tente novamente...")
