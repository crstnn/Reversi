#Bubble sort algorithm implemented in MIPS assembly language
.data
.globl bubble_sort

.text

bubble_sort:
	#save $ra and $fp in the stack 
	addi $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, ($sp)
	

	# Copy $sp to $fp
	addi $fp, $sp, 0
	#instantiate locals (5 of them: n, a, i, item, item_to_right)
	addi $sp, $sp, -20
	

	# local variable loading "the_list" arg
	lw $t7, 8($fp)
	# n = len(the_list)
	lw $t6, ($t7)
	sw $t6, -20($fp)

	# initialise a = 0, prior to loop
	sw $zero, -16($fp)

outer_for:
	# outer for loop
	# retrieve a
	lw $t6, -16($fp)
	# end when a == len(the_list)-1
	lw $t7, -20($fp)
	addi $t7, $t7, -1
		
	slt $t5, $t6, $t7
	beq $t5, $zero, end_outer_for
	
	# intialise i = 0, prior to loop
	sw $zero, -12($fp)
inner_for:	
		#inner for loop (loading i and len)
		lw $t5, -12($fp)
		lw $t7, -20($fp)
		addi $t7, $t7, -1

		# end when i == len(the_list)-1
		slt $t4, $t5, $t7
		beq $t4, $zero, end_inner_for
			# item = the_list[i]
			lw $t5, -12($fp)
			sll $t2, $t5, 2		# i * 4
			# load arg
			lw $t7, 8($fp)
			add $t7, $t7, $t2
			lw $t4, 4($t7)
			sw $t4, -8($fp)
			
			#load arg (also calculation done above so use from there)
			lw $t7, 8($fp)
			add $t7, $t7, $t2
			lw $t3, 8($t7)
			# item_to_right = the_list[i+1]
			sw $t3, -4($fp)
			
			#if item_to_right < item
			lw $t3, -4($fp)
			lw $t4, -8($fp)
			slt $t5, $t3, $t4
			beq $t5, $zero , endif_inner
				#list length calculation
				lw $t5, -12($fp)
				sll $t2, $t5, 2		# i * 4
	
				# the_list[i] = item_to_right ('i' already calculated above)
				lw $t7, 8($fp)
				add $t7, $t7, $t2
				lw $t3, -4($fp)
				sw $t3, 4($t7)
				# the_list[i+1] = item ('i' already calculated above)
				lw $t7, 8($fp)
				add $t7, $t7, $t2
				lw $t3, -8($fp)
				sw $t3, 8($t7)

		
endif_inner:
		
		# i++
		lw $t5, -12($fp)
		addi $t5, $t5, 1
		sw $t5, -12($fp)
		
		j inner_for
		
end_inner_for:	
	
	
	# a++
	lw $t6, -16($fp)
	addi $t6, $t6, 1
	sw $t6, -16($fp)
	
	j outer_for
	

end_outer_for:
	
	#remove locals
	addi $sp, $sp, 20
	
	#restore $fp and $ra
	lw $fp, 0($sp)
	lw $ra, 4($sp)
	addi $sp, $sp, 8
	
	jr $ra
	
	
