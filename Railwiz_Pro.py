import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
from datetime import date
from PIL import Image, ImageTk

# Connect to MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mymql71045",
    database="railway_management"
)
cursor = db.cursor()


def view_tickets():
    cursor.execute("SELECT t.ticket_id, p.name, t.train_id, t.booking_date, t.seat_number FROM tickets t JOIN passengers p ON t.passenger_id = p.passenger_id")
    records = cursor.fetchall()

    ttk.Label(view_tickets_frame, text="Ticket ID").grid(row=0, column=0)
    ttk.Label(view_tickets_frame, text="Passenger Name").grid(row=0, column=1)
    ttk.Label(view_tickets_frame, text="Train ID").grid(row=0, column=2)
    ttk.Label(view_tickets_frame, text="Booking Date").grid(row=0, column=3)
    ttk.Label(view_tickets_frame, text="Seat Number").grid(row=0, column=4)

    for i, row in enumerate(records):
        for j, val in enumerate(row):
            ttk.Label(view_tickets_frame, text=val).grid(row=i+1, column=j)

def clear_entry(entry_field):
    entry_field.delete(0, tk.END)

def update_frame(frame_number):
    """Update the background image with the next frame of the GIF."""
    # Update the label with the next frame of the GIF
    frame_image = frames[frame_number]
    background_label.config(image=frame_image)

    # Schedule the next frame update
    next_frame = (frame_number + 1) % len(frames)  # Loop through frames
    root.after(4000, update_frame, next_frame)  # Update every 4s





def book_ticket():
    """Books the ticket and updates the data in the database"""
    name = name_entry.get()
    age = age_entry.get()
    gender = gender_var.get()
    phone = phone_entry.get()
    train_id = train_id_entry.get()
    clear_entry(name_entry)
    clear_entry(age_entry)
    clear_entry(phone_entry)
    clear_entry(train_id_entry)
    
    if name and age and gender and phone and train_id:
        cursor.execute(f"SELECT available_seats FROM trains WHERE train_id={train_id}")
        result = cursor.fetchone()
        if result and result[0] > 0:
            available_seats = result[0]
            seat_number = available_seats
            cursor.execute(f"INSERT INTO passengers (name, age, gender, phone) VALUES ('{name}', {age}, '{gender}', '{phone}')")
            passenger_id = cursor.lastrowid
            cursor.execute(f"INSERT INTO tickets (passenger_id, train_id, booking_date, seat_number) VALUES ({passenger_id}, {train_id}, '{date.today()}', {seat_number})")
            cursor.execute(f"UPDATE trains SET available_seats = available_seats - 1 WHERE train_id = {train_id}")
            db.commit()
            messagebox.showinfo("Success", f"Ticket booked successfully! Seat Number: {seat_number}")
        else:
            messagebox.showerror("Error", "No seats available or invalid train ID")
    else:
        messagebox.showerror("Error", "All fields are required") 
    
def cancel_ticket():
    """Cancels a ticket and updates the data in database"""
    ticket_id = cancel_ticket_entry.get()
    clear_entry(cancel_ticket_entry)

    if ticket_id:
        cursor.execute(f"SELECT train_id, seat_number FROM tickets WHERE ticket_id = {ticket_id}")
        result = cursor.fetchone()
        
        if result:
            train_id, seat_number = result
            cursor.execute(f"DELETE FROM tickets WHERE ticket_id = {ticket_id}")
            cursor.execute(f"UPDATE trains SET available_seats = available_seats + 1 WHERE train_id = {train_id}")
            db.commit()
            messagebox.showinfo("Success", "Ticket cancelled successfully")
        else:
            messagebox.showerror("Error", "Invalid ticket ID")
    else:
        messagebox.showerror("Error", "Please enter a ticket ID")

# Create the main application window
root = tk.Tk()
root.title("RailWiz Pro: Smart Railway Ticketing System")
width= root.winfo_screenwidth() 
height= root.winfo_screenheight()
root.geometry("%dx%d" % (width, height))
root.configure(bg='#2c3e50')

image = Image.open("t13.jpg")
background_image = ImageTk.PhotoImage(image)

# Set style for ttk widgets
style = ttk.Style()
style.configure('TFrame', background='#34495e')
style.configure('TLabel', background='#34495e', foreground='white', font=('Arial', 20))
style.configure('TEntry', background='white', foreground='black', font=('Arial', 30))
style.configure('TButton', background='black', foreground='green', font=('Arial', 20), padding=10, margin=5)

# Function to change the content based on button clicks
def show_frame(frame):
    frame.tkraise()

# Create a Header Frame
header_frame = ttk.Frame(root, height=800, relief="raised", padding=8)
header_frame.pack(side='top', fill='x')

