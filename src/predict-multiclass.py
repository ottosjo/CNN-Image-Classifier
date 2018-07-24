
import os
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
#os.environ["CUDA_VISIBLE_DEVICES"] = "0"        # specify gpu numbers to use
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"        # specify gpu numbers to use

import numpy as np
from keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
from keras.models import Sequential, load_model

img_width, img_height = 150, 150
model_path = './models/model.h5'
model_weights_path = './models/weights.h5'
model = load_model(model_path)
model.load_weights(model_weights_path)

def predict(file):
  x = load_img(file, target_size=(img_width, img_height))
  x = img_to_array(x)
  x = np.expand_dims(x, axis=0)
  array = model.predict(x)
  result = array[0]
  answer = np.argmax(result)
  # during training the classification number is dependent on the name of the folders
  # hence, the order of the prediction must 
  if answer == 0:
    print("  => Prediction: Pizza")
  elif answer == 1:
    print("  => Prediction: Plane")
  elif answer == 2:
    print("  => Prediction: Poodle")

  return answer

test_failures = []
pizza_t = 0
pizza_f = 0
poodle_t = 0
poodle_f = 0
plane_t = 0
plane_f = 0

print("Label: Pizza")
for i, ret in enumerate(os.walk('./images/test/pizza')):
  for i, filename in enumerate(ret[2]):
    if filename.startswith("."):
      continue
    result = predict(ret[0] + '/' + filename)
    if result == 0:
      pizza_t += 1
    else:
      pizza_f += 1
      test_failures.append(filename)

print("Label: Plane")
for i, ret in enumerate(os.walk('./images/test/plane')):
  for i, filename in enumerate(ret[2]):
    if filename.startswith("."):
      continue
    result = predict(ret[0] + '/' + filename)
    if result == 1:
      plane_t += 1
    else:
      plane_f += 1
      test_failures.append(filename)

print("Label: Poodle")
for i, ret in enumerate(os.walk('./images/test/poodle')):
  for i, filename in enumerate(ret[2]):
    if filename.startswith("."):
      continue
    result = predict(ret[0] + '/' + filename)
    if result == 2:
      poodle_t += 1
    else:
      poodle_f += 1
      test_failures.append(filename)

"""
Check metrics
"""
print("True Pizza: ", pizza_t)
print("False Pizza: ", pizza_f)
print("True Poodle: ", poodle_t)
print("False Poodle: ", poodle_f)
print("True Plane: ", plane_t)
print("False Plane: ", plane_f)

print("\nTest failures:")
for f in test_failures: print (f)