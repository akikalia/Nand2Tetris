@17
D=A
@SP
A=M
M=D
@SP
M=M+1

@17
D=A
@SP
A=M
M=D
@SP
M=M+1

@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@CMP0
D;JEQ
D=0
@CMP_END0
0;JMP
(CMP0)
D=-1
@CMP_END0
0;JMP
(CMP_END0)
@SP
A=M
M=D
@SP
M=M+1

@17
D=A
@SP
A=M
M=D
@SP
M=M+1

@16
D=A
@SP
A=M
M=D
@SP
M=M+1

@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@CMP1
D;JEQ
D=0
@CMP_END1
0;JMP
(CMP1)
D=-1
@CMP_END1
0;JMP
(CMP_END1)
@SP
A=M
M=D
@SP
M=M+1

@16
D=A
@SP
A=M
M=D
@SP
M=M+1

@17
D=A
@SP
A=M
M=D
@SP
M=M+1

@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@CMP2
D;JEQ
D=0
@CMP_END2
0;JMP
(CMP2)
D=-1
@CMP_END2
0;JMP
(CMP_END2)
@SP
A=M
M=D
@SP
M=M+1

@892
D=A
@SP
A=M
M=D
@SP
M=M+1

@891
D=A
@SP
A=M
M=D
@SP
M=M+1

@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@CMP3
D;JLT
D=0
@CMP_END3
0;JMP
(CMP3)
D=-1
@CMP_END3
0;JMP
(CMP_END3)
@SP
A=M
M=D
@SP
M=M+1

@891
D=A
@SP
A=M
M=D
@SP
M=M+1

@892
D=A
@SP
A=M
M=D
@SP
M=M+1

@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@CMP4
D;JLT
D=0
@CMP_END4
0;JMP
(CMP4)
D=-1
@CMP_END4
0;JMP
(CMP_END4)
@SP
A=M
M=D
@SP
M=M+1

@891
D=A
@SP
A=M
M=D
@SP
M=M+1

@891
D=A
@SP
A=M
M=D
@SP
M=M+1

@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@CMP5
D;JLT
D=0
@CMP_END5
0;JMP
(CMP5)
D=-1
@CMP_END5
0;JMP
(CMP_END5)
@SP
A=M
M=D
@SP
M=M+1

@32767
D=A
@SP
A=M
M=D
@SP
M=M+1

@32766
D=A
@SP
A=M
M=D
@SP
M=M+1

@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@CMP6
D;JGT
D=0
@CMP_END6
0;JMP
(CMP6)
D=-1
@CMP_END6
0;JMP
(CMP_END6)
@SP
A=M
M=D
@SP
M=M+1

@32766
D=A
@SP
A=M
M=D
@SP
M=M+1

@32767
D=A
@SP
A=M
M=D
@SP
M=M+1

@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@CMP7
D;JGT
D=0
@CMP_END7
0;JMP
(CMP7)
D=-1
@CMP_END7
0;JMP
(CMP_END7)
@SP
A=M
M=D
@SP
M=M+1

@32766
D=A
@SP
A=M
M=D
@SP
M=M+1

@32766
D=A
@SP
A=M
M=D
@SP
M=M+1

@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@CMP8
D;JGT
D=0
@CMP_END8
0;JMP
(CMP8)
D=-1
@CMP_END8
0;JMP
(CMP_END8)
@SP
A=M
M=D
@SP
M=M+1

@57
D=A
@SP
A=M
M=D
@SP
M=M+1

@31
D=A
@SP
A=M
M=D
@SP
M=M+1

@53
D=A
@SP
A=M
M=D
@SP
M=M+1

@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=D+M
@SP
A=M
M=D
@SP
M=M+1

@112
D=A
@SP
A=M
M=D
@SP
M=M+1

@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@SP
A=M
M=D
@SP
M=M+1

@SP
M=M-1
A=M
D=M
D=-D
@SP
A=M
M=D
@SP
M=M+1

@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M&D
@SP
A=M
M=D
@SP
M=M+1

@82
D=A
@SP
A=M
M=D
@SP
M=M+1

@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M|D
@SP
A=M
M=D
@SP
M=M+1

@SP
M=M-1
A=M
D=M
D=!D
@SP
A=M
M=D
@SP
M=M+1

