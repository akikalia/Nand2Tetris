#!/usr/bin/python3
import string
import sys

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

    def __writeBuff(self):
        self.outCode+="\n"
        self.file.write(self.outCode)
        self.outCode = ""

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

def main():
    if len(sys.argv) > 1:
        file = sys.argv[1]
        if file[len(file) - 3:] != ".vm":
            print("File format incorrect")
            sys.exit()
        vm = file
        asm = file[:len(file) - 3] + ".asm"
    else:
        print("Usage: python VMTranslator.py <filename.vm>")
        sys.exit()
    p = Parser(vm)
    cw = CodeWriter(asm)
    while p.hasMoreCommands():
        p.advance()
        currCmd = p.commandType()
        if currCmd == "C_ARITHMETIC":
            cw.writeArithmetic(p.arg1())
        elif currCmd == "C_PUSH" or currCmd == "C_POP" :
            cw.writePushPop(currCmd, p.arg1(), p.arg2())
        else :
            pass
    cw.Close()


if __name__ == "__main__":
  main()