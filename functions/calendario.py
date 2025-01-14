import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import Toplevel
from tkcalendar import Calendar
from functions.rango_fecha import rango_fecha_search


def open_calendar_popup(entry_widget):
    """Open a calendar popup to select a date."""
    calendar_popup = Toplevel()
    calendar_popup.title("Seleccionar Fecha")
    calendar_popup.geometry("300x300")
    calendar_popup.resizable(width=False, height=False)

    # Add Calendar widget
    calendar = Calendar(calendar_popup, date_pattern="dd-mm-yyyy")  # Use desired format
    calendar.pack(padx=10, pady=10)

    # Function to handle date selection
    def select_date():
        selected_date = calendar.get_date()
        entry_widget.delete(0, "end")  # Clear existing value in the entry
        entry_widget.insert(0, selected_date)  # Insert selected date
        calendar_popup.destroy()  # Close the calendar popup

    # Add button to confirm date selection
    select_button = ctk.CTkButton(calendar_popup, text="Seleccionar", command=select_date)
    select_button.pack(pady=10)


def create_date_range_selector(parent_frame, searchbtn, my_tree, original_data):
    poppins12 = ("Poppins", 12, "bold")

    date_range_frame = ctk.CTkFrame(parent_frame)
    date_range_frame.pack(pady=10, padx=10, fill="x")

    start_date_entry = ctk.CTkEntry(date_range_frame, placeholder_text="Fecha Inicio", font=poppins12, width=150)
    start_date_entry.pack(padx=5, pady=5, side="left")

    start_date_button = ctk.CTkButton(
        date_range_frame, text="📅", width=50, command=lambda: open_calendar_popup(start_date_entry)
    )
    start_date_button.pack(pady=5, padx=5, side="left")

    end_date_entry = ctk.CTkEntry(date_range_frame, placeholder_text="Fecha Fin", font=poppins12, width=150)
    end_date_entry.pack(padx=5, pady=5, side="left")

    end_date_button = ctk.CTkButton(
        date_range_frame, text="📅", width=50, command=lambda: open_calendar_popup(end_date_entry)
    )
    end_date_button.pack(pady=5, padx=5, side="left")

    # Set the search button command to call the date range search function
    if searchbtn.winfo_exists():
        print("Btn exist")
        searchbtn.configure(command=lambda: rango_fecha_search(
            my_tree, original_data, 
            start_date_entry.get(), end_date_entry.get()))
    else:
        print("Btn doesn't exist")
    return start_date_entry, end_date_entry
