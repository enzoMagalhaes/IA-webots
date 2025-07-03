# TODO: CHANGE THIS TO A REAL BAYESIAN NETWORK STRUCTURE!!!! ( BUILD A TABLE OR USE A BAYESIAN NETWORK FRAMEWORK)

YELLOW_MAX_COLOR_DISTANCE = 100

class BayesianNetwork:
    # left = -1 , forward = 0, right = 1
    def __init__(self):
        # (obstacle_detected, target_visible, direction, action) -> success
        self.success_cpt = {}
        for obstacle_detected in (True, False):
            for target_visible in (True, False):
                for direction in range(-1,2):
                    for action in range(-1,2):
                        prob = 0.5

                        # if obstacle was detected and it is not the target, go to the opposite direction
                        if obstacle_detected:
                            if not target_visible:
                                if direction == action:
                                    prob = 0.1
                                elif direction == -action:
                                    prob = 0.8
                            else:
                                if direction == action:
                                    prob = 0.9
                                elif direction == -action:
                                    prob = 0.1
                        else:
                            if action == 0:
                                prob = 0.7

                        self.success_cpt[(obstacle_detected, target_visible, direction, action)] = prob
                                
    def obstacle_detected(self, dist):
        return dist < 0.4

    def direction(self,angle):
        if angle <= 30:
            return -1
        elif angle <= 60:
            return 0
        else:
            return 1

    def target_visible(self,is_yellow):
        return is_yellow < YELLOW_MAX_COLOR_DISTANCE
    
    def next_action(self, dist,angle,is_yellow):
        obstacle_detected = self.obstacle_detected(dist)
        direction = self.direction(angle)
        target_visible = self.target_visible(is_yellow)
        
        mx_action = [None, 0]
        for action in range(-1,2):
            success_probability = self.success_cpt[(obstacle_detected, target_visible, direction, action)]
            if success_probability > mx_action[1]:
                mx_action = [action, success_probability]
        return mx_action[0]