	AREA RESET,DATA,READONLY
	EXPORT __Vectors

__Vectors
	
	DCD 0x10001000
	DCD Reset_Handler
	ALIGN
	AREA mycode,CODE,READONLY
	ENTRY
	EXPORT Reset_Handler	

Reset_Handler
		
	MOV R1, #1
	MOV R2, #6
	MOV R3, #4
	MOV R4, #7
	MOV R5, #9
	MOV R6, #3
	MOV R7, #2
	MOV R8, #5
	MOV R9, #8
	MOV R10, #10
	STMDB R13!, {R1-R10}
	MOV R0,R13
	MOV R8,#9
	
LOOP
	LDM R0,{R1}
	ADD R0,#4
	MOV R7,R8
	MOV R2,R0

LOOP2
	LDM R2!,{R3}
	CMP R1,R3
	BLO SKIP
	STMDB R0,{R3}
	STMDB R2,{R1}
	MOV R1,R3
SKIP
	SUBS R7,#1
	BNE LOOP2
	SUBS R8,#1
	BNE LOOP
	LDM R13, {R1-R10}
		
	NOP
	END