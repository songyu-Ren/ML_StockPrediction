import math
import pandas_datareader as web
import numpy as np 
import pandas as pd 
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM
import matplotlib.pyplot as plt 
plt.style.use("fivethirtyeight")

df=web.DataReader("AAPL", data_source="yahoo", start="2012-01-01", end='2022-10-18')

plt.figure(figsize=(16,8))
plt.title("Clos price history")
plt.plot(df['Close'])
plt.xlabel('Data', fontsize=18)
plt.ylabel('Close price usd', fontsize=18)
# plt.show()

data=df.filter(['Close'])
dataset=data.values
#get the number of rows to train the model on 

training_data_len=math.ceil(len(dataset)* 0.8)

# print(training_data_len)

scaler=MinMaxScaler(feature_range=(0,1))
scaled_data=scaler.fit_transform(dataset)


# Create the training data set
# Create the scaled training data set

train_data=scaled_data[0:training_data_len, :]

# print(len(train_data))

#Splite the data into X_train and Y_train data sets

X_train=[]
Y_train=[]

for i in range(60, len(train_data)):
    X_train.append(train_data[i-60:i, 0])
    Y_train.append(train_data[i,0])
    if i<61 :
        print(X_train)
        print(Y_train)

X_train,Y_train=np.array(X_train), np.array(Y_train)

X_train=np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

#build the LSTM model

model=Sequential()
model.add(LSTM(50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
model.add(LSTM(50, return_sequences=False))
model.add(Dense(25))
model.add(Dense(1))

#Compile the model
model.compile(optimizer="adam", loss='mean_squared_error')

#Train the model
model.fit(X_train, Y_train, batch_size=1, epochs=3)

#Create the testing data set
#create a new array contining scaled values 
test_data=scaled_data[training_data_len -60 :, :]

#Create the data sets x test and y_test
X_test = []
Y_test = dataset [training_data_len:, :]
for i in range(60, len(test_data)):
    X_test.append(test_data[i-60:i, 0])

#Convert the data to a numpy array
X_test=np.array(X_test)

#reshep the data
X_test=np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

# Get the models predicted price values
predictions=model.predict(X_test)
predictions=scaler.inverse_transform(predictions)

#Get the root mean squard error (RMSE)
rmse=np.sqrt(np.mean(((predictions- Y_test)**2)))

print(rmse)

train=data[: training_data_len]
valid =data[training_data_len:]
valid["Predictions"]=predictions
plt.figure(figsize=(16,8))
plt.title("Model")
plt.xlabel("date", fontsize=18)
plt.ylabel('close price usd')
plt.plot(train['Close'])
plt.plot(valid[["Close", "Predictions"]])
plt.legend(['Train', 'Val', 'Predictions'], loc='lower right')
plt.show()
print(valid)

#Save trained model
model.save(r'C:\Users\songyu.ren\Downloads\Self_learning\ML_stockPredictioni\m1.h5')


apple_quote=web.DataReader('AAPL', data_source='yahoo',
 start='2012-01-01', end='2022-10-18')

new_df=apple_quote.filter(['Close'])

last_60_days=new_df[-60:].values

last_60_days_scaled=scaler.transform(last_60_days)

X_test_New=[]
X_test_New.append(last_60_days_scaled)
X_test_New=np.array(X_test_New)
X_test_New=np.reshape(X_test_New, (X_test_New.shape[0], X_test_New.shape[1], 1))

#Get the predicted scale price
pred_price=model.predict(X_test_New)
pred_price=scaler.inverse_transform(pred_price)
print(pred_price)


print('exit 0')
