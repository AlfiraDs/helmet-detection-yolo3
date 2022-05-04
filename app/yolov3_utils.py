import os
import sys
import json
import cv2
import numpy as np

CONFIDENCE = 0.5
IOU_THRESHOLD = 0.5
SCORE_THRESHOLD = 0.5
labels = open("app/model/helmet.names").read().strip().split("\n")
weights = "app/model/yolov3-tiny-obj_1000.weights"
config_path = "app/model/yolov3-tiny-obj.cfg"


net = cv2.dnn.readNetFromDarknet(config_path, weights)

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)

def model_output(path_name):
    # image = cv2.imread(path_name)
    h,w = path_name.shape[:2]
    
    '''
    
    cv2.dnn.blobFromImage function is used for preprocessing required before sending it to dnn model. It does mean_subtraction
    (taking out mu_red, mu_green and mu_blue and subtarcting from each pixel values.) , centre cropping,
     changing it to size we want...here...(416,416)
    Also scaling is done(1/sigma), ...here...1/255.0 is the sacle factor...
    
    '''
    
    blob = cv2.dnn.blobFromImage(path_name, 1/255.0,(416,416), swapRB = True, crop = False)
    
    net.setInput(blob)  # Sets the new input value for the network
    
    ln = net.getLayerNames()
    ln = [ln[i- 1] for i in net.getUnconnectedOutLayers()]  #ln is a list comprsisng all models in config file
    layer_outputs = net.forward(ln)
    boxes, confidences, class_ids = [], [], []
    for output in layer_outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence>CONFIDENCE:
                box = detection[:4]*np.array([w,h,w,h])
                (centerX, centerY, width, height) = box.astype("int")
                x = int(centerX - (width/2))
                y = int(centerY - (height/2))
                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                class_ids.append(class_id)
    return boxes, confidences, class_ids

def detection_recognition(path_name):
    # image = cv2.imread(path_name)
    boxes, confidences, class_ids = model_output(path_name)
    idxs = cv2.dnn.NMSBoxes(boxes, confidences, SCORE_THRESHOLD, IOU_THRESHOLD)
    text = f"{labels[class_ids[0]]}:{confidences[0]:.2f}"
    # print(text)
    
    result = json.dumps({"bboxes":boxes, "confidence":confidences, "class_ids":class_ids, "index":idxs.tolist()}, cls=NpEncoder) #})

    # print(result)
    return result
    # font_scale = 1
    # thickness= 1
    # if len(idxs)>0:
    #     for i in idxs.flatten():
    #         x, y, w, h = boxes[i][0], boxes[i][1], boxes[i][2], boxes[i][3]
    #         print(x,y,w,h)
    #         cv2.rectangle(image, (x,y), (x+w, y+h), color = (255,20,147), thickness = thickness)
    #         text = f"{labels[class_ids[i]]}:{confidences[i]:.2f}"
    #         (text_width, text_height) = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, fontScale = font_scale, thickness = thickness)[0]
    #         text_offset_x = x
    #         text_offset_y = y - 5
    #         box_coords = ((text_offset_x, text_offset_y), (text_offset_x + text_width + 2, text_offset_y - text_height))
    #         overlay = image.copy()
    #         cv2.rectangle(overlay, box_coords[0], box_coords[1], color = (255,20,147), thickness = cv2.FILLED)
    #         image = cv2.addWeighted(overlay, 0.6, image, 0.4, 0)
    #         cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,
    #         fontScale=font_scale, color=(0, 0, 0), thickness=thickness)
    # plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    # plt.show()