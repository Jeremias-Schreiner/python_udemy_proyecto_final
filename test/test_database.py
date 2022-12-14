import unittest
import database as db
import copy

from helpers import dni_validator

class TestDatabase(unittest.TestCase):

    def setUp(self) -> None:
        db.Clientes.listaClientes = [
            db.Cliente('20-40828342-6',"Jeremias", "Perez"),
            db.Cliente('20-40458981-6', "Pedro", "A"),
            db.Cliente('20-40828981-2', "N", "a"),
            db.Cliente('20-40823212-6', "Jeremias", "2"),
            db.Cliente('20-40828985-6', "Jeremias", "2"),
        ]

    def test_buscar(self):
        cliente_existente = db.Clientes.buscar('20-40828342-6')
        cliente_inexistente = db.Clientes.buscar('20-40828342-1')

        self.assertIsNotNone(cliente_existente)
        self.assertIsNone(cliente_inexistente)
    
    def test_crear(self):
        lenAntesDeCrear = len(db.Clientes.listaClientes)
        nuevo_cliente = db.Clientes.crear('22-40828342-6', "Jer","sch")
        self.assertEqual(len(db.Clientes.listaClientes),lenAntesDeCrear+1)
        self.assertEqual(nuevo_cliente.dni, '22-40828342-6')
        self.assertEqual(nuevo_cliente.nombre, "Jer")
        self.assertEqual(nuevo_cliente.apellido, "sch")

    def test_modificar_cliente(self):
        cliente_a_modificar = copy.copy(db.Clientes.buscar('20-40828342-6'))
        cliente_modificado = db.Clientes.modificar('20-40828342-6', "Jeremías", "Schreiner")
        self.assertEqual(cliente_a_modificar.nombre, "Jeremias")
        self.assertEqual(cliente_a_modificar.apellido, "Perez")
        self.assertEqual(cliente_modificado.apellido, "Schreiner")
    
    def test_borrar_cliente(self):
        cliente_borrado = db.Clientes.borrar('20-40828342-6')
        cliente_buscado = db.Clientes.buscar('20-40828342-6')
        self.assertEqual(cliente_borrado.dni,'20-40828342-6')
        self.assertIsNone(cliente_buscado)
    

    def test_dni(self):
        self.assertTrue(dni_validator('20-40828342-1', db.Clientes.listaClientes))
        self.assertFalse(dni_validator('20-40828342-6', db.Clientes.listaClientes))
        self.assertFalse(dni_validator('r',db.Clientes.listaClientes))
        self.assertFalse(dni_validator('40828981',db.Clientes.listaClientes))
    
    def test_escritura_csv(self):
        db.Clientes.borrar('20-40828342-6')
        db.Clientes.borrar('20-40458981-6')
        db.Clientes.modificar('20-40823212-6',"Fake Jeremias", 'Fake Schreiner')
