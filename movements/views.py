from movements import app
from flask import render_template, request, url_for, redirect
import csv
import sqlite3
from movements import forms

DBFILE = 'movements/data/DBFLASK.db'

def consulta(query, params=()):
    conn = sqlite3.connect(DBFILE)
    c = conn.cursor()
    '''
    'SELECT * FROM TABLA' -> [(),(), (),]
    'SELECT * FROM TABLA VACIA ' -> []
    'INSERT ...' -> []
    'UPDATE ...' -> []
    'DELETE ...' -> []
    '''

    c.execute(query, params)
    conn.commit()

    filas = c.fetchall()
    print(filas)

    conn.close()


    if len(filas) == 0:
        return filas

    columnNames = []
    for columnName in c.description:
        columnNames.append(columnName[0])

    listaDeDiccionarios = []

    for fila in filas:
        d = {}
        for ix, columnName in enumerate(columnNames):
            d[columnName] = fila[ix]
        listaDeDiccionarios.append(d)

    return listaDeDiccionarios

@app.route('/')
def listaIngresos():
    miformulario=myform.alta()
    ingresos = consulta('SELECT fecha, concepto, cantidad, id FROM movimientos;')

    total = 0
    for ingreso in ingresos:
        total += float(ingreso['cantidad'])


    return render_template("movementsList.html",datos=ingresos, total=total)

@app.route('/creaalta', methods=['GET', 'POST'])
def nuevoIngreso():
    if request.method == 'POST':
        # iNSERT INTO movimientos (cantidad, concepto, fecha) VALUES (1500, "Paga extra", "2020-12-16" )

        cantidad = request.form.get('cantidad')
        try:
            cantidad = float(cantidad)
        except ValueError:
            msgError = 'Cantidad debe ser numérico'
            return render_template("alta", errores = msgError)

        consulta('INSERT INTO movimientos (cantidad, concepto, fecha) VALUES (?, ? ,? );', 
                 (
                    float(request.form.get('cantidad')),
                    request.form.get('concepto'),
                    request.form.get('fecha')
                 )
        )

        return redirect(url_for('listaIngresos'))
        


    return render_template("alta.html")


@app.route("/modifica/<id>", methods=['GET', 'POST'])
def modificaIngreso(id):
    conn = sqlite3.connect(DBFILE)
    c = conn.cursor()

    if request.method == 'GET':

        registro = consulta('SELECT fecha, concepto, cantidad, id FROM movimientos where id = ?', (id,))[0] 

        return render_template("modifica.html", registro=registro)
    else:
        consulta('UPDATE movimientos SET fecha = ?, concepto= ?, cantidad = ? WHERE id = ?',
                  (request.form.get('fecha'),
                   request.form.get('concepto'),
                   float(request.form.get('cantidad')),
                   id
                  )
        )

        return redirect(url_for("listaIngresos"))
    

@app.route('/mi_alta', methods=['GET', 'POST'])
def nuevoIngreso():
    if request.method == 'POST':
        # iNSERT INTO movimientos (cantidad, concepto, fecha) VALUES (1500, "Paga extra", "2020-12-16" )

        cantidad = request.form.get('cantidad')
        try:
            cantidad = float(cantidad)
        except ValueError:
            msgError = 'Cantidad debe ser numérico'
            return render_template("mi_alta", errores = msgError)

        consulta('INSERT INTO movimientos (cantidad, concepto, fecha) VALUES (?, ? ,? );', 
                 (
                    float(request.form.get('cantidad')),
                    request.form.get('concepto'),
                    request.form.get('fecha')
                 )
        )

        return redirect(url_for('listaIngresos'))

    return render_template("mi_alta.html")





'''
def diccionarios():
    if len(listaDeDiccionarios) ==1:
        return listaDeDiccionarios[0]
    elif len(listaDeDiccionarios) ==0:
        return None
    else:
        return listaDeDiccionarios
'''