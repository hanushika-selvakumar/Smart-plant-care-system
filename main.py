import cv2
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras.models import load_model

model = load_model('efficientnet.h5')

# Disease classes
disease_classes = {
    0: 'Aphids',
    1: 'Armyworm',
    2: 'Beetle',
    3: 'Bollworm',
    4: 'Grasshopper',
    5: 'Mites',
    6: 'Mosquito',
    7: 'Sawfly',
    8: 'Stem_borer',
}

video = cv2.VideoCapture('jpg_0.jpg')
while True:
    ret, frame = video.read()
    if not ret:
        break
    
    img = cv2.resize(frame, (300, 300))
    a = tf.keras.preprocessing.image.img_to_array(img)
    a = np.expand_dims(a, axis=0)
    imag = np.vstack([a])
    predict = model.predict(imag)
    classes = np.argmax(predict)
    print(classes)
#     if classes == 0 or 1 or 2 or 3 or 4 or 5 or 6 or 7 or 8:
#         GPIO.output(relay_plant, GPIO.HIGH)
#         sleep(1)
#         GPIO.output(relay_plant, GPIO.LOW)
#         sleep(1)
    text = disease_classes[classes]
    print(text)
    # Draw text on the frame
    cv2.putText(frame, text, (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.25, (255, 255, 0), 3)
    cv2.imshow('Smart Plant Care System', frame)

    if cv2.waitKey(1) == ord('q'):
        break

video.release()
cv2.destroyAllWindows()

