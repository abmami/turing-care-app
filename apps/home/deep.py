import numpy as np
import tensorflow as tf
from tensorflow import keras

# Display
from IPython.display import Image, display
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from PIL import Image as im
from django.core.files.storage import FileSystemStorage

def get_img_array(img_path, size):
    # `img` is a PIL image of size 299x299
    img = keras.preprocessing.image.load_img(img_path, target_size=size)
    # `array` is a float32 Numpy array of shape (299, 299, 3)
    array = keras.preprocessing.image.img_to_array(img)
    # We add a dimension to transform our array into a "batch"
    # of size (1, 299, 299, 3)
    array = np.expand_dims(array, axis=0)
    return array


def make_gradcam_heatmap(img_array, model, last_conv_layer_name, pred_index=None):
    # First, we create a model that maps the input image to the activations
    # of the last conv layer as well as the output predictions
    grad_model = tf.keras.models.Model(
        [model.inputs], [model.get_layer(last_conv_layer_name).output, model.output]
    )

    # Then, we compute the gradient of the top predicted class for our input image
    # with respect to the activations of the last conv layer
    with tf.GradientTape() as tape:
        last_conv_layer_output, preds = grad_model(img_array)
        if pred_index is None:
            pred_index = tf.argmax(preds[0])
        class_channel = preds[:, pred_index]

    # This is the gradient of the output neuron (top predicted or chosen)
    # with regard to the output feature map of the last conv layer
    grads = tape.gradient(class_channel, last_conv_layer_output)

    # This is a vector where each entry is the mean intensity of the gradient
    # over a specific feature map channel
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

    # We multiply each channel in the feature map array
    # by "how important this channel is" with regard to the top predicted class
    # then sum all the channels to obtain the heatmap class activation
    last_conv_layer_output = last_conv_layer_output[0]
    heatmap = last_conv_layer_output @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)

    # For visualization purpose, we will also normalize the heatmap between 0 & 1
    heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
    return heatmap.numpy()



def make_overlay(img_path, heatmap, cam_path="cam.jpg", alpha=0.4):
    # Load the original image
    img = keras.preprocessing.image.load_img(img_path)
    img = keras.preprocessing.image.img_to_array(img)

    # Rescale heatmap to a range 0-255
    heatmap = np.uint8(255 * heatmap)

    # Use jet colormap to colorize heatmap
    jet = cm.get_cmap("jet")

    # Use RGB values of the colormap
    jet_colors = jet(np.arange(256))[:, :3]
    jet_heatmap = jet_colors[heatmap]

    # Create an image with RGB colorized heatmap
    jet_heatmap = keras.preprocessing.image.array_to_img(jet_heatmap)
    jet_heatmap = jet_heatmap.resize((img.shape[1], img.shape[0]))
    jet_heatmap = keras.preprocessing.image.img_to_array(jet_heatmap)

    # Superimpose the heatmap on original image
    superimposed_img = jet_heatmap * alpha + img
    superimposed_img = keras.preprocessing.image.array_to_img(superimposed_img)

    # Save the superimposed image
    #fs = FileSystemStorage()
    #x = fs.save("temp/1.png", im.fromarray(array)
    #superimposed_img.save(fs.location+"/temp/"+cam_path)

    # Display Grad CAM
    #display(Image(cam_path))
    #x = Image.load(fs.location+"/temp/"+cam_path)
    return superimposed_img



def ProcessImg(img):
    rgb_weights = [0.2989, 0.5870, 0.1140]
    imgGray = np.dot(img[...,:3], rgb_weights)
    img_4d = imgGray.reshape(-1,150,150,1)
    img_4d /= 255.0
    return img_4d



def predict_image(model,img):
  class_names = ['covid19','normal','pneumonia','tuberculosis']
  rgb_weights = [0.2989, 0.5870, 0.1140]
  imgGray = np.dot(img[...,:3], rgb_weights)
  img_4d = imgGray.reshape(-1,150,150,1)
  img_4d /= 255.0
  prediction=model.predict(img_4d)[0]
  preds = {class_names[i]: float(prediction[i])*100 for i in range(4)}
  return preds




def toGRADCAM(img_path, model):
    img_size = (150, 150)
    img_array = ProcessImg(get_img_array(img_path,size=img_size)) #process image (grayscale+resize+rescale)
    last_conv_layer_name = 'conv2d_2' # ['conv2d','conv2d_1','conv2d_2', 'conv2d_3'] list of conv2dLayers
    model1 = model
    # Remove last layer's softmax
    model1.layers[-1].activation = None
    heatmap = make_gradcam_heatmap(img_array, model1, last_conv_layer_name)
    return make_overlay(img_path,heatmap)
