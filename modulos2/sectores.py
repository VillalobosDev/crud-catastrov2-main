import customtkinter as ctk
from modulos.menubar import menubar
from functions.functions import * 
import tkinter as tk
from tkinter import ttk, filedialog
from functions.rectangle import rectangle
from PIL import ImageTk, Image
import sys
import os


def create_image_folder():
    image_folder = "images"
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)
    return image_folder

def cargar_imagen(frameimg):
    global image_path  # Hacer la variable global para acceder a ella en guardar_datos
    file_path = filedialog.askopenfilename()
    if file_path:
        image = Image.open(file_path)
        image = image.resize((240, 240), Image.LANCZOS)
        image_path = file_path  # Guardar la ruta original de la imagen
        
        image_tk = ImageTk.PhotoImage(image)
        
        img_label = ctk.CTkLabel(frameimg, image=image_tk, text="", width=240, height=240)
        img_label.place(x=10, y=10)
        img_label.image = image_tk  # Guardar referencia para evitar que la imagen sea recolectada por el garbage collector

def ifasignar(bottom_frame, window, last_window):
      
    poppins14bold = ("Poppins", 14, "bold")
    poppins30bold = ("Poppins", 30, "bold")
    poppins20bold = ("Poppins", 20, "bold")
    poppins12 = ("Poppins", 12)

    for widget in bottom_frame.winfo_children():
        widget.destroy()
      
    # Contenido del bottom frame
    left_frame = ctk.CTkFrame(bottom_frame, corner_radius=15)
    left_frame.pack(side="left", padx=10, pady=10, fill="both")

    center_frame = ctk.CTkFrame(bottom_frame, corner_radius=15, width=300)
    center_frame.pack(padx=10, pady=10, side="left", fill="both", expand=True)
    
    right_frame_bajo = ctk.CTkFrame(bottom_frame, corner_radius=15)
    right_frame_bajo.pack(side="right", padx=10, pady=10, fill="both")    

    text = ctk.CTkLabel(left_frame, text="Nuevo Sector",font=poppins14bold,width=250)
    text.pack(padx=10, pady=10)    
  
    nom_sectores_frame = ctk.CTkFrame(left_frame)
    nom_sectores_frame.pack(padx=10, pady=5, fill="x")    

    cod_sectores_frame = ctk.CTkFrame(left_frame)
    cod_sectores_frame.pack(padx=10, pady=5, fill="x")
    
    img_sectores_frame = ctk.CTkFrame(center_frame, width=260, height=260)
    img_sectores_frame.pack(pady=50)    
    
    nom_sectores = ctk.CTkEntry(nom_sectores_frame, placeholder_text="Nombre del Sector", font=poppins14bold, width=250)
    nom_sectores.pack(pady=5, padx=5, side="left")
    
    cod_sectores = ctk.CTkEntry(cod_sectores_frame, placeholder_text="Codigo del Sector", font=poppins14bold, width=250)
    cod_sectores.pack(pady=5, padx=5, side="left")

    btncargar = ctk.CTkButton(center_frame, text="Buscar Imagen", command=lambda: cargar_imagen(img_sectores_frame), font=poppins14bold)
    btncargar.pack(padx=30, pady=10)
    
    def guardar_datos():
        nombre = nom_sectores.get()
        codigo = cod_sectores.get()
        
        if not nombre or not codigo:
            text = ctk.CTkLabel(left_frame, text="Todos los campos son obligatorios", text_color="red", font=poppins14bold)
            text.place(x=15, y=350)
            return
        
        try:
            with connection() as conn:
                cursor = conn.cursor()
                # Verificar si el código ya existe
                cursor.execute('SELECT COUNT(*) FROM sectores WHERE cod_sector = ?', (codigo,))
                if cursor.fetchone()[0] > 0:
                    text = ctk.CTkLabel(left_frame, text="       El código del sector ya existe     ", text_color="red", font=poppins14bold,width=260)
                    text.place(x=10, y=350)
                else:
                    # Mover la imagen a la carpeta de imágenes
                    image_folder = create_image_folder()
                    image_name = os.path.basename(image_path)
                    image_save_path = os.path.join(image_folder, image_name)
                    os.rename(image_path, image_save_path)
                    
                    sql = 'INSERT INTO sectores (nom_sector, cod_sector, image_path) VALUES (?, ?, ?)'
                    cursor.execute(sql, (nombre, codigo, image_save_path))
                    conn.commit()
                    print("Datos guardados exitosamente.")
                    
                    # Actualizar el Treeview
                    my_tree.insert("", "end", values=(nombre, codigo))
        except Exception as e:
            print(f"Error al guardar los datos: {e}")

    btnsave = ctk.CTkButton(left_frame, text="Guardar", command=guardar_datos, font=poppins14bold)
    btnsave.pack(padx=10, pady=10, anchor="e", side="bottom")
    
    btnvolver = ctk.CTkButton(left_frame, text="Cancelar", command=lambda: sectores(window, last_window), font=poppins14bold)
    btnvolver.pack(padx=10, pady=10, anchor="e", side="bottom")
    
    # Creando el treeview para mostrar los registros
    
    frame_tree = ctk.CTkFrame(right_frame_bajo, fg_color='white', width=580, height=360)
    frame_tree.pack(pady=10, padx=10, fill="both", expand=True)  

    style = ttk.Style()
    style.configure("Custom.Treeview", font=("Poppins", 12), rowheight=25)  
    style.configure("Custom.Treeview.Heading", font=("Poppins", 14, "bold")) 

    my_tree = ttk.Treeview(frame_tree, style="Custom.Treeview", show="headings")
    my_tree.pack(pady=10, padx=10, fill="both", expand=True)
    
    horizontal_scrollbar = ttk.Scrollbar(frame_tree, orient="horizontal", command=my_tree.xview)
    my_tree.configure(xscrollcommand=horizontal_scrollbar.set)
    horizontal_scrollbar.pack(side="bottom", fill="x")

    my_tree['columns'] = ('Nombre sector', 'Codigo del sector')

    for col in my_tree['columns']:
        my_tree.heading(col, text=col.capitalize(), anchor='center')  # Con el metodo de string capitalize() mostramos el texto en mayusculas
        my_tree.column(col, anchor='center')

    canvas = ctk.CTkCanvas(frame_tree, width=0, height=0, highlightthickness=0, bg='white')
    canvas.pack()  # Posicionamos el canvas
    rectangle(canvas, 10, 10, 0, 0, r=5, fill='lightgray', outline='black')
    
    try:
        with connection() as conn:
            print("Database connection established.")
            cursor = conn.cursor()
            sql = 'SELECT nom_sector, cod_sector FROM sectores'
            cursor.execute(sql)
            results = cursor.fetchall()
            print(f"Query executed successfully, fetched results: {results}")

            # Ensure data fits Treeview structure
            for row in results:
                my_tree.insert("", "end", values=row)

    except Exception as e:
        print(f"Error during database operation: {e}")

