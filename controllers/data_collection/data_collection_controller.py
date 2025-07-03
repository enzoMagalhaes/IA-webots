
from controller import Supervisor

sup = Supervisor()
timestep = int(sup.getBasicTimeStep())

robot = sup.getFromDef("MY_ROBOT")
if robot is None:
    raise RuntimeError("Robot DEF 'MY_ROBOT' not found!")

camera = sup.getDevice("camera")  
camera.enable(timestep)

lidar = sup.getDevice("lidar")
lidar.enable(timestep)

translation = robot.getField("translation")
rotation = robot.getField("rotation")

###############
import math
def distance(p1, p2):
    return math.sqrt(
        (p2[0] - p1[0]) ** 2 +
        (p2[1] - p1[1]) ** 2 +
        (p2[2] - p1[2]) ** 2
    )

# position, buffer
OBSTACLES_CENTERS = [
    [[1.81,-1.74,0.0999], 0.4],
    [[0.708,-1.38,0.43], 0.7],
    [[-0.591,-0.859,0.3], 0.65],
    [[-1.57,-1.45,0.3], 0.65],
    [[1.9,-0.726,0.3], 0.65],
    [[0.495,0.104,0.454], 0.75],
    [[-0.867,0.2,0.0999], 0.65],
    [[-1.25,0.461,0.3], 0.7],
    [[1.52,0.752,0.119], 0.65],
    [[1.14,1.38,0.25], 0.65],
    [[0.287,1.5,0.23], 0.65]
]

ANGLE_INC = 2*math.pi / 18 # 360 / 18 = 20 degres rotation
ROTATION_AXIS = [0, 0, 1] 


pos = [-1.81186, 1.83154, -0.00238899]
INITIAL_X = pos[0]
step = 0.2

res = []
while sup.step(timestep) != -1:
    too_near = False
    for obs_pos, obs_buff in OBSTACLES_CENTERS:
        if distance(pos, obs_pos) <= obs_buff:
            too_near = True
            break
    
    if not too_near:
        translation.setSFVec3f(pos)

        curr_rotation = rotation.getSFRotation()
        for i in range(18):
            rotation.setSFRotation(ROTATION_AXIS + [i*ANGLE_INC])
            sup.step(timestep)

            res.append({
                "img": camera.getImageArray(),
                "lidar": lidar.getRangeImage()
            })

    # update_position
    if pos[0] < 1.73:
        pos[0] += step
    else:    
        pos[0] = INITIAL_X        
        pos[1] -= step


    if pos[1] <= -2.16:
        break

import json
with open("output.json", "w") as f:
    json.dump(res, f)