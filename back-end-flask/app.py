import dbm
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
import mariadb
import sys

#imporst db access config
from config import DATABASE_CONFIG

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clinic.db'
db = SQLAlchemy(app)


try:
        conn = mariadb.connect(**DATABASE_CONFIG)
except mariadb.Error as e:
        print(f"Error  on connection: {e}")
        sys.exit(1)

cursor = conn.cursor()

@app.route('/api/hello', methods=['GET'])
def hello_world():
        return jsonify({'message': '¡Hola, mundo con Flask!'})

@app.route('/api/misdatos/', methods=['GET'])
def mis_datos():
        return jsonify({'datos': '** SU NOMBRE ** !'})

# Buscar Pacientes
@cross_origin()
@app.route('/api/get_pacientes', methods=['GET'])
def get_pacientes():
    cursor.execute("SELECT * FROM Pacientes")
    pacientes = cursor.fetchall()
    list = []
    for paciente in pacientes:
        list.append({
              "id_paciente":paciente[0],
              "nombre":paciente[1],
              "fecha_nacimiento":paciente[2],
              "datos_medicos":paciente[3],
        })
    # Convertir los resultados en un formato más amigable o devolverlos directamente
    response = jsonify({"data":list})
    response.headers.add("Content-type",'application/json')
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# Buscar un paciente
@app.route('/api/get_paciente/<int:id>', methods=['GET'])
def get_paciente(id):
    if (id == 0):
           return jsonify({"error":"Invalid ID"}), 404
    else:
        cursor.execute("SELECT * FROM Pacientes where id_paciente = ?", (id,))
        paciente = cursor.fetchone()
        # Convertir los resultados en un formato más amigable o devolverlos directamente
        return jsonify({"id_paciente": paciente[0], "nombre": paciente[1],"fecha_nacimiento":paciente[2],"datos_medicos":paciente[3]})

#Añadir paciente
@app.route('/api/new_paciente', methods=['POST'])
def new_paciente():
        datos = request.json
        nombre = datos.get('nombre')
        fecha_nacimiento = datos.get('fecha_nacimiento')
        datos_medicos = datos.get('datos_medicos')
        
        strQry = 'insert into Pacientes'
        strQry += "(nombre, fecha_nacimiento, datos_medicos ) "
        strQry += f"values ('{nombre}','{fecha_nacimiento}','{datos_medicos}')"

        cursor.execute(strQry)
        conn.commit()

        response = {"message":"Record inserted"}
    
        return jsonify(response) , 200

# Actualizar paciente
@cross_origin()
@app.route('/api/update_paciente', methods=['POST'])
def update_paciente():
        datos = request.json
        id_paciente = datos.get('id_paciente')
        nombre = datos.get('nombre')
        fecha_nacimiento = datos.get('fecha_nacimiento')
        datos_medicos = datos.get('datos_medicos')

        strQry = 'update Pacientes '
        strQry += f"set nombre = '{nombre}', "
        strQry += f"fecha_nacimiento = '{fecha_nacimiento}', "
        strQry += f"datos_medicos = '{datos_medicos}' "
        strQry += f"where id_paciente = {id_paciente} "

        cursor.execute(strQry)
        conn.commit()

        response = {"message":"Record updated"}
    
        return jsonify(response) , 200

# Eliminar paciente
@app.route('/api/del_paciente/<int:id>', methods=['DELETE'])
def del_paciente(id):
#     datos = request.json
#     id = datos.get('id')    
    print(id)
    if (id == 0):
           return jsonify({"error":"Invalid ID"}), 404
    else:
        cursor.execute("DELETE FROM Pacientes WHERE id_paciente = ?", (id,))
        conn.commit()
        return jsonify({"message": "Paciente Borrado"}), 200