def sectores(window, last_window):
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
    
    # Contenido del top frame
    menu = last_window
    volver_btn = ctk.CTkButton(top_frame, text="Volver", command=lambda: menu(window), font=poppins20bold)
    volver_btn.pack(padx=10, pady=10, side="left")
    
    window_title = ctk.CTkLabel(top_frame, text="Visualizador de Sectores", font=poppins30bold)
    window_title.pack(padx=10, pady=10, side="left")

    # Contenido del top frame 2
    crearliq = ctk.CTkButton(top_frame2, text="Asignar", command=lambda: ifasignar(bottom_frame, window, last_window), font=poppins14bold)
    crearliq.pack(padx=5, pady=5, side="left")

    gestionarliq = ctk.CTkButton(top_frame2, text="Gestionar", command=lambda: print("ifgestionar(bottom_frame)"), font=poppins14bold)
    gestionarliq.pack(padx=5, pady=5, side="left")

    eliminarliq = ctk.CTkButton(top_frame2, text="Eliminar", command=lambda: print("Example"), font=poppins14bold)
    eliminarliq.pack(padx=5, pady=5, side="left")

    busquedaliq = ctk.CTkEntry(top_frame2, placeholder_text="Buscar por codigo", font=poppins14bold, width=200)
    busquedaliq.pack(padx=5, pady=5, side="right")

    # Contenido del bottom frame
    left_frame = ctk.CTkFrame(bottom_frame, corner_radius=15)
    left_frame.pack(side="left", padx=10, pady=10, fill="both", expand=True)

    # Frame para la imagen
    image_frame = ctk.CTkFrame(left_frame, width=330, height=330, corner_radius=15)
    image_frame.pack(pady=60)
    image_frame.pack_propagate(False)  # Evita que el frame cambie de tamaño

    image_label = ctk.CTkLabel(image_frame, text="Selecciona un sector para continuar", font=poppins14bold)
    image_label.pack(expand=True, padx=10, pady=10)
    
    confirmar_btn = ctk.CTkButton(left_frame, text="Confirmar", font=poppins14bold, command=lambda: None)
    confirmar_btn.pack(pady=0)

    right_frame_bajo = ctk.CTkFrame(bottom_frame, corner_radius=15)
    right_frame_bajo.pack(side="bottom", padx=10, pady=10, fill="both", expand=True)    
    
    # Creando el treeview para mostrar los registros
    frame_tree = ctk.CTkFrame(right_frame_bajo, fg_color='white', width=580, height=360)
    frame_tree.pack(pady=10, padx=10, fill="both", expand=True)  

    style = ttk.Style()
    style.configure("Custom.Treeview", font=("Poppins", 12), rowheight=25)  
    style.configure("Custom.Treeview.Heading", font=("Poppins", 14, "bold")) 

    my_tree = ttk.Treeview(frame_tree, style="Custom.Treeview", show="headings")
    my_tree.pack(pady=10, padx=10, fill="both", expand=True)
    
    horizontal_scrollbar = ttk.Scrollbar(frame_tree, orient="horizontal", command=my_tree.xview)
    my_tree.configure(xscrollcommand=horizontal_scrollbar.set)
    horizontal_scrollbar.pack(side="bottom", fill="x")

    my_tree['columns'] = ('Nombre sector', 'Codigo del sector')
    for col in my_tree['columns']:
        my_tree.heading(col, text=col.capitalize(), anchor='center')  # Con el metodo de string capitalize() mostramos el texto en mayusculas
        my_tree.column(col, anchor='center')

    def on_tree_select(event):
        selected_item = my_tree.selection()
        if selected_item:
            item = my_tree.item(selected_item)
            sector_name = item['values'][0]
            try:
                with connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT image_path FROM sectores WHERE nom_sector = ?", (sector_name,))
                    image_path = cursor.fetchone()[0]
                    if image_path and os.path.exists(image_path):
                        image = Image.open(image_path)
                        image = image.resize((300, 300), Image.LANCZOS)
                        photo = ImageTk.PhotoImage(image)
                        image_label.configure(image=photo, text="")
                        image_label.image = photo
                    else:
                        print(f"Image not found: {image_path}")
            except Exception as e:
                print(f"Error loading image: {e}")

    my_tree.bind("<<TreeviewSelect>>", on_tree_select)

    try:
        with connection() as conn:
            print("Database connection established.")
            cursor = conn.cursor()
            sql = 'SELECT nom_sector, cod_sector FROM sectores'
            cursor.execute(sql)
            results = cursor.fetchall()
            print(f"Query executed successfully, fetched results: {results}")

            # Ensure data fits Treeview structure
            for row in results:
                my_tree.insert("", "end", values=row)

    except Exception as e:
        print(f"Error during database operation: {e}")
   
