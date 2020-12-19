#!/usr/bin/python3
import string
import sys
import os
import re
import time


class JackTokenizer:
    symbols_re = r'[\{\}\(\)\[\]\.\,\;\+\-\*\/\&\<\>\=\~\|]'
    keywords_re = r'class|constructor|function|method|field|static|var|int|char|boolean|void|true|false|null|this|let|do|if|else|while|return'
    string_const_re = r'"[^"\n]*"'
    int_const_re = r"\d+"
    ident_re = r"[^\d\W]\w*"


    def __init__(self, input):
        self.file = open(input , "r")
        rawFile = self.file.read()
        self.file.close()
        self.tokens = self.__parse(rawFile)
        self.size = len(self.tokens)
        self.curr = -1

    def __parse(self, content):
        content = self.__removeSegments(content, '/*', '*/', False)
        content = self.__removeSegments(content, '//', '\n', False)
        search = re.compile(self.symbols_re + '|'+ self.keywords_re +'|'+ self.string_const_re +'|'+ self.int_const_re+'|'+ self.ident_re)
        return search.findall(content)


    def __removeSegments(self, content, strA, strB, keepEnd):
        while strA in content:
            beg = content.find(strA)
            temp = content[:beg] 
            temp = temp + content[content.find(strB, beg) + len(strB) - int(keepEnd):]
            content = temp
        return content

    def hasMoreTokens(self):
        if self.curr == self.size - 1:
            return False
        return True

    def advance(self):
        self.curr += 1

    def peekTokenType(self):
        return self.__type(self.tokens[self.curr+1])

    def peek(self):
        return self.tokens[self.curr + 1]

    def tokenType(self):
        return self.__type(self.tokens[self.curr])


    def __type(self, str):
        if re.match(self.symbols_re, str) :
            return "symbol"
        elif re.match(self.keywords_re, str):
            return "keyword"
        elif re.match(self.ident_re, str):
            return "identifier"
        elif re.match(self.int_const_re, str) and int(str) >= 0 and int(str) <= 32767:
            return "integerConstant"
        elif re.match(self.string_const_re, str):
            return "stringConstant"
        else:
            return ""

    def getVal(self):
        return self.tokens[self.curr]

    def keyword(self):
        return self.tokens[self.curr]

    def symbol(self):
        return self.tokens[self.curr]

    def identifier(self):
        return self.tokens[self.curr]
    
    def intVal(self):
        return self.tokens[self.curr]

    def stringVal(self):
        return self.tokens[self.curr]



