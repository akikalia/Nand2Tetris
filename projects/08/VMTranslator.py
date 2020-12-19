#!/usr/bin/python3
import string
import sys
import os

class Parser:

    def __init__(self, inFile):
        self.file = open(inFile , "r")
        self.nextLine = self.__getParsedLine()
        self.cmds = {
             "push": "C_PUSH",
             "pop":"C_POP",
             "label": "C_LABEL", 
             "goto":"C_GOTO",
             "if-goto":"C_IF",
             "return":"C_RETURN",
             "function":"C_FUNCTION",
             "call":"C_CALL"
        }

    def __getParsedLine(self):
        line = self.file.readline()
        if not line:
            return line.split()
        line = line[:line.find('//')]
        line = line.strip()
        if not line:
            return self.__getParsedLine()
        return line.split()

    #checks file for more commands    
    def hasMoreCommands(self):
        if not self.nextLine:
            return False
        return True

    #should be  called if hasmorecommands true
    #makes current comand equal to next
    def advance(self):
        self.currentLine = self.nextLine
        self.nextLine = self.__getParsedLine()        
        self.type = self.cmds.get(self.currentLine[0], "C_ARITHMETIC")
        if not self.nextLine:
            self.file.close()
        

    #returns type of operation constant
    def commandType(self):
       return self.type
        

    #should not be caled for return
    def arg1(self):
        if self.type == "C_ARITHMETIC":
            return self.currentLine[0]
        else:
            return self.currentLine[1]

    #should be called for push pop function call
    def arg2(self):
        return int(self.currentLine[2])
    


