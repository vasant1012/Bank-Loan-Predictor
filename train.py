import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import make_column_transformer
from sklearn.pipeline import make_pipeline
from sklearn.ensemble import RandomForestClassifier

import warnings

warnings.filterwarnings('ignore')

df = pd.read_csv('Churn_Modelling.csv')

df.drop(columns=['RowNumber', 'CustomerId', 'Surname'], inplace=True)

X = df.drop(['Exited'], 1)
y = df['Exited']

X_train, X_test, y_train, y_test = train_test_split(X,
                                                    y,
                                                    train_size=0.7,
                                                    random_state=21)

col_trans = make_column_transformer(
    (OneHotEncoder(drop='first'), ['Geography', 'Gender']),
    (StandardScaler(), [
        'CreditScore', 'Age', 'Tenure', 'Balance', 'NumOfProducts',
        'HasCrCard', 'IsActiveMember', 'EstimatedSalary'
    ]))

numerical_cols = [
    col for col in X_train.columns
    if X_train[col].dtype in ['int64', 'float64']
]
categorical_cols = [
    col for col in X_train.columns if X_train[col].dtype == 'object'
]

print("record:--", X_train.iloc[[3]].info())
print('numerical_cols:--', numerical_cols)
print('categorical_cols:--', categorical_cols)

# col_trans = make_column_transformer(
#     (OneHotEncoder(drop='first'), categorical_cols),
#     (StandardScaler(), numerical_cols))
# model = RandomForestClassifier()
# pipe = make_pipeline(col_trans, model)
# pipe.fit(X_train, y_train)
# filename = 'Bank_Loan_model.pkl'
# pickle.dump(pipe, open(filename, 'wb'))

# model = pickle.load(open("Bank_Loan_model.pkl", "rb"))
# print(model.predict(X_test.iloc[[5]]))