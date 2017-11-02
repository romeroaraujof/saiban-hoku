# -*- coding: utf-8 -*-
# UFPk - Useful Functions Pack - Development Module
# 11/05/2009 - 15/04/2010
# Romero Gomes da Silva Araujo Filho
# Marvin Dalkiri - Monkey's Translations
# Nesse módulo ficam todas as funções em fase de testes.
# Além de algumas que eu não tenho muita paciência de implementar :)
# E outras que servem para jogos específicos (possivelmente irão para o módulo __specifics__.py)
# Tenho que separar os módulos...

import UFPk
import os, os.path, sys
try:
    import psyco
    psyco.full()
except: pass

def specialReplace(tableDictionary, textFile, mode):
    """
    [$73]27 = ~
    Não tente entender, isso aqui é só pra mim mesmo :P
    """
    if mode == "d":
        replaceDictionary = importTableSpecial(tableDictionary)
        for key in replaceDictionary.keys():
            textFile = textFile.replace(key, replaceDictionary.get(key))
        return textFile
    elif mode == "i":
        replaceDictionary = importTableSpecial(tableDictionary)
        invertedReplaceDictionary = UFPk.invertTable(replaceDictionary)
        for key in invertedReplaceDictionary.keys():
            textFile = textFile.replace(key, invertedReplaceDictionary.get(key))
        return textFile
    else:
        print "Unknown mode. Please reconsider. Program will return the original text"
        return textFile
    return None

def importTableSpecial(tableName):
    """
    UFPk.importTableSpecial(tableDictionary)
    Função para importação de caracteres especiais, onde Importa uma tabela Thingy modificada,
    e retorna seus valores em formato de um dicionário.
    """
    newTable={}
    tableFile=open(tableName, "rb")
    if UFPk.numberString(tableFile.read(3), True).upper() == "EFBBBF":
        pass
    else:
        tableFile.seek(0)
    for line in tableFile:
        line=line.strip("\r\n")
        try:
            equal=line.index("=")
            if len(line[:equal])<=4:
                pass
            else:
                newTable[line[:equal]]=line[equal+1:]
        except:
            if line == "":
                pass
            elif "=" not in line: # Dado: Essa parte foi feita para compatibilidade com as pessoas que usam "/" como fim de diálogo, e "*" como fim de texto.
                pass
            else: # Condição para eventuais bookmarks
                pass
    tableFile.close()
    return newTable

def variableImportTable(tableName):
    """
    UFPk.variableTable(tableName) -> Dicionário com Tabela
    Função para importação de valores variáveis de tabelas, onde importa uma tabela Thingy modificada,
    e retorna seus valores que aceitam variáveis em formato de um dicionário.
    """
    newTable={}
    tableFile=open(tableName, "rb")
    if UFPk.numberString(tableFile.read(3), True).upper() == "EFBBBF":
        pass
    else:
        tableFile.seek(0)
    for line in tableFile:
        line=line.strip("\r\n")
        if "=" and "=<" and ":(" in line:
            equal = line.index("=")
            variable = line.index("(")
            variableSize = int(line[variable+1:-1])
            newTable[UFPk.getChars(line[:equal])]=[line[equal+1:variable], variableSize]
    tableFile.close()
    return newTable

def variableDump(rawInput, tableName, i, saveFile = True, nameFile = None):
    try:
        os.mkdir("Dumped Scripts")
    except:
        pass
    if nameFile == None:
        scriptName="script-%03d.txt" %i
    else:
        scriptName=nameFile

    try: f1=open("dumptemp.dat", "w+b")
    except: f1=open("dumptemp.dat", "wb")
    f1.write(rawInput)
    f1.seek(0)

    tableDictionary = UFPk.importTable(tableName)
    eightBitsTable, sixteenBitsTable = UFPk.stripTableSize(tableDictionary)
    variableTable = variableImportTable(tableName)
    eightBitsVariableTable, sixteenBitsVariableTable = UFPk.stripTableSize(variableTable)
    
    f2 = ""

    scriptSize = 0

    while scriptSize < len(rawInput):
        char = f1.read(1)
        scriptSize += 1
        if char in sixteenBitsVariableTable:
            try: char += f1.read(1)
            except: break
            scriptSize += 1
            if char in variableTable:
                try: variable = f1.read(variableTable[char][1])
                except: break
                f2 += UFPk.getChar(char, variableTable)[0]
                for i in range(len(variable)-1):
                    f2 += str(ord(variable[i])) + ","
                f2 += str(ord(variable[i+1]))
                f2 += ">"
                scriptSize += len(variable)
            else:
                if char[0] in eightBitsVariableTable:
                    f1.seek(-1, 1)
                    try: variable = f1.read(variableTable[char][1])
                    except: break
                    f2 += UFPk.getChar(char, variableTable)[0]
                    for i in range(len(variable)-1):
                        f2 += str(ord(variable[i])) + ","
                    f2 += str(ord(variable[i+1]))
                    f2 += ">"
                    scriptSize += len(variable)
                elif char[0] in sixteenBitsTable:
                    if char in tableDictionary:
                        f2 += UFPk.getChar(char, tableDictionary)
                    else:
                        if char in tableDictionary:
                            f2 += UFPk.getChar(char, tableDictionary)
                        elif char[0] in eightBitsTable:
                            f2 += UFPk.getChar((char[0]), tableDictionary)
                            f1.seek(-1, 1)
                            scriptSize -= 1
                        else:
                            f2 += ("[$" + hex(ord(char[0]))[2:] + "]")
                            f1.seek(-1, 1)
                            char = char[0]
                            scriptSize -= 1
                elif char[0] in eightBitsTable:
                    f2 += UFPk.getChar((char[0]), tableDictionary)
                    f1.seek(-1, 1)
                    scriptSize -= 1
                else:
                    f2 += ("[$" + hex(ord(char[0]))[2:] + "]")
                    f1.seek(-1, 1)
                    char = char[0]
                    scriptSize -= 1
        elif char in eightBitsVariableTable:
            try: variable = f1.read(variableTable[char][1])
            except: break
            f2 += UFPk.getChar(char, variableTable)[0]
            for i in range(len(variable)-1):
                f2 += str(ord(variable[i])) + ","
            f2 += str(ord(variable[-1]))
            f2 += ">"
            scriptSize += len(variable)
        elif char in sixteenBitsTable:
            try: char += f1.read(1)
            except: break
            scriptSize += 1
            if char in tableDictionary:
                f2 += UFPk.getChar(char, tableDictionary)
            else:
                if char[0] in eightBitsTable:
                    f2 += UFPk.getChar((char[0]), tableDictionary)
                    f1.seek(-1, 1)
                    scriptSize -= 1
                else:
                    f2 += ("[$" + hex(ord(char[0]))[2:] + "]")
                    f1.seek(-1, 1)
                    char = char[0]
                    scriptSize -= 1
        elif char in eightBitsTable:
            f2 += UFPk.getChar(char, tableDictionary)
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
