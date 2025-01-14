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

def update_contribuyente_info(ci_entry, nombre_entry, inmueble_menu):
    ci_contribuyente = ci_entry.get()
    try:
        with connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id_contribuyente, nombres || ' ' || apellidos FROM contribuyentes WHERE ci_contribuyente = ?", (ci_contribuyente,))
            contribuyente = cursor.fetchone()
            if contribuyente:
                id_contribuyente, nombre_completo = contribuyente
                nombre_entry.delete(0, tk.END)
                nombre_entry.insert(0, nombre_completo)

                cursor.execute("SELECT nom_inmueble FROM inmuebles WHERE id_contribuyente = ?", (id_contribuyente,))
                inmuebles = cursor.fetchall()
                inmueble_menu.configure(values=[inmueble[0] for inmueble in inmuebles])
            else:
                nombre_entry.delete(0, tk.END)
                inmueble_menu.configure(values=[""])
    except Exception as e:
        print(f"Error updating contribuyente info: {e}")

def save_liquidacion(my_tree, ci_entry, nombre_entry, inmueble_menu, monto1_entry, monto2_entry, fecha1_entry, fecha2_entry):
    ci_contribuyente = ci_entry.get()
    inmueble = inmueble_menu.get()
    monto1 = monto1_entry.get()
    monto2 = monto2_entry.get()
    fecha1 = fecha1_entry.get()
    fecha2 = fecha2_entry.get()

    try:
        with connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id_contribuyente FROM contribuyentes WHERE ci_contribuyente = ?", (ci_contribuyente,))
            contribuyente = cursor.fetchone()
            if contribuyente:
                id_contribuyente = contribuyente[0]
                cursor.execute("SELECT id_inmueble FROM inmuebles WHERE nom_inmueble = ? AND id_contribuyente = ?", (inmueble, id_contribuyente))
                inmueble = cursor.fetchone()
                if inmueble:
                    id_inmueble = inmueble[0]
                    cursor.execute("SELECT * FROM liquidaciones WHERE id_inmueble = ?", (id_inmueble,))
                    liquidacion = cursor.fetchone()
                    if liquidacion:
                        print("Ya existe una liquidación para este inmueble.")
                    else:
                        cursor.execute("INSERT INTO liquidaciones (id_contribuyente, id_inmueble, monto_1, monto_2, fecha_Liquidacion_1, fecha_Liquidacion_2) VALUES (?, ?, ?, ?, ?, ?)",
                                       (id_contribuyente, id_inmueble, monto1, monto2, fecha1, fecha2))
                        conn.commit()
                        load_liquidaciones_data(my_tree)
                        print("Liquidación guardada exitosamente.")
                        clearentrys(ci_entry, nombre_entry, inmueble_menu, monto1_entry, monto2_entry, fecha1_entry, fecha2_entry)
                else:
                    print("Inmueble no encontrado.")
            else:
                print("Contribuyente no encontrado.")
    except Exception as e:
        print(f"Error guardando la liquidación: {e}")

def gestionar_liquidacion(treeview, ci_entry, nombre_entry, inmueble_menu, monto1_entry, monto2_entry, fecha1_entry, fecha2_entry):
    selected_item = treeview.selection()
    if selected_item:
        item = treeview.item(selected_item)
        values = item['values']
        ci_entry.delete(0, tk.END)
        ci_entry.insert(0, values[0])
        nombre_entry.delete(0, tk.END)
        nombre_entry.insert(0, values[1])
        inmueble_menu.set(values[2])
        monto1_entry.delete(0, tk.END)
        monto1_entry.insert(0, values[3])
        monto2_entry.delete(0, tk.END)
        monto2_entry.insert(0, values[4])
        fecha1_entry.delete(0, tk.END)
        fecha1_entry.insert(0, values[5])
        fecha2_entry.delete(0, tk.END)
        fecha2_entry.insert(0, values[6])

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

