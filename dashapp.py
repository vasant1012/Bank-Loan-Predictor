import pandas as pd
from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import os
import pickle
import warnings
warnings.filterwarnings('ignore')

# Application and it's stylesheet
app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
pipe = pickle.load(open("Bank_Loan_model.pkl","rb"))

ccscore = dbc.FormFloating([
    dbc.Input(type="number",
              placeholder="Enter your credit score",
              min=0,
              max=999,
              id="ccscore"),
    dbc.Label("Enter your Credit Score")
])

country_dropdown = html.Div(
    [
        dbc.Label("Select your country", html_for="dropdown"),
        dcc.Dropdown(id="country",
                     options=[{
                         "label": "France",
                         "value": "France"
                     }, {
                         "label": "Spain",
                         "value": "Spain"
                     }, {
                         "label": "Germany",
                         "value": "Germany"
                     }])
    ],
    className="mb-3",
)

gender_dropdown = html.Div(
    [
        dbc.Label("Select your gender", html_for="dropdown"),
        dcc.Dropdown(id="gender",
                     options=[{
                         "label": "Male",
                         "value": "Male"
                     }, {
                         "label": "Female",
                         "value": "Female"
                     }])
    ],
    className="mb-3",
)

age = dbc.FormFloating([
    dbc.Input(type="number",
              placeholder="Enter your age",
              min=0,
              max=100,
              id="age"),
    dbc.Label("Enter your age")
])

tenure = dbc.FormFloating([
    dbc.Input(type="number",
              placeholder="Enter the tenure",
              min=0,
              max=5,
              id="tenure"),
    dbc.Label("Enter the tenure")
])

balance = dbc.FormFloating([
    dbc.Input(type="number",
              placeholder="How much do you have balance in your account?",
              min=0,
              max=100000,
              id="balance"),
    dbc.Label("How much do you have balance in your account?")
])

product = dbc.FormFloating([
    dbc.Input(type="number",
              placeholder="How much product are you using?",
              min=0,
              max=5,
              id="product"),
    dbc.Label("How much product are you using?")
])

cccard_dropdown = html.Div([
    dbc.Label("Do you have credit card", html_for="dropdown"),
    dcc.Dropdown(id="cccard",
                 options=[{
                     "label": "Yes",
                     "value": "Yes"
                 }, {
                     "label": "No",
                     "value": "No"
                 }])
],
    className="mb-3")

net_banking_dropdown = html.Div([
    dbc.Label("Do you use net-banking frequently?", html_for="dropdown"),
    dcc.Dropdown(id="netbanking",
                 options=[{
                     "label": "Yes",
                     "value": "Yes"
                 }, {
                     "label": "No",
                     "value": "No"
                 }])
],
    className="mb-3")

income = dbc.FormFloating([
    dbc.Input(type="number",
              placeholder="What is your yearly income?",
              min=0,
              max=100000,
              id="income"),
    dbc.Label("What is your yearly income?")
])

Button = html.Div(
    [dbc.Button("Submit", id="submit", className="mb-3", n_clicks=0)])

app.layout = html.Div([
    html.H3("Bank Loan Predictor",
            className="card-title",
            style={'textAlign': 'center'}),
    html.Br(),
    dbc.Row([dbc.Col(html.Div(ccscore)),
             dbc.Col(html.Div(balance))]),
    html.Br(),
    dbc.Row([
        dbc.Col(html.Div(gender_dropdown)),
        dbc.Col(html.Div(country_dropdown))
    ]),
    html.Br(),
    dbc.Row([dbc.Col(html.Div(age)),
             dbc.Col(html.Div(product))]),
    html.Br(),
    dbc.Row([
        dbc.Col(html.Div(cccard_dropdown)),
        dbc.Col(html.Div(net_banking_dropdown))
    ]),
    html.Br(),
    dbc.Row([dbc.Col(html.Div(tenure)),
             dbc.Col(html.Div(income))]),
    html.Br(),
    dbc.Row([dbc.Col(html.Div(Button))]),
    html.Br(),
    html.Span(id="example-output", style={"verticalAlign": "middle"})
])


@app.callback(Output("example-output", "children"),
              Input("submit", "n_clicks"), [
                  State("ccscore", "value"),
                  State("gender", "value"),
                  State("balance", "value"),
                  State("country", "value"),
                  State("age", "value"),
                  State("product", "value"),
                  State("cccard", "value"),
                  State("netbanking", "value"),
                  State("tenure", "value"),
                  State("income", "value")
])
def on_button_click(n_clicks, ccscore, gender, balance, country, age, product,
                    cccard, netbanking, tenure, income):
    if n_clicks > 0 and not [ccscore, gender, balance, country, age, product,
                             cccard, netbanking, tenure, income]:
        return "Please enter full details and then submit"
    elif n_clicks > 0 and [ccscore, gender, balance, country, age, product,
                           cccard, netbanking, tenure, income]:
        record = pd.DataFrame([[
            int(ccscore), gender,
            int(balance), country,
            int(age),
            int(product), cccard, netbanking,
            int(tenure), int(income)
        ]], columns = ["CreditScore", "Gender", "Balance", "Geography", "Age", "NumOfProducts",
                           "HasCrCard", "IsActiveMember", "Tenure", "EstimatedSalary"])
        record = record[['CreditScore', 'Geography', 'Gender', 'Age', 'Tenure', 'Balance', 'NumOfProducts',
                            'HasCrCard', 'IsActiveMember', 'EstimatedSalary']]
        print(record)
        # print(record.info())    
        prediction = pipe.predict(record)[0]
        if prediction>=1:
            output = html.H3(
            ["You are eligible for loan."])
        else:
            output = html.H3(
            [ "Sorry! Please try next time."])
        # return dbc.Table.from_dataframe(record, striped=True, bordered=True, hover=True)

if __name__ == '__main__':
    app.run_server(debug=False, use_reloader=False, port=7480)