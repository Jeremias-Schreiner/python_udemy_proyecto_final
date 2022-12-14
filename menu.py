import os
import helpers
import database as db

def iniciar():
    while True:
        helpers.limpiar_pantalla()
        print("========================")
        print("  BIENVENIDO AL Manager ")
        print("========================")
        print("[1] Listar clientes     ")
        print("[2] Buscar cliente      ")
        print("[3] Añadir cliente      ")
        print("[4] Modificar cliente   ")
        print("[5] Borrar cliente      ")
        print("[6] Cerrar el Manager   ")
        print("========================")

        opcion = input("> ")
        helpers.limpiar_pantalla()

        if opcion == '1':
            if len(db.Clientes.listaClientes) != 0:
                for cliente in db.Clientes.listaClientes:
                    print(cliente)
            else:
                print("No se encuentran cargados clientes")
        elif opcion == '2':
            print("Buscando un cliente...\n")
            dni = helpers.leer_texto(13, 13, "DNI (fomato de numero: xx-xxxxxxxx-x)")
            cliente = db.Clientes.buscar(dni)
            print(cliente) if cliente else print("Cliente no encontrado")
        elif opcion == '3':
            print("Añadiendo un cliente...\n")
            dni = None
            while True:
                dni = helpers.leer_texto(13, 13, "DNI (fomato de numero: xx-xxxxxxxx-x)")
                validacion = helpers.dni_validator(dni, db.Clientes.listaClientes)
                if validacion:
                    break
                

            nombre = helpers.leer_texto(2, 30, "Nombre (2 a 30 char)").capitalize()
            apellido = helpers.leer_texto(2, 30, "Apellido (2 a 30 char)").capitalize()

            db.Clientes.crear(dni=dni, nombre=nombre, apellido=apellido)

        elif opcion == '4':
            print("Modificando un cliente...\n")
            dni = helpers.leer_texto(13, 13, "DNI (fomato de numero: xx-xxxxxxxx-x)")
            cliente = db.Clientes.buscar(dni)

            if cliente:
                nombre = helpers.leer_texto(2,30, f"Nombre (de 2 a 30 chars) [{cliente.nombre}]").capitalize()
                apellido = helpers.leer_texto(2,30, f"Apellido (de 2 a 30 chars) [{cliente.apellido}]").capitalize()

                db.Clientes.modificar(dni=dni, nombre=nombre, apellido=apellido)
                print("Cliente modificado correctamente")
            else:
                print("Cliente no encontrado")
        elif opcion == '5':
            print("Borrando un cliente...\n")
            dni = helpers.leer_texto(13, 13, "DNI (fomato de numero: xx-xxxxxxxx-x)")
            cliente = db.Clientes.buscar(dni)

            cliente = db.Clientes.borrar(dni=dni)
            print("Cliente borrado correctamente") if cliente else print("Cliente no encontrado")
        elif opcion == '6':
            print("Saliendo...\n")
            break

        input("\n Presiona ENTER para continuar")