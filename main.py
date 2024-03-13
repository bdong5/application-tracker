import tkinter as tk
from database import *

# Main app
class InsertApp(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        job_label = tk.Label(self, text="Job Title: ")
        job_label.grid(row=0, column=0)
        self.job_title_entry = tk.Entry(self)
        self.job_title_entry.grid(row=0, column=1)

        company_label = tk.Label(self, text="Company: ")
        company_label.grid(row=1, column=0)
        self.company_entry = tk.Entry(self)
        self.company_entry.grid(row=1, column=1)

        location_label = tk.Label(self, text="Location: ")
        location_label.grid(row=2,column=0)
        self.location_entry = tk.Entry(self)
        self.location_entry.grid(row=2,column=1)

        insert_button = tk.Button(self, text="Add Application", command=self.insert_data)
        insert_button.grid(row=3, column=1)
    
    def insert_data(self):

        job = self.job_title_entry.get()
        company = self.company_entry.get()
        location = self.location_entry.get()

        app.db.insert_app(self, job, company, location)

        self.job_title_entry.delete(0, 'end')
        self.company_entry.delete(0,'end')
        self.location_entry.delete(0,'end')


class Main(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title('AppTrack')
        self.geometry("500x500")

        self.welcome_msg = tk.Label(self, text = "Welcome to AppTrack")
        self.welcome_msg.pack(pady=20)

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)
        
        self.db = Database('user.db')
        self.db.setup()

        self.insert_button = tk.Button(self, text="Insert New Application", command=self.insert_window) # Stack on top
        self.insert_button.place(relx=0.5, rely=0.5, anchor="center")

    def insert_window(self):
        self.window = tk.Toplevel(self) # Create new window
        self.window.geometry("250x250")
        self.insert_frame = InsertApp(self.window, self)
        self.insert_frame.pack(fill="both", expand=True)


app = Main()
app.mainloop()