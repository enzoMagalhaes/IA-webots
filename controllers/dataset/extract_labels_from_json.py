import json
import os
import numpy as np
import cv2
import pandas as pd  
import math


OUTPUT_FOLDER = "dataset"
os.makedirs(f"{OUTPUT_FOLDER}/images", exist_ok=True)
os.makedirs(f"{OUTPUT_FOLDER}/lidar", exist_ok=True)

with open("output.json", "r") as f:
    data = json.load(f)


INITIAL_X = -1.81186
INITIAL_Y = 1.83154
STEP = 0.2
ANGLE_INC = 2 * math.pi / 18


robot_positions = []
x, y = INITIAL_X, INITIAL_Y
for j in range(12): 
    for i in range(18):  
        for k in range(int((1.73 - INITIAL_X) // STEP) + 1):
            robot_positions.append((x + k*STEP, y - j*STEP, i * ANGLE_INC))

# Definindo onde está o alvo
TARGET_POS = [0.0, 0.0, 0.2] 

def euclidean(p1, p2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))

def angle_to_target(robot_pos, target_pos, yaw_rad):
    dx = target_pos[0] - robot_pos[0]
    dy = target_pos[1] - robot_pos[1]
    target_angle = math.atan2(dy, dx)
    angle_diff = target_angle - yaw_rad
    angle_diff = (angle_diff + math.pi) % (2 * math.pi) - math.pi  
    return math.degrees(angle_diff)


labels = []
for idx, (entry, (x, y, yaw)) in enumerate(zip(data, robot_positions)):
    # Salvar imagem
    img_array = np.array(entry["img"], dtype=np.uint8)
    img_array = cv2.resize(img_array, (64, 64))
    img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    img_path = os.path.join(OUTPUT_FOLDER, "images", f"{idx:04}.png")
    cv2.imwrite(img_path, img_bgr)

    # Salvar LIDAR
    lidar_array = np.array(entry["lidar"], dtype=np.float32)
    np.save(os.path.join(OUTPUT_FOLDER, "lidar", f"{idx:04}.npy"), lidar_array)

    # Calcular labels
    dist = np.min(lidar_array)
    angle = angle_to_target([x, y], TARGET_POS[:2], yaw)

    labels.append({"id": int(i), "distance": dist, "angle": angle})

# Salvar CSV
df = pd.DataFrame(labels)
df.to_csv(os.path.join(OUTPUT_FOLDER, "labels.csv"), index=False)
print(f"Exported {len(labels)} samples.")
