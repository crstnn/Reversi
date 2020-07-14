
.data
	size_prompt:	.asciiz "Enter list size: "
	element_prompt:	.asciiz "Enter element "
	min_str:	.asciiz "The minimum element in this list is "
	colon_str:	.asciiz ": "
	newline_str:	.asciiz "\n"
	size:		.word 0
	the_list:	.word 0
	i:		.word 0
	min:		.word 0
	item:		.word 0

.text
	# ignore this line, it is for later testing
	# la $ra, test
	
	# CODE FOR READING LIST HERE
main: 
	#user prompt 	
	la $a0, size_prompt
	addi $v0, $zero, 4
	syscall
	
	#input "size"
	addi $v0, $zero, 5	
	syscall
	sw $v0, size
	
	#print newline
	la $a0, newline_str
	addi $v0, $zero, 4
	syscall
	
	# list length calculation
	lw $t1, size
	sll $t3, $t1, 2
	addi $t3, $t3, 4
	
	#list initialisation
	addi $v0, $zero, 9	# allocate
	add $a0, $zero, $t3	# $a0 = size
	syscall	
	sw $v0, the_list	# the list = address
				# $t0 = size
	sw $t1, 0($v0)		# total.length = size
	

	#before loop enters make sure 'i' is intitialised to 0
	sw $zero, i
	
list_loop:
 	# for loop
	lw $t2, i
	# end when i == size
	slt $t4, $t2, $t1
	beq $t4, $zero, compute_min
	# for loop body
	
		# print user prompt 	
		la $a0, element_prompt
		addi $v0, $zero, 4
		syscall
	
		# print i
		add $a0, $zero ,$t2
		addi $v0, $zero, 1
		syscall
	
		# print colon 	
		la $a0, colon_str
		addi $v0, $zero, 4
		syscall
		
		#input "element"
		addi $v0, $zero, 5	
		syscall
		add $t6, $zero, $v0
	
		#newline
		la $a0, newline_str
		addi $v0, $zero, 4
		syscall
	
		# the_list[i] = (user input)
		lw $t0, the_list
		lw $t2, i
		sll $t2, $t2, 2		# i * 4
		add $t0, $t0, $t2	
		sw $t6, 4($t0)
		
		# i ++
		lw $t2, i
		addi $t2, $t2, 1
		sw $t2, i
		
	j list_loop



compute_min:

 	# CODE FOR COMPUTING THE MIN

# second if statement: size > 0
	lw $t1, size
	slt $t2, $zero, $t1
	beq $t2, $zero, exit
	
	
	# min = the_list[0]
	lw $t0, the_list
	lw $t4, 4($t0)
	sw $t4, min

	
	#set i = 1	
	lw $t2, i
	addi $t2, $zero, 1
	sw $t2, i
second_loop:
		#for loop body
		lw $t2, i
		# end when i == size
		lw $t1, size
		slt $t5, $t2, $t1
		beq $t5, $zero, endif_outer
		
			# item = the_list[i]
			lw $t0, the_list
			lw $t2, i
			sll $t2, $t2, 2		# i * 4
			add $t0, $t0, $t2	
			lw $t3, 4($t0)
			sw $t3, item
		
inner_if:	
			#if min > item
			# $t4 = min, $t3 = item
			lw $t3, item
			lw $t4, min
			slt $t2, $t3, $t4
			beq $t2, $zero, endif_inner
					#index calculation
					lw $t0, the_list
					lw $t2, i
					sll $t2, $t2, 2		# i * 4
					add $t0, $t0, $t2
					# min = item
					lw $t4, 4($t0)
					sw $t4, min							
endif_inner: 
			# i ++
			lw $t2, i
			addi $t2, $t2, 1
			sw $t2, i
		
			j second_loop
	
		
endif_outer: 

	#print min element
	#user prompt 	
	la $a0, min_str
	addi $v0, $zero, 4
	syscall
	
	#print min element
	lw $a0, min
	addi $v0, $zero, 1
	syscall
	
	#print newline
	la $a0, newline_str
	addi $v0, $zero, 4
	syscall
	
	
exit:
	# Exit the program
	addi $v0, $zero, 10
	syscall
