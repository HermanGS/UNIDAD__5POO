from flask import Flask, request, redirect, url_for, render_template,session
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import hashlib
from datetime import datetime

app = Flask(__name__)
app.config.from_pyfile('config2.py')
app.app_context().push()

from Models import db
from Models import Padre,Estudiante,Curso,Asistencia,Preceptor

@app.route('/')
def inicio():
    return render_template('ingreso_usuario.html')


#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@app.route('/registrar_usuario', methods = ['GET','POST'])
def registrar_usuario():
    if request.method == 'POST':
        if not request.form['nombre'] or not request.form['apellido'] or not request.form['email']  or not request.form['password'] or not request.form['tipoUsuario']:
            return render_template('error.html',error = "Falta ingresar algun campo")
        else:
            if request.form['tipoUsuario'] == 'Preceptor':
                
                ultimaID = Preceptor.query.count()
                print("ultima ID : ",ultimaID)
                
                nuevoPreceptor = Preceptor(id = ultimaID+1 , nombre = request.form['nombre'] , apellido = request.form['apellido'] , correo = request.form['email'] , clave = hashlib.md5(bytes(request.form['password'], encoding='utf-8')).hexdigest() )
                db.session.add(nuevoPreceptor)
                db.session.commit()
                return render_template('mensaje.html',mensaje = 'Preceptor Registrado Correctamente')

            else:  # request.form['tipoUsuario] == 'Padre':
                
                ultimaID = Padre.query.count()
                print("ultima ID : ",ultimaID)
                
                nuevoPadre = Padre(id = ultimaID+1 ,nombre = request.form['nombre'] , apellido = request.form['apellido'] , correo = request.form['email'] , clave = hashlib.md5(bytes(request.form['password'], encoding='utf-8')).hexdigest() )
                db.session.add(nuevoPadre)
                db.session.commit()
                return render_template('mensaje.html',mensaje = 'Padre Registrado Correctamente') 
            
    else:
        return render_template('registrar_usuario.html')
    

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


"""
@app.route('/nuevo_usuario', methods = ['GET','POST'])
def nuevo_usuario():   
	if request.method == 'POST':
		if not request.form['nombre'] or not request.form['email'] or not request.form['password']:
			return render_template('error.html', error="Los datos ingresados no son correctos...")
		else:
			nuevo_usuario = Usuario(nombre=request.form['nombre'], correo = request.form['email'], clave=generate_password_hash(request.form['password']))       
			db.session.add(nuevo_usuario)
			db.session.commit()
			return render_template('aviso.html', mensaje="El usuario se registró exitosamente")
	return render_template('nuevo_usuario.html')
"""

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


@app.route('/pagina_inicio' , methods = ['GET','POST'])
def pagina_inicio(): #valida el ingreso de un usuario , ya sea un preceptor o un padre y lo dirige a un menu de opciones
    if request.method == 'POST':



        if not request.form['email'] or request.form['tipoUsuario'] == None or not request.form['password']:
            return render_template('error.html',error = 'Faltó ingresar alguno de los campos')

        else:
            if request.form['tipoUsuario'] == 'Preceptor':                                             # preceptor
                preceptor_actual = Preceptor.query.filter_by(correo = request.form['email']).first()


                if preceptor_actual is None:
                    return render_template('error.html',error = "El Preceptor no se encuentra Registrado")
                else:
                    
                    #verificacion = check_password_hash(preceptor_actual.clave,request.form['password'])
                    
                    claveEncriptada = hashlib.md5(bytes(request.form['password'], encoding='utf-8')).hexdigest()
                    
                    print("clave encriptada : ",claveEncriptada)
                    print("clave de la base de datos : ",preceptor_actual.clave)
                    
                    verificacion = (claveEncriptada == preceptor_actual.clave)

                    
                    print(verificacion)
                    if (verificacion):
                        
                        session['correo'] = preceptor_actual.correo
                        session['id'] = preceptor_actual.id

                        return render_template('pagina_inicio_preceptor.html',usuario = preceptor_actual)
                    else:
                        return render_template('error.html',error = 'La Contraseña No es Válida')
            


            else: # request.form['tipoUsuario'] == 'Padre':                                            # padre
                padre_actual = Padre.query.filter_by(correo = request.form['email']).first()
            
                if  padre_actual is None:
                    return render_template('error.html',error = "El Padre no se encuentra Registrado")
                else:
                    claveEncriptada = hashlib.md5(bytes(request.form['password'], encoding='utf-8')).hexdigest()
                    print("clave encriptada : ",claveEncriptada)
                    print("clave de la base de datos : ",padre_actual.clave)
                    
                    verificacion = (claveEncriptada == padre_actual.clave)
                    if (verificacion):
                        

                        session['correo'] = padre_actual.correo
                        session['id'] = padre_actual.id

                        return render_template('pagina_inicio_padre.html',usuario = padre_actual)
                    else:
                        return render_template('error.html',error = 'La Contraseña No es Válida')
    else: 
        print("entraste con el método get")
        return render_template('ingreso_usuario.html')

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------

