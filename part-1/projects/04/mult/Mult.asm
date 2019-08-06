@R2
M=0

@iterations
M=0

// if any of the number is zero, the output is zero
@R0
D=M
@SETZERO
D;JEQ

// if any of the number is zero, the output is zero
@R1
D=M
@SETZERO
D;JEQ

// preserve the signs of each number and make them positive
@R0
D=M
@STORESIGNR0
D;JLT

@signR0
M=1

(R1CODE)
    @R1
    D=M
    @STORESIGNR1
    D;JLT

    @signR1
    M=1

(MULT)
    @R0
    D=M

    @iterations
    D=D-M
    @RESTORESIGN
    D;JEQ

    @R1
    D=M
    @R2
    D=D+M
    M=D

    @iterations
    D=M
    D=D+1
    M=D

    @MULT
    0;JMP

(SETZERO)
    @R2
    M=0
    @END
    0;JMP

(END)
    @END
    0;JMP

(STORESIGNR0)
    @signR0
    M=-1
    @R0
    M=-M
    @R1CODE
    0;JMP

(STORESIGNR1)
    @signR1
    M=-1
    @R1
    M=-M
    @MULT
    0;JMP

(RESTORESIGN)
    @signR0
    D=M
    @signR1
    D=D+M
    @MAKENEGATIVE
    D;JEQ
    @END
    0;JMP

(MAKENEGATIVE)
    @R2
    M=-M
    @END
    0;JMP





