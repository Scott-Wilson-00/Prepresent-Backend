import numpy as np
import argparse
import matplotlib.pyplot as plt
import cv2
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator
#from test_assets import asset_paths
import os
import json
import ffmpeg 
from decimal import Decimal, getcontext
getcontext().prec = 2

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# command line argument
ap = argparse.ArgumentParser()
ap.add_argument("--mode",help="train/display")
mode = ap.parse_args().mode

# plots accuracy and loss curves
def plot_model_history(model_history):
    """
    Plot Accuracy and Loss curves given the model_history
    """
    fig, axs = plt.subplots(1,2,figsize=(15,5))
    # summarize history for accuracy
    axs[0].plot(range(1,len(model_history.history['accuracy'])+1),model_history.history['accuracy'])
    axs[0].plot(range(1,len(model_history.history['val_accuracy'])+1),model_history.history['val_accuracy'])
    axs[0].set_title('Model Accuracy')
    axs[0].set_ylabel('Accuracy')
    axs[0].set_xlabel('Epoch')
    axs[0].set_xticks(np.arange(1,len(model_history.history['accuracy'])+1),len(model_history.history['accuracy'])/10)
    axs[0].legend(['train', 'val'], loc='best')
    # summarize history for loss
    axs[1].plot(range(1,len(model_history.history['loss'])+1),model_history.history['loss'])
    axs[1].plot(range(1,len(model_history.history['val_loss'])+1),model_history.history['val_loss'])
    axs[1].set_title('Model Loss')
    axs[1].set_ylabel('Loss')
    axs[1].set_xlabel('Epoch')
    axs[1].set_xticks(np.arange(1,len(model_history.history['loss'])+1),len(model_history.history['loss'])/10)
    axs[1].legend(['train', 'val'], loc='best')
    fig.savefig('plot.png')
    plt.show()

# Define data generators
# train_dir = 'data/train'
# val_dir = 'data/test'

# num_train = 28709
# num_val = 7178
# batch_size = 64
# num_epoch = 50

# train_datagen = ImageDataGenerator(rescale=1./255)
# val_datagen = ImageDataGenerator(rescale=1./255)

# train_generator = train_datagen.flow_from_directory(
#         train_dir,
#         target_size=(48,48),
#         batch_size=batch_size,
#         color_mode="grayscale",
#         class_mode='categorical')

# validation_generator = val_datagen.flow_from_directory(
#         val_dir,
#         target_size=(48,48),
#         batch_size=batch_size,
#         color_mode="grayscale",
#         class_mode='categorical')

# Create the model
def initialize():
    model = Sequential()

    model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(48,48,1)))
    model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(1024, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(7, activation='softmax'))

    model.load_weights('src/model.h5')
    return model

"""
# Function called by server once file is received from user POST request
def process_sentiment(fileName, file=None):
    # Create a VideoCapture object and read from file input
    cap = cv2.VideoCapture(fileName)
    fps = cap.get(cv2.CAP_PROP_FPS) # gets fps

    number_of_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) #gets no of frames

    length_of_video = number_of_frames/fps #gets length

    emotion_dict = {0: ["Angry", 0], 1: ["Disgusted", 0], 2: ["Fearful", 0], 3: ["Happy", 0], 
                    4: ["Neutral", 0], 5: ["Sad", 0], 6: ["Surprised", 0]}


    # Check if camera opened successfully
    if (cap.isOpened()== False):
        print("Error opening video file")
    
    # Read until video is completed
    while(cap.isOpened()):
        
    # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            #print("Can't receive frame (stream end?). Exiting ...")
            break

        facecasc = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = facecasc.detectMultiScale(gray,scaleFactor=1.3, minNeighbors=5)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y-50), (x+w, y+h+10), (255, 0, 0), 2)
            roi_gray = gray[y:y + h, x:x + w]
            cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray, (48, 48)), -1), 0)
            prediction = model.predict(cropped_img)
            maxindex = int(np.argmax(prediction))
            cv2.putText(frame, emotion_dict[maxindex][0], (x+20, y-60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

            emotion_dict[maxindex][1] += 1

        # Display the resulting frame     /// AKA apply model to frame
        cv2.imshow('Frame', frame)
            
        # Press Q on keyboard to exit // Should be taken out
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    
    # When everything done, release
    # the video capture object
    cap.release()
    
    # Closes all the frames
    cv2.destroyAllWindows()

    for key in range(len(emotion_dict)):
        print(emotion_dict[key])
"""

