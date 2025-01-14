import tkinter as tk
from PIL import Image, ImageTk
import customtkinter as ctk
import traceback
from modulos.menu import menu
from modulos2.menu import menu2
from modulos.transitions import transition_to_next_ui


def resize_background(event, window, original_image, background_label):
    """Resize the background image dynamically when the window is resized."""
    try:
        # Check if the background_label exists (widget might have been destroyed)
        if not background_label.winfo_exists():
            return

        # Get the new window dimensions
        width, height = event.width, event.height

        # Get the original image dimensions
        img_width, img_height = original_image.size

        # Initialize variables for new width and height
        new_width = width
        new_height = int((img_height / img_width) * width)
        
        if new_height > height:
            new_height = height
            new_width = int((img_width / img_height) * height)

        # Resize the image only if the window is larger than the image
        if width >= img_width and height >= img_height:
            # Resize to fit the window, maintaining aspect ratio
            resized_image = original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        else:
            # Keep the image at its original size if window is smaller than the image
            resized_image = original_image

        # Convert the resized image for display in Tkinter
        background_photo = ImageTk.PhotoImage(resized_image)

        # Update the background image on the label
        background_label.configure(image=background_photo)
        background_label.image = background_photo  # Keep reference to avoid garbage collection
        print(f"Resized background to {new_width}x{new_height}")
    except Exception as e:
        print(f"Error resizing background: {e}")


def set_initial_background(window, original_image, background_label):
    """Set the initial background image once window is initialized."""
    try:
        # Get the initial window dimensions
        width = window.winfo_width()
        height = window.winfo_height()

        # Resize the image to fit the initial window size if necessary
        resized_image = original_image.resize((width, height), Image.Resampling.LANCZOS)
        background_photo = ImageTk.PhotoImage(resized_image)

        # Set the initial background image
        background_label.configure(image=background_photo)
        background_label.image = background_photo  # Keep a reference to avoid garbage collection
        print(f"Initial background set to {width}x{height}")
    except Exception as e:
        print(f"Error setting initial background: {e}")

def login(window):
    """Pantalla de inicio de sesión"""
    # Configuración de fuentes
    poppins30bold = ("Poppins", 30, "bold")
    poppins20bold = ("Poppins", 20)
    poppins16bold = ("Poppins", 16, "bold")

    try:
        # Load the original background image
        original_image = Image.open("assets/login.png")
        print("Original image loaded successfully.")

        # Create a Label for the background image and place it
        background_label = tk.Label(window)
        background_label.place(relwidth=1, relheight=1)  # Make the label fill the entire window

        # Set the initial background image with a delay after the window is loaded
        window.after(1, set_initial_background, window, original_image, background_label)

        # Bind the "<Configure>" event to dynamically resize the background when the window is resized
        window.bind("<Configure>", lambda event: resize_background(event, window, original_image, background_label))

        # Frame principal
        left_frame = ctk.CTkFrame(window, width=500)
        left_frame.pack(side="left", fill="y", padx=10, pady=10)

        # Contenido del frame
        text = ctk.CTkLabel(left_frame, text="¡Bienvenido!", font=poppins30bold)
        text.place(x=155, y=150)

        text2 = ctk.CTkLabel(left_frame, text="¿Cómo desea ingresar?", font=poppins20bold)
        text2.place(x=130, y=250)

        text3 = ctk.CTkLabel(left_frame, text="o", font=poppins20bold)
        text3.place(x=250, y=370)

        admin = ctk.CTkButton(
            left_frame,
            text="Administrador",
            command=lambda: loginadmin(left_frame, window),
            width=200,
            font=poppins16bold,
        )
        admin.place(x=150, y=320)

        usuario = ctk.CTkButton(
            left_frame,
            text="Usuario",
            command=lambda: menu2(window),
            width=200,
            font=poppins16bold,
        )
        usuario.place(x=150, y=420)

    except Exception as e:
        print(f"Error during login setup: {e}")
        traceback.print_exc()

def loginadmin(left_frame, window):
    """Pantalla de inicio de sesión del administrador"""
    # Limpiar el frame actual
    for widget in left_frame.winfo_children():
        widget.destroy()

    # Configuración de fuentes
    poppins30bold = ("Poppins", 30, "bold")
    poppins16bold = ("Poppins", 16, "bold")

    # Contenido del frame
    text = ctk.CTkLabel(left_frame, text="¡Bienvenido administrador!", font=poppins30bold)
    text.place(x=40, y=150)

    contrasena = ctk.CTkEntry(
        left_frame, placeholder_text="Ingrese Contraseña", show="*", font=poppins16bold, width=250
    )
    contrasena.place(x=125, y=300)

    inicio = ctk.CTkButton(
        left_frame,
        text="Iniciar Sesión",
        command=lambda: check(contrasena, window),
        width=200,
        font=poppins16bold,
    )
    inicio.place(x=150, y=370)

def check(entry, window):
    """Validación de contraseña"""
    contr = "1234"
    if entry.get() == contr:
        transition_to_next_ui(window, login, menu)
    else:
        print("Contraseña incorrecta")


