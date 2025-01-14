import time
import customtkinter as ctk

def transition_to_next_ui(window, current_ui, next_ui_func, duration=1000, **kwargs):
    """
    Handles the transition between UIs while ensuring the next UI is fully loaded in the background.
    Tracks the time taken for each part to understand where the delay or flicker might be coming from.
    """
    start_time = time.time()  # Record start time of the transition
    
    # Step 1: Create transition frame
    transition_frame = ctk.CTkFrame(window, fg_color="gray")
    transition_frame.place(relwidth=1, relheight=1)

    loading_label = ctk.CTkLabel(transition_frame, text="Loading...", font=("Poppins", 30))
    loading_label.place(relx=0.5, rely=0.5, anchor="center")

    print(f"Transition started at: {start_time}")  # Debug

    # Step 2: Function to load the next UI after a slight delay
    def load_next_ui():
        print("Start loading next UI...")
        ui_start_time = time.time()  # Measure UI load time
        
        # Step 3: Clear the previous UI (if any)
        if current_ui:
            current_ui.destroy()

        # Load the next UI (you can pass any required arguments)
        next_ui_func(window, **kwargs)

        ui_end_time = time.time()  # Measure UI load completion time
        print(f"UI loaded in: {ui_end_time - ui_start_time:.3f} seconds.")  # Debug
        
        # Destroy the transition screen once the new UI is fully loaded
        transition_frame.destroy()

    # Step 3: Preload the next UI in the background after the transition starts (ensure background loading)
    window.after(100, load_next_ui)  # Preload the UI

    # Step 4: Ensure the transition lasts for the specified duration
    window.after(duration, lambda: transition_frame.destroy())  # Remove transition screen after duration
    print(f"Transition ends at: {time.time() - start_time:.3f} seconds.")  # Debug
