
# coding: utf-8

# In[ ]:


import pickle
import numpy as np
from flask import Flask, render_template, request
app = Flask(__name__, template_folder='templates', static_folder='static')

default = [36, 'Private', 'HS-grad', 'Married-civ-spouse', 'Prof-specialty', 'Husband', 'White', 'Male', 0, 0, 40, 'United-States']

def mapInput(arrinput):
    arrstring = ['Private, Self-emp-not-inc, Self-emp-inc, Federal-gov, Local-gov, State-gov, Without-pay, Never-worked',
     'Bachelors, Some-college, 11th, HS-grad, Prof-school, Assoc-acdm, Assoc-voc, 9th, 7th-8th, 12th, Masters, 1st-4th, 10th, Doctorate, 5th-6th, Preschool',
     'Married-civ-spouse, Divorced, Never-married, Separated, Widowed, Married-spouse-absent, Married-AF-spouse',
     'Tech-support, Craft-repair, Other-service, Sales, Exec-managerial, Prof-specialty, Handlers-cleaners, Machine-op-inspct, Adm-clerical, Farming-fishing, Transport-moving, Priv-house-serv, Protective-serv, Armed-Forces',
     'Wife, Own-child, Husband, Not-in-family, Other-relative, Unmarried',
     'White, Asian-Pac-Islander, Amer-Indian-Eskimo, Other, Black',
     'Female, Male',
     'United-States, Cambodia, England, Puerto-Rico, Canada, Germany, Outlying-US(Guam-USVI-etc), India, Japan, Greece, South, China, Cuba, Iran, Honduras, Philippines, Italy, Poland, Jamaica, Vietnam, Mexico, Portugal, Ireland, France, Dominican-Republic, Laos, Ecuador, Taiwan, Haiti, Columbia, Hungary, Guatemala, Nicaragua, Scotland, Thailand, Yugoslavia, El-Salvador, Trinadad&Tobago, Peru, Hong, Holand-Netherlands']
    mapcol = [1, 2, 3, 4, 5, 6, 7, 11]
    j = 0
    for string in arrstring:
        arr = [x.strip() for x in string.split(',')]
        mapping = {}
        for i in range(0, len(arr)):
            mapping[arr[i]] = i
        if arrinput[mapcol[j]] in mapping:
            arrinput[mapcol[j]] = mapping[arrinput[mapcol[j]]]
        else:
            arrinput[mapcol[j]] = mapping[default[mapcol[j]]]
        j += 1
    numcol = [0, 8, 9, 10]
    for i in range(0, len(numcol)):
        if not arrinput[numcol[i]]:
            arrinput[numcol[i]] = default[numcol[i]]
    return arrinput

def predictIncome(arrinput):
    filename = 'saved_model.sav'
    model = pickle.load(open(filename, 'rb'))
    arrinput = mapInput(arrinput)
    nparr = np.array([arrinput])
    predict = model.predict(nparr)
    predict = predict.tolist()
    resmap = {0: '>50K', 1: '<=50K'}
    return resmap[predict[0]]

@app.route("/", methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        arr = [request.form.get('age'), request.form.get('workclass'), request.form.get('education'), request.form.get('marital-status'), request.form.get('occupation'), request.form.get('relationship'), request.form.get('race'), request.form.get('sex'), request.form.get('capital-gain'), request.form.get('capital-loss'), request.form.get('hours-per-week'), request.form.get('native-country')]
        result = predictIncome(arr)
        return render_template('AI.html', result=result)
    return render_template('AI.html')

if __name__ == "__main__":
    app.run()