""" MAIN PROGRAM FOUND BELOW - mode=='upload' is for the file upload"""

emotion_dict = {0: ["Angry", 0], 1: ["Disgusted", 0], 2: ["Fearful", 0], 3: ["Happy", 0], 
                    4: ["Neutral", 0], 5: ["Sad", 0], 6: ["Surprised", 0]}

def calculate_emotions():
    emotions = get_emotions()
    totalFrames = 0
    for key in emotions:
        totalFrames += emotions[key][1]

    txt = "{val:.1f}"

    anger = emotions[0][1] / totalFrames * 100
    disgust = emotions[1][1] / totalFrames * 100
    fear = emotions[2][1] / totalFrames * 100
    happiness = emotions[3][1] / totalFrames * 100
    neutral = emotions[4][1] / totalFrames * 100
    sadness = emotions[5][1] / totalFrames * 100
    suprise = emotions[6][1] / totalFrames * 100

    anger = txt.format(val = anger)
    disgust = txt.format(val = disgust)
    fear = txt.format(val = fear)
    happiness = txt.format(val = happiness)
    neutral = txt.format(val = neutral)
    sadness = txt.format(val = sadness)
    suprise = txt.format(val = suprise)

    percentages = { "Angry": anger, 
                    "Disgusted": disgust,
                    "Fearful": fear, 
                    "Happy": happiness,
                    "Neutral": neutral , 
                    "Sad": sadness,
                    "Surprised": suprise 
                    }

    return percentages


def get_emotions():
    global emotion_dict
    res = emotion_dict.copy()
    emotion_dict = {0: ["Angry", 0], 1: ["Disgusted", 0], 2: ["Fearful", 0], 3: ["Happy", 0], 
                    4: ["Neutral", 0], 5: ["Sad", 0], 6: ["Surprised", 0]}
    return res

def process_sentiment():
    # model.load_weights('./model.h5')
    model = initialize()


    # prevents openCL usage and unnecessary logging messages
    cv2.ocl.setUseOpenCL(False)

    # dictionary which assigns each label an emotion (alphabetical order)
    #emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}
    global emotion_dict

    # start the webcam feed
    cap = cv2.VideoCapture(0)

    while True:
        # Find haar cascade to draw bounding box around face
        ret, frame = cap.read()

        if not ret:
            # Doesn't recieve frame, so ends stream
            print("doesn't receive it")
            break

        facecasc = cv2.CascadeClassifier('src/haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = facecasc.detectMultiScale(gray,scaleFactor=1.3, minNeighbors=5)

        for (x, y, w, h) in faces:
            # Prepares frame for the application of the model
            cv2.rectangle(frame, (x, y-50), (x+w, y+h+10), (255, 0, 0), 2)
            roi_gray = gray[y:y + h, x:x + w]
            cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray, (48, 48)), -1), 0)

            # Applies model and determines sentiment index
            prediction = model.predict(cropped_img)
            maxindex = int(np.argmax(prediction))

            """ Testing only! (Displays current emotion in real time)"""
            cv2.putText(frame, emotion_dict[maxindex][0], (x+20, y-60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

            # Updates the number of frames of the predicted sentiment

            emotion_dict[maxindex][1] += 1

        # cv2.imshow('Video', cv2.resize(frame,(1600,960),interpolation = cv2.INTER_CUBIC))
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield(b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    print(emotion_dict)
    return "hello"

# If you want to train the same model or try other models, go for this
if mode == "train":
    model = initialize()

    model.compile(loss='categorical_crossentropy',optimizer=Adam(lr=0.0001, decay=1e-6),metrics=['accuracy'])
    model_info = model.fit_generator(
            train_generator,
            steps_per_epoch=num_train // batch_size,
            epochs=num_epoch,
            validation_data=validation_generator,
            validation_steps=num_val // batch_size)
    plot_model_history(model_info)
    model.save_weights('model.h5')

# emotions will be displayed on your face from the webcam feed
elif mode == "display":
    process_sentiment()

elif mode=="upload":
    #process_sentiment(asset_paths.vid1)
    pass



