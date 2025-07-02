import another_image
import plot_error
import pandas as pd
import subprocess
import numpy as np
import matplotlib.pyplot as plt

df_actual = pd.read_csv("/home/anant/VBN/Performance/far_range_5.csv")
for i in range (len(df_actual)):
    for j in range (0,6):
        another_image.make_image(df_actual.iloc[i+j]["Pitch"], df_actual.iloc[i+j]["Yaw"], df_actual.iloc[i+j]["Roll"],
                   df_actual.iloc[i+j]["Y"], df_actual.iloc[i+j]["Z"], df_actual.iloc[i+j]["X"])
        print(df_actual.iloc[i+j]["Roll"], df_actual.iloc[i+j]["Pitch"], df_actual.iloc[i+j]["Yaw"],
                   df_actual.iloc[i+j]["Y"], df_actual.iloc[i+j]["Z"], df_actual.iloc[i+j]["X"])
        subprocess.run("./pipeline", shell=True)
    df_result = pd.read_csv("/home/anant/VBN/Performance/result.txt")
    for j in range (0,10):
        data = { "Roll": abs(df_actual.iloc[i+j]["Roll"]-df_result.iloc[i+j]["Roll"]),
                 "Pitch": abs(df_actual.iloc[i+j]["Pitch"]-df_result.iloc[i+j]["Pitch"]),
                 "Yaw": abs(df_actual.iloc[i+j]["Yaw"]-df_result.iloc[i+j]["Yaw"]),
                 "X": abs(df_actual.iloc[i+j]["X"]-df_result.iloc[i+j]["X"]),
                 "Y": abs(df_actual.iloc[i+j]["Y"]-df_result.iloc[i+j]["Y"]),
                 "Z": abs(df_actual.iloc[i+j]["Z"]-df_result.iloc[i+j]["Z"]),
             }
        df_error = pd.DataFrame(data) 
        df_error.to_csv(f"/home/anant/VBN/Performance/error.csv", index=False)
        plot_error.plot_error(df_actual.iloc[i+j]["Roll"], df_actual.iloc[i+j]["Pitch"], df_actual.iloc[i+j]["Yaw"],
                   df_actual.iloc[i+j]["Y"], df_actual.iloc[i+j]["Z"], df_actual.iloc[i+j]["X"])
    break
    i+=10


