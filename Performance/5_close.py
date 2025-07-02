import another_image
import subprocess
import csv
roll = [0, 5, 15,25 ,35]
pitch = [0, 5, 10 ,15]
yaw = [0, 5, 10 ,15]
X = [30,50,70,90 ]
# Y = [0]
# Z = [0]

for i in range (len(roll)):
    for j in range (len(pitch)):
        for k in range (len(yaw)):
            for l in range (len(X)):
                # for m in range (len(Y)):
                    # for n in range (len(Z)):
                        print(f"Roll: {roll[i]}, Pitch: {pitch[j]}, Yaw: {yaw[k]}, X: {X[l]}, Y: 0, Z: 0")
                        row = [roll[i], pitch[j], yaw[k], 0, 0, X[l]]
                        # with open('/home/anant/VBN/Performance/close_range_5led.csv', 'a', newline='') as f:
                        #     csv.writer(f).writerow(row)  
                        another_image.make_image( pitch[j], yaw[k],roll[i],0, 0,X[l])
                        subprocess.run("./pipeline", shell=True)
