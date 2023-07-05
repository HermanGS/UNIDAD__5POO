from __main__ import app
from flask_sqlalchemy import SQLAlchemy,session
from datetime import datetime
import sqlalchemy

db = SQLAlchemy(app)

db.Model




class Padre(db.Model):
    __tablename__ = "padre"
    id = db.Column(db.Integer,primary_key =True)
    nombre = db.Column(db.String(50),nullable = False)
    apellido = db.Column(db.String(50),nullable = False)
    correo = db.Column(db.String(50),unique = True ,nullable = False)
    clave = db.Column(db.String(120),nullable = False)

    #asociacion 1 con estudiante
    estudiantes = db.relationship('Estudiante',backref = 'padre',cascade = "all, delete-orphan")

class Estudiante(db.Model):
    __tablemaname__ = "estudiante"
    id = db.Column(db.Integer,primary_key =True)
    nombre = db.Column(db.String(50),nullable = False)
    apellido = db.Column(db.String(50),nullable = False)
    dni = db.Column(db.String(8),nullable = False)

    #asociacion 1 con asistencia
    asistencias = db.relationship('Asistencia',backref='estudiante',cascade ="all,  delete-orphan")
    #asociacion muchos con curso
    idcurso = db.Column(db.Integer,db.ForeignKey('curso.id'))
    #asociacion muchos con padre
    idpadre = db.Column(db.Integer,db.ForeignKey('padre.id'))

    def __str__(self):
        return "id estudiante : {} nombre estudiante : {}".format(self.id,self.nombre)
    
    def retornaNombreyApellido(self):
        return str(self.nombre + self.apellido)

    def retornaNombreyApellidoSpace(self):
        return str(self.nombre +" "+ self.apellido)

    def __lt__(self,otro):
        if type(self) == type(otro):
            return (self.retornaNombreyApellido() < otro.retornaNombreyApellido())

class Asistencia(db.Model):
    __tablename__ = "asistencia"
    id = db.Column(db.Integer,primary_key = True)
    fecha = db.Column(db.String(12),nullable = False)
    codigoclase = db.Column(db.Integer,db.ForeignKey('curso.id'),nullable = False)
    asistio = db.Column(db.String(1),nullable = False)
    justificacion = db.Column(db.String(100),nullable = False)

    #asociacion muchos con estudiante
    idestudiante = db.Column(db.Integer,db.ForeignKey('estudiante.id'))
    
    """
    def __init__(self,id,fecha,codigoclase,asistio,justificacion):
        self.id = id
        self.fecha = fecha
        self.codigoclase = codigoclase
        self.asistio = asistio
        self.justificacion = justificacion
    """

class Curso(db.Model):
    __tablename__ = "curso"
    id =  db.Column(db.Integer,primary_key = True)
    anio =  db.Column(db.Integer,nullable = False)
    division = db.Column(db.Integer,nullable = False)
    
    #asociacion 1 con estudiante
    estudiantes = db.relationship('Estudiante',backref = 'Curso',cascade ="all,  delete-orphan")

    #asociacion muchos con preceptor
    idpreceptor = db.Column(db.Integer,db.ForeignKey('preceptor.id'))

class Preceptor(db.Model):
    __tablename__ = "preceptor"
    id = db.Column(db.Integer,primary_key =True)
    nombre = db.Column(db.String(50),nullable = False)
    apellido = db.Column(db.String(50),nullable = False)
    correo = db.Column(db.String(50),nullable = False, unique = True)
    clave = db.Column(db.String(120),nullable = False)

    #asociacon 1 con curso
    cursos = db.relationship('Curso', backref = 'preceptor',)

    def __init__(self,id,nombre,apellido,correo,clave):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.correo = correo
        self.clave = clave



    def __str__(self):
        return "id preceptor : {} nombre preceptor : {}".format(self.id,self.nombre)





