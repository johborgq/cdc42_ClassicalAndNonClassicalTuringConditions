#==============================================================================================
# FEM-SIMULATION OF  Cdc42-POLARISATION
#==============================================================================================
# DATE:
# 2020-10-08
# WRITTEN BY:
# Johannes Borgqvist, Adam Malik and Carl Lundholm
# DESCRIPTION:
# The program simulates the "bulk-surface" RD-model of cell polarisation where we have
#  a coupled system of three ODEs describing the dynamics of three states: GTP-bound or active
# Cdc42 u, GDP-bound inactive Cdc42 v and GDI-bound cytosolic Cdc42 V. The first two states live
#  on the membrane which is why we use the surface measure "ds" in the variational formulation
# while the cytosolic species V exists within the cell and therefore has the corresponding measure
# "dx". We solve the PDE by using the Finite Element Method (FEM) in space and
# Finite Differences (FD) in time. We use a "Implicit-Explicit" solution algorithm where the
# we use the explicit Euler algorithm in time (FD) and where the non-linearities in the reaction
# term are evaluated at the previous time point which boils down to solving a linear problem
# in space (FEM). The program starts with the various rate parameters as input and conducts
# the simulation in three steps.
# (1) Calculating the steady states
# (2) Checking the Turing conditions
# (3) If the Turing conditions are satisfied, solve the PDEs using the implicit-explicit FD-FEM algorithm.
#-----------------------------------------------------------------------------------------------------------------------------
# WE run the scripts twice, one for each parameter set:
# namely (high gamma, high d) and  (low gamma, low d)
#-----------------------------------------------------------------------------------------------------------------------------
#=================================================================================================
#=================================================================================================
#=================================================================================================
#=================================================================================================
# Two data sets, which we print to the user
print('===========================================================================================================================================================\n')
print('\tTwo data sets:\n\n\t\t(1) (high gamma,high d)\n\t\t(2)(low gamma,low d)\n')
print('===========================================================================================================================================================\n')
#=================================================================================================
#=================================================================================================
#=================================================================================================
#=================================================================================================
# Nice package to create vectors, innit?
import numpy as np
import os
#import pymp
# The proportion of the surface are over the volume
a = 3
# The cytosolic diffusion is general for all data sets
D = 10000
# maximum concentration in the membrane    
cmax = 3
# Initial concentration V0
V0_init = 6.0
# The reaction strength parameter
d = 10
#=================================================================================================
# Variable for denoting the dataSet
#=================================================================================================
#=================================================================================================
# Loop over the various data sets and solve the FEM problem
for dataIter in range(2): #Dont do special cases as for now
    dataSet = dataIter + 1
    print("\t Dataset %d\n" %(dataSet))
    #-----------------------------------------------------------------------------------------------------------------------------
    # IMPORT PARAMETERS FROM THE PARAMETER FILE
    #-----------------------------------------------------------------------------------------------------------------------------
    # We have four parameter sets, hey?
    # The first two are the classic Turing and
    # the second two are the unclassic Turing.
    # The first and third are with high values of gamma, while
    # the second and fourth are with low values of gamma.
    #--------------------------------------------------------------------------------------------------------------------------------------------------------
    if dataSet == 1:# Classic, increasing d
        c1 =  0.05
        c_1 =  0.04
        c2 = 0.45
        u0 = 1.2263
        v0 = 0.6276
        strBase = '../../../Results/increasingGamma/Classical/21'
        os.mkdir("../../../Results/increasingGamma/Classical/21")
        
    else: # Non-classic, increasing d
        c1 =  0.05
        c_1 = 0.03
        c2 = 0.15
        u0 = 0.9059
        v0 = 0.9332
        strBase = '../../../Results/increasingGamma/NonClassical/21'
        os.mkdir("../../../Results/increasingGamma/NonClassical/21")         
        
     # Initial concentraiton cytosolic cdc42, V (i.e. cdc42-GDI)
    V0 = (V0_init - ( a * (u0+v0)) )
    #--------------------------------------------------------------------------------------------------------------------------------------------------------

    # number of diffusion coefficients
    gammaVec = np.arange(10,163,10)
    #-------------------------------------------------------------------------------------------------------------------------------------------------------
    #-------------------------------------------------------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------------------------------------------------------- 
    #--------------------------------------------------------------------------------------------------------------------------------------------------------    # Repat for stochasticity
    nuOfRepeats = 1
    print('\tWe repeat %d times!\n\n' % (nuOfRepeats))    
    # Files for saving the tex-files, hey? Now, we save everything and do the plottung afterwards
    uMaxAvg_file = open("%s/uMax.csv" % (strBase), "w")
    uMinAvg_file = open("%s/uMin.csv" % (strBase), "w")
    ratioPoleAvg_file = open("%s/ratioPole.csv" % (strBase), "w")
    tPoleAvg_file = open("%s/tPole.csv" % (strBase), "w")
    gamma_file = open("%s/gamma.csv" % (strBase), "w")        
    # Define the average parameters
    u_maxAvg = np.zeros((len(gammaVec),nuOfRepeats),dtype=np.double)
    u_minAvg = np.zeros((len(gammaVec),nuOfRepeats),dtype=np.double)
    t_poleAvg = np.zeros((len(gammaVec),nuOfRepeats),dtype=np.double)
    ratio_poleAvg = np.zeros((len(gammaVec),nuOfRepeats),dtype=np.double)
    #-------------------------------------------------------------------------------------------------------------------------------------------------------     #-------------------------------------------------------------------------------------------------------------------------------------------------------      
    for innerIndex in range(nuOfRepeats):                     
        # We now loop through the various values of c_1 to run the calculations
        for i in range(len(gammaVec)):
            #--------------------------------------------------------------------------------------------------------------------------------------------------------
            #--------------------------------------------------------------------------------------------------------------------------------------------------------
            gamma = gammaVec[i] # Relative diffusion of active versus the inactive
            #=================================================================================================
            #=================================================================================================
            #=================================================================================================
            #=================================================================================================
            # Welcome prompt to user
            print('===========================================================================================================================================================\n')
            print('\tFEM-solution to the RD problem modelling Cdc42 activation\n')
            print('===========================================================================================================================================================\n')
            #=================================================================================================
            #=================================================================================================
            #=================================================================================================
            #=================================================================================================
            #-----------------------------------------------------------------------------------------------------------------------------
            # Calculating the FD-FEM solution of the PDE-problem
            #-----------------------------------------------------------------------------------------------------------------------------
            
            
            print('===========================================================================================================================================================\n')
            print('\tCalculating the FD-FEM solution of the PDE-problem!\n\n')        
            import FEMandFD_solver_ImpExp_linear_tAdaptive_PoleFinder
            t_pole, ratio_pole, u_max, u_min, poleIndicator, strBase_2 = FEMandFD_solver_ImpExp_linear_tAdaptive_PoleFinder.solvePDE(u0, v0, V0, c1,c_1,c2,cmax,gamma,d,D,dataSet,i,innerIndex)
            # Save the values to the matrix, hey?
            u_maxAvg[i,innerIndex] = u_max
            u_minAvg[i,innerIndex] = u_min
            t_poleAvg[i,innerIndex] = t_pole
            ratio_poleAvg[i,innerIndex] = ratio_pole
            #-----------------------------------------------------------------------------------------
            print('\t\tCalculations are finished!')
            # Close the two tex-files which we write to as well
            
            
    for i in range(len(gammaVec)):
        gamma_file.write("%d\n" % (gammaVec[i])) 
        for j in range(nuOfRepeats):
            # SAVE TO FILES
            uMaxAvg_file.write("%0.5f\t" % (u_maxAvg[i,j]))
            uMinAvg_file.write("%0.5f\t" % (u_minAvg[i,j]))
            tPoleAvg_file.write("%0.5f\t" % (t_poleAvg[i,j]))
            ratioPoleAvg_file.write("%0.5f\t" % (ratio_poleAvg[i,j]))
    uMaxAvg_file.write("\n")
    uMinAvg_file.write("\n")
    tPoleAvg_file.write("\n")
    ratioPoleAvg_file.write("\n")                         
    # Close the files, hey?    
    gamma_file.close()
    uMaxAvg_file.close()
    uMinAvg_file.close()
    tPoleAvg_file.close()
    ratioPoleAvg_file.close()                  
