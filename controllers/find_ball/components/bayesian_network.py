# TODO: CHANGE THIS TO A REAL BAYESIAN NETWORK STRUCTURE!!!! ( BUILD A TABLE OR USE A BAYESIAN NETWORK FRAMEWORK)

YELLOW_MAX_COLOR_DISTANCE = 100

class BayesianNetwork:
    def __init__(self):
        self.success_cpt = {
            (True, True, -1, -1): 0.9,
            (True, True, -1, 0): 0.5,
            (True, True, -1, 1): 0.1,
            (True, True, 0, -1): 0.5,
            (True, True, 0, 0): 0.9,
            (True, True, 0, 1): 0.5,
            (True, True, 1, -1): 0.1,
            (True, True, 1, 0): 0.5,
            (True, True, 1, 1): 0.9,
            (True, False, -1, -1): 0.1,
            (True, False, -1, 0): 0.5,
            (True, False, -1, 1): 0.8,
            (True, False, 0, -1): 0.5,
            (True, False, 0, 0): 0.1,
            (True, False, 0, 1): 0.5,
            (True, False, 1, -1): 0.8,
            (True, False, 1, 0): 0.5,
            (True, False, 1, 1): 0.1,
            (False, True, -1, -1): 0.5,
            (False, True, -1, 0): 0.7,
            (False, True, -1, 1): 0.5,
            (False, True, 0, -1): 0.5,
            (False, True, 0, 0): 0.7,
            (False, True, 0, 1): 0.5,
            (False, True, 1, -1): 0.5,
            (False, True, 1, 0): 0.7,
            (False, True, 1, 1): 0.5,
            (False, False, -1, -1): 0.5,
            (False, False, -1, 0): 0.7,
            (False, False, -1, 1): 0.5,
            (False, False, 0, -1): 0.5,
            (False, False, 0, 0): 0.7,
            (False, False, 0, 1): 0.5,
            (False, False, 1, -1): 0.5,
            (False, False, 1, 0): 0.7,
            (False, False, 1, 1): 0.5,
        }

    def obstacle_detected(self, dist):
        return dist < 0.4

    def direction(self, angle):
        if angle <= 30:
            return -1
        elif angle <= 60:
            return 0
        else:
            return 1

    def target_visible(self, is_yellow):
        return is_yellow < YELLOW_MAX_COLOR_DISTANCE

    def next_action(self, dist, angle, is_yellow):
        obstacle_detected = self.obstacle_detected(dist)
        direction = self.direction(angle)
        target_visible = self.target_visible(is_yellow)

        mx_action = [None, 0]
        for action in range(-1, 2):
            success_probability = self.success_cpt[
                (obstacle_detected, target_visible, direction, action)
            ]
            if success_probability > mx_action[1]:
                mx_action = [action, success_probability]
        return mx_action[0]
