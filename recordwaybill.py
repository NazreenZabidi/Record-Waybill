import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import customtkinter as ctk
import os
from datetime import datetime
from tkcalendar import DateEntry

# Set appearance and color theme for customtkinter
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("green")

# Create main application window
root = ctk.CTk()
root.title("Waybill Record Form")

# Get screen width and height
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.geometry(f"{width}x{height}+0+0")

# Create a directory to save uploaded images
save_dir = "waybill_images"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

def save_record():
    date = entry_date.get()
    receiver_address = text_receiver_address.get("1.0", tk.END).strip()
    number_reference = entry_number_reference.get()
    code_waybill = entry_code_waybill.get()
    description = text_description.get("1.0", tk.END).strip()
    image_paths = label_image_path.cget("text").strip().split("\n")

    if not (date and receiver_address and number_reference and code_waybill and description):
        messagebox.showerror("Input Error", "Date, receiver address, number reference, code waybill, and description are required!")
        return

    # Save record to a text file
    record = f"Date: {date}\nReceiver Address: {receiver_address}\nNumber Reference: {number_reference}\nCode Waybill: {code_waybill}\nDescription: {description}\n"
    if image_paths:
        record += f"Image Paths:\n" + "\n".join(image_paths) + "\n"
    record += "\n"

    with open("waybill_records.txt", "a") as file:
        file.write(record)

    messagebox.showinfo("Success", "Record saved successfully!")
    clear_form()

def upload_image():
    # Allow selection of multiple files
    file_paths = filedialog.askopenfilenames(filetypes=[("All files", "*.*")])
    if file_paths:
        saved_paths = []
        for file_path in file_paths:
            filename = os.path.basename(file_path)
            save_path = os.path.join(save_dir, filename)
            try:
                with open(file_path, 'rb') as src_file:
                    with open(save_path, 'wb') as dest_file:
                        dest_file.write(src_file.read())
                saved_paths.append(save_path)
            except Exception as e:
                messagebox.showerror("Upload Error", f"Failed to upload file: {filename}\nError: {str(e)}")
                return  # Stop further processing if an error occurs

        # Update label with paths of all uploaded files
        label_image_path.configure(text="\n".join(saved_paths))
        messagebox.showinfo("Success", f"Files uploaded successfully!\nSaved at:\n" + "\n".join(saved_paths))
    else:
        messagebox.showinfo("Info", "No files selected.")

def clear_form():
    entry_date.set_date(datetime.today())
    text_receiver_address.delete("1.0", tk.END)
    entry_number_reference.delete(0, tk.END)
    entry_code_waybill.delete(0, tk.END)
    text_description.delete("1.0", tk.END)
    label_image_path.configure(text="")

def show_records():
    # Create a new window for displaying records
    record_window = tk.Toplevel(root)
    record_window.title("Stored Records")
    record_window.geometry("800x600")
    
    # Create a Listbox to display records
    listbox = tk.Listbox(record_window, width=100, height=30)
    listbox.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
    
    # Scrollbar for the Listbox
    scrollbar = ttk.Scrollbar(record_window, orient=tk.VERTICAL, command=listbox.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    listbox.configure(yscrollcommand=scrollbar.set)
    
    # Load records from the text file into the Listbox
    if os.path.exists("waybill_records.txt"):
        with open("waybill_records.txt", "r") as file:
            records = file.readlines()
            record = ""
            for line in records:
                record += line
                if line.strip() == "":
                    listbox.insert(tk.END, record.strip())
                    record = ""

    def delete_selected_record():
        selected_index = listbox.curselection()
        if not selected_index:
            messagebox.showerror("Selection Error", "No record selected!")
            return
        
        # Get the selected record
        selected_record = listbox.get(selected_index)
        
        # Read all records from the file
        with open("waybill_records.txt", "r") as file:
            records = file.readlines()

        # Remove the selected record from the text file
        with open("waybill_records.txt", "w") as file:
            record = ""
            for line in records:
                record += line
                if line.strip() == "":
                    if record.strip() != selected_record:
                        file.write(record)
                    record = ""

        # Remove from Listbox
        listbox.delete(selected_index)
        messagebox.showinfo("Success", "Record deleted successfully!")

    # Add a delete button
    delete_button = ctk.CTkButton(record_window, text="Delete Selected Record", command=delete_selected_record)
    delete_button.pack(pady=10)

# Create the title label
lblTitle = ctk.CTkLabel(root, text="- RECORD WAYBILL -", font=('Century Gothic', 25), text_color="lightgreen")
lblTitle.pack(pady=30, anchor=tk.CENTER)

# Create the main container frame
main_frame = ctk.CTkFrame(root, width=600, height=630, corner_radius=15, fg_color="#293E3B")
main_frame.place(relx=0.5, rely=0.52, anchor=tk.CENTER)

# Create the waybill details frame
wayb_frame = ctk.CTkFrame(main_frame, width=550, height=450)
wayb_frame.place(x=25, y=25)

# Create and place form widgets using place method
ctk.CTkLabel(wayb_frame, text="Date :").place(x=10, y=10)
entry_date = DateEntry(wayb_frame, date_pattern='yyyy-mm-dd', width=46)
entry_date.place(x=150, y=10)

ctk.CTkLabel(wayb_frame, text="Receiver Address :").place(x=10, y=50)
text_receiver_address = ctk.CTkTextbox(wayb_frame, height=100, width=300)
text_receiver_address.place(x=150, y=50)

ctk.CTkLabel(wayb_frame, text="Number Reference :").place(x=10, y=170)
entry_number_reference = ctk.CTkEntry(wayb_frame, width=300)
entry_number_reference.place(x=150, y=170)

ctk.CTkLabel(wayb_frame, text="Code Waybill :").place(x=10, y=210)
entry_code_waybill = ctk.CTkEntry(wayb_frame, width=300)
entry_code_waybill.place(x=150, y=210)

ctk.CTkLabel(wayb_frame, text="Description :").place(x=10, y=250)
text_description = ctk.CTkTextbox(wayb_frame, height=100, width=300)
text_description.place(x=150, y=250)

# Button frame
btn_frame = ctk.CTkFrame(main_frame, width=550, height=100)
btn_frame.place(x=25, y=500)

upload_button = ctk.CTkButton(btn_frame, text="Upload Files", command=upload_image)
upload_button.place(x=10, y=10)

label_image_path = ctk.CTkLabel(btn_frame, text="", wraplength=300)
label_image_path.place(x=150, y=10)

save_button = ctk.CTkButton(btn_frame, text="Save Record", command=save_record)
save_button.place(x=10, y=50)

# Show Records button
show_records_button = ctk.CTkButton(btn_frame, text="Show Records", command=show_records)
show_records_button.place(x=160, y=50)

root.mainloop()
