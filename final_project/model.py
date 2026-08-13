import pandas as pd
from sklearn.model_selection import train_test_split

from sklearn.linear_model import LogisticRegression

from sklearn.metrics import accuracy_score

# Importing the dataset
dataset = pd.read_csv('data.csv')

# Splitting the dataset into Features and Target
X = dataset.iloc[:,:-1]
y = dataset.iloc[:,-1]

# Split the dataset into training and testing set
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=42)

# Initialized the model
model = LogisticRegression()

# Training
model.fit(X_train, y_train)

# Testing

def predict(age,bmi,glucose,bp):
  y_pred = model.predict([[age,bmi,glucose,bp]])  
  if y_pred[0] == 0:
    return 'No Diabetes'
  return 'Diabetes'
