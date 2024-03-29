#This code allows you to check the accuracy of the Face Recognition Code

import cv2, os
import numpy as np
from PIL import Image
faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

#Different face recognizing algorithms
#recognizer=cv2.face.createEigenFaceRecognizer()

#Using LBPH because it works with different image sizes too
recognizer = cv2.face.createLBPHFaceRecognizer()

#recognizer=cv2.face.createFisherFaceRecognizer()

def get_images_and_labels(path):
    image_paths = [os.path.join(path, f) for f in os.listdir(path) if not f.endswith('.sad')]

    # images will contains face images
    images = []

    # labels will contains the label that is assigned to the image
    labels = []

    for image_path in image_paths:

    	# convert the image to grayscale image for clarity and noise reduction
        image_pil = Image.open(image_path).convert('L')

        # Convert the image format into numpy array because furthur functions use this array to work on
        image = np.array(image_pil, 'uint8')

        # Get the label of the image
        label = int(os.path.split(image_path)[1].split(".")[0].replace("subject", ""))
        
        # Detect the face in the image, uses opencv function to do that
        faces = faceCascade.detectMultiScale(image,1.3)
        
        # If face is detected, append the face to images and the label to labels 
        # x,y  -->  Starting point or top-left corner of the face rectangle
        # w,h  -->  Height and width of the rectangle
        for (x, y, w, h) in faces:
            images.append(image[y: y + h, x: x + w])
            labels.append(label)
            cv2.imshow("Adding faces to traning set...", image[y: y + h, x: x + w])
            cv2.waitKey(50)

    # return the images list and labels list
    return images, labels

#Path to the Our Dataset, can also use Yale Dataset, but be careful for the image sizes
path = './yalefaces_centerlight'
path_test = './yalefaces_centerlight_test'
# Call the get_images_and_labels function and get the face images and the corresponding labels
images, labels = get_images_and_labels(path)
cv2.destroyAllWindows()

# Perform the tranining, also uses predefined function provided by opencv
recognizer.train(images, np.array(labels))

# Append the images with the extension .sad into image_paths
image_paths = [os.path.join(path_test, f) for f in os.listdir(path_test) if f.endswith('.sad')]

for image_path in image_paths:

	#same convert to grayscale
    predict_image_pil = Image.open(image_path).convert('L')
    
    #make an array of pixels of the image
    predict_image = np.array(predict_image_pil, 'uint8')
    
    #detect only the face in the picture and make an array
    faces = faceCascade.detectMultiScale(predict_image)

    for (x, y, w, h) in faces:

        #Uses opencv predefined function and returns outcome and the confidence of the outcome
        label_predicted, confidence = recognizer.predict(predict_image[y: y + h, x: x + w])

        label_actual = int(os.path.split(image_path)[1].split(".")[0].replace("subject", ""))
        
        if label_actual == label_predicted:
            print "{} is Correctly Recognized as {}".format(label_actual, label_predicted)
        else:
            print "{} is Incorrect Recognized as {}".format(label_actual, label_predicted)
        
        #Shows the face currently recognizing
        cv2.imshow("Recognizing Face", predict_image[y: y + h, x: x + w])
        cv2.waitKey(1000)
