#!/usr/bin/python

import subprocess
import json
import asyncio
from fastapi import FastAPI, Request
import threading
import socket
import structlog
from structlog.dev import set_exc_info, ConsoleRenderer
from structlog.processors import StackInfoRenderer, TimeStamper, add_log_level
import logging
import sys
import datetime
import os
from pydantic import BaseModel
from urllib.parse import urlparse, parse_qs

class TCPServer:
    def __init__(self, host=os.getenv("SERVERHOST", "127.0.0.1"), port=int(os.getenv("SERVERPORT", 8001))):
        self.clients: list[socket.socket] = []
        self.host = host
        self.port = port
        self.lock = threading.Lock() 
        self.running = False
        
    def run(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(3)
        self.running = True
        accept_thread = threading.Thread(target=self._accept_connections)
        accept_thread.daemon = True
        accept_thread.start()

    def stop(self):
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        with self.lock:
            for client in self.clients:
                client.close()
            self.clients.clear()

    def _accept_connections(self):
        while self.running:
            try:
                client_socket, addr = self.server_socket.accept()
                with self.lock:
                    self.clients.append(client_socket)
            except OSError:                
                break
            except Exception as e:
                print (str(e))

    def send_message(self, message: str):
        dead_clients = []

        with self.lock:
            for client in self.clients:
                try:
                    client.sendall(message.encode("utf-8"))
                except Exception as e:
                    dead_clients.append(client)

            for client in dead_clients:
                try:
                    client.close()
                    self.clients.remove(client)
                except ValueError:
                    pass  # already removed
                    
            

# Настройка стандартного логгера
logging.basicConfig(
    format="%(message)s",
    stream=sys.stdout,
    level=logging.INFO,
)


def config_structlog():
    structlog.configure_once(
        processors=[
            add_log_level,
            StackInfoRenderer(),
            set_exc_info,
            TimeStamper(fmt="%Y-%m-%d %H:%M.%S", utc=False),
            ConsoleRenderer(),
        ], 
	logger_factory=structlog.stdlib.LoggerFactory(), 
	cache_logger_on_first_use=True, 
    )



def config_JSON_logger(): 
    fileHandler = logging.FileHandler("log.json") 
    fileFormatter = structlog.stdlib.ProcessorFormatter ( 
        processor=structlog.processors.JSONRenderer(),
	foreign_pre_chain=[ 
	    structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M.%S", utc=False), 
	    structlog.processors.StackInfoRenderer(), 
	    set_exc_info, 
	    add_log_level, 
	], 
    ) 
    fileHandler.setFormatter(fileFormatter) 
    logging.getLogger().addHandler(fileHandler)

# Вызов конфигурации логирования
config_structlog()
config_JSON_logger() 
# Создание логгера
logger = structlog.get_logger()

MMS = TCPServer()
async def lifespan(app: FastAPI):
    MMS.run()
    yield
    MMS.stop()

class Body(BaseModel):
    expression: str
    is_float: bool

app = FastAPI(lifespan = lifespan)
history = "./history.txt"

@app.get("/")
async def answer():
    return

@app.post("/calc")
async def post_answer(body: Body):
    logger.info("POST request received %s, %s", body.expression, body.is_float)
        
    is_float_mode = body.is_float
        
    content_length = int(len(body.expression))
    expression = body.expression
        
    if ((expression is None)or(expression == '')):
        logger.error("Bad request: missing expression")
        return {"error": "missing expression"}

    mode_flag = '--float' if is_float_mode else '--int'
    logger.info("Calculating expression", expression=expression, mode=mode_flag)
    result = subprocess.run(["./../build/app.exe", mode_flag], input = expression, text=True, capture_output=True)

    if result.returncode == 0:
        response = {"result": result.stdout.strip()}
        logger.info("Calculation successful", result=response["result"])
        MMS.send_message(json.dumps({"expression": expression, "result": result.stdout.strip()}))
        try:
            with open(history, 'a') as his_file:
                his_file.write(str({"expression": expression, "result": result.stdout.strip()}) + '\n')
        except Exception as e:
            logger.error("Saving history failed: %s", str(e))
        return response
    else:
        logger.error("Calculation failed", error=result.stderr)
        return {"error": result.returncode}

@app.get("/history")
async def h_answer():
    try:
        res = []
        with open(history, 'r') as his_file:
            while True:
                line = his_file.readline()
                if not line:
                    break
                res.append(line)
    except Exception as e:
        res = [{"error": "error while reading file"}]
    return res