@app.route('/RegistrarAsistencia' , methods = ['GET','POST'])
def RegistrarAsistencia(): # muestra los cursos que le corresponden al preceptor que inicio sesion y permite elegir uno
    if 'correo' in session:
        correoPreceptorSession = session.get('correo') 
        
        idPreceptorSession =  session.get('id')
        print("correo preceptor session : ",correoPreceptorSession)
        
        preceptor_actual  = Preceptor.query.filter_by(correo = correoPreceptorSession).first()
        print("preceptor actual : ",preceptor_actual)
        
        cursosPreceptor = Curso.query.filter_by(idpreceptor = idPreceptorSession).all()
        print("cursos : ",cursosPreceptor)
        
        return render_template('selecciona_cursoRegistrarA.html',preceptor = preceptor_actual ,cursos = cursosPreceptor)
    
    else:
        return render_template('ingreso_usuario.html')

@app.route('/RegistrarAsistencia/AsistenciaCurso/' , methods = ['GET','POST'])
def AsistenciaCurso(): # muestra los alumnos del curso seleccionado y permite elegir uno para cargar una asistencia
    if 'correo' in session:
        if request.method == 'POST':
            if  not request.form['idcurso']:
                return render_template('errorRegistrarAsistencia.html',error = "No se especificado el curso")
            
            else:
                
                preceptor_actual = Preceptor.query.filter_by(correo = session.get('correo')).first()
                
                
                idcursoFormulario = request.form['idcurso']
                cursoPorID = Curso.query.filter_by(id = idcursoFormulario ).first()
                
                estudiantes = Estudiante.query.filter_by(idcurso = idcursoFormulario).all()
                estudiantes.sort()
                
                #estudiantes.sort(key = lambda x: x.retornaNombreyApellido())
                
                print("id de curso : ",cursoPorID)
                print("estudiantes de ese curso : ",estudiantes)

                return render_template('seleccionar_alumno.html',curso = cursoPorID, alumnos = estudiantes ,preceptor = preceptor_actual)
        else:
            return redirect(url_for('RegistrarAsistencia'))
    else:
        return render_template('ingreso_usuario.html')

@app.route('/RegistrarAsistencia/AsistenciaCurso/AsistenciaAlumno/' , methods = ['GET'])
def AsistenciaAlumno(): #muestra el alumno y el curso al que pertenece y le permite ingresar una asistencia
    if 'correo' in session:
        if request.method == 'GET':
            preceptor_actual = Preceptor.query.filter_by(correo = session.get('correo')).first()
            
            alumnoid = request.args.get('alumnoid')
            if alumnoid == None:
                return redirect(url_for('AsistenciaCurso'))
            else:
                alumnoPorID = Estudiante.query.filter_by(id = alumnoid).first() 
                cursoid = request.args.get('cursoid')
                cursoPorID = Curso.query.filter_by(id = cursoid).first()
                print("curso id :",cursoid) 
                print("alumno id : ",alumnoid)
                return render_template('formulario_asistencia.html',curso = cursoPorID, alumnoid = alumnoid ,alumno = alumnoPorID, preceptor = preceptor_actual)     
    else:
        return render_template('ingreso_usuario.html')

