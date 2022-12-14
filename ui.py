from tkinter import *
from tkinter import ttk
from tkinter.messagebox import askokcancel, showerror, WARNING, ERROR

import database as db

from helpers import dni_validator


class GrayButton(Button):
    def __init__(self, master, **kwargs):
        super().__init__(master=master, **kwargs, bg="gray", fg="white")


class CenterWidgetMixin:
    def center(self):
        self.update()

        width = self.winfo_width()
        height = self.winfo_height()

        screenWidth = self.winfo_screenwidth()
        screenHeight = self.winfo_screenheight()

        x = int(screenWidth / 2 - width / 2)
        y = int(screenHeight / 2 - height / 2)

        self.geometry(f"{width}x{height}+{x}+{y}")


class CreateClientWindow(Toplevel, CenterWidgetMixin):
    def __init__(self, parent):
        super().__init__(parent)
        self.title = "Crear Cliente"
        self.build()
        self.center()
        # Esto es para obligar a resolver la sub ventana primero
        self.transient(parent)
        self.grab_set()

    def build(self):
        frame = Frame(self)
        frame.pack(padx=20, pady=20)

        Label(frame, text="DNI (xx-xxxxxxxx-x").grid(row=0, column=0)
        Label(frame, text="Nombre (de 2 a 30 chars)").grid(row=0, column=1)
        Label(frame, text="Apellido (de 2 a 30 chars)").grid(row=0, column=2)

        dni = Entry(frame)
        dni.grid(row=1, column=0)
        dni.bind("<KeyRelease>", lambda event: self.validate(event, 0))

        nombre = Entry(frame)
        nombre.grid(row=1, column=1)
        nombre.bind("<KeyRelease>", lambda event: self.validate(event, 1))

        apellido = Entry(frame)
        apellido.grid(row=1, column=2)
        apellido.bind("<KeyRelease>", lambda event: self.validate(event, 2))

        frame = Frame(self)
        frame.pack(pady=10)

        self.crear = GrayButton(frame, text="Crear", command=self.create_client)
        self.crear.config(state=DISABLED)
        self.crear.grid(row=0, column=0)

        GrayButton(frame, text="Cancelar", command=self.close).grid(row=0, column=1)

        self.validaciones = [False, False, False]

        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido

    def create_client(self):
        self.master.treeView.insert(
            parent="",
            index="end",
            iid=self.dni.get(),
            values=(self.dni.get(), self.nombre.get(), self.apellido.get())
        )
        db.Clientes.crear(
            self.dni.get(),
            self.nombre.get(), 
            self.apellido.get()
        )
        self.close()

    def validate(self, event, target):
        text = event.widget.get()
        valido = (
            dni_validator(text, db.Clientes.listaClientes)
            if target == 0
            else text.isalpha() and 2 <= len(text) <= 30
        )
        event.widget.configure({"bg": "green" if valido else "red"})

        self.validaciones[target] = valido

        self.crear.config(state=NORMAL if self.validaciones == [1, 1, 1] else DISABLED)

    def close(self):
        self.destroy()
        self.update()


