"""
Created on Wed Mar 16 2022 at 15:37
Modified on Thur Dec 01 2022 at 10:00

@author: sdaniel
@author: rviala
@author: ngauthier
"""
import math

import ELECTRE_Tri_B
import matplotlib.pyplot as plt


########################################################################################################################
# ===========================================   Input data import   ================================================== #
########################################################################################################################

CAT = ['C1', 'C2', 'C3', 'C4', 'C5']
S = ['S1.1', 'S1.2', 'S1.3', 'S1.4', 'S2.1', 'S2.2', 'S2.3', 'S2.4', 'S3.1', 'S3.2', 'S3.3', 'S3.4', 'S4.1', 'S4.2',
     'S4.3',
     'S4.4', 'S5.1', 'S5.2', 'S5.3', 'S5.4', 'S6.1', 'S6.2', 'S6.3', 'S6.4', 'S7.1', 'S7.2', 'S7.3', 'S7.4']
variance = 0.1
repetition = 10000

########################################################################################################################
# ================================   Automatic execution of the ELECTRE Tri-B   ====================================== #
########################################################################################################################


memoire_opti = {}
memoire_pessi = {}
for s in S:
    memoire_opti[s] = [0, 0, 0, 0, 0]
    memoire_pessi[s] = [0, 0, 0, 0, 0]

for s in range(repetition):
    C, W, A, AP, B, BP, T = ELECTRE_Tri_B.input_data('01_Weights.csv',
                                                     '02_Actions_performancesMY.csv',
                                                     '03_Distribution_Types.csv',
                                                     '04_Boundaries_actions_performances.csv',
                                                     '05_Thresholds.csv', variance)
    Sigma_bk_init, Separability_init = ELECTRE_Tri_B.separability_test(C, W, B, BP, T, display='NO')
    λ_min = math.ceil(max(Sigma_bk_init.values()) * 1000) / 1000
    λ = 0.75
    Test_init = ELECTRE_Tri_B.ELECTRE_Tri_B(C, W, A, AP, B, BP, T, CAT, λ, display='NO')
    Conc, Disc, Glob_conc, Cred, Over_rank, Pessi_sort, Opti_sort, Med_rank, Sigma_bk, Separability = \
        ELECTRE_Tri_B.ELECTRE_Tri_B(C, W, A, AP, B, BP, T, CAT, λ, display='NO')
    memoire_opti = ELECTRE_Tri_B.compter(Opti_sort[1], memoire_opti)
    memoire_pessi = ELECTRE_Tri_B.compter(Pessi_sort[1], memoire_pessi)
    print(s)

ELECTRE_Tri_B.Write_csv_Results(memoire_opti, memoire_pessi)

for r in S:
    x = CAT
    y = memoire_opti[r]
    plt.title(r + ' (var=' + str(variance) + ') ')
    plt.xlabel('categories')
    plt.ylabel('values')
    plt.bar(x, y, color=(0.5, 0.1, 0.5, 0.6))
    plt.show()

print('variance: ' + str(variance))
print('λ: '+ str(λ))
print(memoire_opti)
print(memoire_pessi)


