from controller import Robot

from components.robot_controller import RobotActionController
from components.bayesian_network import BayesianNetwork, YELLOW_MAX_COLOR_DISTANCE
from components.cnn.model import CNN

robot = Robot()
timestep = int(robot.getBasicTimeStep())

camera = robot.getDevice("camera")
camera.enable(timestep)

lidar = robot.getDevice("lidar")
lidar.enable(timestep)

robot_controller = RobotActionController(robot, timestep)
bayesian_network = BayesianNetwork()
model = CNN()

while robot.step(timestep) != -1:
    img = camera.getImageArray()
    lidar_ranges = lidar.getRangeImage()

    dist, angle, yellow_distance = model.predict(img, lidar_ranges)

    if yellow_distance < YELLOW_MAX_COLOR_DISTANCE and dist < 0.3:
        break

    next_action = bayesian_network.next_action(dist, angle, yellow_distance)
    robot_controller.perform_action(next_action)

    print(next_action)
