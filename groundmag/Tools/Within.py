import numpy as np


def Within(x,x0,x1):
	
	return (x > x0) & (x < x1)

def WithinInc(x,x0,x1):
	
	return (x >= x0) & (x <= x1)
