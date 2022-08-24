import numpy as np 

class muscle:
	def __init__(self, baseMuscleAvg, baseMuscleStdDev, expEndRatioAvg, expEndRatioStdDev):
		
	    baselineMuscle = np.random.normal(baseMuscleAvg, baseMuscleStdDev, 1)
	    explosiveEnduranceRatio = np.random.normal(expEndRatioAvg, expEndRatioStdDev, 1)
		    
	    if baselineMuscle < 0 :
	       baselineMuscle = 1
			
	    if baselineMuscle > 100 :
	       baselineMuscle = 100

	    if explosiveEnduranceRatio < 0 :
	       explosiveEnduranceRatio = .01

	    if explosiveEnduranceRatio > 1 :
	       explosiveEnduranceRatio = 1

	    self.baselineMuscle = baselineMuscle
	    self.explosiveEnduranceRatio = explosiveEnduranceRatio
