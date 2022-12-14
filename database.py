import csv
import config

class Cliente:

    def __init__(self, dni, nombre, apellido) -> None:
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido
    
    def __str__(self) -> str:
        return f"{self.dni} {self.nombre} {self.apellido}"
    
class Clientes:

    listaClientes = []

    with open(config.DATABASE_PATH, newline='\n') as archivo:
        reader = csv.reader(archivo, delimiter=';')
        for dni, nombre, apellido in reader:
            cliente = Cliente(dni=dni, nombre=nombre, apellido=apellido)
            listaClientes.append(cliente)

    @staticmethod
    def buscar(dni):
        for cliente in Clientes.listaClientes:
            if cliente.dni == dni:
                return cliente
    
    @staticmethod
    def crear(dni, nombre, apellido):
        cliente = Cliente(dni, nombre, apellido)
        Clientes.listaClientes.append(cliente)
        Clientes.guardar()
        return cliente
    
    @staticmethod
    def modificar(dni, nombre, apellido):
        for indice,cliente in enumerate(Clientes.listaClientes):
            if cliente.dni == dni:
                cliente.nombre = nombre
                cliente.apellido = apellido
                Clientes.guardar()
                return cliente

    @staticmethod
    def borrar(dni):
        for indice, cliente in enumerate(Clientes.listaClientes):
            if cliente.dni == dni:
                cliente = Clientes.listaClientes.pop(indice)
                Clientes.guardar()
                return cliente
    

    @staticmethod
    def guardar():
        with open(config.DATABASE_PATH, 'w+', newline='\n') as archivo:
            writer = csv.writer(archivo, delimiter=';')
            for cliente in Clientes.listaClientes:
                writer.writerow([cliente.dni, cliente.nombre, cliente.apellido])