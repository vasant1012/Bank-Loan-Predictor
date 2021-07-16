from os import pipe
from flask import Flask, render_template, request
import sklearn
import pandas as pd
import pickle


app = Flask(__name__)
pipe = pickle.load(open("Bank_Loan_model.pkl","rb")) 

df = pd.read_csv('Churn_Modelling.csv')


@app.route('/')
def index(): 
    country = sorted(df['Geography'].unique())
    gender = sorted(df['Gender'].unique())
    return render_template('index.html', country=country, gender=gender)



@app.route('/predict', methods =['POST'])
def predict():
    ccscore= int(float(request.form.get("ccscore")))
    country=request.form.get("country")
    gender=request.form.get("gender")
    age=int(request.form.get("age"))
    tenure=int(request.form.get('tenure'))
    balance=float(request.form.get("balance"))
    product=int(request.form.get("product"))
    cccard=int(request.form.get("cccard"))
    net_banking=int(request.form.get("net_banking"))
    income=float(request.form.get("income"))

    input = pd.DataFrame([[ccscore, country, gender, age, tenure, balance, product, cccard, net_banking, income]],
                    columns=['CreditScore', 'Geography', 'Gender', 'Age', 'Tenure', 'Balance', 'NumOfProducts', 'HasCrCard', 'IsActiveMember', 'EstimatedSalary'])
 
    prediction = pipe.predict(input)[0]

    if prediction>=1:
       return "You are eligible for loan."
    else:
       return "Sorry! Please try next time."

if __name__ == '__main__':
    app.run(debug=True, port=8050)
