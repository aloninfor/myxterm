from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from models import db, User, ConnectionLog
from services import connect_ssh, connect_rdp, connect_vnc
import os

app = Flask(__name__)

# Configuración básica
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["JWT_SECRET_KEY"] = "super_secret_key"  # Cambiar a algo seguro en producción
db.init_app(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Ruta de inicialización del usuario admin
@app.before_first_request
def create_admin():
    db.create_all()
    if not User.query.filter_by(username="admin").first():
        hashed_pwd = bcrypt.generate_password_hash("admin123").decode("utf-8")
        admin = User(username="admin", password=hashed_pwd, role="admin")
        db.session.add(admin)
        db.session.commit()
        print("Usuario administrador creado con contraseña: admin123")

# Ruta de autenticación
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(username=data["username"]).first()
    if user and bcrypt.check_password_hash(user.password, data["password"]):
        access_token = create_access_token(identity={"username": user.username, "role": user.role})
        return jsonify({"access_token": access_token}), 200
    return jsonify({"msg": "Usuario o contraseña incorrectos"}), 401

# Ruta protegida para obtener conexiones
@app.route("/connect/<service>", methods=["POST"])
@jwt_required()
def connect(service):
    current_user = get_jwt_identity()
    data = request.json

    if service == "ssh":
        result = connect_ssh(data["host"], data["port"], data["username"], data["password"])
    elif service == "rdp":
        result = connect_rdp(data["host"], data["port"], data["username"], data["password"])
    elif service == "vnc":
        result = connect_vnc(data["host"], data["port"], data["password"])
    else:
        return jsonify({"msg": "Servicio no soportado"}), 400

    log = ConnectionLog(user=current_user["username"], service=service, status=result)
    db.session.add(log)
    db.session.commit()

    return jsonify({"result": result}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
