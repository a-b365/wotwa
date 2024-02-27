import tensorflow as tf
from keras.layers import Conv2D, UpSampling2D, BatchNormalization, Softmax, Conv2DTranspose, Dropout
from keras.models import Sequential

def dlModel(input_shape):
    model = Sequential()
    model.add(Conv2D(64, (3, 3), strides=1, padding="same", activation='relu',input_shape=input_shape))
    model.add(Conv2D(64, (3, 3), strides=2, padding="same", activation='relu'))
    model.add(BatchNormalization())

    model.add(Conv2D(128, (3, 3), strides=1, padding="same", activation='relu'))
    model.add(Conv2D(128, (3, 3), strides=2, padding="same", activation='relu'))
    model.add(BatchNormalization())

    model.add(Conv2D(256, (3, 3), strides=1, padding="same", activation='relu',kernel_regularizer =tf.keras.regularizers.l2( l=0.01)))
    model.add(Conv2D(256, (3, 3), strides=1, padding="same", activation='relu'))
    model.add(Conv2D(256, (3, 3), strides=2, padding="same", activation='relu'))
    model.add(BatchNormalization())

    model.add(Conv2D(512, (3, 3), strides=1, padding="same", activation='relu',kernel_regularizer =tf.keras.regularizers.l2( l=0.01)))
    model.add(Conv2D(512, (3, 3), strides=1, padding="same", activation='relu'))
    model.add(Conv2D(512, (3, 3), strides=1, padding="same", activation='relu'))
    model.add(BatchNormalization())

    model.add(Conv2D(512, (3, 3), strides=1, padding="same", dilation_rate=1, activation='relu',kernel_regularizer =tf.keras.regularizers.l2( l=0.01)))
    model.add(Conv2D(512, (3, 3), strides=1, padding="same", dilation_rate=1, activation='relu'))
    model.add(Conv2D(512, (3, 3), strides=1, padding="same", dilation_rate=1, activation='relu'))
    model.add(BatchNormalization())

    model.add(Conv2D(512, (3, 3), strides=1, padding="same", dilation_rate=1, activation='relu',kernel_regularizer =tf.keras.regularizers.l2( l=0.01)))
    model.add(Conv2D(512, (3, 3), strides=1, padding="same", dilation_rate=1, activation='relu'))
    model.add(Conv2D(512, (3, 3), strides=1, padding="same", dilation_rate=1, activation='relu'))
    model.add(BatchNormalization())

    model.add(Conv2D(256, (3, 3), strides=1, padding="same", activation='relu'))
    model.add(Conv2D(256, (3, 3), strides=1, padding="same", activation='relu'))
    model.add(Conv2D(256, (3, 3), strides=1, padding="same", activation='relu'))
    model.add(BatchNormalization())

    model.add(Conv2DTranspose(128, (3, 3), strides=2, padding="same", activation='relu'))
    model.add(Conv2D(128, (3, 3), strides=1, padding="same", activation='relu'))
    model.add(Conv2D(128, (3, 3), strides=1, padding="same", activation='relu'))
    model.add(BatchNormalization())

    model.add(Conv2D(313, (1, 1), strides=1, padding="valid"))
    model.add(Softmax(axis=1))
    model.add(Conv2D(2, (1,1), padding="valid", dilation_rate=1, strides=1))
    model.add(UpSampling2D(size=(4,4),interpolation="bilinear"))
            
    return model