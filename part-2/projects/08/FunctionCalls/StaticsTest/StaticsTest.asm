// Initialization
@261
D=A
@SP
M=D
// function Sys.init 0
(Sys.init)

// push constant 6
@6
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 8
@8
D=A
@SP
A=M
M=D
@SP
M=M+1

// call Class1.set 2
// saving Class1.setret$1
@Class1.setret$1
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
@2
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
@Class1.set
0;JMP
// returning point fClass1.set
(Class1.setret$1)

// pop temp 0
@SP
M=M-1
@5
D=A
@0
D=D+A
@R15
M=D
@SP
A=M
D=M
@R15
A=M
M=D

// push constant 23
@23
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 15
@15
D=A
@SP
A=M
M=D
@SP
M=M+1

// call Class2.set 2
// saving Class2.setret$2
@Class2.setret$2
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
@2
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
@Class2.set
0;JMP
// returning point fClass2.set
(Class2.setret$2)

// pop temp 0
@SP
M=M-1
@5
D=A
@0
D=D+A
@R15
M=D
@SP
A=M
D=M
@R15
A=M
M=D

// call Class1.get 0
// saving Class1.getret$3
@Class1.getret$3
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
@0
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
@Class1.get
0;JMP
// returning point fClass1.get
(Class1.getret$3)

// call Class2.get 0
// saving Class2.getret$4
@Class2.getret$4
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
@0
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
@Class2.get
0;JMP
// returning point fClass2.get
(Class2.getret$4)

// label WHILE
(WHILE)

// goto WHILE
@WHILE
0;JMP

// function Class1.set 0
(Class1.set)

// push argument 0
@ARG
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1

// pop static 0
@SP
M=M-1
@SP
A=M
D=M
@Class1.0
M=D

// push argument 1
@1
D=A
@ARG
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1

// pop static 1
@SP
M=M-1
@SP
A=M
D=M
@Class1.1
M=D

// push constant 0
@0
D=A
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

// function Class1.get 0
(Class1.get)

// push static 0
@Class1.0
D=M
@SP
A=M
M=D
@SP
M=M+1

// push static 1
@Class1.1
D=M
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

// function Class2.set 0
(Class2.set)

// push argument 0
@ARG
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1

// pop static 0
@SP
M=M-1
@SP
A=M
D=M
@Class2.0
M=D

// push argument 1
@1
D=A
@ARG
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1

// pop static 1
@SP
M=M-1
@SP
A=M
D=M
@Class2.1
M=D

// push constant 0
@0
D=A
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

// function Class2.get 0
(Class2.get)

// push static 0
@Class2.0
D=M
@SP
A=M
M=D
@SP
M=M+1

// push static 1
@Class2.1
D=M
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

