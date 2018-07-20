import math
def ex1():
	m=0
	u=1.0;
	while u+1!=1:
		m+=1
		u=u/10.0
	return (10**-m)
print ("Precizia masinii este data de numarul: "+str(ex1()))

#2

def ex2():
	u=ex1()
	y,z=u,u
	x=1.0
	if (x+y)+z==x+(y+z):
		return "Operatia + este asociativa"
	else:
		return "Operatia + nu este asociativa... Diferenta: "+ str((x+y)+z-(x+(y+z)))
print(ex2())	
def ex2_cont(y,z):
	x=ex1()
	#x=1.0
	if (x*y)*z==x*(y*z):
		return "Operatia * este asociativa"
	else:
		return "Operatia * nu este asociativa... Diferenta: "+ str((x*y)*z-(x*(y*z)))
print (ex2_cont(1/10**27,1/10**27))

def read_m(file_name1, file_name2):
	file1 = open(file_name1, "r").read()
	file2 = open(file_name2, "r").read()
	A = [item.split() for item in file1.split('\n')]
	B = [item.split() for item in file2.split('\n')]

	for i in range(0,len(A)):
		for j in range(0,len(A)):
			A[i][j]=int(A[i][j])
			B[i][j]=int(B[i][j])
	return (A, B)

def print_m(matrix):
	for i in range(0,len(matrix)):
		print(matrix[i])
		
def matrix_product(A, B):
	result = []
	for i in range(0,len(A)):
		result.append([0]*len(A))
	for i in range (0,len(A)):
		for j in range(0,len(A)):
			for k in range(0,len(A)):
				result[i][k] += A[i][j] *B[j][k]
	return result
	
def matrix_add(A, B):
	result = [[A[i][j]+B[i][j] for j in range(0,len(A))] for i in range(0,len(A))]
	return result
		
def matrix_substract(A, B):
	result = [[A[i][j]-B[i][j] for j in range(0,len(A))] for i in range(0,len(A))]
	return result

def get_next_power_of_2(number):
	i = 1
	power = 0
	while i<number:
		i*=2
		power+=1
	return power
	
def multiply_Strassen(A, B, q, d):
	n = 2**q
	n_min = 2**d
	
	if n<=n_min:
		return matrix_product(A, B)
	else:	
		A11 = []
		A12 = []
		A21 = []
		A22 = []
	
		B11 = []
		B12 = []
		B21 = []
		B22 = []
	
		for i in range (0, n//2): 
			line_A = []
			line_B = []
			for j in range(0, n//2):
				line_A.append(A[i][j])
				line_B.append(B[i][j])
			A11.append(line_A)
			B11.append(line_B)
		
		for i in range (0, n//2):
			line_A = []
			line_B = []
			for j in range (n//2, n):
				line_A.append(A[i][j])
				line_B.append(B[i][j])
			A12.append(line_A)
			B12.append(line_B)
		
		for i in range (n//2, n ):
			line_A = []
			line_B = []
			for j in range (0, n//2):
				line_A.append(A[i][j])
				line_B.append(B[i][j])
			A21.append(line_A)
			B21.append(line_B)
			
		for i in range (n//2, n ):
			line_A = []
			line_B = []
			for j in range (n//2, n):
				line_A.append(A[i][j])
				line_B.append(B[i][j])
			A22.append(line_A)
			B22.append(line_B)
		
		p1 = multiply_Strassen(matrix_add(A11, A22),matrix_add(B11, B22), q//2, d)
		p2 = multiply_Strassen(matrix_add(A21,A22),B11, q//2, d)
		p3 = multiply_Strassen(A11,matrix_substract(B12,B22), q//2, d)
		p4 = multiply_Strassen(A22,matrix_substract(B21, B11), q//2, d)
		p5 = multiply_Strassen(matrix_add(A11,A12), B22, q//2, d)
		p6 = multiply_Strassen(matrix_substract(A21,A11),matrix_add(B11,B12), q//2, d)
		p7 = multiply_Strassen(matrix_substract(A12,A22), matrix_add(B21,B22), q//2,d)
		
		C11 = matrix_substract(matrix_add(matrix_add(p1,p4),p7), p5)
		C12 = matrix_add(p3, p5)
		C21 = matrix_add(p2, p4)
		C22 = matrix_substract(matrix_add(matrix_add(p1,p3),p6),p2)
		
		C = []
		for i in range(0,n):
			C.append([0]*n)

		for i in range(0, n//2):
			for j in range(0,n//2):
				C[i][j] = C11[i][j]
				C[i][j+n//2] = C12[i][j]
				C[i+n//2][j] = C21[i][j]
				C[i+n//2][j+n//2] = C22[i][j]
				
		return C	
	
m = read_m("m1.txt", "m2.txt")	
A = m[0]
B = m[1]

print("\nPrima matrice: ")	
print_m(A)
print("\nA doua matrice: ")	
print_m(B)
n = len(A)

print(int(math.log(len(A),2)))
if math.log(len(A),2)!=int(math.log(len(A),2)):
	new_A = []
	new_B = []
	next_power_of_2 = get_next_power_of_2(len(A))
	new_n = 2**next_power_of_2
	for i in range(0,new_n):
		new_A.append([0]*new_n)
		new_B.append([0]*new_n)
	for i in range(0,len(A)):
		for j in range(0,len(A)):
			new_A[i][j] = A[i][j]
			new_B[i][j] = B[i][j]

	A = new_A
	B = new_B
	#print(A)

C = multiply_Strassen(A, B, 3, 1)
print("\nRezultatul inmultirii:")
rezult = []
for i in range(0,n):
	rezult.append([0]*n)
for i in range(0,n):
	for j in range(0,n):
		rezult[i][j] = C[i][j]
print_m(rezult)	