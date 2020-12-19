// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.


@8192 //set screen size
D=A
@size
M=D
@isblack
M=0
@MAIN_LOOP
0;JMP

(MAIN_LOOP)
    @KBD //check keyboard
    D=M
    @FILL_BLACK
    D;JGT
    @FILL_WHITE
    0;JMP

(FILL_WHITE)
    @isblack
    D=M
    @MAIN_LOOP
    D;JEQ
    @isblack
    M=0
    @color //color = <white>
    M=0
    @FILL
    0;JMP

(FILL_BLACK)
    @isblack
    D=M
    @MAIN_LOOP
    D;JNE
    @isblack
    M=1
    @color// color = <black>
    M=-1
    @FILL
    0;JMP

(FILL)
    @i
    M=0
    @FILL_LOOP
    0;JMP

(FILL_LOOP)
    @i //if i < size
    D=M
    @size
    D=M-D
    @MAIN_LOOP
    D;JEQ

    @SCREEN //screen[i] = color
    D=A
    @i
    D=D+M
    @addr
    M=D
    @color
    D=M
    @addr
    A=M
    M=D
    
    @i //i++
    D=M+1
    M=D
    @FILL_LOOP
    0;JMP