import pandas as pd
import matplotlib.pyplot as plt

data_file = pd.read_csv("graph_plot.csv")

data_file.columns=["Error Rate", "BER"]
plt.xlabel("Error Rate")
plt.ylabel("Bit Error Rate")
plt.title("Error Rate vs Bit Error Rate")
plt.plot(data_file["Error Rate"],data_file["BER"])
plt.show()



data_file = pd.read_csv("graph_psnr.csv")

data_file.columns=["Error Rate", "PSNR"]
plt.xlabel("Error Rate")
plt.ylabel("PSNR(in dB)")
plt.title("Error Rate vs PSNR")
plt.plot(data_file["Error Rate"],data_file["PSNR"])
plt.show()
