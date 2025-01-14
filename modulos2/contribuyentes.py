import customtkinter as ctk
import tkinter as tk
from modulos.menubar import menubar
from functions.functions import * 
from tkinter import ttk, messagebox
from functions.rectangle import rectangle
import tkinter


def contribuyentes(window, last_window):
    global busquedainm, busquedabtn, refrescarbtn
    
    for widget in window.winfo_children():
        widget.destroy()

    ctk.set_appearance_mode('dark')
    ctk.set_default_color_theme('dark-blue')
    
    poppins30bold = ("Poppins", 30, "bold")
    poppins20bold = ("Poppins", 20, "bold")
    poppins14bold = ("Poppins", 14, "bold")
    poppins12 = ("Poppins", 12)
    
    menubar(window)
    
    top_frame = ctk.CTkFrame(window, height=100, corner_radius=15)
    top_frame.pack(fill="x", padx=10, pady=10)

    top_frame2 = ctk.CTkFrame(window, height=100, corner_radius=15)
    top_frame2.pack(fill="x", padx=10)

    bottom_frame = ctk.CTkFrame(window, corner_radius=15)
    bottom_frame.pack(padx=10, pady=10, fill="both", expand=True)
    
    #Contenido del top frame
    menu = last_window
    volver_btn = ctk.CTkButton(top_frame, text="Volver", command=lambda: menu(window), font=poppins20bold)
    volver_btn.pack(padx=10, pady=10, side="left")
    
    window_title = ctk.CTkLabel(top_frame, text="Contribuyentes Catastrales", font=poppins30bold)
    window_title.pack(padx=10, pady=10, side="left")

    #Contenido del top frame 2

    refrescarbtn = ctk.CTkButton(top_frame2, text="Refrescar Tabla", font=poppins14bold, width=80, command=lambda: loaddata(my_tree))
    refrescarbtn.pack(padx=5, pady=5, side="right")

    busquedabtn = ctk.CTkButton(top_frame2, text="Buscar", font=poppins14bold, width=80, command=lambda: reload_treeviewsearch(my_tree, busquedainm))
    busquedabtn.pack(padx=5, pady=5, side="right")

    busquedainm = ctk.CTkEntry(top_frame2, placeholder_text="Buscar por cedula", font=poppins14bold, width=200)
    busquedainm.pack(padx=5, pady=5, side="right")

    #Contenido del bottom frame

    treeframe = ctk.CTkFrame(bottom_frame, corner_radius=15)
    treeframe.pack(padx=5, pady=5, fill="both", expand=True)
    
    # Creando el treeview para mostrar los registros
    frame_tree = ctk.CTkFrame(treeframe, fg_color='white', width=580, height=360)
    frame_tree.pack(pady=10, padx=10, expand=True, fill="both")  

    style = ttk.Style()
    style.configure("Custom.Treeview", font=("Poppins", 12), rowheight=25)  
    style.configure("Custom.Treeview.Heading", font=("Poppins", 14, "bold")) 

    my_tree = ttk.Treeview(frame_tree, style="Custom.Treeview", show="headings")
    my_tree.pack(pady=10, padx=10, fill="both", expand=True)
    
    horizontal_scrollbar = ttk.Scrollbar(frame_tree, orient="horizontal", command=my_tree.xview)

    my_tree.configure(xscrollcommand=horizontal_scrollbar.set)

    horizontal_scrollbar.pack(side="bottom", fill="x")

    my_tree['columns'] = ('nombre', 'apellido', 'cedula', 'rif', 'telefono', 'correo')

    for col in my_tree['columns']:
        my_tree.heading(col, text=col.capitalize(), anchor='center')  # Con el metodo de string capitalize() mostramos el texto en mayusculas
        my_tree.column(col, anchor='center')

    canvas = ctk.CTkCanvas(frame_tree, width=0, height=0, highlightthickness=0, bg='white')
    canvas.pack()  # Posicionamos el canvas
    rectangle(canvas, 10, 10, 0, 0, r=5, fill='lightgray', outline='black')
    
    loaddata(my_tree)
    
    return window

def reload_treeviewsearch(treeview, ci):
    ci = ci.get()
    try:
        with connection() as conn:
            cursor = conn.cursor()
            sql = ''' 
            SELECT id_contribuyente, nombres, apellidos, v_e || "-" || ci_contribuyente AS cedula_completa, j_c_g || "-" || rif AS rif_completo,
            telefono, correo FROM contribuyentes where ci_contribuyente = ?
            '''
            cursor.execute(sql,(ci,))
            results = cursor.fetchall()

            # Clear existing rows
            for row in treeview.get_children():
                treeview.delete(row)

            # Insert updated rows
            for row in results:
                treeview.insert("", "end", iid=row[0], values=row[1:])
    except Exception as e:
        print(f"Error refreshing Treeview: {e}")
        
def loaddata(treeview):
    try:
        with connection() as conn:
            cursor = conn.cursor()
            sql = 'SELECT id_contribuyente, nombres, apellidos, v_e || "-" || ci_contribuyente AS cedula_completa, j_c_g || "-" || rif AS rif_completo, telefono, correo FROM contribuyentes'
            cursor.execute(sql)
            results = cursor.fetchall()

            # Clear existing rows
            for row in treeview.get_children():
                treeview.delete(row)

            # Insert updated rows
            for row in results:
                treeview.insert("", "end", iid=row[0], values=row[1:])
    except Exception as e:
        print(f'Ocurrio un error: {e}')
