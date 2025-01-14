import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import customtkinter as ctk
from functions.functions import *
from modulos.menubar import menubar
from functions.calendario import open_calendar_popup  # Import the calendar popup function

def setup_treeview(frame):
    style = ttk.Style()
    style.configure("Custom.Treeview", font=("Poppins", 12), rowheight=25)
    style.configure("Custom.Treeview.Heading", font=("Poppins", 14, "bold"))

    treeview = ttk.Treeview(frame, style="Custom.Treeview", show="headings")
    treeview.pack(pady=10, padx=10, fill="both", expand=True)

    treeview["columns"] = ("CI","Contribuyente Nombre", "Inmueble", "Monto 1", "Monto 2", "Fecha Liq 1", "Fecha Liq 2")
    for col in treeview["columns"]:
        treeview.heading(col, text=col.capitalize(), anchor="center")
        treeview.column(col, anchor="center")

    return treeview

def load_liquidaciones_data(treeview):
    try:
        with connection() as conn:
            cursor = conn.cursor()
            sql = """
            SELECT l.id_liquidacion, c.ci_contribuyente, c.nombres || ' ' || c.apellidos AS contribuyente_nombre, i.nom_inmueble, l.monto_1, l.monto_2, l.fecha_Liquidacion_1, l.fecha_Liquidacion_2
            FROM liquidaciones l
            JOIN inmuebles i ON l.id_inmueble = i.id_inmueble
            JOIN contribuyentes c ON l.id_contribuyente = c.id_contribuyente
            """
            cursor.execute(sql)
            results = cursor.fetchall()

            # Clear existing rows
            for row in treeview.get_children():
                treeview.delete(row)

            # Insert updated rows
            for row in results:
                treeview.insert("", "end", iid=row[0], values=row[1:])

    except Exception as e:
        print(f"Error fetching data: {e}")

def reload_treeviewsearch(treeview, ci_contribuyente):
    ci_contribuyente = ci_contribuyente.get()
    try:
        with connection() as conn:
            cursor = conn.cursor()
            sql = ''' 
            SELECT  l.id_liquidacion, c.ci_contribuyente, c.nombres || ' ' || c.apellidos AS contribuyente_nombre, i.nom_inmueble, l.monto_1, l.monto_2, l.fecha_Liquidacion_1, l.fecha_Liquidacion_2
            FROM liquidaciones l
            JOIN inmuebles i ON l.id_inmueble = i.id_inmueble
            JOIN contribuyentes c ON l.id_contribuyente = c.id_contribuyente
            WHERE c.ci_contribuyente = ?
            '''
            cursor.execute(sql, (ci_contribuyente,))
            results = cursor.fetchall()

            # Clear existing rows
            for row in treeview.get_children():
                treeview.delete(row)

            # Insert updated rows
            for row in results:
                treeview.insert("", "end", iid=row[0], values=row[1:])
    except Exception as e:
        print(f"Error refreshing Treeview: {e}")

def clearentrys(ci_entry, nombre_entry, inmueble_menu, monto1_entry, monto2_entry, fecha1_entry, fecha2_entry):
        ci_entry.delete(0, tk.END)
        ci_entry.configure(placeholder_text="Cedula Contribuyente")

        nombre_entry.delete(0, tk.END)
        nombre_entry.configure(placeholder_text="Nombre Contribuyente")

        monto1_entry.delete(0, tk.END)
        monto1_entry.configure(placeholder_text="Monto 1")

        monto2_entry.delete(0, tk.END)
        monto2_entry.configure(placeholder_text="Monto 2")
        
        fecha1_entry.delete(0, tk.END)
        fecha1_entry.configure(placeholder_text="Fecha Liquidación 1")

        fecha2_entry.delete(0, tk.END)
        fecha2_entry.configure(placeholder_text="Fecha Liquidación 2")

        inmueble_menu.set("Inmuebles")

def liquidacion(window, last_window):
    global busquedabtn, busquedaliq


    for widget in window.winfo_children():
        widget.destroy()

    ctk.set_appearance_mode('dark')
    ctk.set_default_color_theme('dark-blue')

    poppins30bold = ("Poppins", 30, "bold")
    poppins20bold = ("Poppins", 20, "bold")
    poppins14bold = ("Poppins", 14, "bold")
    poppins12 = ("Poppins", 12, "bold")

    menubar(window)

    top_frame = ctk.CTkFrame(window, height=100, corner_radius=15)
    top_frame.pack(fill="x", padx=10, pady=10)

    top_frame2 = ctk.CTkFrame(window, height=100, corner_radius=15)
    top_frame2.pack(fill="x", padx=10)

    bottom_frame = ctk.CTkFrame(window, corner_radius=15)
    bottom_frame.pack(padx=10, pady=10, fill="both", expand=True)

    # Contenido del top frame
    menu = last_window
    volver_btn = ctk.CTkButton(top_frame, text="Volver", command=lambda: menu(window), font=poppins20bold)
    volver_btn.pack(padx=10, pady=10, side="left")

    window_title = ctk.CTkLabel(top_frame, text="Sección de Gestión Liquidaciones", font=poppins30bold)
    window_title.pack(padx=10, pady=10, side="left")

    # Contenido del top frame 2
    
    refreshtreeview = ctk.CTkButton(top_frame2, text="Refrescar Arbol", font=poppins14bold, width=80, command=lambda: load_liquidaciones_data(my_tree, ))
    refreshtreeview.pack(padx=5, pady=5, side="right")

    busquedabtn = ctk.CTkButton(top_frame2, text="Buscar", font=poppins14bold, width=80, command=lambda: reload_treeviewsearch(my_tree, busquedaliq))
    busquedabtn.pack(padx=5, pady=5, side="right")

    busquedaliq = ctk.CTkEntry(top_frame2, placeholder_text="Buscar por cedula", font=poppins14bold, width=200)
    busquedaliq.pack(padx=5, pady=5, side="right")

    # Contenido del bottom frame
    treeframe = ctk.CTkFrame(bottom_frame, corner_radius=15)
    treeframe.pack(padx=5, pady=5, fill="both", expand=True)

    # Creando el treeview para mostrar los registros
    frame_tree = ctk.CTkFrame(treeframe, fg_color='white', width=580, height=360)
    frame_tree.pack(pady=10, padx=10, expand=True, fill="both")

    my_tree = setup_treeview(frame_tree)
    load_liquidaciones_data(my_tree)
