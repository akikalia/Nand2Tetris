// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

//for(i = 0 ; i < r1; i++ )
//  r0 = r0+ r0

@i
M=1

@res
M=0

@LOOP
0;JMP

(LOOP)
    @i
    D=M
    @R1
    D=D-M
    @STOP
    D;JGT
    //res+=R0
    @res
    D=M
    @R0
    D=D+M
    @res
    M=D
    //i++
    @i
    D=M
    D=D+1
    M=D
    @LOOP
    0;JMP


(STOP)
    @res
    D=M
    @R2
    M=D
    //goto end
    @END
    0;JMP

(END)
    @END
    0;JMP