class EditClientWindow(Toplevel, CenterWidgetMixin):
    def __init__(self, parent):
        super().__init__(parent)
        self.title = "Actualizar Cliente"
        self.build()
        self.center()
        # Esto es para obligar a resolver la sub ventana primero
        self.transient(parent)
        self.grab_set()

    def build(self):
        frame = Frame(self)
        frame.pack(padx=20, pady=20)

        Label(frame, text="DNI No editable").grid(row=0, column=0)
        Label(frame, text="Nombre (de 2 a 30 chars)").grid(row=0, column=1)
        Label(frame, text="Apellido (de 2 a 30 chars)").grid(row=0, column=2)

        dni = Entry(frame)
        dni.grid(row=1, column=0)

        nombre = Entry(frame)
        nombre.grid(row=1, column=1)
        nombre.bind("<KeyRelease>", lambda event: self.validate(event, 0))

        apellido = Entry(frame)
        apellido.grid(row=1, column=2)
        apellido.bind("<KeyRelease>", lambda event: self.validate(event, 1))

        cliente = self.master.treeView.focus()
        campos = self.master.treeView.item(cliente, 'values')

        dni.insert(0, campos[0])
        dni.config(state=DISABLED)
        nombre.insert(0, campos[1])
        apellido.insert(0, campos[2])

        frame = Frame(self)
        frame.pack(pady=10)

        self.actualizar = GrayButton(frame, text="Actualizar", command=self.edit_client)
        self.actualizar.grid(row=0, column=0)

        GrayButton(frame, text="Cancelar", command=self.close).grid(row=0, column=1)

        self.validaciones = [1, 1]

        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido

    def edit_client(self):
        cliente = self.master.treeView.focus()
        self.master.treeView.item(cliente, values=(
            self.dni.get(),
            self.nombre.get(),
            self.apellido.get(),
        ))

        db.Clientes.modificar(
            self.dni.get(),
            self.nombre.get(),
            self.apellido.get(),
        )

        self.close()

    def validate(self, event, target):
        text = event.widget.get()
        valido = text.isalpha() and 2 <= len(text) <= 30
        event.widget.configure({"bg": "green" if valido else "red"})

        self.validaciones[target] = valido

        self.actualizar.config(state=NORMAL if self.validaciones == [1, 1] else DISABLED)

    def close(self):
        self.destroy()
        self.update()


class MainWindow(Tk, CenterWidgetMixin):
    def __init__(self):
        super().__init__()
        self.title("Gestor de Clientes")
        self.build()
        self.center()

    def build(self):
        self.call("source", "forest-dark.tcl")

        tkStyle = ttk.Style(self)
        tkStyle.theme_use("forest-dark")

        frame = Frame(self)
        frame.pack()

        treeView = ttk.Treeview(frame)
        treeView["columns"] = ("DNI", "Nombre", "Apellido")

        treeView.column("#0", width=0, stretch=NO)
        treeView.column("DNI", anchor=CENTER)
        treeView.column("Nombre", anchor=CENTER)
        treeView.column("Apellido", anchor=CENTER)

        treeView.heading("DNI", text="DNI", anchor=CENTER)
        treeView.heading("Nombre", text="Nombre", anchor=CENTER)
        treeView.heading("Apellido", text="Apellido", anchor=CENTER)

        scrollbar = Scrollbar(frame, cursor="hand2", command=treeView.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        treeView["yscrollcommand"] = scrollbar.set

        for cliente in db.Clientes.listaClientes:
            treeView.insert(
                parent="",
                index="end",
                iid=cliente.dni,
                values=(cliente.dni, cliente.nombre, cliente.apellido),
            )

        treeView.pack()

        frame = Frame()
        frame.pack(pady=20)

        aF = GrayButton(frame, text="Crear", command=self.create).grid(row=0, column=0)
        button = GrayButton(frame, text="Modificar", command=self.edit).grid(row=0, column=1)
        button = GrayButton(frame, text="Borrar", command=self.delete).grid(
            row=0, column=3
        )

        self.treeView = treeView

    def delete(self):
        cliente = self.treeView.focus()
        if cliente:
            clienteCampos = self.treeView.item(cliente, "values")
            confirmar = askokcancel(
                title="Confirmar borrado",
                message=f"¿Desea borrar a {clienteCampos[2]} {clienteCampos[1]} {clienteCampos[0]}?",
                icon=WARNING,
            )
            if confirmar:
                self.treeView.delete(cliente)
                db.Clientes.borrar(clienteCampos[0])

    def create(self):
        CreateClientWindow(self)

    def edit(self):
        if self.treeView.focus() != "":
            EditClientWindow(self)
        else:
            showerror(title="Error de Cliente", message="Cliente no seleccionado")

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