# Buscar Medicos
@app.route('/api/get_medicos', methods=['GET'])
def get_medicos():
    cursor.execute("SELECT * FROM Medicos")
    medicos = cursor.fetchall()
    list = []
    for medico in medicos:
        list.append({
              "id_medico":medico[0],
              "nombre":medico[1],
              "especializacion":medico[2],
              "horario_consulta":medico[3],
              "contacto":medico[4],
        })
    # Convertir los resultados en un formato más amigable o devolverlos directamente
    response = jsonify({"data":list})
    response.headers.add("Content-type",'application/json')
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# Buscar Medico
@app.route('/api/get_medico/<int:id>', methods=['GET'])
def get_medico(id):
    if (id == 0):
           return jsonify({"error":"Invalid ID"}), 404
    else:
        cursor.execute("SELECT * FROM Medicos where id_medico = ?", (id,))
        medico = cursor.fetchone()
        # Convertir los resultados en un formato más amigable o devolverlos directamente
        return jsonify(medico)

# Añadir medico
@app.route('/api/new_medico', methods=['POST'])
def new_medico():
        datos = request.json
        id_medico = datos.get('id_medico')
        nombre = datos.get('nombre')
        especializacion = datos.get('especializacion')
        horario_consulta = datos.get('horario_consulta')
        contacto = datos.get('contacto')
        
        strQry = 'insert into Medicos'
        strQry += "(id_medico, nombre, especializacion, horario_consulta, contacto ) "
        strQry += f"values ('{id_medico}','{nombre}','{especializacion}','{horario_consulta}','{contacto}')"

        cursor.execute(strQry)
        conn.commit()

        response = {"message":"Record inserted"}
    
        return jsonify(response) , 200

# Actualizar medico
@app.route('/api/update_medico', methods=['POST'])
def update_medico():
        datos = request.json
        id_medico = datos.get('id_medico')
        nombre = datos.get('nombre')
        especializacion = datos.get('especializacion')
        horario_consulta = datos.get('horario_consulta')
        contacto = datos.get('contacto')

        strQry = 'update Medicos '
        strQry += f"set nombre = '{nombre}', "
        strQry += f"especializacion = '{especializacion}', "
        strQry += f"horario_consulta = '{horario_consulta}', "
        strQry += f"contacto = '{contacto}' "
        strQry += f"where id_medico = {id_medico} "

        cursor.execute(strQry)
        conn.commit()

        response = {"message":"Record updated"}
    
        return jsonify(response) , 200

# Eliminar medicos
@app.route('/api/del_medico/<int:id>', methods=['DELETE'])
def del_medico(id):
#     datos = request.json
#     id = datos.get('id')    
    print(id)
    if (id == 0):
           return jsonify({"error":"Invalid ID"}), 404
    else:
        cursor.execute("DELETE FROM Medicos WHERE id_medico = ?", (id,))
        conn.commit()
        return jsonify({"message": "Medico Borrado"}), 200

class Paciente(db.Model):
    __tablename__ = 'Pacientes'
    id_paciente = db.Column(db.Integer, primary_key=True)

class Medico(db.Model):
    __tablename__ = 'Medicos'  
    id_medico = db.Column(db.Integer, primary_key=True)  

class Cita(db.Model):
    __tablename__ = 'Citas'
    id_cita = db.Column(db.Integer, primary_key=True)
    id_paciente = db.Column(db.Integer, db.ForeignKey('Pacientes.id_paciente'), nullable=False)
    id_medico = db.Column(db.Integer, db.ForeignKey('Medicos.id_medico'), nullable=False)
    fecha_cita = db.Column(db.Date, nullable=False)
    hora_cita = db.Column(db.Time, nullable=False)

# @app.route('/api/get_citas', methods=['GET'])
# def get_citas():
#     try: 
#             citas = db.session.query(Cita, Medico, Paciente) \
#                   .join(Medico, Cita.id_medico == Medico.id_medico) \
#                   .join(Paciente, Cita.id_paciente == Paciente.id_paciente) \
#                   .all()
#             lista_citas = []
#             for cita, medico, paciente in citas:
#               lista_citas.append({
#               "id_cita": cita.id_cita,
#               "id_paciente": paciente.id_paciente,
#               "id_medico": medico.id_medico,
#               "fecha_cita": cita.fecha.strftime("%Y-%m-%d"),
#               "hora_cita": cita.hora.strftime("%H:%M:%S")
#               })
#             response = jsonify({"data": lista_citas})
#             response.headers.add("Content-type", 'application/json')
#             response.headers.add('Access-Control-Allow-Origin', '*')
#             return response
#     except ValueError:
#            response = jsonify({"data": ValueError})
#            response.headers.add("Content-type", 'application/json')
#            response.headers.add('Access-Control-Allow-Origin', '*')
#            return response
          





