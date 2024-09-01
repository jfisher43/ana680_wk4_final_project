from flask import Flask, render_template, request
import numpy as np
import pickle
import os

#initialize flask app
app = Flask(__name__)

#set current working directory
#os.chdir('C:/Users/unkno/Desktop/MS Data Science/Class 9 - ANA680/Week 4/fp/src')

#load model
#filename = 'model.pkl'
filename = 'simpler_model.pkl'
model = pickle.load(open(filename, 'rb'))
print(dir(model))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        #extract form values
        Bene_Male_Cnt = int(request.form['Bene_Male_Cnt'])
        Tot_Sbmtd_Chrg = float(request.form['Tot_Sbmtd_Chrg'])
        is_NP = 1 if 'is_NP' in request.form else 0
        Tot_Mdcr_Pymt_Amt = float(request.form['Tot_Mdcr_Pymt_Amt'])
        Tot_HCPCS_Cds = int(request.form['Tot_HCPCS_Cds'])
        Bene_Feml_Cnt = int(request.form['Bene_Feml_Cnt'])
        has_MD = 1 if 'has_MD' in request.form else 0
        Bene_Avg_Risk_Scre = float(request.form['Bene_Avg_Risk_Scre'])
        Med_Tot_Srvcs = int(request.form['Med_Tot_Srvcs'])
        Med_Tot_Benes = int(request.form['Med_Tot_Benes'])
        Tot_Benes = int(request.form['Tot_Benes'])
        Tot_Srvcs = int(request.form['Tot_Srvcs'])

        #combine input values into array
        input_data = np.array([[Bene_Male_Cnt, Tot_Sbmtd_Chrg, is_NP, Tot_Mdcr_Pymt_Amt, 
                                Tot_HCPCS_Cds, Bene_Feml_Cnt, has_MD, Bene_Avg_Risk_Scre,
                                Med_Tot_Srvcs, Med_Tot_Benes, Tot_Benes, Tot_Srvcs]])
        
        print("Input data for prediction:", input_data)

        #make prediction
        pred = model.predict(input_data)
        if pred[0] == 0:
            result = "Male"
        elif pred[0] == 1:
            result = "Female"
        else:
            result = "Unknown"

        return render_template('index.html', predict=result)
    
    except Exception as e:
        print("Error occurred:", e)
        return render_template('index.html', predict="An error occurred. Please try again.")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