def update_liquidacion(tree, ci_entry, nombre_entry, inmueble_menu, monto1_entry, monto2_entry, fecha1_entry, fecha2_entry):
    ci_contribuyente = ci_entry.get()
    inmueble = inmueble_menu.get()
    monto1 = monto1_entry.get()
    monto2 = monto2_entry.get()
    fecha1 = fecha1_entry.get()
    fecha2 = fecha2_entry.get()

    try:
        with connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id_contribuyente FROM contribuyentes WHERE ci_contribuyente = ?", (ci_contribuyente,))
            contribuyente = cursor.fetchone()
            if contribuyente:
                id_contribuyente = contribuyente[0]
                cursor.execute("SELECT id_inmueble FROM inmuebles WHERE nom_inmueble = ? AND id_contribuyente = ?", (inmueble, id_contribuyente))
                inmueble = cursor.fetchone()
                if inmueble:
                    id_inmueble = inmueble[0]
                    cursor.execute("UPDATE liquidaciones SET monto_1 = ?, monto_2 = ?, fecha_Liquidacion_1 = ?, fecha_Liquidacion_2 = ? WHERE id_inmueble = ?",
                                   (monto1, monto2, fecha1, fecha2, id_inmueble))
                    conn.commit()
                    load_liquidaciones_data(tree)
                    clearentrys(ci_entry, nombre_entry, inmueble_menu, monto1_entry, monto2_entry, fecha1_entry, fecha2_entry)

                    print("Liquidación actualizada exitosamente.")
                else:
                    print("Inmueble no encontrado.")
            else:
                print("Contribuyente no encontrado.")
    except Exception as e:
        print(f"Error actualizando la liquidación: {e}")

def delete_liquidacion(ci_entry, inmueble_menu, my_tree):
    ci_contribuyente = ci_entry.get()
    inmueble = inmueble_menu.get()

    confirm = messagebox.askyesno("Confirmación", "¿Está seguro de que desea eliminar esta liquidación?")
    if not confirm:
        return

    try:
        with connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id_contribuyente FROM contribuyentes WHERE ci_contribuyente = ?", (ci_contribuyente,))
            contribuyente = cursor.fetchone()
            if contribuyente:
                id_contribuyente = contribuyente[0]
                cursor.execute("SELECT id_inmueble FROM inmuebles WHERE nom_inmueble = ? AND id_contribuyente = ?", (inmueble, id_contribuyente))
                inmueble = cursor.fetchone()
                if inmueble:
                    id_inmueble = inmueble[0]
                    cursor.execute("DELETE FROM liquidaciones WHERE id_inmueble = ?", (id_inmueble,))
                    conn.commit()
                    print("Liquidación eliminada exitosamente.")
                    load_liquidaciones_data(my_tree)
                else:
                    print("Inmueble no encontrado.")
            else:
                print("Contribuyente no encontrado.")
    except Exception as e:
        print(f"Error eliminando la liquidación: {e}")

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

    crearinm = ctk.CTkButton(top_frame2, text="Asignar", command=lambda: ifasignar(window, bottom_frame, top_frame2, busquedabtn, busquedaliq), font=poppins14bold)
    crearinm.pack(padx=5, pady=5, side="left")

    gestionarinm = ctk.CTkButton(top_frame2, text="Gestionar", command=lambda: ifgestionar(window, bottom_frame, top_frame2, busquedabtn, busquedaliq), font=poppins14bold)
    gestionarinm.pack(padx=5, pady=5, side="left")

    # Contenido del bottom frame
    treeframe = ctk.CTkFrame(bottom_frame, corner_radius=15)
    treeframe.pack(padx=5, pady=5, fill="both", expand=True)

    # Creando el treeview para mostrar los registros
    frame_tree = ctk.CTkFrame(treeframe, fg_color='white', width=580, height=360)
    frame_tree.pack(pady=10, padx=10, expand=True, fill="both")

    my_tree = setup_treeview(frame_tree)
    load_liquidaciones_data(my_tree)

