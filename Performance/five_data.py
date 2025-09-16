import another_image
import subprocess
import csv
roll = [0,0.5, 1,1.5,2,2.5]
pitch = [0, 0.5, 1,1.5,2,2.5]
yaw = [0, 0.5, 1,1.5,2,2.5]
X = [30,40,50,60,70,80,90 ]
Y = [0,5,10,15]
Z = [0,5,10,15]

for i in range (len(roll)):
    for j in range (len(pitch)):
        for k in range (len(yaw)):
            for l in range (len(X)):
                for m in range (len(Y)):
                    for n in range (len(Z)):
                        print(f"Roll: {roll[i]}, Pitch: {pitch[j]}, Yaw: {yaw[k]}, X: {X[l]}, Y: {Y[m]}, Z: {Z[n]}")
                        row = [roll[i], pitch[j], yaw[k], Y[m], Z[n], X[l]]
                        with open('/home/anant/VBN/Performance/result.csv', 'a', newline='') as f:
                             csv.writer(f).writerow(row)  
                        another_image.make_image( pitch[j], yaw[k],roll[i],Y[m], Z[n],X[l])
                        subprocess.run("./pipeline", shell=True)

