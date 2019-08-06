// Initialization
@261
D=A
@SP
M=D
// function Sys.init 0
(Sys.init)

// push constant 4
@4
D=A
@SP
A=M
M=D
@SP
M=M+1

// call Main.fibonacci 1
// saving Main.fibonacciret$1
@Main.fibonacciret$1
D=A
@SP
A=M
M=D
@SP
M=M+1
// saving LCL
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
// saving ARG
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
// saving THIS
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
// saving THAT
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
// reinitializing ARG
@5
D=A
@R13
M=D
@1
D=A
@R14
M=D
@SP
D=M
@R13
D=D-M
@R14
D=D-M
@ARG
M=D
// reinitializing LCL
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
// returning point fMain.fibonacci
(Main.fibonacciret$1)

// label WHILE
(WHILE)

// goto WHILE
@WHILE
0;JMP

// function Main.fibonacci 0
(Main.fibonacci)

// push argument 0
@ARG
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1

// push constant 2
@2
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
@R14LT2
D;JLT
@SP
A=M
M=0
@NEXT2
0;JMP
(R14LT2)
@SP
A=M
M=-1
(NEXT2)
@SP
M=M+1

// if-goto IF_TRUE
@SP
M=M-1
@SP
A=M
D=M
@IF_TRUE
D;JNE

// goto IF_FALSE
@IF_FALSE
0;JMP

// label IF_TRUE
(IF_TRUE)

// push argument 0
@ARG
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1

// return
// set endframe
@LCL
D=M
@R13
M=D
// saving return addr to temp
@5
D=A
@R13
D=M-D
A=D
D=M
@R14
M=D
// return value to arg
@SP
M=M-1
@0
D=A
@ARG
D=D+M
@R15
M=D
@SP
A=M
D=M
@R15
A=M
M=D
// reposition SP
@ARG
D=M+1
@SP
M=D
// reposition THIS
@2
D=A
@R13
D=M-D
A=D
D=M
@THIS
M=D
// reposition THAT
@1
D=A
@R13
D=M-D
A=D
D=M
@THAT
M=D
// reposition ARG
@3
D=A
@R13
D=M-D
A=D
D=M
@ARG
M=D
// reposition LCL
@4
D=A
@R13
D=M-D
A=D
D=M
@LCL
M=D
// return to caller
@R14
A=M
0;JMP

// label IF_FALSE
(IF_FALSE)

// push argument 0
@ARG
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1

// push constant 2
@2
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

// call Main.fibonacci 1
// saving Main.fibonacciret$3
@Main.fibonacciret$3
D=A
@SP
A=M
M=D
@SP
M=M+1
// saving LCL
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
// saving ARG
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
// saving THIS
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
// saving THAT
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
// reinitializing ARG
@5
D=A
@R13
M=D
@1
D=A
@R14
M=D
@SP
D=M
@R13
D=D-M
@R14
D=D-M
@ARG
M=D
// reinitializing LCL
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
// returning point fMain.fibonacci
(Main.fibonacciret$3)

// push argument 0
@ARG
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1

// push constant 1
@1
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

// call Main.fibonacci 1
// saving Main.fibonacciret$4
@Main.fibonacciret$4
D=A
@SP
A=M
M=D
@SP
M=M+1
// saving LCL
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
// saving ARG
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
// saving THIS
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
// saving THAT
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
// reinitializing ARG
@5
D=A
@R13
M=D
@1
D=A
@R14
M=D
@SP
D=M
@R13
D=D-M
@R14
D=D-M
@ARG
M=D
// reinitializing LCL
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
// returning point fMain.fibonacci
(Main.fibonacciret$4)

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

// return
// set endframe
@LCL
D=M
@R13
M=D
// saving return addr to temp
@5
D=A
@R13
D=M-D
A=D
D=M
@R14
M=D
// return value to arg
@SP
M=M-1
@0
D=A
@ARG
D=D+M
@R15
M=D
@SP
A=M
D=M
@R15
A=M
M=D
// reposition SP
@ARG
D=M+1
@SP
M=D
// reposition THIS
@2
D=A
@R13
D=M-D
A=D
D=M
@THIS
M=D
// reposition THAT
@1
D=A
@R13
D=M-D
A=D
D=M
@THAT
M=D
// reposition ARG
@3
D=A
@R13
D=M-D
A=D
D=M
@ARG
M=D
// reposition LCL
@4
D=A
@R13
D=M-D
A=D
D=M
@LCL
M=D
// return to caller
@R14
A=M
0;JMP

