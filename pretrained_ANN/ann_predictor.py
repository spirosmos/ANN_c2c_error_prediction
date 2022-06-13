import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,Dropout
import pandas as pd
import numpy as np
import joblib
import sys


def main():


	#data_filename = "data_Woman_of_Pindos.csv"
	data_filename = sys.argv[1]

	input_data = pd.read_csv(data_filename)
	X_test = input_data.iloc[:,0:10]
	print(input_data.head())

	model = Sequential()
	model.add(Dense(128, input_dim=10, activation='relu'))
	model.add(Dense(128, activation='relu'))
	model.add(Dense(64, activation='relu'))
	model.add(Dropout(.1))
	model.add(Dense(1,activation = 'relu'))

	model.load_weights('trained_model.h5')
	scaler = joblib.load('Standard_Scaler.pkl', 'r')


	X_test = scaler.transform(X_test)
	c2c_predictions = model.predict(X_test)

	print("MEAN predicted dimensional error (mm): " + str(sum(c2c_predictions)[0] / len(c2c_predictions)))




	f_ply = open("predictedError.ply","w")
	f_ply.write("ply\nformat ascii 1.0\ncomment Error Extracted From ANN\nelement vertex " + str(X_test.shape[0]) + "\nproperty float x\nproperty float y\nproperty float z\nproperty float prediction_C2C\nend_header\n")

	XTest=np.array(input_data.iloc[:,0:3])
	for i in range(XTest.shape[0]):
		f_ply.write(str(XTest[i][0]) + " " + str(XTest[i][1])+ " " + str(XTest[i][2]) + " " + str(c2c_predictions[i][0]) + "\n")
	f_ply.close()

if __name__ == '__main__':
	main()
