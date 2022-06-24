
#NAIMATUL MAUDIYAH (190900008)
#Essi Nurjanah (19090009)

from flask import Flask, render_template, flash, request, jsonify, url_for, redirect, session
import os
import pickle
import pandas as pd
import random
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from flask_uploads import UploadSet,configure_uploads,IMAGES,DATA,ALL


app = Flask( __name__)

@app.route('/upload_data', methods=['GET', 'POST'])
def upload_data_set():
    if request.method == 'POST' and 'file' in request.files:
        Filename = os.listdir('static/uploads')
        with open('pickle_file/train_data.pickle','ab') as f:
            f.close()
        with open('pickle_file/classifier_data.pickle','ab') as f:
            f.close()
        file = request.files['file']
        if file.filename == "":
            s="No file selected"
            return jsonify(msg=s)
        filename = secure_filename(file.filename)
        list1=[]
        for file2 in Filename:
            list1.append(file2)
        if filename in list1:
            s="File already exist"
            return jsonify(msg=s)
        else:
            code= random.randrange(100,999)
            file.save(os.path.join('static/uploads', filename))
            data_code = (code,filename)
            with open('pickle_file/data.pickle', 'ab') as f:
                pickle.dump(data_code,f)
            s='File'+filename+' uploaded successfully. Code:'+str(code)

            Filenames=os.listdir('static/uploads')
            lst = []

            with open('pickle_file/data.pickle', 'rb') as f:
                for i in range(0,len(Filenames)):
                    lst.append(pickle.load(f))
                return jsonify(msg=s)
    elif request.method != 'POST':
        s="Methods NOt Allowed HEre"
        return jsonify(msg=s)
    else:
        s="No file selected. . . ."
        return jsonify(msg=s)


@app.route('/train', methods=['GET', 'POST'])
def train1():
    Filenames=os.listdir('static/uploads')
    if (request.method == 'POST' or request.method == 'GET') and 'code' in request.form:
        code = int(request.form.get('code'))
        if code != '':
            lst = []
            with open('pickle_file/data.pickle', 'rb') as f:
                for i in range(0,len(Filenames)):
                    lst.append(pickle.load(f))
            str_ = []
            file_name = ''
            for item in lst:
                while(code in item):
                    str_.append('True')
                    file_name = item[1]
                    break
            objects = []
            with open ('pickle_file/train_data.pickle', 'rb') as f:
                while True:
                    try:
                        objects.append(pickle.load(f))
                    except EOFError:
                        break
            training_data_list = []
            for item in object:
                training_data_list.append(item[0])
            if 'True' in str_ and file_name not in training_data_list:
                td = TrainingData()
                score = td.train_data(file_name)
                s='Traing done'+' '+file_name + score
                training_data = []
                training_data.append(file_name)
                with open('pickle_file/train_data.pickle', 'ab') as f:
                    pickle.dump(training_data,f)
                return jsonify(msg=s,file_name=file_name)
            elif file_name in training_data_list:
                return jsonify(msg="File already trained")
            else:
                return jsonify(msg="File Not Found from this code : "+str(code))
        else: 
            return jsonify(msg="Please input code for file name")
    else:
        return jsonify(msg="Method not allowed here")




@app.route('/predict', methods=['GET', 'POST'])
def predictform():
    Filenames=os.listdir('static/uploads')
    if ( request. method == 'POST' or request.method == 'GET') and 'code'in request.form and 'comment' in request.form:
        code = int(request.form. get( 'code' ))
        data = request.form.get('comment')
        if str(code) == '' and data == '':
            return jsonify (msg='please enter code and review' )
        elif str(code) == '' and data != '':
            return jsonify(msg='Please Enter code')
        elif str(code) != '' and data == '':
            return jsonify(msg='Please enter review')
        elif type(code) is str:
            return jsonify(msg='Code must be a numeric value')
        else:
            lst =[]
            with open ('pickle_file/data.pickle', 'rb') as f:
                for i in range(0, len(Filenames)):
                    lst.append(pickle.load(f))
            str_ = []
            file_name = ''
            for item in lst:
                while (code in item):
                    str_.append('True')
                    file_name = item[1]
                    break
            objects = []
            with open('pickle_file/train_data.pickle', 'rb') as f:
                while True:
                    try:
                        objects.extend(pickle.load(f))
                    except EOFError:
                        break
            if 'True' in str_ and file_name in objects:
                td = TrainingData()
                dict_ = {'review':data}
                df = pd.DataFrame(dict_, index=[0])
                result = td.Dataframe(df, file_name)
                if result[0] == 1:
                    return jsonify(msg="Positive")
                else:
                    return jsonify(msg="Negative")
            elif 'True' in str_ and file_name not in object:
                return jsonify(msg="File assosiated with yhis code"+str(code)+"is not trained")
            else:
                return jsonify(msg="File not found from this key code")

if __name__ == "__main__":
    app.run(debug=True)