# Create a label with the background image inside the frame
background_label = tk.Label(header_frame, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Add header label
header_label = ttk.Label(header_frame, text="RailWiz Pro", font=("Helvetica", 50, 'bold'))
header_label.pack(pady=25)
header_label = ttk.Label(header_frame, text="Smart Railway Ticketing System", font=("Helvetica", 50, 'bold'))
header_label.pack(pady=25)

# Create a Sidebar Frame
sidebar_frame = ttk.Frame(root, width=200, relief="sunken", padding=10)
sidebar_frame.pack(side='left', fill='y')

# Create a Main Content Frame (to hold different content screens)
main_content_frame = ttk.Frame(root, padding=20)
main_content_frame.pack(side='right', fill='both', expand=True)  # Fill and expand to fill remaining space

# Create different frames (screens) inside the main content area
view_trains_frame = ttk.Frame(main_content_frame)
book_ticket_frame = ttk.Frame(main_content_frame)
view_tickets_frame = ttk.Frame(main_content_frame)
cancel_ticket_frame = ttk.Frame(main_content_frame)
welcome_frame = ttk.Frame(main_content_frame)

# Arrange the frames in the same grid, so we can switch between them
for frame in (welcome_frame, view_trains_frame, book_ticket_frame, view_tickets_frame, cancel_ticket_frame):
    frame.grid(row=0, column=0, sticky="nsew")
    # frame.config()
    frame.config(width = 1100, height = 400)

# Add content to each frame (you can customize this)
# Welcome Frame
frames = [tk.PhotoImage(file="RAILWIZ PRO.gif", format=f"gif -index {i}") for i in range(2)]  

# Create a label with the first frame of the GIF inside the frame
background_label = tk.Label(welcome_frame, image=frames[0], width=800, height=800)
background_label.place(x=0, y=0, relwidth=1, relheight=1)  # Stretch to full frame size

# Start the animation
root.after(0, update_frame, 0)

# Book Ticket Frame
ttk.Label(book_ticket_frame, text="Book Ticket").grid(row=0, column=1)


ttk.Label(book_ticket_frame, text="Name:").grid(row=1, column=0)
name_entry = ttk.Entry(book_ticket_frame)
name_entry.grid(row=1, column=1)

ttk.Label(book_ticket_frame, text="Age:").grid(row=2, column=0)
age_entry = ttk.Entry(book_ticket_frame)
age_entry.grid(row=2, column=1)

ttk.Label(book_ticket_frame, text="Gender:").grid(row=3, column=0)
gender_var = tk.StringVar()
ttk.Radiobutton(book_ticket_frame, text="Male", variable=gender_var, value="Male").grid(row=3, column=1)
ttk.Radiobutton(book_ticket_frame, text="Female", variable=gender_var, value="Female").grid(row=3, column=2)

ttk.Label(book_ticket_frame, text="Phone:").grid(row=4, column=0)
phone_entry = ttk.Entry(book_ticket_frame)
phone_entry.grid(row=4, column=1)

ttk.Label(book_ticket_frame, text="Train ID:").grid(row=5, column=0)
train_id_entry = ttk.Entry(book_ticket_frame)
train_id_entry.grid(row=5, column=1)

ttk.Button(book_ticket_frame, text="Book Ticket", command=book_ticket).grid(row=6, column=1)

# View Tickets Frame

ttk.Button(view_tickets_frame, text="Refresh", command=view_tickets).grid(row=50, column=50)
# Cancel Ticket Frame
ttk.Label(cancel_ticket_frame, text="Ticket Cancellation").pack(padx = 10)

ttk.Label(cancel_ticket_frame, text="Ticket ID:").pack(padx = 10)
cancel_ticket_entry = tk.Entry(cancel_ticket_frame)
cancel_ticket_entry.pack(padx = 10)

ttk.Button(cancel_ticket_frame, text="Cancel", command=cancel_ticket).pack(padx= 10)

cursor.execute("SELECT train_id, train_name, source, destination, available_seats from trains")
records = cursor.fetchall()

ttk.Label(view_trains_frame, text="Train ID").grid(row=0, column=0)
ttk.Label(view_trains_frame, text="Train Name").grid(row=0, column=1)
ttk.Label(view_trains_frame, text="Source").grid(row=0, column=2)
ttk.Label(view_trains_frame, text="Destination").grid(row=0, column=3)
ttk.Label(view_trains_frame, text="Available Seats").grid(row=0, column=4)

for i, row in enumerate(records):
    for j, val in enumerate(row):
        ttk.Label(view_trains_frame, text=val).grid(row=i+1, column=j)

# Add buttons to the sidebar for navigation
nav_buttons = [
    ("Home", welcome_frame),
    ("View Trains", view_trains_frame),
    ("Book Ticket", book_ticket_frame),
    ("View Tickets", view_tickets_frame),
    ("Cancel Ticket", cancel_ticket_frame)
]

# Create sidebar buttons and associate them with frames to switch content
for btn_text, target_frame in nav_buttons:
    btn = ttk.Button(sidebar_frame, text=btn_text, command=lambda f=target_frame: show_frame(f))
    btn.pack(fill='x', pady=5)
ttk.Button(sidebar_frame,text="Exit", command = quit).pack(fill='x', pady=5)
# Show the welcome frame initially
show_frame(welcome_frame)

# Start the application
root.mainloop()

# Close the database connection when done
db.close()