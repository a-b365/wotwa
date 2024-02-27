import base64
import numpy as np
import io
import os
import pickle
import tensorflow as tf
import matplotlib.pyplot as plt
from skimage.color import rgb2lab, lab2rgb
from skimage.transform import resize
from .colorizer import dlModel
from PIL import ImageDraw,ImageFont

animals = {

	'0':"Wildebeest",
	'1':'Elephant',
	'2':'Rhino',
	'3':'Zebra'
}


def preprocess(path):
	augs_datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale = 1. / 255, validation_split=0.1)
	train = augs_datagen.flow_from_directory(path,target_size=(224,224),batch_size=24,class_mode=None,shuffle=True,subset='training')
	return train

def cvrt2lab():
	X =[]
	Y =[]
	for img in preprocess(os.environ['MEDIA_DIR'])[0]:
		try:
			lab = rgb2lab(img)
			X.append(lab[:,:,0])
			Y.append(lab[:,:,1:]/128)
		except:
			print('Error Occured while converting RGB to LAB color space.')

	X = np.array(X)
	Y = np.array(Y)
	X = X.reshape(X.shape+(1,))
	return X,Y

def performanceGraph(history):
    
    accuracy = history.history['accuracy']
    loss = history.history['loss']
    val_loss = history.history['val_loss']
    val_accuracy = history.history['val_accuracy']
    
    epochs_range=range(100)

    plt.subplot(1, 2, 1)
    plt.plot(epochs_range, accuracy, label='Training Accuracy')
    plt.plot(epochs_range, val_accuracy, label='Validation Accuracy')
    plt.legend(loc='lower right')
    plt.title('Training and Validation Accuracy')

    plt.subplot(1, 2, 2)
    plt.plot(epochs_range, loss, label='Training Loss')
    plt.plot(epochs_range, val_loss, label='Validation Loss')
    plt.legend(loc='upper right')
    plt.title('Training and Validation Loss')
    plt.show()

def CompileModel(modelName):

	model = dlModel((224,224,1))
	X,Y = cvrt2lab()
	model.compile(optimizer="adam", loss="mse" , metrics=['accuracy'])
	history = model.fit(X,Y,epochs=100,batch_size=24)
	performanceGraph(history) #Creates performanceGraph
	model.save(modelName)

def loadModel(modelName):
	return tf.keras.models.load_model(modelName,compile=True)

def cvrt2rgb(filepath,modelName):
	#Test the Grayscale Image
	model = loadModel(os.environ['MODELS_DIR'] + modelName)
	img = tf.keras.utils.load_img(filepath).resize((224,224))
	img_2_array = tf.keras.utils.img_to_array(img)/255.0
	output = model.predict(img_2_array.reshape(-1,224,224,3))
	(x,y,width,height) = output[1][0]
	draw = ImageDraw.Draw(img)
	draw.rectangle(((x-width/2)*224, (y-height/2)*224, (x+width/2)*224, (y+height/2)*224),fill=None, outline="red",width=2)
	draw.text((width*224/2,height*224/2),animals[str(np.argmax(output[0][0]))],fill="blue")
	buffer = io.BytesIO() #Creates a memory buffer
	img.save(buffer,format='JPEG') #Saves the image in buffer with supportable formats
	byte_im = buffer.getvalue()
	result = base64.b64encode(byte_im).decode('utf-8') #b64 encoding
	return result

def rgb2cvrt(filepath,modelName):
	kmeans = pickle.load(open(os.environ['MODELS_DIR'] + modelName,'rb'))
	img = tf.keras.utils.load_img(filepath).resize((224,224))
	img_2_array = tf.keras.utils.img_to_array(img)/255.0
	output = kmeans.predict(img_2_array.reshape(-1,3))
	recovered_image = kmeans.cluster_centers_[output,:]
	rimg_2_array = recovered_image.reshape(224,224,3)*255.0
	rimg = tf.keras.utils.array_to_img(rimg_2_array)
	buffer = io.BytesIO() #Creates a memory buffer
	rimg.save(buffer,format='JPEG') #Saves the image in buffer with supportable formats
	byte_im = buffer.getvalue()
	result = base64.b64encode(byte_im).decode('utf-8') #b64 encoding
	return result