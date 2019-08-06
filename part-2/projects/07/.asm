// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1

// eq
@SP
M=M-1
@SP
A=M
D=M
@R13
M=D
@SP
M=M-1
@SP
A=M
D=M
@R14
M=D
@R13
D=M
@R14
D=D-M
@EQ
D;JEQ
@SP
A=M
M=0
@NEXT
0;JMP
(EQ)
@SP
A=M
M=-1
(NEXT)
@SP
M=M+1

