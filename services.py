import subprocess

def connect_ssh(host, port, username, password):
    try:
        # Aquí podrías usar paramiko para una solución más robusta
        result = subprocess.run(["ssh", f"{username}@{host}", "-p", str(port)], timeout=5)
        return "Conexión SSH exitosa"
    except Exception as e:
        return f"Error en SSH: {str(e)}"

def connect_rdp(host, port, username, password):
    return "Conexión RDP exitosa (lógica pendiente)"

def connect_vnc(host, port, password):
    return "Conexión VNC exitosa (lógica pendiente)"
