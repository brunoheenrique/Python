import pandas as pd

import os

from tkinter import Tk

from tkinter.filedialog import askopenfilename


Tk().withdraw()

dirOrigem = askopenfilename(filetypes = (("Arquivos de texto", "*.txt"), ("Arquivos csv", "*.csv")))

basename = os.path.basename(dirOrigem)

file_name = os.path.splitext(basename)[0]

dirDestino= os.getcwd() + f"\\{file_name}.csv"

read_file = pd.read_fwf (dirOrigem, encoding='cp1252', errors='ignore')

read_file.to_csv (dirDestino, index=None)

# try:

#     os.mkdir('./Baixados')

#     os.mkdir('./Enviados')

# except OSError:

#     pass

# testeArray = pd.read_csv("C:\\Users\\Felip\\Desktop\\Gerar_02_Exp_1200_2022.csv", sep=",")

# print(testeArray)

# TotalElementos = len(testeArray)

# matriz = [0] * 90 + [0] * 90

# lt = 0

# for l in range(TotalElementos):

#     novaBase = []

#     print(testeArray[0][l])

#     if testeArray[0][l].strip() == '1200':

#         string = str(testeArray[0][l])

#         novaBase.append(string)

#         matriz=[lt] = novaBase

#         lt = lt +1

# Totalnovo = len(novaBase)

# teste = 10

# print(novaBase)

# # logger_file = open(r"C:\\Users\\Felip\\Desktop\\Gerar_02_Exp_1200_2022.txt", "r+")

# # read_file.to_csv (r"C:\\Users\\Felip\\Downloads\\Gerar_02_Exp_1200_2022.csv", index=None)

# # import pandas as pd

# # # from sklearn import linear_model

# # # import matplotlib.pyplot as plt

# # dataframe = pd.read_fwf(r"C:\\Users\\Felip\\Desktop\\Gerar_02_Exp_1200_2022.txt")

# # x_values = dataframe[['Brain']]

# # y_values = dataframe[['Body']]

# # # body_reg = linear_model.LinearRegression()

# # # body_reg.fit(x_values,y_values)

# # print(x_values,y_values)

# # # plt.plot(x_values,body_reg.predict(x_values))