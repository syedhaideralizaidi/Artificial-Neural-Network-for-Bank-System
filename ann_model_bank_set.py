# -*- coding: utf-8 -*-
"""ANN Model Bank Set.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1b0PgEQN7HZec-yCw1I1uvFijQqLJ3auT
"""

from google.colab import drive
drive.mount('/content/drive')

import tensorflow as tf
import numpy as np
import pandas as pd

tf.__version__

"""***Part1 - Data Preprocessing***"""

dataset=pd.read_csv('/content/drive/MyDrive/Colab Notebooks/Churn_Modelling.csv')
X=dataset.iloc[:,3:-1].values
y=dataset.iloc[:,-1].values
print("x", X)
print("y",y)

"""*Encoding Categorical Data*

--- Label encoding Gender column
"""

from sklearn.preprocessing import LabelEncoder
le=LabelEncoder()
X[:,2]=le.fit_transform(X[:,2]) 
print(X)

"""-- One Hot Encoding Geography column"""

from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer

ct= ColumnTransformer(transformers=[('encoder', OneHotEncoder(), [1])], remainder='passthrough')
X=np.array(ct.fit_transform(X))

print(X)

"""*Splitting the dataset into Training and Test set*"""

from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=0)

"""*Feature Scaling*"""

from sklearn.preprocessing import StandardScaler
sc=StandardScaler()
X_train=sc.fit_transform(X_train)
X_test=sc.fit_transform(X_test)

"""***Part 2 - Building ANN***

*Initializing an ANN*
"""

ann = tf.keras.models.Sequential()

"""*Add Input layer and first Hiddem layer in the network*"""

ann.add(tf.keras.layers.Dense(units=6,activation='relu'))

"""Add second hidden layer in the network"""

ann.add(tf.keras.layers.Dense(units=6,activation='relu'))

"""Adding the output"""

ann.add(tf.keras.layers.Dense(units=1,activation='sigmoid'))

"""***Part3 - Training the ANN***

*Compiling the ANN*
"""

ann.compile(optimizer= 'adam' ,loss= 'binary_crossentropy' ,metrics= ['accuracy'])

"""*Training ANN on training dataset*"""

ann.fit(X_train,y_train,batch_size= 32, epochs= 100)

"""***Part 4 - Making predictions and evaluating the Model***

*Predict the result of single observation*


Use our ANN model to predict if the customer with the following informations will leave the bank:

Geography: France

Credit Score: 600

Gender: Male

Age: 40 years old

Tenure: 3 years

Balance: $ 60000

Number of Products: 2

Does this customer have a credit card? Yes

Is this customer an Active Member: Yes

Estimated Salary: $ 50000

# So, should we say goodbye to that customer?
"""

print(ann.predict(sc.transform([[1,0,0,600,1,40,3,60000,2,1,1,50000]]))>0.5)

"""*Predicting Test Set results*"""

y_pred = ann.predict(X_test)
y_pred = (y_pred > 0.5)
print(np.concatenate((y_pred.reshape(len(y_pred),1), y_test.reshape(len(y_test),1)),1))

"""*Making the Confusion Matrix*"""

from sklearn.metrics import confusion_matrix, accuracy_score
cm = confusion_matrix(y_test, y_pred)
print(cm)
accuracy_score(y_test, y_pred)

"""**We got 84% accurracy (1543 is the number customer leaves the bank and 139 customer stays in the bank)**"""