class CodeWriter:
    #receives output file stream
    #opens it and writes into it
    def __init__(self, outFile):
        self.fileName = outFile[outFile.rfind("/")+1:len(outFile)-4]
        self.file = open(outFile , "w+")
        self.outCode = ""
        self.cmpNum = 0
        self.retNum = 1#label generation for function return 
        self.currFunc = ""#label generation for function return 



    def setFileName(self, name):
        self.fileName = name[name.rfind("/")+1:]
        self.retNum = 1

    def __writeBuff(self):
        self.file.write(self.outCode)
        self.outCode = ""
    
    def writeInit(self):
        ##
        # ##
        self.outCode +="@256\n"
        self.outCode +="D=A\n"
        self.outCode +="@SP\n"
        self.outCode +="M=D\n"
        self.writeCall("Sys.init", 0)

    def __label(self, label):
        self.outCode +="("+label+")\n"

    def writeLabel(self, label):
        self.__label(self.currFunc+"$"+label)
        self.__writeBuff()

    def __goto(self, label):
        self.outCode +="@"+label+"\n"
        self.outCode +="0;JMP\n"

    def writeGoto(self, label):
        self.__goto(self.currFunc+"$"+label)
        self.__writeBuff()

    def __if(self, label):
        self.__pop(True)
        self.outCode +="@"+self.currFunc+"$"+label+"\n"
        self.outCode +="D;JNE\n"

    def writeIf(self, label):
        self.__if(label)
        self.__writeBuff()

    def writeFunction(self, name, numVars):
        self.currFunc = name
        self.__label(name)##############################
        self.outCode +="D=0\n"
        for i in range(0,numVars):
            self.__push()
        self.__writeBuff()


    def writeCall(self, name, numArgs):
        ##
        ##
        #generate label
        ret = self.fileName + "$ret." + str(self.retNum)
        self.retNum+=1
        self.outCode +="@"+ret+"\n"
        self.outCode +="D=A\n"
        self.__push()
        self.outCode +="@LCL\n"
        self.outCode +="D=M\n"
        self.__push()
        self.outCode +="@ARG\n"
        self.outCode +="D=M\n"
        self.__push()
        self.outCode +="@THIS\n"
        self.outCode +="D=M\n"
        self.__push()
        self.outCode +="@THAT\n"
        self.outCode +="D=M\n"
        self.__push()
        self.outCode +="@SP\n"
        self.outCode +="D=M\n"
        self.outCode +="@5\n"
        self.outCode +="D=D-A\n"
        self.outCode +="@"+str(numArgs)+"\n"
        self.outCode +="D=D-A\n"
        self.outCode +="@ARG\n"
        self.outCode +="M=D\n"
        self.outCode +="@SP\n"
        self.outCode +="D=M\n"
        self.outCode +="@LCL\n"
        self.outCode +="M=D\n"
        self.__goto(name)##############################################
        self.__label(ret)#write generated label #########################
        self.__writeBuff()

    def __endframeMinus(self):
        self.outCode +="@R13\n"
        self.outCode +="M=M-1\n"
        self.outCode +="A=M\n"
        self.outCode +="D=M\n"

    def writeReturn(self):
        ##
        ##
        #endframe = LCL
        self.outCode +="@LCL\n"
        self.outCode +="D=M\n"
        self.outCode +="@R13\n"##endFrame
        self.outCode +="M=D\n"
        #retaddr = *(endframe - 5)
        #endframe - 5
        self.outCode +="@5\n"
        self.outCode +="D=D-A\n"
        #D=*endframe
        self.outCode +="A=D\n"
        self.outCode +="D=M\n"
        self.outCode +="@R14\n"##retAddr
        self.outCode +="M=D\n"
        #*ARG = POP()
        self.__pop(True)
        self.outCode +="@ARG\n"
        self.outCode +="A=M\n"
        self.outCode +="M=D\n"
        #sp = ARG + 1
        self.outCode +="D=A+1\n"
        self.outCode +="@SP\n"
        self.outCode +="M=D\n"
        #D = endframe - 1
        self.__endframeMinus()
        self.outCode +="@THAT\n"
        self.outCode +="M=D\n"
        self.__endframeMinus()
        self.outCode +="@THIS\n"
        self.outCode +="M=D\n"
        self.__endframeMinus()
        self.outCode +="@ARG\n"
        self.outCode +="M=D\n"
        self.__endframeMinus()
        self.outCode +="@LCL\n"
        self.outCode +="M=D\n"
        self.outCode +="@R14\n"##retAddr
        self.outCode +="A=M\n"
        self.outCode +="0;JMP\n"
        self.__writeBuff()

    #receives a string, writes implementation of arithmetic command
    def writeArithmetic(self, command):
        self.__pop(True)
        if command == "add":
            self.__pop(False)
            self.outCode +="D=D+M\n"
        elif command == "sub":
            self.__pop(False)
            self.outCode +="D=M-D\n"
        elif command == "neg":
            self.outCode +="D=-D\n"
        elif command in ["eq", "gt", "lt"]:
            cmpNumStr = str(self.cmpNum)
            self.__pop(False)
            self.outCode +="D=M-D\n"
            self.outCode +="@CMP"+cmpNumStr+"\n"
            self.outCode +="D;J"+command.upper()+"\n"
            self.outCode +="D=0\n"
            self.outCode +="@CMP_END"+cmpNumStr+"\n"
            self.outCode +="0;JMP\n"
            self.outCode +="(CMP"+cmpNumStr+")\n"
            self.outCode +="D=-1\n"
            self.outCode +="@CMP_END"+cmpNumStr+"\n"
            self.outCode +="0;JMP\n"
            self.outCode +="(CMP_END"+cmpNumStr+")\n"
            self.cmpNum+=1
        elif command == "and":
            self.__pop(False)
            self.outCode +="D=M&D\n"
        elif command == "or":
            self.__pop(False)
            self.outCode +="D=M|D\n"
        elif command == "not":
            self.outCode +="D=!D\n"
        self.__push()
        self.__writeBuff()


    def __pointer(self, command, i):
        if i == 0:
            seg = "THIS"
        else:
            seg = "THAT"
        if command == "C_PUSH":
            self.outCode +="@"+seg+"\n"
            self.outCode +="D=M\n"
            self.__push()
        elif command == "C_POP":
            self.__pop(True)
            self.outCode +="@"+seg+"\n"
            self.outCode +="M=D\n"

    #local, arg, this, that, temp

    def __push(self):
        #*sp = D
        self.outCode +="@SP\n"
        self.outCode +="A=M\n"
        self.outCode +="M=D\n"
        #SP++
        self.outCode +="@SP\n"
        self.outCode +="M=M+1\n"

    def __pop(self, resetD):
        #sp--
        self.outCode +="@SP\n"
        self.outCode +="M=M-1\n"
        #D = *sp
        self.outCode +="A=M\n"
        if resetD:
            self.outCode +="D=M\n"


    def __lat(self, command, segment, i):
        #addr = <segment> + <i>
        if segment != "5":
            self.outCode +="@"+segment+"\n"
            self.outCode +="D=M\n"
        else:
            self.outCode +="@5\n"
            self.outCode +="D=A\n"
        self.outCode +="@"+i+"\n"
        self.outCode +="D=D+A\n"
        if (command == "C_PUSH"):
            #D = *addr
            self.outCode +="A=D\n"
            self.outCode +="D=M\n"
            self.__push();     
        else:
            #addr = D
            self.outCode +="@R13\n"
            self.outCode +="M=D\n"
            self.__pop(True)
            #*sp = *addr
            self.outCode +="@R13\n"
            self.outCode +="A=M\n"
            self.outCode +="M=D\n"
    
    def __constant(self, i):
        #D = i
        self.outCode +="@"+i+"\n"
        self.outCode +="D=A\n"
        self.__push()

    def __static(self, command, i):
        if command == "C_POP":
            self.__pop(True)
            self.outCode +="@"+self.fileName+"."+i+"\n"
            self.outCode +="M=D\n"
        else:
            self.outCode +="@"+self.fileName+"."+i+"\n"
            self.outCode +="D=M\n"
            self.__push()

        

    #command : C_PUSH/C_POP, segment: string, index: int 
    def writePushPop(self, command, segment, index ):
        i = str(index)
        if segment == "constant" and command == "C_PUSH":
            self.__constant(i)
        elif segment == "argument":
            self.__lat(command, "ARG", i)
        elif segment == "this":
            self.__lat(command, "THIS", i)
        elif segment == "that":
            self.__lat(command, "THAT", i)
        elif segment == "local":
            self.__lat(command, "LCL", i)
        elif segment == "static":
            self.__static(command, i)
        elif segment == "temp":
            self.__lat(command, "5", i)
        elif segment == "pointer":
            self.__pointer(command, index)
        self.__writeBuff()

        
    #closes outFIle
    def Close(self):
        self.file.close()


