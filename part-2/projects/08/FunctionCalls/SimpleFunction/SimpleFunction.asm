// Initialization
@261
D=A
@SP
M=D
// function SimpleFunction.test 2
(SimpleFunction.test)
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

// push argument 0
@ARG
A=M
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