class CompilationEngine:
    ops = ['+','-','*','/','&','|','<','>','=']
    subs = {"<" : "&lt;", ">" : "&gt;", "&" : "&amp;", "\"": "&quot;",}

    def __init__(self, input, output):
        self.tk = JackTokenizer(input)
        self.out = open(output, "w+")
        self.buffer = ''
        self.globalSpaces = 0
        if self.tk.hasMoreTokens():
            self.tk.advance()


    def __writeFile(self):
        self.out.write(self.buffer)
        self.buffer = ''

    #check if correct type is followed in the structure, and write appropriate command to file
    def __compile(self, type, value=""):
        assert(self.tk.tokenType() == type)
        if value:
            assert value == self.tk.getVal()
        tagCont = self.tk.getVal()
        if (type == "stringConstant"):
            tagCont = tagCont[1:-1]
        elif tagCont in self.subs:
            tagCont = self.subs[tagCont]
        self.__tag(type, tagCont)
        if self.tk.hasMoreTokens():
            self.tk.advance()
        self.__writeFile()

    def __space(self):
        return ('  ' * self.globalSpaces)

    def __tag(self, tagname, content):
        self.buffer += self.__space() +'<'+tagname+'> '+content+' </'+tagname+'>\n'

    def __open(self,tagname):
        self.buffer += self.__space() + '<'+tagname+'>\n'
        self.globalSpaces += 1

    def __close(self, tagname):
        self.globalSpaces -= 1
        self.buffer += self.__space() + '</'+tagname+'>\n'

    def compileClass(self):
        self.__open("class")
        self.__compile("keyword","class")
        self.__compile("identifier")
        self.__compile("symbol", '{')
        while self.tk.tokenType() == "keyword" and self.tk.keyword() in ['static', 'field']:
            self.compileClassVarDec()
        while self.tk.tokenType() == "keyword" and self.tk.keyword() in ['constructor', 'function', 'method']:
            self.compileSubroutineDec()
        self.__compile("symbol", '}')
        self.__close("class")
        self.__writeFile()


    def compileClassVarDec(self):
        self.__open("classVarDec")
        self.__compile("keyword")
        self.__compileType(False)
        self.__compile("identifier")
        while self.tk.tokenType() == "symbol" and self.tk.symbol() == ',':
            self.__compile("symbol")
            self.__compile("identifier")
        self.__compile("symbol", ';')        
        self.__close("classVarDec")



    def __compileType(self, includeVoid):
        types = ['boolean', 'char', 'int']
        if self.tk.tokenType() == "keyword" and self.tk.keyword() in types or (self.tk.keyword() == 'void' and includeVoid):
            self.__compile("keyword")
        else:
            self.__compile("identifier")
        

    def compileSubroutineDec(self):
        self.__open("subroutineDec")        
        self.__compile("keyword")
        self.__compileType(True)
        self.__compile("identifier")
        self.__compile("symbol", '(')
        self.compileParameterList()
        self.__compile("symbol", ')')
        self.compileSubroutineBody()
        self.__close("subroutineDec")

    def compileParameterList(self):
        self.__open("parameterList")
        if self.tk.tokenType() == "keyword":    
            self.__compileType(False)
            self.__compile("identifier")
            while self.tk.tokenType() == "symbol" and self.tk.symbol() == ',':
                self.__compile("symbol")
                self.__compileType(False)
                self.__compile("identifier")
        self.__close("parameterList")
        

    def compileSubroutineBody(self):
        self.__open("subroutineBody")
        self.__compile("symbol", '{')
        while self.tk.tokenType() == "keyword" and self.tk.keyword() == "var":
            self.compileVarDec()
        self.compileStatements()
        self.__compile("symbol", '}')
        self.__close("subroutineBody")

    def compileVarDec(self):
        self.__open("varDec")
        self.__compile("keyword", 'var')
        self.__compileType(False)
        self.__compile("identifier")
        while self.tk.tokenType() == "symbol" and self.tk.symbol() == ',':
            self.__compile("symbol")
            self.__compile("identifier")
        self.__compile("symbol", ';')
        self.__close("varDec")


    def compileStatements(self):
        self.__open("statements")
        keyword = self.tk.keyword()
        while self.tk.tokenType() == "keyword" and keyword in ['let', 'if', 'while', 'do', 'return']:
            if keyword == 'while':
                self.compileWhile()
            elif keyword  == 'if':
                self.compileIf()
            elif keyword  == 'let':
                self.compileLet()
            elif keyword  == 'do':
                self.compileDo()
            elif keyword  == 'return':
                self.compileReturn()
            keyword = self.tk.keyword()
        self.__close("statements")


    def compileLet(self):
        self.__open("letStatement")
        self.__compile("keyword", 'let')
        self.__compile("identifier")
        if self.tk.tokenType() == "symbol" and self.tk.symbol() == '[':
            self.__compile("symbol", '[')
            self.compileExpression()
            self.__compile("symbol", ']')
        self.__compile("symbol", '=')
        self.compileExpression()
        self.__compile("symbol", ';')
        self.__close("letStatement")

    def compileIf(self):
        self.__open("ifStatement")
        self.__compile("keyword", 'if')
        self.__compile("symbol", '(')
        self.compileExpression()
        self.__compile("symbol", ')')
        self.__compile("symbol", '{')
        self.compileStatements()
        self.__compile("symbol", '}')
        if self.tk.tokenType() == "keyword" and self.tk.keyword() == 'else':
            self.__compile("keyword", 'else')
            self.__compile("symbol", '{')
            self.compileStatements()
            self.__compile("symbol", '}')
        self.__close("ifStatement")

    def compileWhile(self):
        self.__open("whileStatement")
        self.__compile("keyword", 'while')
        self.__compile("symbol", '(')
        self.compileExpression()
        self.__compile("symbol", ')')
        self.__compile("symbol", '{')
        self.compileStatements()
        self.__compile("symbol", '}')
        self.__close("whileStatement")

    def compileDo(self):
        self.__open("doStatement")
        self.__compile("keyword", 'do')
        self.__subroutineCall()
        self.__compile("symbol", ';')
        self.__close("doStatement")

    def compileReturn(self):
        self.__open("returnStatement")
        self.__compile("keyword", 'return')
        if not (self.tk.tokenType() == "symbol" and self.tk.getVal() == ';'):
            self.compileExpression()
        self.__compile("symbol", ';')
        self.__close("returnStatement")

    def compileExpression(self):
        self.__open("expression")
        self.compileTerm()
        while self.tk.tokenType() == "symbol" and self.tk.symbol() in self.ops:
            self.__compile("symbol")
            self.compileTerm()
        self.__close("expression")

    def __subroutineCall(self):
        self.__compile("identifier")
        if self.tk.tokenType() == "symbol" and self.tk.symbol() == '.':
            self.__compile("symbol")
            self.__compile("identifier")
        self.__compile("symbol", '(')
        self.compileExpressionList()
        self.__compile("symbol", ')')

    def compileTerm(self):
        self.__open("term")
        type = self.tk.tokenType()
        if type == "keyword":
            if self.tk.keyword() in ['true','false','null','this']:
                self.__compile("keyword")
        elif type == "symbol":
            if self.tk.symbol() in ['-','~']:
                self.__compile("symbol")
                self.compileTerm()
            elif self.tk.symbol() == '(':
                self.__compile("symbol")
                self.compileExpression()
                self.__compile("symbol", ')')
        elif type == "identifier":
            if self.tk.peekTokenType() == "symbol" and self.tk.peek() in ['(','.']:
                self.__subroutineCall()
            else:
                self.__compile("identifier")
                if self.tk.tokenType() == "symbol" and self.tk.symbol() == '[':
                    self.__compile("symbol")
                    self.compileExpression()
                    self.__compile("symbol", ']')
        elif type == "integerConstant":
            self.__compile("integerConstant")
        elif type == "stringConstant":
            self.__compile("stringConstant")
        self.__close("term")

    def compileExpressionList(self):
        self.__open("expressionList")
        if not (self.tk.tokenType() == "symbol" and self.tk.symbol() == ')'):
            self.compileExpression()
        while self.tk.tokenType() == "symbol" and self.tk.symbol() == ',':
            self.__compile("symbol")
            self.compileExpression()
        self.__close("expressionList")

        
def compileFile(filename):
    if filename[-4:] == "jack": 
        ce = CompilationEngine(filename, filename[:-4] + "xml")
        ce.compileClass()
    
def main():
    numArgs = len(sys.argv)
    for i in range(1, numArgs):
        file = sys.argv[i]
        if os.path.isdir(file):
            entries = os.listdir(file)
            if (file[-1] != '/'):
                file += '/'
            for entry in entries:
                compileFile(file + entry)
        else:
            compileFile(file)
        
if __name__ == "__main__":
  main()