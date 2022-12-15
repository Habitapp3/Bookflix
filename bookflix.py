from flask import Flask
from flask import render_template, request, redirect
from flask import url_for, flash
from flaskext.mysql import MySQL

app = Flask(__name__) #Se monta en app la aplicacion Flask

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

mysql = MySQL() #se monta en la variable mysql el objeto MySQL que es la conexion con la bdd
app.config['MYSQL_DATABASE_HOST'] ='localhost'
app.config['MYSQL_DATABASE_USER'] ='root'
app.config['MYSQL_DATABASE_PASSWORD'] =''
app.config['MYSQL_DATABASE_BD'] ='cac_bookflix'
mysql.init_app(app) #con este METODO de MySQL, se setean los datos de la configuracion MySQL anterior.

# PAGINA INICIAL
@app.route('/') #le indicamos a app que en la ruta raiz haga..
def index():#funcion definida por nosotros que se va a ejecutar cuando se vaya a la raiz del sitio
    sql = "SELECT * FROM `cac_bookflix`.`libros`;" #query SQL para obtener todos los datos de la tabla libros
    sql_rnd = "SELECT * FROM `cac_bookflix`.`libros` ORDER BY RAND();" #query igual al previo pero ordenados de manera aleatoria
    conn = mysql.connect() #conector necesario de mysql
    cursor = conn.cursor() #cursor unido al conector. Es quien "lleva y trae"
    cursor.execute(sql) #metodo que ejecuta el query que se le pase como argumento
    libros = cursor.fetchall() #guardamos en la variable libros todos los registros obtenidos por el execute previo
    cursor.execute(sql_rnd)#metodo que ejecuta el query que se le pase como arguemnto
    recomendado = cursor.fetchone()#guardamos en la variable recomendado UN REGISTRO de los obtenidos aleatoriamente
    conn.commit()#metodo necesario del conector para "confirmar y terminar" la interaccion con la bdd (CREO)
    return render_template('dashboard/index.html', libros = libros, recomendado = recomendado) #el return de la funcion llama al metodo render_template
#de flask, y se le pasa como argumento en 1er lugar el template, y luego las variables a embeber en el template (en este caso, index.html)


# VISTA POR ID
@app.route('/view/<int:id>/')#le indicamos a app que en la ruta VIEW con TAL ID como argumento haga..
def view(id): #se pasa el id como parametro de la funcion view, que es lo que se va a ejecutar en esta ruta
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM `cac_bookflix`.`libros` WHERE lid=%s", (id))#query que pide todos los registros donde el id del libro en la BD sea igual 
    #al id que se paso como parametro en la ruta
    libro = cursor.fetchone()#se guarda en libro el resutado del query
    conn.commit()
    return render_template('dashboard/view.html', libro = libro)

# BUSCADOR
@app.route('/search')#le indicamos que la ruta SEARCH va a recibir un parametro de tipo String llamado "q"
def search():#recuperamos el parametro "q" y lo usamos dentro de la funcion
    q = request.args.get('q')
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM `cac_bookflix`.`libros` WHERE titulo LIKE %s", ('%' + q + '%'))
    res = cursor.fetchall()
    conn.commit()
    return render_template('dashboard/results.html', res = res, query = q)#le enviamos al "results.html" el resultado de la búsqueda (res) y lo que
    #el usuario busco como (query)

# CREACIÓN DE REGISTRO
@app.route('/create') 
def create():
    return render_template('dashboard/create.html')#en la ruta create se carga el template con el formulario de creacion de registro.
# GUARDA DE DATOS
@app.route('/store', methods=['POST'])#en la ruta store, con el metodo POST (YA QUE VAN A INGRESAR DATOS) pasa lo siguiente
def storage():# funcion definida por nosotros para guardar los datos
    # Recuperamos valores de los input del HTML
    _titulo = request.form['titulo']#con el metodo request.form de Flask se guarda en _titulo el valor de 'titulo', que viene de lo completado en "create.html" de los atributos "name" de cada input, select o textarea del formulario
    _descripcion = request.form['descripcion']
    _fecha_publicacion = request.form['fecha_publicacion'] #ej. <input name="fecha_publicacion" /> --> atributo name
    _categoria = request.form['categoria']
    _autor = request.form['autor']
    _imagen = request.form['imagen']
    _pdf = request.form['pdf']

    # Validamos los campos
    errors = []#lista para guardar los strings que describan los campos vacios
    if _titulo == '':#si titulo esta vacio..
        errors.append('El campo Título no debe estar vacío')#guarda el argumento en la lista errors
        flash('El campo Título no debe estar vacío')#muestra en pantalla 
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

    if len(errors) > 0:#Comprueba si hay errores acumulados en la lista. Si los hay...
        return redirect(url_for('create'))#metodo importado redirect de Flask redirige al formulario de /create (url_for apunta a la ruta)
    
    data = (_titulo,_descripcion,_fecha_publicacion,_categoria,_autor,_imagen,_pdf)#se guarda en la tupla data lo que completo el usuario
    
    sql = "INSERT INTO `cac_bookflix`.`libros` \
          (`lid`, `titulo`, `descripcion`, `fecha_publicacion`, `categoria`, `autor`, `imagen`, `pdf`) \
          VALUES (NULL, %s, %s, %s, %s, %s, %s, %s);" #query para insertar los registros en la BDD. los %s van a recibir los datos de la variable data

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, data)#query, y datos para "llenar" el query obtenidos de la tupla de arriba (data)
    conn.commit()
    
    flash('Libro cargado con éxito')

    return redirect('/')#redirigimos a la raiz del sitio

# CONFIRMAR BORRAR REGISTRO
@app.route('/destroy/<int:id>')#le indicamos a app que en la ruta destroy con TAL ID como argumento haga..
def destroy(id):#se pasa el id como parametro de la funcion destroy, que es lo que se va a ejecutar en esta ruta
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT lid, titulo FROM `cac_bookflix`.`libros` WHERE lid=%s", (id))
    borrado=cursor.fetchone()
    conn.commit()
    return render_template('dashboard/delete.html', borrado = borrado)
# BORRAR DEFINITIVO REGISTRO
@app.route('/deleted/<int:id>')
def delete(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM `cac_bookflix`.`libros` WHERE lid=%s", (id))#query directo que borra el registro con el lid(bbd) igual al id pasado como arg.
    conn.commit()
    
    flash('Libro borrado con éxito')
    
    return redirect('/')#volvemos a la raiz..

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
        return redirect('/edit/{}'.format(_lid))
    
    data = (_titulo,_descripcion,_fecha_publicacion,_categoria,_autor,_imagen,_pdf,_lid)
    
    sql = "UPDATE `cac_bookflix`.`libros` SET `titulo`=%s, `descripcion`=%s, `fecha_publicacion`=%s, `categoria`=%s, `autor`=%s, `imagen`=%s, `pdf`=%s WHERE lid=%s;"

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, data)
    conn.commit()
    
    flash('Libro editado con éxito')

    return redirect('/')


if __name__=='__main__':
    app.run(debug=True)