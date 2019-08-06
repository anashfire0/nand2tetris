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

// Put your code here.

(PROBE)
    @KBD
    D=M
    @SCREEN
    D=D-M
    @PROBE
    D;JEQ

    @SCREEN
    D=A
    @start
    M=D
    
    @KBD
    D=A
    @end
    M=D

    @KBD
    D=M
    @SETBLACK
    D;JNE
    @black
    M=0
    @PAINT
    0;JMP

    (SETBLACK)
        @black
        M=-1
        @PAINT
        0;JMP


    (PAINT)
        @start
        D=M
        @end
        D=M-D
        @PROBE
        D;JEQ
        
        @black
        D=M

        @start
        A=M
        M=D

        @start
        M=M+1
        
        @PAINT
        0;JMP

