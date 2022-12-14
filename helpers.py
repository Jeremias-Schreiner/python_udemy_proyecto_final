import os
import platform
import re


def limpiar_pantalla():
    os.system('cls') if platform.system() == "Windows" else os.system('clear')


def leer_texto(longitud_min=0, longitud_max=100, mensaje=None):
    print(mensaje) if mensaje else None
    while True:
        texto = input("> ")
        print(texto)
        if len(texto) >= longitud_min and len(texto)<= longitud_max:
            return texto
        print("Longitud Incorrecta")


def dni_validator(dni, listaClientes):
    if not re.match('[0-9]{2}-[0-9]{8}-[0-9]',dni):#En realidad esto es el cuil pero es mejor para practicar
        print("DNI incorrecto")
        return False
    for cliente in listaClientes:
        if cliente.dni == dni:
            print("DNI utilizado por otro cliente")
            return False

    return True
        