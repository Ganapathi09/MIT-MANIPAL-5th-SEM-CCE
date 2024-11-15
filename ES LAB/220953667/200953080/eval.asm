	AREA RESET, DATA, READONLY
	EXPORT __Vectors

__Vectors
    DCD 0x10001000      ; STACK POINTER VALUE WHEN STACK IS EMPTY
    DCD Reset_Handler   ; RESET VECTOR

	ALIGN
	AREA mycode, CODE, READONLY
ENTRY
	EXPORT Reset_Handler

Reset_Handler
	LDR R0, =src
	LDR R1,[R0]
	MOV R2,#8
	MOV R7, #0	; ODD
	MOV R8, #0	; EVEN
BACK
	CMP R2, #0
	BEQ STOP

	AND R4, R1, #0x0F
	LDRB R5, [R4]
	
	CMP R5, #0
	BEQ EVEN
	
	BL ODD

EVEN
	CMP R5, #0
	ADD R8, R8, #1
	SUBS R2, R2, #1
	CMP R2, #0
	LSR R1, #4
	BNE BACK

ODD
	CMP R5, #0
	ADD R7, R7, #1
	SUBS R2, R2, #1
	CMP R2, #0
	LSR R1, #4
	BNE BACK

src DCD 0x00000123
STOP B STOP
	AREA data, DATA, READWRITE
DST DCD 0,0,0,0,0,0,0,0,0
	END