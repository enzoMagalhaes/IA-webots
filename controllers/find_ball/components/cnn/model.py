from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, Flatten, Dense, Concatenate

import numpy as np
def preprocessing(img, lidar, single=False):
    if single:
        img = [img]
        for i in range(len(lidar)):
            lidar[i] = min(5, lidar[i])
        lidar = [lidar]

    return np.array(img) / 255, np.array(lidar) / 5


class CNN():
    def __init__(self, image_shape=(64, 64, 3), lidar_shape=(128,)):
        # Entrada imagem
        image_input = Input(shape=image_shape, name='image_input')
        x = Conv2D(32, (3, 3), activation='relu')(image_input)
        x = MaxPooling2D((2, 2))(x)
        x = Conv2D(64, (3, 3), activation='relu')(x)
        x = MaxPooling2D((2, 2))(x)
        x = Flatten()(x)

        # Entrada LIDAR
        lidar_input = Input(shape=lidar_shape, name='lidar_input')
        y = Dense(64, activation='relu')(lidar_input)

        # Concatenação
        combined = Concatenate()([x, y])
        z = Dense(64, activation='relu')(combined)
        z = Dense(32, activation='relu')(z)

        # Saídas contínuas
        dist_output = Dense(1, name='distance')(z)
        angle_output = Dense(1, name='angle')(z)
        yellow_distance = Dense(1, name='yellow_distance')(z)


        model = Model(inputs=[image_input, lidar_input], outputs=[dist_output, angle_output, yellow_distance])
        model.compile(optimizer='adam', loss='mse', metrics=['mae', 'mae', 'mae'])

        model.load_weights("data/weights.h5")
        self.model = model

    def predict(self,img,lidar):
        img,lidar =  preprocessing(img,lidar, single=True)
        pdist,pangle,pyellow_distance = self.model.predict([img,lidar])
        return pdist.item(),pangle.item(),pyellow_distance.item()