def getFiles(file, vms):
    if file[len(file) - 3:] == ".vm":
        vms.append(file)
        return file
    elif os.path.isdir(file):
        entries = os.listdir(file)
        if file[len(file)-1] == "/":
            file = file[:len(file)-1]
        for entry in entries:
            #print(entry)
            if entry[len(entry) - 3:] == ".vm":
                vms.append(file+"/"+entry)
        file = file+"/"+ file[file.rfind("/")+1:]
        return file
    else:
        print("File format incorrect")
        sys.exit()

def main():
    numArgs = len(sys.argv)
    for i in range(1, numArgs):
        vms = []
        oldFile = sys.argv[1]
        isDir = True
        file = getFiles(oldFile, vms)
        if file == oldFile:
            isDir = False
        if isDir:
            print(file)
            cw = CodeWriter(file + ".asm")
            if len(vms) > 1:
                cw.writeInit()
        for vm in vms:
            p = Parser(vm)
            if not isDir:
                cw = CodeWriter(vm[:len(vm) - 3] + ".asm")
            else:
                cw.setFileName(vm[:len(vm) - 3])
            while p.hasMoreCommands():
                p.advance()
                currCmd = p.commandType()
                if currCmd == "C_ARITHMETIC":
                    cw.writeArithmetic(p.arg1())
                elif currCmd == "C_PUSH" or currCmd == "C_POP" :
                    cw.writePushPop(currCmd, p.arg1(), p.arg2())
                elif currCmd == "C_LABEL":
                    cw.writeLabel(p.arg1())
                elif currCmd == "C_GOTO":
                    cw.writeGoto(p.arg1())
                elif currCmd == "C_RETURN":
                    cw.writeReturn()
                elif currCmd == "C_FUNCTION":
                    cw.writeFunction(p.arg1(),p.arg2() )
                elif currCmd == "C_CALL":
                    cw.writeCall(p.arg1(), p.arg2())
                elif currCmd == "C_IF":
                    cw.writeIf(p.arg1())
            if not isDir:
                cw.Close()
        if isDir:
            cw.Close()

if __name__ == "__main__":
  main()