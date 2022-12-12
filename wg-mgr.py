from string import Template
import json
import os
import shutil
import pathlib

in_folder = "in"
out_folder = "out"
out_folder_clients = os.path.join(out_folder, "clients")

if os.path.exists(out_folder):
    shutil.rmtree(out_folder)

pathlib.Path(out_folder_clients).mkdir(parents=True)

with open(os.path.join(in_folder, 'server.json'), 'r') as f:
    server_data = json.load(f)

with open(os.path.join(in_folder, 'clients.json'), 'r') as f:
    clients_data = json.load(f)

with open(os.path.join(in_folder, 'server.conf.in'), 'r') as f:
    src = Template(f.read())
    server_conf = src.substitute(server_data)
    with open(os.path.join(in_folder, 'server.peers.conf.in'), 'r') as f:
        srcc = Template(f.read())
        for client in clients_data:
            server_conf += srcc.substitute(client)
        with open(os.path.join(out_folder, f"{server_data['wireguard_interface']}.conf"), 'w') as f:
            f.write(server_conf)
    
with open(os.path.join(in_folder, 'client.conf.in'), 'r') as f:
    src = Template(f.read())
    for client in clients_data:
        client_merged = {**server_data, **client}
        client_conf = src.substitute(client_merged)
        with open(os.path.join(out_folder_clients, f"{client['client_name']}.conf"), 'w') as f:
            f.write(client_conf)
