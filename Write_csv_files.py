
import csv
import xlrd

Read = True
Write = True

if Read:
    myBook = xlrd.open_workbook('00_Performances_test.xls')
    Actions_performances = myBook.sheet_by_name('Evaluations')
    Boundaries_actions_performances = myBook.sheet_by_name('Seuils et profils')
    Weights = myBook.sheet_by_name('Poids')
    Actions = myBook.sheet_by_name('Scenarios')

    C = []
    for row in range(1, 17):
        C.append(Weights.cell_value(row, 0))

    # Récupérer 1 poids

    W = []
    for row in range(1, 17):
        W.append(Weights.cell_value(row, 2))

    # récupérer plusieurs poids

    #  DM = int(Weights.cell_value(19, 2))

    #  W = {}
    # for row in range(1, 17):
    #        Ww = []
    #        for col in range(2, 2+DM):
    #                Ww.append(Weights.cell_value(row, col))
    #                W[Weights.cell_value(row, 0)] = Ww

    A = []
    for row in range(3, 31):
        A.append(Actions_performances.cell_value(row, 0))

    MY = {}
    for row in range(3, 31):
        perf = []
        for col in range(1, 17):
            if Actions_performances.cell_value(row, col) == 'OUI':
                perf.append(1)
            elif Actions_performances.cell_value(row, col) == 'NON':
                perf.append(0)
            elif col in [1, 2, 4, 5, 10, 16]:
                perf.append(Actions_performances.cell_value(row, col) * (-1))
            else:
                perf.append(Actions_performances.cell_value(row, col))
        
        MY[Actions_performances.cell_value(row, 0)] = perf

    # dictionnary with datas 'S1.1':[perf1, perf2 ]

    ### pour ajouter la variance

    ## VR = {}
    # for row in range(3, 31):
    #   perfvar = []
    #  for col in range(20, 36):
    #         perfvar.append(Actions_performances.cell_value(row, col))
    # VR[Actions_performances.cell_value(row, 1)] = perfvar


    # ### pour choisir le type
    D = []
    Cri = []
    for col in range(20, 36):
        Cri.append(Actions_performances.cell_value(1, col))
        if Actions_performances.cell_value(31, col) == 'Poisson':
            D.append('P')
        elif Actions_performances.cell_value(31, col) == 'Exponentielle':
            D.append('E')
        elif Actions_performances.cell_value(31, col) == 'Normale':
            D.append('N')
        else:
            D.append('LN')

    # D = []
    # for col in range(20, 35):
    #     D.append(Actions_performances.cell_value(31, col))
    #
    # DV = {}
    # for col in range(20, 35):
    #     perf_dv = []
    #     for row in range(2, 30):
    #         if Actions_performances.cell_value(row, col) == 'OUI':
    #             perf_dv.append(1)
    #         elif Actions_performances.cell_value(row, col) == 'NON':
    #             perf_dv.append(0)
    #         elif col in [20, 21, 23, 24, 29, 35]:
    #             perf_dv.append(Actions_performances.cell_value(row, col) * (-1))
    #         else:
    #             perf_dv.append(Actions_performances.cell_value(row, col))
    #     DV[Actions_performances.cell_value(31, col)] = perf_dv

    #
    B = []
    for col in range(4, 10):
        B.append(Boundaries_actions_performances.cell_value(1, col))

    BP = {}
    for col in range(4, 10):
        perf = []
        for row in range(3, 19):
            perf.append(Boundaries_actions_performances.cell_value(row, col))
        BP[Boundaries_actions_performances.cell_value(1, col)] = perf

    CAT = ['C1', 'C2', 'C3', 'C4', 'C5']

    T = {}
    for row in range(3, 19):
        T[Boundaries_actions_performances.cell_value(row, 0)] = [Boundaries_actions_performances.cell_value(row, 10),
                                                                 Boundaries_actions_performances.cell_value(row, 11),
                                                                 Boundaries_actions_performances.cell_value(row, 12)]


    if Write:

        with open('01_Weights.csv', 'w', encoding='UTF8', newline='') as W_csv:
            writer = csv.writer(W_csv)
            # write the first header corresponding to the criteria
            writer.writerow(C)
            # write the second header corresponding to the weights
            writer.writerow(W)

        with open('02_Actions_performancesMY.csv', 'w', encoding='UTF8', newline='') as MY_csv:
            writer = csv.writer(MY_csv)
            # write the first header corresponding to the scenarios
            writer.writerow(A)
            #write the criteria
            writer.writerow(Cri)
            # write the data corresponding to the performances
            for a in A :
                writer.writerow(MY[a])

        with open('03_Distribution_Types.csv', 'w', encoding='UTF8', newline='') as D_csv:
            writer = csv.writer(D_csv)
            # write the criteria
            writer.writerow(Cri)
            # write the first header corresponding to the distribution
            writer.writerow(D)
            # # write the variance for each distribution
            # for d in D:
            #     writer.writerow(DV[d])

        with open('04_Boundaries_actions_performances.csv', 'w', encoding='UTF8', newline='') as BP_csv:
            writer = csv.writer(BP_csv)
            # write the first header corresponding to the boundaries actions
            writer.writerow(B)
            # write the data corresponding to the performances
            for b in B:
                writer.writerow(BP[b])

        with open('05_Thresholds.csv', 'w', encoding='UTF8', newline='') as T_csv:
            writer = csv.writer(T_csv)
            # write the header corresponding to the name of the thresholds
            writer.writerow(['q', 'p', 'v'])
            # write the data corresponding to the thresholds
            for c in C:
                writer.writerow(T[c])
