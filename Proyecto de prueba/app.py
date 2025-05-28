from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import os

# Crear la aplicación Flask
app = Flask(__name__)

# Clave secreta necesaria para manejar sesiones y mensajes flash de forma segura
app.secret_key = 'clave_secreta_segura'


# Ruta principal ("/") que muestra la página de inicio
@app.route('/')
def index():
    # Obtener un posible mensaje desde los parámetros URL (GET)
    msg = request.args.get('msg')
    # Renderizar la plantilla index.html, enviando el mensaje (si hay)
    return render_template('index.html', msg=msg)


# Ruta para registrar usuarios (tanto GET para mostrar el formulario como POST para procesar datos)
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Obtener datos enviados desde el formulario
        nombres = request.form['nombres']
        primer_apellido = request.form['primer_apellido']
        segundo_apellido = request.form['segundo_apellido']
        fecha_nacimiento = request.form['fecha_nacimiento']
        telefono = request.form['telefono']
        email = request.form['email']
        contraseña = request.form['contraseña']

        # Conectar a la base de datos SQLite
        conn = sqlite3.connect('stock_plus.db')
        cursor = conn.cursor()
        try:
            # Intentar insertar un nuevo usuario con los datos recibidos
            cursor.execute(
                'INSERT INTO usuarios (nombres, primer_apellido, segundo_apellido, fecha_nacimiento, telefono, email, contraseña) VALUES (?, ?, ?, ?, ?, ?, ?)',
                (nombres, primer_apellido, segundo_apellido, fecha_nacimiento, telefono, email, contraseña))
            conn.commit()  # Guardar cambios
            conn.close()   # Cerrar conexión
            # Redirigir al login con mensaje de éxito en registro
            return redirect(url_for('login', msg='registro_exitoso'))
        except sqlite3.IntegrityError:
            # En caso de error (ej. email duplicado), cerrar conexión y redirigir al registro con mensaje de error
            conn.close()
            return redirect(url_for('register', msg='error_registro'))

    # Si es GET, obtener mensaje (si existe) y mostrar el formulario
    msg = request.args.get('msg')
    return render_template('register.html', msg=msg)


# Ruta para iniciar sesión (GET para mostrar formulario, POST para validar usuario)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Obtener datos del formulario
        email = request.form['email']
        contraseña = request.form['contraseña']

        # Conectar a la base de datos
        conn = sqlite3.connect('stock_plus.db')
        cursor = conn.cursor()
        # Buscar usuario con email y contraseña coincidentes
        cursor.execute('SELECT * FROM usuarios WHERE email = ? AND contraseña = ?', (email, contraseña))
        user = cursor.fetchone()
        conn.close()

        if user:
            # Si se encuentra usuario, guardar datos en sesión para mantener login activo
            session['email'] = email
            nombres = user[1]           # Asumiendo que el nombre está en la columna 1
            primer_apellido = user[2]   # Primer apellido en la columna 2
            session['nombre_completo'] = f"{nombres} {primer_apellido}"
            # Redirigir a página de éxito con mensaje de login correcto
            return redirect(url_for('success', msg='login_exitoso'))
        else:
            # Si no se encuentra usuario, redirigir a login con mensaje de error
            return redirect(url_for('login', msg='error_login'))
    
    # Si es GET, obtener mensaje para mostrar en la plantilla
    msg = request.args.get('msg')
    return render_template('login.html', msg=msg)


# Ruta para mostrar página de éxito luego de iniciar sesión correctamente
@app.route('/success')
def success():
    # Verificar si el usuario está logueado revisando sesión
    if 'email' in session:
        nombre_completo = session.get('nombre_completo', 'Usuario')
        msg = request.args.get('msg')  # Obtener mensaje desde URL (opcional)
        # Renderizar plantilla success.html con nombre completo y mensaje
        return render_template('success.html', nombre_completo=nombre_completo, msg=msg)
    # Si no está logueado, redirigir a login
    return redirect(url_for('login'))


# Ruta para cerrar sesión, limpia la sesión y redirige a inicio con mensaje
@app.route('/logout')
def logout():
    session.clear()  # Elimina toda la información de sesión (logout)
    return redirect(url_for('index', msg='logout_exitoso'))


# Ejecutar la aplicación en modo debug para desarrollo
if __name__ == '__main__':
    app.run(debug=True)
