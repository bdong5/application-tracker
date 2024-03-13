import tkinter as tk
from tkinter import ttk
from database import *

class ViewApp(tk.Frame):

    def __init__(self,parent,controller):

        tk.Frame.__init__(self,parent)
        self.controller = controller

        self.jid = tk.Label(self,text="Job ID: ")
        self.jid.grid(row=0,column=0)
        
        self.jid_entry = tk.Entry(self)
        self.jid_entry.grid(row=0, column=1)

        self.jid_entry.bind('<Return>', lambda event: self.view_app())

    def view_app(self):
        
        id = self.jid_entry.get()
        rows = app.db.display_specific_db(id)

        for row in rows:
            window = tk.Toplevel(self) # Create new window
            window.geometry("300x150") # Set the geometry as per your requirements
            job_frame = tk.Frame(window) # Create a new frame
            job_frame.pack(fill="both", expand=True) # Pack the frame

            # Add the job details to the frame
            job_label = tk.Label(job_frame, text=f"Job Title: {row[0]}")
            job_label.pack()
            company_label = tk.Label(job_frame, text=f"Company: {row[1]}")
            company_label.pack()
            location_label = tk.Label(job_frame, text=f"Location: {row[2]}")
            location_label.pack()
            date_label = tk.Label(job_frame, text=f"Date: {row[3]}")
            date_label.pack()
            status_label = tk.Label(job_frame, text=f"Status: {row[4]}")
            status_label.pack()



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

        self.location_entry.bind('<Return>', lambda event: self.insert_data())
    
    def insert_data(self):

        job = self.job_title_entry.get()
        company = self.company_entry.get()
        location = self.location_entry.get()

        app.db.insert_app_db(self, job, company, location)
        self.controller.update_treeview()


        self.job_title_entry.delete(0, 'end')
        self.company_entry.delete(0,'end')
        self.location_entry.delete(0,'end')

        self.success_label = tk.Label(self.controller, text="Insertion successful.")
        self.success_label.pack()
        self.controller.after(2000, self.success_label.destroy) # Message disappears after two second delay
        self.controller.window.destroy()

class DeleteApp(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.delete_label = tk.Label(self, text="Enter Job ID to Delete: ")
        self.delete_label.grid(row=1,column=1)
        self.delete_entry = tk.Entry(self)
        self.delete_entry.grid(row=1, column=2)
        self.delete_entry.bind('<Return>', lambda event: self.delete_app()) # User can press Enter instead of a button.


    def delete_app(self):

        job_id = self.delete_entry.get()
        
        app.db.remove_app_db(job_id)

        self.controller.update_treeview()

        self.delete_entry.delete(0,'end')

        self.success_label = tk.Label(self.controller, text="Deletion successful.")
        self.success_label.pack()
        self.controller.after(2000, self.success_label.destroy) # Message disappears after two second delay

        self.controller.window.destroy()

class Main(tk.Tk):

    def __init__(self):

        tk.Tk.__init__(self)
        self.title('AppTrack')
        self.geometry("800x500")

        self.welcome_msg = tk.Label(self, text = "Welcome to AppTrack! \nHere are your active applications.")
        self.welcome_msg.pack(pady=20)

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)
        
        self.db = Database('user.db')
        self.db.setup()

        self.tree = ttk.Treeview(self.container, columns=('Title', 'Company', 'Location', 'ID'), show='headings')
        self.tree.heading('Title', text='Title')
        self.tree.heading('Company', text='Company')
        self.tree.heading('Location', text='Location')
        self.tree.heading('ID', text='Job ID')
        self.tree.pack()

        self.insert_button = tk.Button(self, text="Insert New Application", command=self.open_insert_window) # Stack on top
        self.insert_button.place(relx=0.5, rely=0.7, anchor="center")

        self.delete_button = tk.Button(self, text="Delete Existing Application", command=self.open_delete_window) # Stack on top
        self.delete_button.place(relx=0.5, rely=0.8, anchor="center")

        self.view_button = tk.Button(self, text="View Exisiting Application", command=self.open_view_window)
        self.view_button.place(relx=0.5, rely=0.9, anchor = "center")
        self.update_treeview()

    def open_insert_window(self):
        self.window = tk.Toplevel(self) # Create new window
        self.window.geometry("240x100")
        self.insert_frame = InsertApp(self.window, self)
        self.insert_frame.pack(fill="both", expand=False)
    
    def open_delete_window(self):
        self.window = tk.Toplevel(self) # Create new window
        self.window.geometry("250x30")
        self.delete_frame = DeleteApp(self.window, self)
        self.delete_frame.pack(fill="both", expand=False)
    
    def open_view_window(self):
        self.window = tk.Toplevel(self) # Create new window
        self.window.geometry("250x30")
        self.view_frame = ViewApp(self.window,self)
        self.view_frame.pack(fill="both", expand = False)

        
    def update_treeview(self):
        for i in self.tree.get_children():
            self.tree.delete(i)  # Clear the treeview
        apps = self.db.display_all_db()
        for app in apps:
            self.tree.insert('', 'end', values=(app[0],app[1], app[2], app[5]))



app = Main()
app.mainloop()
