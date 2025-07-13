import math

DEFAULT_YELLOW = [255, 170, 0]

def minimum_distance_idx(lidar):
    min_i = 0
    for i in range(1,len(lidar)):
        if lidar[i] < lidar[min_i]:
            min_i = i
    return min_i

def distance(p1, p2):
    return math.sqrt(
        (p2[0] - p1[0]) ** 2 +
        (p2[1] - p1[1]) ** 2 +
        (p2[2] - p1[2]) ** 2
    )

def infer_values(img,lidar):
    idx = minimum_distance_idx(lidar)

    angle = (idx/128)*90

    pixel_idx = int((idx/128)*64)
    middle_pixel = img[32][pixel_idx]
    is_yellow = distance(DEFAULT_YELLOW, middle_pixel)

    return lidar[idx], angle, is_yellow


