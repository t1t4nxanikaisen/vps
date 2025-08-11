from flask import Flask, jsonify, request
import docker
import subprocess
import os

app = Flask(__name__)

# Initialize Docker client
client = docker.from_env()

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

@app.route('/api/vps', methods=['POST'])
def create_vps():
    data = request.json
    image = data.get('image', 'ubuntu:latest')
    name = data.get('name', 'my-vps')
    ports = data.get('ports', {})
    
    try:
        container = client.containers.run(
            image,
            name=name,
            ports=ports,
            detach=True,
            tty=True,
            stdin_open=True
        )
        return jsonify({
            "id": container.id,
            "name": name,
            "status": "created"
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/vps/<vps_id>', methods=['GET'])
def get_vps(vps_id):
    try:
        container = client.containers.get(vps_id)
        return jsonify({
            "id": container.id,
            "name": container.name,
            "status": container.status,
            "image": container.image.tags[0] if container.image.tags else ""
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 404

@app.route('/api/vps/<vps_id>/start', methods=['POST'])
def start_vps(vps_id):
    try:
        container = client.containers.get(vps_id)
        container.start()
        return jsonify({"status": "started"})
    except Exception as e:
        return jsonify({"error": str(e)}), 404

@app.route('/api/vps/<vps_id>/stop', methods=['POST'])
def stop_vps(vps_id):
    try:
        container = client.containers.get(vps_id)
        container.stop()
        return jsonify({"status": "stopped"})
    except Exception as e:
        return jsonify({"error": str(e)}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