@app.route('/RegistrarAsistencia/AsistenciaCurso/AsistenciaAlumno/IngresoAsistencia/', methods = ['GET','POST'])
def IngresoAsistencia(): # añade la asistencia a la base de datos y redirige de nuevo a RegistrarAsistencia
    if 'correo' in session:
        if request.method == 'POST':
            print("pooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooost")
            if not request.form['alumnoid'] or not request.form['tipoClase'] or not request.form['fecha']  or not request.form['asistio']:

                return redirect(url_for('AsistenciaCurso'))
            else:
                print("Request alumnoid",request.form['alumnoid'])
                print("Request tipoclase",request.form['tipoClase'])
                print("Request fecha",request.form['fecha'])
                print("Request asistio",request.form['asistio'])
                
                
                fechastr = request.form['fecha'].replace('-','/')
                """
                fechaDatetime = datetime.strptime(fechastr,'%Y/%m/%d')
                print("tipo de dato de fecha ",type(fechaDatetime),"dato : ",fechaDatetime)
                """

                if request.form['justificacion'] is None:
                    justi = '' 
                else:
                    justi = request.form['justificacion']

                asistencia = Asistencia(fecha = fechastr , codigoclase = request.form['tipoClase'] , asistio = request.form['asistio'] , justificacion = justi , idestudiante = request.form['alumnoid'] )
                db.session.add(asistencia)
                db.session.commit()
                return redirect(url_for('RegistrarAsistencia'))

                
        else:
            return redirect(url_for('AsistenciaCurso'))
    else:
        return redirect(url_for('inicio'))

#-------------------------------------------------------------------------------------------------------------------------------------------------------

@app.route('/InformarAsistencia/')
def InformarAsistencia():
    if 'correo' in session:

        preceptor_actual = Preceptor.query.filter_by(correo = session.get('correo')).first()

        cursosPreceptor = Curso.query.filter_by(idpreceptor = session.get('id')).all()

        return render_template('selecciona_cursoInformarA.html',cursos = cursosPreceptor, preceptor = preceptor_actual)
    
    else:
        return render_template('ingreso_usuario.html')

@app.route('/InformarAsistencia/ListadoAsistencia/', methods = ['GET','POST'])
def ListadoAsistencia():
    if 'correo' in session:
        if request.method == 'POST':
            idcursoFormulario = request.form['idcurso']
            cursoF = Curso.query.filter_by(id = idcursoFormulario)
            alumnosFiltrado = Estudiante.query.filter_by(idcurso = idcursoFormulario).all()
            
            alumnos = Estudiante.query.all()
            asistencia = Asistencia.query.all()
            print(cursoF)
            print(alumnos)
            print(asistencia)
            alumnos.sort()

            for alumno in alumnosFiltrado:
                contador = {
                'aulaasistencia': 0,
                'eduasistencia': 0,
                'aulajustificada': 0,
                'aulainjustificada': 0,
                'edujustificada': 0,
                'eduinjustificada': 0,
                'total': 0
                } 
                """
                for asis in asistencia:
                    if asis.idestudiante == alumno.id:
                        print(alumno.nombre)
                """        




            return render_template('mostrar_ListadoAsistenciaCurso_1.html',curso = cursoF, alumnos = alumnosFiltrado, asistencia = asistencia)
        else:
            return redirect(url_for('InformarAsistencia'))
    else:
        return render_template('ingreso_usuario.html')


if __name__ == '__main__':
    
        db.create_all()
        app.run(debug=True)

