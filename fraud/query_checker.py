from rule_matcher import *
from cosine_module import *
import math

def driver(trans):
	a = (1-r_matcher(trans))
	return a
	b = cosine_cal_1(trans)
	# print(a,b)
	w1 = 5
	w2 = 0
	fin = (a*w1 + b*w2)/(w1+w2)
	# fin = (a+b)/2
	return fin
	# return cosine_cal(trans)

def checker(trans):
	x = driver(trans)
	print(x)
	if x>=0.4:
		return 0
	else:
		return 1
