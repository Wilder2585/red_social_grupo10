from flask import Flask, render_template
from flask import request
from utils.jsonUtils import loadStartData
from markupsafe import escape

# Formularios
from forms import Search
from forms import LogIn
from forms import Form

from flask import redirect


import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
sesion_iniciada = False 

def searchEmpleado(text, usuarios):
    resultado = []

    if (text == ''):
        return usuarios

    for usuario in usuarios:
        if (usuario['usuario'] == text):
            resultado.append(usuario)

    return resultado

def crearEmpleado(form, usuarios):
    nuevoEmpleado = {
        'nombre': form["nombre"],
        "apellido": form["apellido"],
        "usuario": form["usuario"],
        "megusta":form["megusta"],
        "fecIngreso": form["fecIngreso"],
        "tipoUsuario": "Empleado"
    }

    usuarios.append(nuevoEmpleado)
    return True

@app.route('/')
@app.route('/home/')
@app.route('/index/')
def main():
    return render_template('home.html', titulo='Home::red social')


@app.route("/login/", methods=["GET","POST"])
def login():
    frm = LogIn()
    global sesion_iniciada      
                                
    if request.method == "GET":
        
        return render_template("login.html",form=frm, titulo='Login::red social')
      
    else:
        sesion_iniciada = True
        
        log = escape(request.form['usr']) 
        cla = escape(request.form['pwd'])

        if len(log.strip())==0:
            pass
        if len(cla.strip())==0:
            pass
            
        if log=='administrador' and cla=='12345':
           
            return redirect("/dashboard")
            
        if log== 'mario' and cla=='12345':
            return redirect("/paginausuario")
        else:
            return "<h1>Error de Autenticacion</h1>"
    
@app.route('/paginausuario')
def datosempleado():
    global data
    data = loadStartData.data
    form = Search()
    return render_template('paginausuario.html', data = data, form = form)


@app.route('/dashboard')
def dashboard():
    global data
    data = loadStartData.data
    form = Search()
    return render_template('dashboard.html', data = data, form = form)

@app.route('/buscar', methods=["POST"])
def search():
    form = Search()
    busqueda = searchEmpleado(request.form["name"], data['empleados'])
    return render_template('dashboard.html', data = {"empleados": busqueda}, form = form)

@app.route('/crear', methods=["GET"])
def crear():
    form = Form()
    return render_template('layout.html', form = form)

@app.route('/crear', methods=["POST"])
def accionCrear():
    if (crearEmpleado(request.form, data['empleados'])):
        return redirect("/dashboard")

    return render_template('layout.html', form = request.form)

if __name__=='__main__':
    app.run(debug=True)
