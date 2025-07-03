class RobotActionController:
    def __init__(self,robot, timestep):
        self.consecutive_rotations = 0 # to handle robot stuck between two near obstacles

        self.robot = robot
        self.timestep = timestep
        self.motors = {
                "front_left": self.robot.getDevice("front left wheel"),
                "back_left": self.robot.getDevice("back left wheel"),
                "front_right": self.robot.getDevice("front right wheel"),
                "back_right": self.robot.getDevice("back right wheel")
        }

        # set motor velocities to control
        for motor in self.motors.values():
            motor.setPosition(float('inf'))

    def rotate(self, left=True, angle= 3.14159 / 4, angular_speed=0.5):
        self.consecutive_rotations +=1

        if left:
            left_speed = -angular_speed
            right_speed = angular_speed
        else:
            left_speed = angular_speed
            right_speed = -angular_speed

        self.motors["front_left"].setVelocity(left_speed)
        self.motors["back_left"].setVelocity(left_speed)
        self.motors["front_right"].setVelocity(right_speed)
        self.motors["back_right"].setVelocity(right_speed)

        duration = (angle * self.consecutive_rotations) / angular_speed # angle of rotation increases with number of consecutive rotations
        steps = int((duration * 1000) / self.timestep)
        for _ in range(steps):
            self.robot.step(self.timestep)

    def move_forward(self, distance_meters):
        self.consecutive_rotations = 0 # to handle robot stuck between two near obstacles

        WHEEL_RADIUS = 0.0975  # meters
        ANGULAR_VELOCITY = 6.4  # rad/s

        time_seconds = distance_meters / (ANGULAR_VELOCITY * WHEEL_RADIUS)
        steps = int((time_seconds * 1000) / self.timestep)

        for motor in self.motors.values():
            motor.setVelocity(ANGULAR_VELOCITY)

        for _ in range(steps):
            self.robot.step(self.timestep)

    def perform_action(self,action):
        if action == 0:
            self.move_forward(distance_meters=0.1)
        elif action -1:
            self.rotate(left=True)
        else:
            self.rotate(left=False)

        # stop motors after performing action
        for motor in self.motors.values():
            motor.setVelocity(0)        