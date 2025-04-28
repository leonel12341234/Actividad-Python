import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="curso"
    )

def insertar():
    nombre = entry_nombre.get()
    edad = entry_edad.get()
    materia = entry_materia.get()
    if nombre and edad and materia:
        db = conectar()
        cursor = db.cursor()
        cursor.execute("INSERT INTO estudiantes (Nombres, Edad, Materia) VALUES (%s, %s, %s)", (nombre, edad, materia))
        db.commit()
        db.close()
        messagebox.showinfo("Éxito", "Estudiante agregado")
        mostrar_tabla()  # Mostrar la tabla después de insertar
    else:
        messagebox.showwarning("Faltan datos", "Completá todos los campos")

def consultar():
    materia = entry_materia.get()
    if materia:
        db = conectar()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM estudiantes WHERE Materia = %s", (materia,))
        resultados = cursor.fetchall()
        db.close()
        # Limpiar el Treeview
        for row in treeview.get_children():
            treeview.delete(row)
        # Insertar los resultados de la consulta en el Treeview
        for row in resultados:
            treeview.insert("", tk.END, values=row)
    else:
        messagebox.showwarning("Faltan datos", "Ingresá una materia")

def actualizar():
    id_ = entry_id.get()
    nueva = entry_materia.get()
    if id_ and nueva:
        db = conectar()
        cursor = db.cursor()
        cursor.execute("UPDATE estudiantes SET Materia = %s WHERE id = %s", (nueva, id_))
        db.commit()
        db.close()
        messagebox.showinfo("Éxito", "Materia actualizada")
        mostrar_tabla()  # Mostrar la tabla después de actualizar
    else:
        messagebox.showwarning("Faltan datos", "Completá ID y nueva materia")

def eliminar():
    id_ = entry_id.get()
    if id_:
        db = conectar()
        cursor = db.cursor()
        cursor.execute("DELETE FROM estudiantes WHERE id = %s", (id_,))
        db.commit()
        db.close()
        messagebox.showinfo("Éxito", "Estudiante eliminado")
        mostrar_tabla()  # Mostrar la tabla después de eliminar
    else:
        messagebox.showwarning("Faltan datos", "Ingresá un ID")

def mostrar_tabla():
    db = conectar()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM estudiantes")
    resultados = cursor.fetchall()
    db.close()
    # Limpiar el Treeview
    for row in treeview.get_children():
        treeview.delete(row)
    # Insertar los resultados en el Treeview
    for row in resultados:
        treeview.insert("", tk.END, values=row)

# Interfaz
root = tk.Tk()
root.title("CRUD de Estudiantes")
root.geometry("600x500")

# Entradas y botones
tk.Label(root, text="ID (para modificar/eliminar)").pack()
entry_id = tk.Entry(root)
entry_id.pack()

tk.Label(root, text="Nombres").pack()
entry_nombre = tk.Entry(root)
entry_nombre.pack()

tk.Label(root, text="Edad").pack()
entry_edad = tk.Entry(root)
entry_edad.pack()

tk.Label(root, text="Materia").pack()
entry_materia = tk.Entry(root)
entry_materia.pack()

tk.Button(root, text="Insertar", command=insertar).pack(pady=5)
tk.Button(root, text="Consultar por materia", command=consultar).pack(pady=5)
tk.Button(root, text="Actualizar materia", command=actualizar).pack(pady=5)
tk.Button(root, text="Eliminar por ID", command=eliminar).pack(pady=5)

# Treeview para mostrar la tabla
columns = ("ID", "Nombres", "Edad", "Materia")
treeview = ttk.Treeview(root, columns=columns, show="headings")

# Configuración de las columnas
for col in columns:
    treeview.heading(col, text=col)
    treeview.column(col, width=100)

treeview.pack(pady=20)

# Mostrar los datos al inicio
mostrar_tabla()

root.mainloop()
