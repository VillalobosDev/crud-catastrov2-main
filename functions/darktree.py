
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk  # Si usas customtkinter

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('dark-blue')


window = ctk.CTk()
window.title("Menu")
window.geometry("1080x720")

right_frame = ctk.CTkFrame(window, fg_color="black", width=600, height=400)
right_frame.pack(pady=10, padx=10, fill="both", expand=True)

frame_tree = ctk.CTkFrame(right_frame, fg_color="#2B2B2B", width=580, height=360)  # Fondo oscuro para todo el frame
frame_tree.pack(pady=10, padx=10, expand=True, fill="both")

style = ttk.Style()
style.theme_use('default')  # Asegúrate de usar el tema predeterminado para máxima personalización
style.configure(
    "Custom.Treeview",
    background="#2B2B2B",       # Fondo del Treeview
    foreground="white",         # Texto del Treeview
    rowheight=25,               # Altura de las filas
    fieldbackground="#2B2B2B",  # Fondo de las áreas vacías
    borderwidth=0               # Sin bordes
)
style.configure(
    "Custom.Treeview.Heading",
    background="#2B2B2B",  # Fondo del encabezado
    foreground="white",     # Texto del encabezado
    font=("Poppins", 14, "bold")
)
style.map("Custom.Treeview", background=[("selected", "#505050")])  # Color al seleccionar una fila

my_tree = ttk.Treeview(frame_tree, style="Custom.Treeview", show="headings")
my_tree.pack(pady=10, padx=10, fill="both", expand=True)

horizontal_scrollbar = ttk.Scrollbar(frame_tree, orient="horizontal", command=my_tree.xview)
my_tree.configure(xscrollcommand=horizontal_scrollbar.set)
horizontal_scrollbar.pack(side="bottom", fill="x")

my_tree['columns'] = ('nombre', 'apellido', 'cedula', 'rif', 'telefono', 'correo')
for col in my_tree['columns']:
    my_tree.heading(col, text=col.capitalize(), anchor='center')
    my_tree.column(col, anchor='center', width=100)

data = [
    ('Juan', 'Pérez', '12345678', 'J-12345678', '04141234567', 'juan@example.com'),
    ('Ana', 'Gómez', '87654321', 'V-87654321', '04241234567', 'ana@example.com')
]
for row in data:
    my_tree.insert("", "end", values=row)

canvas = ctk.CTkCanvas(frame_tree, width=0, height=0, highlightthickness=0, bg="#2B2B2B")
canvas.pack()  # Posicionar el canvas

window.mainloop() 
