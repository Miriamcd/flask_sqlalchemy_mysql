from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
# el usuario y contraseña que tenemos en el worbench
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost/flaskmysql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.app_context().push()
db = SQLAlchemy(app)
ma = Marshmallow(app)

## Creamos el modelo para acceder a la base de datos.
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))

    def __init__(self, title, description):
        self.title = title
        self.description = description

## Lee todas las clases que sean db.Models.
## Crea todas las tablas que tengamos definidas como en este caso Task.
db.create_all()

## Creamos un esquema para interactuar de forma fácil con nuestros modelos.
class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description')

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

## Definimos las rutas de nuestra API Rest.

## Ruta de CREATE task - POST
@app.route('/tasks', methods=['POST'])
def create_task():

    # print(request.json)
    title = request.json['title']
    description = request.json['description']

    ## Llamamos al contructor de Task para crear una nueva tarea.
    new_task = Task(title, description)
    print("Tarea creada con exito.")

    ## Almacenamos los datos en la base de datos.
    db.session.add(new_task)#esto equivale a un insert
    db.session.commit()
    print("Almacenamiento en la base de datos --> OK!")

    return task_schema.jsonify(new_task)#devolvemos la tarea en json


## Ruta READ All tasks - GET
@app.route('/tasks', methods=['GET'])
def get_tasks():
    ## Nos devuelve todas las tareas
    all_tasks = Task.query.all()
    ## Lista con los datos
    result = tasks_schema.dump(all_tasks)
    ## Convertimos en JSON los resultados del select de la base de datos por el ORM.
    return jsonify(result)
# return 'Received'

## Ruta READ Single Task - GET
@app.route('/task/<id>', methods=['GET'])
# nuestra pagina tenemos un formulario y para sacar solo una tarea
def get_task(id):
    task = Task.query.get(id)

    return task_schema.jsonify(task)

## Ruta UPDATE Task - PUT
@app.route('/tasks/<id>', methods=['PUT'])
def update_task(id):

    task = Task.query.session.get(Task, id)
    title = request.json['title']
    description = request.json['description']

    task.title = title
    task.description = description

    db.session.commit()

    return task_schema.jsonify(task)

## Ruta DELETE Task - DELETE
@app.route('/tasks/<id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.session.get(Task, id)

    db.session.delete(task)
    db.session.commit()

    return task_schema.jsonify(task)

## Ruta de Landing Page - Página de Inicio /
@app.route('/', methods=['GET'])
def index():

    return jsonify({'message':'Welcome to my first API with Python Flask and MySQL'})

## Ruta DELETE All Tasks - DELETE
@app.route('/tasks/delete', methods=['DELETE'])
def delete_tasks():

    db.session.query(Task).delete()
    db.session.commit()

    return jsonify({"message":"All tasks deleted!!!"})


if __name__ == "__main__":
    app.run(debug=True)


# crearnos una base de datos flaskmysql ponemos en terminal mysql -u  root -p y creamos la bd















