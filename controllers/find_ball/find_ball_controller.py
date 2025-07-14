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

def get_next_action():
    img = camera.getImageArray()
    lidar_ranges = lidar.getRangeImage()
    dist, angle, yellow_distance = model.predict(img, lidar_ranges)

    if yellow_distance < YELLOW_MAX_COLOR_DISTANCE and dist < 0.050:
        return "stop"
    return bayesian_network.next_action(dist, angle, yellow_distance)

def run():
    while robot.step(timestep) != -1:
        action = get_next_action()
        if action == "stop":
            return

        if action != 0:
            next_action = action
            while next_action != 0:
                robot_controller.perform_action(action)
                next_action = get_next_action()
                if next_action == "stop":
                    return    
        else:
            robot_controller.perform_action(action)
run()