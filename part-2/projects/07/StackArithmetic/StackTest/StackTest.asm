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
@EQ1
D;JEQ
@SP
A=M
M=0
@NEXT1
0;JMP
(EQ1)
@SP
A=M
M=-1
(NEXT1)
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

// push constant 16
@16
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
@EQ2
D;JEQ
@SP
A=M
M=0
@NEXT2
0;JMP
(EQ2)
@SP
A=M
M=-1
(NEXT2)
@SP
M=M+1

// push constant 16
@16
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
@EQ3
D;JEQ
@SP
A=M
M=0
@NEXT3
0;JMP
(EQ3)
@SP
A=M
M=-1
(NEXT3)
@SP
M=M+1

// push constant 892
@892
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1

// lt
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
D=M-D
@R14LT4
D;JLT
@SP
A=M
M=0
@NEXT4
0;JMP
(R14LT4)
@SP
A=M
M=-1
(NEXT4)
@SP
M=M+1

// push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 892
@892
D=A
@SP
A=M
M=D
@SP
M=M+1

// lt
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
D=M-D
@R14LT5
D;JLT
@SP
A=M
M=0
@NEXT5
0;JMP
(R14LT5)
@SP
A=M
M=-1
(NEXT5)
@SP
M=M+1

// push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1

// lt
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
D=M-D
@R14LT6
D;JLT
@SP
A=M
M=0
@NEXT6
0;JMP
(R14LT6)
@SP
A=M
M=-1
(NEXT6)
@SP
M=M+1

// push constant 32767
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1

// gt
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
D=M-D
@R14GT7
D;JGT
@SP
A=M
M=0
@NEXT7
0;JMP
(R14GT7)
@SP
A=M
M=-1
(NEXT7)
@SP
M=M+1

// push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 32767
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1

// gt
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
D=M-D
@R14GT8
D;JGT
@SP
A=M
M=0
@NEXT8
0;JMP
(R14GT8)
@SP
A=M
M=-1
(NEXT8)
@SP
M=M+1

// push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1

// gt
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
D=M-D
@R14GT9
D;JGT
@SP
A=M
M=0
@NEXT9
0;JMP
(R14GT9)
@SP
A=M
M=-1
(NEXT9)
@SP
M=M+1

// push constant 57
@57
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 31
@31
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 53
@53
D=A
@SP
A=M
M=D
@SP
M=M+1

// add
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
D=D+M
@SP
A=M
M=D
@SP
M=M+1

// push constant 112
@112
D=A
@SP
A=M
M=D
@SP
M=M+1

// sub
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
D=M-D
@SP
A=M
M=D
@SP
M=M+1

// neg
@SP
M=M-1
@SP
A=M
D=M
@R13
M=D
@R13
D=-M
@SP
A=M
M=D
@SP
M=M+1

// and
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
D=D&M
@SP
A=M
M=D
@SP
M=M+1

// push constant 82
@82
D=A
@SP
A=M
M=D
@SP
M=M+1

// or
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
D=D|M
@SP
A=M
M=D
@SP
M=M+1

// not
@SP
M=M-1
@SP
A=M
D=M
@R13
M=D
@R13
D=!M
@SP
A=M
M=D
@SP
M=M+1

