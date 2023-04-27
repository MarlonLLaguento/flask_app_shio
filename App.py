from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL connection
app.config['MYSQL_HOST'] = '34.203.40.13'
app.config['MYSQL_USER'] = 'support'
app.config['MYSQL_PASSWORD'] = 'sistemas20.'
app.config['MYSQL_DB'] = 'Shio_shop'
mysql = MySQL(app)

# settings
app.secret_key = 'mysecretkey'

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM clientes')
    data=cur.fetchall()
    return render_template('index.html', clientes = data)

@app.route('/add_cliente', methods=['POST'])
def add_cliente():
    if request.method == 'POST': #Define método de envío
        nombre = request.form['nombre'] # request.form recoge datos de formulario
        apellido = request.form['apellido']
        dni = request.form['dni']
        telefono = request.form['telefono']
        email = request.form['email']
        direccion = request.form['direccion']
        distrito = request.form['distrito']
        
        cur = mysql.connection.cursor() #genera conexion DB SQL
        cur.execute('INSERT INTO clientes (nombre, apellido, dni, telefono, email, direccion, distrito) VALUES (%s, %s, %s,%s,%s,%s,%s)', 
        (nombre, apellido, dni, telefono, email, direccion, distrito)) # ejecuta comando SLQ datos recogidos del form
        mysql.connection.commit() # Guarda cambios en DB
        flash('Client Added Succesfully')
        return redirect(url_for('Index')) #Redirecciona a pagina Index

@app.route('/edit/<id>')
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM clientes WHERE id = %s', (id))
    data = cur.fetchall()
    print(data[0])
    return render_template('edit-contact.html', contact = data[0])

@app.route('/update/<id>', methods = ['POST'])
def update_contact(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        dni = request.form['dni']
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        distrito = request.form['distrito']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE clientes
        SET nombre = %s,
            apellido = %s,
            dni = %s,
            telefono = %s,
            direccion = %s,
            distrito = %s,
            email = %s
        WHERE id = %s
        """, (nombre, apellido, dni, telefono, direccion, distrito, email,id ))
        mysql.connection.commit()
        flash('Client updated successfully')
        return redirect(url_for('Index'))

@app.route('/delete/<string:id>')
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM clientes WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Client Removed Successfully')
    return redirect(url_for('Index'))

if __name__ == '__main__':
    app.run(port = 5000, debug = True)