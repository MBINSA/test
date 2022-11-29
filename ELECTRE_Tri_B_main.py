#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 2022 at 15:59

@author: sdaniel
"""

import ELECTRE_Tri_B
import math
import matplotlib.pyplot as plt
import numpy as np


########################################################################################################################
# ===========================================   Input data import   ================================================== #
########################################################################################################################

CAT = ['C1', 'C2', 'C3', 'C4', 'C5']
S = ['S1.1', 'S1.2','S1.3', 'S1.4','S2.1', 'S2.2','S2.3', 'S2.4','S3.1', 'S3.2','S3.3', 'S3.4','S4.1', 'S4.2','S4.3', 
      'S4.4','S5.1', 'S5.2','S5.3', 'S5.4','S6.1', 'S6.2','S6.3', 'S6.4','S7.1', 'S7.2','S7.3', 'S7.4']
# C, W, A, AP, B, BP, T = ELECTRE_Tri_B.input_data('01_Weights.csv',
#                                                   '02_Actions_performancesMY.csv',
#                                                   '03_Distribution_Types.csv',
#                                                   '04_Boundaries_actions_performances.csv',
#                                                   '05_Thresholds.csv')
# print(MY)
# print(AP)
# print(D)
# print('')
# Sigma_bk_init, Separability_init = ELECTRE_Tri_B.separability_test(C, W, B, BP, T, display='NO')
# λ_min = math.ceil(max(Sigma_bk_init.values()) * 1000) / 1000
# print('Minimum required initial credibility threshold λ =', λ_min)
# λ = 0.75
# print('Chosen initial credibility threshold λ =', λ)

########################################################################################################################
# ================================   Automatic execution of the ELECTRE Tri-B   ====================================== #
########################################################################################################################

repetition = 700

memoire_opti={}
memoire_pessi={}
for s in S:
    memoire_opti[s]=[0,0,0,0,0]
    memoire_pessi[s]=[0,0,0,0,0]

for s in range(repetition):
    C, W, A, AP, B, BP, T = ELECTRE_Tri_B.input_data('01_Weights.csv',
                                                      '02_Actions_performancesMY.csv',
                                                      '03_Distribution_Types.csv',
                                                      '04_Boundaries_actions_performances.csv',
                                                      '05_Thresholds.csv')
    Sigma_bk_init, Separability_init = ELECTRE_Tri_B.separability_test(C, W, B, BP, T, display='NO')
    λ_min = math.ceil(max(Sigma_bk_init.values()) * 1000) / 1000
    # print('Minimum required initial credibility threshold λ =', λ_min)
    λ = 0.75
    # print('Chosen initial credibility threshold λ =', λ)
    Test_init = ELECTRE_Tri_B.ELECTRE_Tri_B(C, W, A, AP, B, BP, T, CAT, λ, display='NO')
    Conc, Disc, Glob_conc, Cred, Over_rank, Pessi_sort, Opti_sort, Med_rank, Sigma_bk, Separability = \
        ELECTRE_Tri_B.ELECTRE_Tri_B(C, W, A, AP, B, BP, T, CAT, λ, display='NO')
    memoire_opti = ELECTRE_Tri_B.compter(Opti_sort[1], memoire_opti)
    memoire_pessi = ELECTRE_Tri_B.compter(Pessi_sort[1], memoire_pessi)
    # print(s)
    


ELECTRE_Tri_B.Write_csv_Results(memoire_opti, memoire_pessi)
   
for r in S:
    # plt.hist(memoire_opti[r])
    # plt.show()
    
    x = CAT
    y = memoire_opti[r]
    plt.title(r+' (var=0.2) ')
    plt.xlabel('categories')
    plt.ylabel('values')
    plt.bar(x,y,color = (0.5,0.1,0.5,0.6))
    plt.show()
    
 
# Add title and axis names


# print(memoire_opti)
# print(memoire_pessi)

# Test_init = ELECTRE_Tri_B.ELECTRE_Tri_B(C, W, A, AP, B, BP, T, CAT, λ, display='YES')
# Conc, Disc, Glob_conc, Cred, Over_rank, Pessi_sort, Opti_sort, Med_rank, Sigma_bk, Separability = \
#     ELECTRE_Tri_B.ELECTRE_Tri_B(C, W, A, AP, B, BP, T, CAT, λ, display='NO')


# =====================================   Counts the number of incomparabilities   =============================== #
#
# R = 0
# for key in Test_init[4].keys():
#     R = R + Test_init[4][key].count('R')
# print('Appearance of incomparabilities : ', R)

########################################################################################################################
# ================================   OR Manual execution of the ELECTRE Tri-B   ====================================== #
########################################################################################################################

# # ======================   Test of the minimum requirements to run the ELECTRE Tri method   ====================== #
#
# # The weights of the criteria must be normalized and their sum must be equal to 1 or 100
# if sum(W.values()) <= 1.000001 and not 0.999999 <= sum(W.values()) <= 1.000001:
#     raise NameError('Condition of normalized weights is not respected')
# elif sum(W.values()) > 1.000001 and not 99.999999 <= sum(W.values()) <= 100.000001:
#     raise NameError('Condition of normalized weights is not respected')
#
# # The values of the thresholds 'q', 'p' and 'v' must be increasing 'q' < 'p' < 'v'
# for gj in T.keys():
#     if not T[gj][0] < T[gj][1] < T[gj][2]:
#         raise NameError('Condition of increasing order of thresholds is not respected')
#
# # Separability test and verification of the minimum required credibility threshold
# Sigma_bk, Separability = ELECTRE_Tri_B.separability_test(C, W, B, BP, T, display='NO')
# if λ < max(Sigma_bk.values()):
#     raise NameError('The chosen credibility threshold is lower than the minimum required credibility threshold '
#                     'λ_min = {}'.format(max(Sigma_bk.values())))
#
# # ==========================   Calculation of the indicators of the ELECTRE Tri method   ========================= #
#
# # Calculation of the concordance matrices for all the boundary scenarios
# Conc = {}
# for b in B:
#     name = '{}'.format(b)
#     Conc[name] = ELECTRE_Tri_B.concordance(C, A, AP, b, BP, T)
#
# # Calculation of the discordance matrices for all the boundary scenarios
# Disc = {}
# for b in B:
#     name = '{}'.format(b)
#     Disc[name] = ELECTRE_Tri_B.discordance(C, A, AP, b, BP, T)
#
# # Calculation of the global concordances vectors for all the boundary scenarios
# Glob_conc = {}
# for b in B:
#     name = '{}'.format(b)
#     Glob_conc[name] = ELECTRE_Tri_B.global_concordance(Conc['{}'.format(b)], b, C, W, A)
#
# # Calculation of the credibility vectors for all the boundary scenarios
# Cred = {}
# for b in B:
#     name = '{}'.format(b)
#     Cred[name] = ELECTRE_Tri_B.credibility(Glob_conc['{}'.format(b)], b, Disc['{}'.format(b)], C, A)
#
# # Building the matrix of outranking relations
# Over_rank = {}
# for b in B:
#     name = '{}'.format(b)
#     Over_rank[name] = ELECTRE_Tri_B.over_ranking_relations(Cred['{}'.format(b)], b, λ)
#
# # ============================   Ranking of actions and calculation of median ranks   ============================ #
#
# # Ranking of actions in the three categories according to the pessimistic procedure and display of the result
# Pessi_sort = ELECTRE_Tri_B.pessimistic_sorting(Over_rank, CAT, A, B)
#
# # Ranking of actions in the three categories according to the optimistic procedure and display of the result
# Opti_sort = ELECTRE_Tri_B.optimistic_sorting(Over_rank, CAT, A, B)
#
# # Calculating the median rank of each share
# Med_rank = ELECTRE_Tri_B.median_rank(Pessi_sort, Opti_sort, A)
#
# # ==========================================   Display of the results   ========================================== #
#
# # Display of the categories in which each action is classified
# print(' ')
# print("Results of the pessimistic sorting : ")
# for cat in Pessi_sort[0].keys():
#     print('{} :'.format(cat), Pessi_sort[0][cat])
# print('Pessimistic category :', Pessi_sort[1])
# print(' ')
# print('Results of the optimistic sorting : ')
# for cat in Opti_sort[0].keys():
#     print('{} :'.format(cat), Opti_sort[0][cat])
# print('Optimistic category : ', Opti_sort[1])
#
# # Display of the median rank of each action
# print(' ')
# ELECTRE_Tri_B.display_results(Pessi_sort, Opti_sort, Med_rank, A)
