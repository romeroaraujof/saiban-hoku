# -*- coding: utf-8 -*-
# Saiban Roku - Phoenix Wright Script Editor - v. 4.0 Final
# 12/07/2009 - 25/05/2010
# Romero Gomes da Silva Araujo Filho
# Marvin Dalkiri - Monkey's Translations
# www.romhacking.trd.br / www.monkeystraducoes.com
# romeroaraujof@gmail.com

import UFPk
import UFPk.__develop__
reload(UFPk)

import os, os.path
import psyco
import time

psyco.full()

tableDictionary = UFPk.importTable("Phoenix Wright Table.tbl")

def main():
    print "Saiban Roku 裁判六 - Phoenix Wright Script Editor - v. 4.0 Final"
    print "Marvin Dalkiri - Monkey's"
    print "www.monkeystraducoes.com / www.romhacking.trd.br"
    print "romeroaraujof@gmail.com"
    condition=False
    while condition != True:
        print "\n\n\nEscolha sua opção:"
        choice=int(raw_input("\n1- Criar scripts\n\t2- Criar mes_all.dat\n\n"))
        choice, condition=UFPk.choice(1, 3, choice)
    if choice == 1:
        try:
            os.mkdir("Dumped Scripts")
        except:
            pass
        f=open("mes_all.bin", "rb")
        numberOfScripts=UFPk.invertPointers(f.read(4))
        scriptsPositions=[]
        scriptsSizes=[]
        for i in range(numberOfScripts):
            scriptsPositions.append(UFPk.invertPointers(f.read(4)))
            scriptsSizes.append(UFPk.invertPointers(f.read(4)))

        for i in range(numberOfScripts):
            f.seek(scriptsPositions[i])
            compressed = f.read(scriptsSizes[i])
            decompressed = UFPk.lzssUncompress(compressed)

            tempFile = open("temporary.dat", "w+b")
            tempFile.write(decompressed)
            tempFile.seek(0)
##            raw_input(i)
            scriptsInScript=UFPk.invertPointers(tempFile.read(4))
            finalScript = ""
            positionsScripts = []
            sizesScripts = []
            specialsScripts = []

            positionsScripts.append(UFPk.invertPointers(tempFile.read(4)))
            for j in range(scriptsInScript - 1):
                position = UFPk.invertPointers(tempFile.read(4))
                if position < os.path.getsize("temporary.dat"):
                    positionsScripts.append(position)
                    sizesScripts.append(positionsScripts[j + 1] - positionsScripts[j])
                else:
                    specialsScripts.append(UFPk.numberString(UFPk.createPointer(position, 4), True) + " ")
            sizesScripts.append(len(decompressed) - positionsScripts[-1])
##            print positionsScripts
##            print sizesScripts

            scriptName="script-%03d.txt" %i

            scriptText = open(os.path.join("Dumped Scripts", scriptName), "wb")

            for j in range(scriptsInScript - len(specialsScripts)):
                tempFile.seek(positionsScripts[j])
                thisScript = tempFile.read(sizesScripts[j])
                dumpedScript = UFPk.__develop__.variableDump(thisScript, "Phoenix Wright Table.tbl", j, saveFile = False)
                scriptText.write("\r\n\r\n{-----SCRIPT-----}\r\n\r\n")
