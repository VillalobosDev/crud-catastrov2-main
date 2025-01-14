from datetime import datetime
from functions.functions import connection

def rango_fecha_search(my_tree, original_data, start_date, end_date):
    """Filter treeview data based on Date Range (Rango Fecha) via DB query."""
    if not start_date or not end_date:
        print("Please provide both start and end date.")
        return

    # Assuming the date format in the entries is dd-mm-yyyy
    try:
        # Convert string dates to datetime objects to check validity if needed
        start_date = datetime.strptime(start_date, "%d-%m-%Y")
        end_date = datetime.strptime(end_date, "%d-%m-%Y")
    except ValueError:
        print("Invalid date format. Please use dd-mm-yyyy.")
        return

    # Assuming you're using SQLite here, but you can adjust this based on your DB.
    with connection() as conn:
        cursor = conn.cursor()

        # Modify your SQL query to filter by date range
        sql = '''
        SELECT 
            inmuebles.nom_inmueble,
            inmuebles.cod_catastral,
            inmuebles.uso,
            contribuyentes.nombres || ' ' || contribuyentes.apellidos AS contribuyente,
            contribuyentes.ci_contribuyente,
            contribuyentes.rif,
            contribuyentes.telefono,
            contribuyentes.correo,
            sectores.nom_sector,
            sectores.ubic_sector,
            liquidaciones.id_liquidacion,
            liquidaciones.monto_1,
            liquidaciones.monto_2,
            liquidaciones.fecha_Liquidacion_1,
            liquidaciones.fecha_Liquidacion_2
        FROM
            inmuebles
        JOIN contribuyentes ON inmuebles.id_contribuyente = contribuyentes.id_contribuyente
        JOIN sectores ON inmuebles.id_sector = sectores.id_sector
        JOIN liquidaciones ON inmuebles.id_inmueble = liquidaciones.id_inmueble
        WHERE liquidaciones.fecha_Liquidacion_1 BETWEEN ? AND ?
        ORDER BY contribuyentes.ci_contribuyente ASC
        '''

        # Execute the query with the date range parameters
        cursor.execute(sql, (start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")))

        # Fetch the filtered data from the query
        filtered_data = cursor.fetchall()

    # Now update your treeview with the fetched data
    update_treeview(my_tree, filtered_data)

def update_treeview(my_tree, data):
    """Update the treeview with new data."""
    for item in my_tree.get_children():
        my_tree.delete(item)

    for row in data:
        my_tree.insert("", "end", values=row)
