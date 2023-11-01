import pygsheets
import tkinter as tk
import tkinter.messagebox
import re
import datetime


class registration:
    
    def __init__(self) -> None:
        gc = pygsheets.authorize(service_account_file="creds.json") #service account creds from google
        reg = gc.open_by_key('') 	#FILE ID for registration form
        chk = gc.open_by_key('')	#FILE ID for check in list
        self.sheet = reg.sheet1
        self.check_in_sheet = chk.sheet1

    def get_row_by_phone(self, phone):
        sheet = self.sheet.get_all_values(returnas='matrix')
        for row in sheet:
            if row[4].find("+1") == 0:
                row[4] = row[4][2:]
            if re.sub("[^0-9]", "", phone) == re.sub("[^0-9]", "", row[4]):
                return row
        return None
    
    def check_in(self, row):
        self.check_in_sheet.insert_rows(self.check_in_sheet.rows, values = [row], inherit=True)

   
   
window = tk.Tk()
window.geometry("700x350")
    
reg_form = registration()

instructions = tk.Label(text="Enter phone number:")
instructions.pack()

phonebox = tk.Entry()
phonebox.pack()

user_frame = tk.Frame(window)


def search():
    phone = phonebox.get()
    if phone != re.sub("[^0-9]", "", phone):
        tkinter.messagebox.showwarning(message="Invalid phone format")
        return
    response = reg_form.get_row_by_phone(phone)
    if response == None:
        tkinter.messagebox.showwarning(message="Phone number not registered!")
        return
    tk.Label(user_frame, text=f"{response[2]} {response[3]}").pack()
    tk.Label(user_frame, text=f"Shirt Size: {response[8]}").pack()
    
    if response[17]=="":
        tk.Label(user_frame, text="HAS NOT SUBMITTED PHOTORELEASE!!").pack()
    tk.Label(user_frame, text="dietary restrictions:").pack()
    dietary_restrictions = tk.Entry(user_frame,text=response[24])
    dietary_restrictions.pack()
    
    def submit():
        response[0] = str(datetime.datetime.now())
        response[24] = dietary_restrictions.get()
        reg_form.check_in(response)
        
        tkinter.messagebox.showinfo(message=f"Successfully checked in {response[2]} {response[3]} ")
        
        for widget in user_frame.winfo_children():
            widget.destroy()
        
    submit_button = tk.Button(user_frame, text="Submit!", command=submit)
    submit_button.pack()
        

search_button = tk.Button(text="search", command=search)
search_button.pack()
user_frame.pack()

window.mainloop()

