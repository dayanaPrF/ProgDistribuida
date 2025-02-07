import os
import json
import threading
import socket
import time
from datetime import datetime
from Archivo import Archivo

class Server:
    def __init__(self, pathCarpeta, update_Time = 30):
        self.pathCarpeta = pathCarpeta
        self.update_Time = update_Time
        self.lista_archivos = []
        self.lista_nombres = []
        self.configurationFile = "config.json"
        self.log_file = "history.log"
        self.server_socket = None
        self.lock = threading.Lock()
        self.stop_event = threading.Event()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.port = 50000
        self.host=socket.gethostname()
    
    def log_historial(self, mensaje):
        #Registra un mensaje en el archivo history.log con la fecha y hora
        try:
            with open(self.log_file, "a") as log:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log.write(f"[{timestamp}]\t {mensaje}\n")
        except Exception as e:
            print(f"Error al escribir en el log: {e}")

     #Para obtener la lista de archivos en la carpeta especificada
    def obtenerNombresArchivos(self,carpeta):
        lista_nombres = []
        try:
            for arch in os.listdir(carpeta): #Obtiene los nombrre de los archivos de la ruta
                if os.path.isfile(os.path.join(carpeta, arch)): #Verifica si existe el archivo en la ruta dada
                    lista_nombres.append(arch) #Añadimos a la lista de nombres
            return lista_nombres
        except Exception as e:
            print(f"Error al obtener archivos: {e}")
            return None
        
    #Cargar JSON
    def cargarConfiguracionJSON(self):
        try:
            with open(self.configurationFile, "r") as f:
                config = json.load(f)  #Cargar el JSON en un diccionario
            return config
        except Exception as e:
            print(f"Error al cargar la configuración: {e}")
    
    