def ifgestionar(bottom_frame):

    poppins14bold = ("Poppins", 14, "bold")

    for widget in bottom_frame.winfo_children():
        widget.destroy()

    frame_left = ctk.CTkFrame(bottom_frame, corner_radius=15, width=300)
    frame_left.pack(padx=5, pady=5, side="left", fill="y")

    frame_right = ctk.CTkFrame(bottom_frame, corner_radius=15)
    frame_right.pack(padx=5, pady=5, side="right", fill="both", expand=True)

    contribuyenteci_frame = ctk.CTkFrame(frame_left)
    contribuyenteci_frame.pack(padx=10, pady=5, fill="x")

    contribuyentenombre_frame = ctk.CTkFrame(frame_left)
    contribuyentenombre_frame.pack(padx=10, pady=5, fill="x")

    inmueble_frame = ctk.CTkFrame(frame_left)
    inmueble_frame.pack(padx=10, pady=5, anchor="w")

    inmueblecod_frame = ctk.CTkFrame(frame_left)
    inmueblecod_frame.pack(padx=10, pady=5, fill="x")

    monto1_frame = ctk.CTkFrame(frame_left)
    monto1_frame.pack(padx=10, pady=5, fill="x")

    monto2_frame = ctk.CTkFrame(frame_left)
    monto2_frame.pack(padx=10, pady=5, fill="x")

    fecha_frame = ctk.CTkFrame(frame_left)
    fecha_frame.pack(padx=10, pady=5, fill="x")

    contribuyenteci = ctk.CTkEntry(contribuyenteci_frame, placeholder_text="Cedula Contribuyente", font=poppins14bold, width=250)
    contribuyenteci.pack(pady=5, padx=5, side="left")

    contribuyentenombre = ctk.CTkEntry(contribuyentenombre_frame, placeholder_text="Contribuyente", font=poppins14bold, width=250)
    contribuyentenombre.pack(pady=5, padx=5, side="left")

    valuesinmuebles = ["Inmuebles"]
    inmueble = ctk.CTkOptionMenu(inmueble_frame, values=valuesinmuebles, font=poppins14bold)
    inmueble.pack(padx=5, pady=5, side="left")

    inmueblecod = ctk.CTkEntry(inmueblecod_frame, placeholder_text="Codigo Catastral", font=poppins14bold, width=250)
    inmueblecod.pack(pady=5, padx=5, side="left")

    monto1 = ctk.CTkEntry(monto1_frame, placeholder_text="Monto 1", font=poppins14bold, width=250)
    monto1.pack(pady=5, padx=5, side="left")

    monto2 = ctk.CTkEntry(monto2_frame, placeholder_text="Monto 2", font=poppins14bold, width=250)
    monto2.pack(pady=5, padx=5, side="left")

    fecha = ctk.CTkEntry(fecha_frame, placeholder_text="Fecha Liquidacion", font=poppins14bold, width=250)
    fecha.pack(pady=5, padx=5, side="left")

    btnsave = ctk.CTkButton(frame_left, text="Guardar", command=lambda: print("Guardar Gestión"), font=poppins14bold)
    btnsave.pack(padx=10, pady=10, anchor="e", side="bottom")

    frame_tree = ctk.CTkFrame(frame_right, fg_color="white")
    frame_tree.pack(pady=10, padx=10, expand=True, fill="both")

    style = ttk.Style()
    style.configure("Custom.Treeview", font=("Poppins", 12), rowheight=25)
    style.configure("Custom.Treeview.Heading", font=("Poppins", 14, "bold"))

    my_tree = ttk.Treeview(frame_tree, style="Custom.Treeview", show="headings")
    my_tree.pack(pady=10, padx=10, fill="both", expand=True)

    my_tree["columns"] = ("CI", "Contribuyente", "Inmueble", "Codigo Catastral", "Monto 1", "Monto 2", "Fecha Liquidacion")
    for col in my_tree["columns"]:
        my_tree.heading(col, text=col.capitalize(), anchor="center")
        my_tree.column(col, anchor="center")

    # Fetch data to populate Treeview
    try:
        with connection() as conn:
            cursor = conn.cursor()
            sql = "SELECT * FROM liquidaciones"  # Modify table name as needed
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                my_tree.insert("", "end", values=row)

    except Exception as e:
        print(f"Error fetching data: {e}")


        
        
