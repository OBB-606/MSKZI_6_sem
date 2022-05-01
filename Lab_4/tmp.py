from collections import Counter
import numpy as np
s1 = '0001111011010010101000011111110000101010101'
s2 = '0'
s3 = '1'
# print(len(s1) == s1.count(s2) + s1.count(s3))
"""nbit = 379881, formula = 772677"""
str_1 = "1001111001000100101100000100001010010110010111010000111101000100"
f = 18 + 8*2 + 3*3 + 4*4 + 5
# print(len(str_1))
# print(f"{str_1.count('0')}, {str_1.count('1')}")

lst = [1,2,3,4,5,999,7,8,9]
new  = np.array(lst).reshape(3,3)
print(np.linalg.det(new))