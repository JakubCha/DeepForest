"""
Prediction module. This module consists of predict utility function for the deepforest class
"""
import numpy as np
import copy
import glob
import keras
import cv2
import pandas as pd

#Retinanet-viz
from keras_retinanet import models
from keras_retinanet.utils import image as keras_retinanet_image
from keras_retinanet.utils.visualization import draw_detections

def predict_image(model, image_path, score_threshold = 0.1, max_detections= 200, return_plot=True):
    """
    Predict an image
    return_plot: Logical. If true, return a image object, else return bounding boxes
    """
    #predict
    raw_image = cv2.imread(image_path)        
    image        = image_utils.preprocess_image(raw_image)
    image, scale = keras_retinanet_image.resize_image(image)

    if keras.backend.image_data_format() == 'channels_first':
        image = image.transpose((2, 0, 1))

    # run network
    boxes, scores, labels = model.predict_on_batch(np.expand_dims(image, axis=0))[:3]

    # correct boxes for image scale
    boxes /= scale

    # select indices which have a score above the threshold
    indices = np.where(scores[0, :] > score_threshold)[0]

    # select those scores
    scores = scores[0][indices]

    # find the order with which to sort the scores
    scores_sort = np.argsort(-scores)[:max_detections]

    # select detections
    image_boxes      = boxes[0, indices[scores_sort], :]
    image_scores     = scores[scores_sort]
    image_labels     = labels[0, indices[scores_sort]]
    image_detections = np.concatenate([image_boxes, np.expand_dims(image_scores, axis=1), np.expand_dims(image_labels, axis=1)], axis=1)

    if return_plot:
        draw_detections(raw_image, image_boxes, image_scores, image_labels, label_to_name=label_to_name, score_threshold=score_threshold)
        return raw_image                
    else:
        return image_boxes

def prediction_wrapper(image_path):
    ##read model
    config = read_config()        
    model = read_model(config["model_path"], config) 
    prediction = predict_image(model, image_path, score_threshold = 0.1, max_detections= 200,return_plot=True)
    save_name = os.path.splitext(image_path)[0] + "_prediction.jpg"
    cv2.imwrite(save_name,prediction)
    return(save_name)

def predict_all_images():
    """
    loop through a dir and run all images
    """
    #Read config
    config = read_config()

    #read model
    model = read_model(config["model_path"], config)
    tifs = glob.glob(os.path.join("data","**","*.tif"))
    for tif in tifs:
        print(tif)
        prediction = predict_image(model, tif, score_threshold = 0.1, max_detections= 200,return_plot=False)

        #reshape and save to csv
        df = pd.DataFrame(prediction)
        df.columns = ["xmin","ymin","xmax","ymax"]

        #save boxes
        file_path = os.path.splitext(tif)[0] + ".csv"
        df.to_csv(file_path)