from flask import Flask
from flask import render_template, request, redirect
from flask import url_for, flash
from flaskext.mysql import MySQL

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] ='localhost'
app.config['MYSQL_DATABASE_USER'] ='root'
app.config['MYSQL_DATABASE_PASSWORD'] =''
app.config['MYSQL_DATABASE_BD'] ='cac_bookflix'
mysql.init_app(app)

# PAGINA INICIAL
@app.route('/')
def index():
    sql = "SELECT * FROM `cac_bookflix`.`libros`;"
    sql_rnd = "SELECT * FROM `cac_bookflix`.`libros` ORDER BY RAND();"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    libros = cursor.fetchall()
    cursor.execute(sql_rnd)
    recomendado = cursor.fetchone()
    conn.commit()
    return render_template('dashboard/index.html', libros = libros, recomendado = recomendado)

# VISTA POR ID
@app.route('/view/<int:id>')
def view(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM `cac_bookflix`.`libros` WHERE lid=%s", (id))
    libro = cursor.fetchone()
    conn.commit()
    return render_template('dashboard/view.html', libro = libro)

# CREACIÓN DE REGISTRO
@app.route('/create')
def create():
    return render_template('dashboard/create.html')
# GUARDA DE DATOS
@app.route('/store', methods=['POST'])
def storage():
    # Recuperamos valores de los input del HTML
    _titulo = request.form['titulo']
    _descripcion = request.form['descripcion']
    _fecha_publicacion = request.form['fecha_publicacion']
    _categoria = request.form['categoria']
    _autor = request.form['autor']
    _imagen = request.form['imagen']
    _pdf = request.form['pdf']

    # Validamos los campos
    errors = []
    if _titulo == '':
        errors.append('El campo Título no debe estar vacío')
        flash('El campo Título no debe estar vacío')
    if _descripcion == '':
        errors.append('El campo Descripción no debe estar vacío')
        flash('El campo Descripción no debe estar vacío')
    if _fecha_publicacion == '':
        errors.append('El campo Fecha de publicación tiene errores')
        flash('El campo Fecha de publicación tiene errores')
    if _categoria == '':
        errors.append('El campo Categoría no puede estar vacío')
        flash('El campo Categoría no puede estar vacío')
    if _autor == '':
        errors.append('El campo Autor no puede estar vacío')
        flash('El campo Autor no puede estar vacío')
    if _imagen == '':
        errors.append('El campo Imagen debe ser un link válido')
        flash('El campo Imagen debe ser un link válido')
    if _pdf == '':
        errors.append('El campo PDF debe ser un link válido')
        flash('El campo PDF debe ser un link válido')

    if len(errors) > 0:
        return redirect(url_for('create'))
    
    data = (_titulo,_descripcion,_fecha_publicacion,_categoria,_autor,_imagen,_pdf)
    
    sql = "INSERT INTO `cac_bookflix`.`libros` \
          (`lid`, `titulo`, `descripcion`, `fecha_publicacion`, `categoria`, `autor`, `imagen`, `pdf`) \
          VALUES (NULL, %s, %s, %s, %s, %s, %s, %s);"

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, data)
    conn.commit()

    return redirect('/')
# BORRAR REGISTRO
@app.route('/destroy/<int:id>')
def destroy(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM `cac_bookflix`.`libros` WHERE lid=%s", (id))
    conn.commit()
    return redirect('/')
# EDITAR REGISTRO
@app.route('/edit/<int:id>')
def edit(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM `cac_bookflix`.`libros` WHERE lid=%s", (id))
    libro=cursor.fetchone()
    conn.commit()
    return render_template('dashboard/edit.html', libro=libro)
# MODIFICACIÓN DE DATOS
@app.route('/update', methods=['POST'])
def update():
    # Recuperamos valores de los input del HTML
    _lid = request.form['lid']
    _titulo = request.form['titulo']
    _descripcion = request.form['descripcion']
    _fecha_publicacion = request.form['fecha_publicacion']
    _categoria = request.form['categoria']
    _autor = request.form['autor']
    _imagen = request.form['imagen']
    _pdf = request.form['pdf']

    # Validamos los campos
    errors = []
    if _lid == '':
        errors.append('Hay un error con el ID del formulario')
        flash('Hay un error con el ID del formulario')
    if _titulo == '':
        errors.append('El campo Título no debe estar vacío')
        flash('El campo Título no debe estar vacío')
    if _descripcion == '':
        errors.append('El campo Descripción no debe estar vacío')
        flash('El campo Descripción no debe estar vacío')
    if _fecha_publicacion == '':
        errors.append('El campo Fecha de publicación tiene errores')
        flash('El campo Fecha de publicación tiene errores')
    if _categoria == '':
        errors.append('El campo Categoría no puede estar vacío')
        flash('El campo Categoría no puede estar vacío')
    if _autor == '':
        errors.append('El campo Autor no puede estar vacío')
        flash('El campo Autor no puede estar vacío')
    if _imagen == '':
        errors.append('El campo Imagen debe ser un link válido')
        flash('El campo Imagen debe ser un link válido')
    if _pdf == '':
        errors.append('El campo PDF debe ser un link válido')
        flash('El campo PDF debe ser un link válido')

    if len(errors) > 0:
        return redirect(url_for(f'edit/{_lid}'))
    
    data = (_titulo,_descripcion,_fecha_publicacion,_categoria,_autor,_imagen,_pdf,_lid)
    
    sql = "UPDATE `cac_bookflix`.`libros` SET `titulo`=%s, `descripcion`=%s, `fecha_publicacion`=%s, `categoria`=%s, `autor`=%s, `imagen`=%s, `pdf`=%s WHERE lid=%s;"

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, data)
    conn.commit()

    return redirect('/')


if __name__=='__main__':
    app.run(debug=True)