import sqlite3

def connection():
    return sqlite3.connect('db.db')

def read():
    try:
        with connection() as conn:
            cursor = conn.cursor()
            sql = """SELECT * FROM contribuyentes"""
            cursor.execute(sql)
            results = cursor.fetchall()

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        results = []

    return results

def refreshTable(my_tree, results=None):
    
    # Limpiamos los elementos existentes en el tree
    my_tree.delete(*my_tree.get_children())


    # Si se añadio un valor para results en el llamado de la funcion se insertan en el tree
    # Donde results usualmente en un read() de la db
    
    if results:
#        print(f'Results type: {type(results)}')
        for i, array in enumerate(results):
            tag = "evenrow" if i % 2 == 0 else "oddrow" # Altenar los colores establecidos en my_tree.tag_configure
            my_tree.insert(parent='', index='end', text="", values=array, tag=tag)

    else:
        print("Something went wrong in refreshtable function")


    # Configuracion para las filas de registros
    my_tree.tag_configure('evenrow', background="#EEEEEE")
    my_tree.tag_configure('oddrow', background="#FFFFFF") 