# Buscar Citas
@app.route('/api/get_citas_by_patient/<int:id>', methods=['GET'])
def get_citas(id):
   cursor.execute("SELECT * From Citas c LEFT JOIN Pacientes p ON c.id_paciente = p.id_paciente JOIN Medicos m on m.id_medico = c.id_medico where c.id_paciente = ?", (int(id),))
   citas = cursor.fetchall()
   list = []
   print(id)
   print(citas)
   for cita in citas:
        list.append({
             "id_cita":cita[0],
             "id_paciente":cita[1],
             "id_medico":cita[2],
             "fecha_cita": str(cita[3]),
             "hora_cita":str(cita[4]),
             "paciente": {
                   "id_paciente": cita[5],
                   "nombre":cita[6],
                   "fecha_nacimiento":str(cita[7]),
                   "datos_medicos":cita[8],
             },
             "medico": {
                   "id_medico": cita[9],
                   "nombre":cita[10],
                   "especializacion":cita[11],
                   "horario_consulta":cita[12],
                   "contacto":cita[13],
             }
        })
#    # Convertir los resultados en un formato más amigable o devolverlos directamente
   response = jsonify({"data": list})
   response.headers.add("Content-type",'application/json')
   response.headers.add('Access-Control-Allow-Origin', '*')
   return response

# Buscar Cita
@app.route('/api/get_cita/<int:id>', methods=['GET'])
def get_cita(id):
    if (id == 0):
           return jsonify({"error":"Invalid ID"}), 404
    else:
        cursor.execute("SELECT * FROM Citas where id_cita = ?", (id,))
        cita = cursor.fetchone()
        # Convertir los resultados en un formato más amigable o devolverlos directamente
        return jsonify(cita)

# Añadir Cita
@app.route('/api/new_cita', methods=['POST'])
def new_cita():
        datos = request.json
        id_paciente = datos.get('id_paciente')
        id_medico = datos.get('id_medico')
        fecha_cita = datos.get('fecha_cita')
        hora_cita = datos.get('hora_cita')
        
        strQry = 'insert into Citas'
        strQry += "(id_paciente, id_medico, fecha_cita, hora_cita) "
        strQry += f"values ('{id_paciente}','{id_medico}','{fecha_cita}','{hora_cita}')"

        cursor.execute(strQry)
        conn.commit()

        response = {"message":"Record inserted"}
    
        return jsonify(response) , 200

# Actualizar Cita
@app.route('/api/update_cita', methods=['POST'])
def update_cita():
        datos = request.json
        id_cita = datos.get('id_cita')
        id_paciente = datos.get('id_paciente')
        id_medico = datos.get('id_medico')
        fecha_cita = datos.get('fecha_cita')
        hora_cita = datos.get('hora_cita')

        strQry = 'update Citas '
        strQry += f"set id_paciente = '{id_paciente}', "
        strQry += f"id_medico = '{id_medico}', "
        strQry += f"fecha_cita = '{fecha_cita}', "
        strQry += f"hora_cita = '{hora_cita}' "
        strQry += f"where id_cita = {id_cita} "

        cursor.execute(strQry)
        conn.commit()

        response = {"message":"Record updated"}
    
        return jsonify(response) , 200

# Eliminar Cita
@app.route('/api/del_cita/<int:id>', methods=['DELETE'])
def del_cita(id):
#     datos = request.json
#     id = datos.get('id')    
    print(id)
    if (id == 0):
           return jsonify({"error":"Invalid ID"}), 404
    else:
        cursor.execute("DELETE FROM Citas WHERE id_cita = ?", (id,))
        conn.commit()
        return jsonify({"message": "Cita Borrada"}), 200


if __name__ == '__main__':
        app.run(debug=True)
        app.run(host='0.0.0.0', port=5000)

