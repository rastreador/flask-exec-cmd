#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template
from flask import request


app = Flask(__name__)

app_data = {
    "name":         "Ejecuta comando",
    "description":  "Ejecuta comando de shell como usuario",
    "author":       "Manuel Ángel Fernández",
    "html_title":   "Ejecuta comando de shell como usuario",
    "project_name": "flask-exec-cmd",
    "keywords":     ""
}



@app.route('/')
def index():
    return render_template('index.html', app_data=app_data)

@app.route('/ejecutar')
def ejecutar():

        cmd_tarea="sudo /root/comando_a_ejecutar.sh"

        try:
            result_tarea = subprocess.check_output([cmd_tarea], shell=True)

        except subprocess.CalledProcessError as e:
            return "Error al ejecutar la tarea: {}.".format(e)


        app_data['resultado_tarea_subprocess']=result_tarea.decode("utf-8")
        #return 'ok {}'.format(result_tarea.decode("utf-8"))

    return render_template('ejecutar.html', app_data=app_data)

if __name__ == '__main__':
#    app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)
