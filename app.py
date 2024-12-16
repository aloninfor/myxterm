# Aplicación web de accesos SSH, RDP, VNC, HTTP, HTTPS con autenticación y gestión de usuarios

## Backend usando Flask y Flask-SocketIO

from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from sqlalchemy.exc import IntegrityError
import paramiko
import docker
import asyncio

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_clave_secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar herramientas
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

docker_client = docker.from_env()

# Definir modelo de base de datos
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), default='user')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Rutas principales
@app.route('/')
@login_required
def index():
    return render_template('index.html', username=current_user.username, role=current_user.role)

@app.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    if request.method == 'POST':
        data = request.form
        username = data['username']
        password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        role = data.get('role', 'user')
        try:
            user = User(username=username, password=password, role=role)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('index'))
        except IntegrityError:
            db.session.rollback()
            return render_template('register.html', error="Usuario ya existe")
    return render_template('register.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        login_user(user)
        return jsonify({"message": "Inicio de sesión exitoso"})
    return jsonify({"message": "Usuario o contraseña incorrectos"}), 401

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Sesión cerrada con éxito"})

# Función de conexión SSH
async def ssh_connect(host, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=host, username=username, password=password)
        return "Conexión SSH exitosa"
    except Exception as e:
        return str(e)
    finally:
        client.close()

# Configuración inicial para crear el usuario administrador
@app.before_first_request
def create_admin():
    admin = User.query.filter_by(role='admin').first()
    if not admin:
        admin_password = bcrypt.generate_password_hash("admin123").decode('utf-8')
        admin = User(username="admin", password=admin_password, role='admin')
        db.session.add(admin)
        db.session.commit()

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, host='0.0.0.0') app.py