def ifgestionar(window, bottom_frame, top_frame2, busquedabtnold, busquedaliqold):
    global busquedabtn, busquedaliq

    if busquedabtnold:
        busquedabtnold.pack_forget()
    if busquedaliqold:
        busquedaliqold.pack_forget()

    poppins14bold = ("Poppins", 14, "bold")

    for widget in bottom_frame.winfo_children():
        widget.destroy()

    



    frame_left = ctk.CTkFrame(bottom_frame, corner_radius=15, width=400)
    frame_left.pack(padx=5, pady=5, side="left", fill="both", expand=True)

    frame_right = ctk.CTkFrame(bottom_frame, corner_radius=15)
    frame_right.pack(padx=5, pady=5, side="right", fill="both", expand=True)

    # Add UI elements for the left frame
    ci_frame = ctk.CTkFrame(frame_left)
    ci_frame.pack(padx=10, pady=5, fill="x")

    nombre_frame = ctk.CTkFrame(frame_left)
    nombre_frame.pack(padx=10, pady=5, fill="x")

    monto1_frame = ctk.CTkFrame(frame_left)
    monto1_frame.pack(padx=10, pady=5, fill="x")

    monto2_frame = ctk.CTkFrame(frame_left)
    monto2_frame.pack(padx=10, pady=5, fill="x")

    fecha1_frame = ctk.CTkFrame(frame_left)
    fecha1_frame.pack(padx=10, pady=5, fill="x")

    fecha2_frame = ctk.CTkFrame(frame_left)
    fecha2_frame.pack(padx=10, pady=5, fill="x")

    inmueble_frame = ctk.CTkFrame(frame_left)
    inmueble_frame.pack(padx=10, pady=5, fill="x")

    ci_entry = ctk.CTkEntry(ci_frame, placeholder_text="Cedula Contribuyente", font=poppins14bold)
    ci_entry.pack(pady=5, padx=5, side="left", fill="x", expand=True)

    nombre_entry = ctk.CTkEntry(nombre_frame, placeholder_text="Nombre Contribuyente", font=poppins14bold)
    nombre_entry.pack(pady=5, padx=5, side="left", fill="x", expand=True)

    monto1 = ctk.CTkEntry(monto1_frame, placeholder_text="Monto 1", font=poppins14bold)
    monto1.pack(pady=5, padx=5, side="left", fill="x", expand=True)

    monto2 = ctk.CTkEntry(monto2_frame, placeholder_text="Monto 2", font=poppins14bold)
    monto2.pack(pady=5, padx=5, side="left", fill="x", expand=True)

    fecha1 = ctk.CTkEntry(fecha1_frame, placeholder_text="Fecha Liquidacion 1", font=poppins14bold)
    fecha1.pack(pady=5, padx=5, side="left", fill="x", expand=True)

    fecha1_btn = ctk.CTkButton(fecha1_frame, text="📅", command=lambda: open_calendar_popup(fecha1), font=poppins14bold, width=30)
    fecha1_btn.pack(pady=5, padx=5, side="left")

    fecha2 = ctk.CTkEntry(fecha2_frame, placeholder_text="Fecha Liquidacion 2", font=poppins14bold)
    fecha2.pack(pady=5, padx=5, side="left", fill="x", expand=True)

    fecha2_btn = ctk.CTkButton(fecha2_frame, text="📅", command=lambda: open_calendar_popup(fecha2), font=poppins14bold, width=30)
    fecha2_btn.pack(pady=5, padx=5, side="left")

    inmueble_menu = ctk.CTkOptionMenu(inmueble_frame, values=["Inmuebles"], font=poppins14bold)
    inmueble_menu.pack(pady=5, padx=5, side="left", fill="x", expand=True)

    ci_entry.bind("<FocusOut>", lambda e: update_contribuyente_info(ci_entry, nombre_entry, inmueble_menu))


    btncancel = ctk.CTkButton(frame_left, text="Cancelar", command=lambda: clearentrys(ci_entry, nombre_entry, inmueble_menu, monto1, monto2, fecha1, fecha2), font=poppins14bold)
    btncancel.pack(padx=10, pady=10, anchor="e", side="bottom")

    btndelete = ctk.CTkButton(frame_left, text="Eliminar", command=lambda: delete_liquidacion(ci_entry, inmueble_menu, my_tree), font=poppins14bold)
    btndelete.pack(padx=10, pady=10, anchor="e", side="bottom")

    btnsave = ctk.CTkButton(frame_left, text="Guardar", command=lambda: update_liquidacion(my_tree, ci_entry, nombre_entry, inmueble_menu, monto1, monto2, fecha1, fecha2), font=poppins14bold)
    btnsave.pack(padx=10, pady=10, anchor="e", side="bottom")

    # Add Treeview for the right frame
    frame_tree = ctk.CTkFrame(frame_right, fg_color="white")
    frame_tree.pack(pady=10, padx=10, expand=True, fill="both")

    my_tree = setup_treeview(frame_tree)
    load_liquidaciones_data(my_tree)

    my_tree.bind("<ButtonRelease-1>", lambda e: gestionar_liquidacion(my_tree, ci_entry, nombre_entry, inmueble_menu, monto1, monto2, fecha1, fecha2))        

    busquedabtn = ctk.CTkButton(top_frame2, text="Buscar", font=poppins14bold, width=80, command=lambda: reload_treeviewsearch(my_tree, busquedaliq))
    busquedabtn.pack(padx=5, pady=5, side="right")

    busquedaliq = ctk.CTkEntry(top_frame2, placeholder_text="Buscar por cedula", font=poppins14bold, width=200)
    busquedaliq.pack(padx=5, pady=5, side="right")