##                scriptText.write("\r\n\r\n{-----SCRIPT-----} {" + str(j) +"}\r\n\r\n")
                scriptText.write(dumpedScript)
            scriptText.write("\r\n\r\n{-----SPECIAL-----}\r\n\r\n")
            scriptText.writelines(specialsScripts)
            scriptText.close()
            tempFile.close()
            os.unlink("temporary.dat")

            print "Script %03d dumpado com sucesso!".center(80) %(i)
        print "\n\nTodos os scripts foram dumpados! Aperte ENTER para sair.".center(80)
        raw_input()


    
    elif choice == 2:
        try:
            os.mkdir("Message Pack")
        except:
            pass
        scriptsFiles = UFPk.filesFolder("Dumped Scripts")
        mesAll = ""
        finalScript = ""

        positionsScripts=[]
        sizesScripts=[]

        for script in scriptsFiles: # cada script-XXX.txt
            f=open(os.path.join("Dumped Scripts", script), "rb")
            wholeScript = f.read()
            f.close()

            wholeScript, specialPart = wholeScript.split("{-----SPECIAL-----}")
            specialPart = UFPk.removeChars(specialPart, ["\r", "\n", "L", "l"])
            specialPart = specialPart.split(" ")[:-1]
            for i in range(len(specialPart)):
                specialPart[i] = UFPk.invertString(UFPk.createPointer(int("0x"+specialPart[i], 16), 4))
##            print specialPart
##            raw_input()

            scriptsInScript = wholeScript.count("{-----SCRIPT-----}") + len(specialPart)

            pointersOfScripts = []
            wholeScript = wholeScript.split("{-----SCRIPT-----}")
            for i in range(1, len(wholeScript)):
                tinyScript = wholeScript[i]
                if "<35:" in tinyScript:
                    scriptSize = len(UFPk.optimizeScript(tinyScript, tableDictionary, UFPk.importVariableTable("Phoenix Wright Table.tbl"), False)) - 8
                    tinyScript = tinyScript.split("<35:")
                    for k in range(1, len(tinyScript)):
                        end35 = tinyScript[k][:tinyScript[k].find(">")]
                        tinyScript[k] = tinyScript[k][len(end35)+1:]
                        end35 = end35.split(",")
                        end35[-1] = str(scriptSize/256)
                        end35[-2] = str(scriptSize%256)
                        end35 = ",".join(end35)
                        tinyScript[k] = end35 + ">" + tinyScript[k]
                    tinyScript = "<35:".join(tinyScript)
                tinyScript = UFPk.optimizeScript(tinyScript, tableDictionary, UFPk.importVariableTable("Phoenix Wright Table.tbl"), False)
                pointersOfScripts.append(UFPk.createPointer(len(finalScript) + 0x4 + 4*scriptsInScript, 4))
                finalScript+=tinyScript
            scriptsInScript = UFPk.createPointer(scriptsInScript, 4)

            g=open("tempscript.dat", "wb")
            g.write(scriptsInScript)
            g.writelines(pointersOfScripts)
            g.writelines(specialPart)
            g.write(finalScript)
            g.close()
            os.system("gbalzss.exe " + "e " + "tempscript.dat" + " " + "tempscriptnew.dat")
            g=open("tempscriptnew.dat", "rb")
            mesAllPart = g.read()
            g.close()

            positionVariable = 0x4 + 8*len(scriptsFiles)

            positionsScripts.append(UFPk.createPointer(len(mesAll) + positionVariable, 4))
            sizesScripts.append(UFPk.createPointer(len(mesAllPart), 4))

            mesAll += mesAllPart
            mesAll += (len(mesAll)%4)*"\x00"
            finalScript = ""
            os.unlink("tempscript.dat")
            os.unlink("tempscriptnew.dat")


        header = []
        header.append(UFPk.createPointer(len(scriptsFiles), 4))
        for i in range(len(positionsScripts)):
            header.append(positionsScripts[i])
            header.append(sizesScripts[i])

        print "\n\n%03d scripts lidos. O arquivo 'mes_all.bin' foi criado na pasta 'Message Pack'." %(len(scriptsFiles))
        messagePack=open(os.path.join("Message Pack", "mes_all.bin"), "wb")
        messagePack.write(UFPk.createPointer(len(scriptsFiles), 4))
        for i in range(len(positionsScripts)):
            messagePack.write(positionsScripts[i])
            messagePack.write(sizesScripts[i])
        messagePack.write(mesAll)
        messagePack.close()
        raw_input("Aperte ENTER para sair.".center(80))

    else:
        print "Escolha incorreta. O programa se fechará automaticamente..."

main()
