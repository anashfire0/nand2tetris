// Initialization
@261
D=A
@SP
M=D
// function Sys.init 0
(Sys.init)

// push constant 4000
@4000
D=A
@SP
A=M
M=D
@SP
M=M+1

// pop pointer 0
@SP
M=M-1
@SP
A=M
D=M
@THIS
M=D

// push constant 5000
@5000
D=A
@SP
A=M
M=D
@SP
M=M+1

// pop pointer 1
@SP
M=M-1
@SP
A=M
D=M
@THAT
M=D

// call Sys.main 0
// saving Sys.mainret$1
@Sys.mainret$1
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
@Sys.main
0;JMP
// returning point fSys.main
(Sys.mainret$1)

// pop temp 1
@SP
M=M-1
@5
D=A
@1
D=D+A
@R15
M=D
@SP
A=M
D=M
@R15
A=M
M=D

// label LOOP
(LOOP)

// goto LOOP
@LOOP
0;JMP

// function Sys.main 5
(Sys.main)
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
@0
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 4001
@4001
D=A
@SP
A=M
M=D
@SP
M=M+1

// pop pointer 0
@SP
M=M-1
@SP
A=M
D=M
@THIS
M=D

// push constant 5001
@5001
D=A
@SP
A=M
M=D
@SP
M=M+1

// pop pointer 1
@SP
M=M-1
@SP
A=M
D=M
@THAT
M=D

// push constant 200
@200
D=A
@SP
A=M
M=D
@SP
M=M+1

// pop local 1
@SP
M=M-1
@1
D=A
@LCL
D=D+M
@R15
M=D
@SP
A=M
D=M
@R15
A=M
M=D

// push constant 40
@40
D=A
@SP
A=M
M=D
@SP
M=M+1

// pop local 2
@SP
M=M-1
@2
D=A
@LCL
D=D+M
@R15
M=D
@SP
A=M
D=M
@R15
A=M
M=D

// push constant 6
@6
D=A
@SP
A=M
M=D
@SP
M=M+1

// pop local 3
@SP
M=M-1
@3
D=A
@LCL
D=D+M
@R15
M=D
@SP
A=M
D=M
@R15
A=M
M=D

// push constant 123
@123
D=A
@SP
A=M
M=D
@SP
M=M+1

// call Sys.add12 1
// saving Sys.add12ret$2
@Sys.add12ret$2
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
@Sys.add12
0;JMP
// returning point fSys.add12
(Sys.add12ret$2)

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

// push local 0
@LCL
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1

// push local 1
@1
D=A
@LCL
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1

// push local 2
@2
D=A
@LCL
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1

// push local 3
@3
D=A
@LCL
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1

// push local 4
@4
D=A
@LCL
A=M+D
D=M
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

// function Sys.add12 0
(Sys.add12)

// push constant 4002
@4002
D=A
@SP
A=M
M=D
@SP
M=M+1

// pop pointer 0
@SP
M=M-1
@SP
A=M
D=M
@THIS
M=D

// push constant 5002
@5002
D=A
@SP
A=M
M=D
@SP
M=M+1

// pop pointer 1
@SP
M=M-1
@SP
A=M
D=M
@THAT
M=D

// push argument 0
@ARG
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1

// push constant 12
@12
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