def ifasignar(window, bottom_frame, top_frame2, busquedabtnold, busquedaliqold):
    global busquedabtn, busquedaliq
    if busquedabtnold:
        busquedabtnold.pack_forget()
    if busquedaliqold:
        busquedaliqold.pack_forget()

    poppins14bold = ("Poppins", 14, "bold")

    for widget in bottom_frame.winfo_children():
        widget.destroy()

    frame_left = ctk.CTkFrame(bottom_frame, corner_radius=15, width=400)
    frame_left.pack(padx=5, pady=5, side="left", fill="both", expand=True)

    frame_right = ctk.CTkFrame(bottom_frame, corner_radius=15)
    frame_right.pack(padx=5, pady=5, side="right", fill="both", expand=True)





    # Add UI elements for the left frame
    ci_frame = ctk.CTkFrame(frame_left)
    ci_frame.pack(padx=10, pady=5, fill="x")

    nombre_frame = ctk.CTkFrame(frame_left)
    nombre_frame.pack(padx=10, pady=5, fill="x")

    monto1_frame = ctk.CTkFrame(frame_left)
    monto1_frame.pack(padx=10, pady=5, fill="x")

    monto2_frame = ctk.CTkFrame(frame_left)
    monto2_frame.pack(padx=10, pady=5, fill="x")

    fecha1_frame = ctk.CTkFrame(frame_left)
    fecha1_frame.pack(padx=10, pady=5, fill="x")

    fecha2_frame = ctk.CTkFrame(frame_left)
    fecha2_frame.pack(padx=10, pady=5, fill="x")

    inmueble_frame = ctk.CTkFrame(frame_left)
    inmueble_frame.pack(padx=10, pady=5, fill="x")

    ci_entry = ctk.CTkEntry(ci_frame, placeholder_text="Cedula Contribuyente", font=poppins14bold)
    ci_entry.pack(pady=5, padx=5, side="left", fill="x", expand=True)

    nombre_entry = ctk.CTkEntry(nombre_frame, placeholder_text="Nombre Contribuyente", font=poppins14bold)
    nombre_entry.pack(pady=5, padx=5, side="left", fill="x", expand=True)

    monto1 = ctk.CTkEntry(monto1_frame, placeholder_text="Monto 1", font=poppins14bold)
    monto1.pack(pady=5, padx=5, side="left", fill="x", expand=True)

    monto2 = ctk.CTkEntry(monto2_frame, placeholder_text="Monto 2", font=poppins14bold)
    monto2.pack(pady=5, padx=5, side="left", fill="x", expand=True)

    fecha1 = ctk.CTkEntry(fecha1_frame, placeholder_text="Fecha Liquidacion 1", font=poppins14bold)
    fecha1.pack(pady=5, padx=5, side="left", fill="x", expand=True)

    fecha1_btn = ctk.CTkButton(fecha1_frame, text="📅", command=lambda: open_calendar_popup(fecha1), font=poppins14bold, width=30)
    fecha1_btn.pack(pady=5, padx=5, side="left")

    fecha2 = ctk.CTkEntry(fecha2_frame, placeholder_text="Fecha Liquidacion 2", font=poppins14bold)
    fecha2.pack(pady=5, padx=5, side="left", fill="x", expand=True)

    fecha2_btn = ctk.CTkButton(fecha2_frame, text="📅", command=lambda: open_calendar_popup(fecha2), font=poppins14bold, width=30)
    fecha2_btn.pack(pady=5, padx=5, side="left")

    inmueble_menu = ctk.CTkOptionMenu(inmueble_frame, values=["Inmuebles"], font=poppins14bold)
    inmueble_menu.pack(pady=5, padx=5, side="left", fill="x", expand=True)

    ci_entry.bind("<FocusOut>", lambda e: update_contribuyente_info( ci_entry, nombre_entry, inmueble_menu))

    ###################################### Add Treeview for the right frame
    frame_tree = ctk.CTkFrame(frame_right, fg_color="white")
    frame_tree.pack(pady=10, padx=10, expand=True, fill="both")
    
    ######################################
    my_tree = setup_treeview(frame_tree)
    ######################################
    
    btncancel = ctk.CTkButton(frame_left, text="Cancelar", command=lambda: clearentrys(ci_entry, nombre_entry, inmueble_menu, monto1, monto2, fecha1, fecha2), font=poppins14bold)
    btncancel.pack(padx=10, pady=10, anchor="e", side="bottom")

    
    btnsave = ctk.CTkButton(frame_left, text="Guardar", command=lambda: save_liquidacion(my_tree, ci_entry, nombre_entry, inmueble_menu, monto1, monto2, fecha1, fecha2), font=poppins14bold)
    btnsave.pack(padx=10, pady=10, anchor="e", side="bottom")

    load_liquidaciones_data(my_tree)

    busquedabtn = ctk.CTkButton(top_frame2, text="Buscar", font=poppins14bold, width=80, command=lambda: reload_treeviewsearch(my_tree, busquedaliq))
    busquedabtn.pack(padx=5, pady=5, side="right")

    busquedaliq = ctk.CTkEntry(top_frame2, placeholder_text="Buscar por cedula", font=poppins14bold, width=200)
    busquedaliq.pack(padx=5, pady=5, side="right")
