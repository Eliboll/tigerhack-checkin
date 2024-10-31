import pygsheets
import tkinter as tk
import tkinter.messagebox
import re
import datetime


class registration:
    
    def __init__(self) -> None:
        gc = pygsheets.authorize(service_account_file="2024-tigerhacks-checkin-0d80523f8de7.json")
        reg = gc.open('Registration Data')
        #chk = gc.open_by_key('Check In Data')
        chk = gc.open_by_url("https://docs.google.com/spreadsheets/d/1Sr45bFsxWc5oHg28v6Y0RZKP3W0zaTmNV1uvAGAUBZk/")
        self.sheet = reg.sheet1
        self.check_in_sheet = chk.sheet1

    def get_row_by_phone(self, phone):
        sheet = self.sheet.get_all_values(returnas='matrix')
        for row in sheet:
            if row[2].find("+1") == 0:
                row[2] = row[2][2:]
            if re.sub("[^0-9]", "", phone) == re.sub("[^0-9]", "", row[2]):
                return row
        return None
    
    def check_in(self, row):
        self.check_in_sheet.insert_rows(self.check_in_sheet.rows, values = [row], inherit=True)
        print(f"inserted {row[0]} {row[1]}")

   
   
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
    tk.Label(user_frame, text=f"{response[0]} {response[1]}").pack()
    tk.Label(user_frame, text=f"Shirt Size: {response[9]}").pack()
    
    # if response[17]=="":
    #     tk.Label(user_frame, text="HAS NOT SUBMITTED PHOTORELEASE!!").pack()
    tk.Label(user_frame, text="dietary restrictions:").pack()
    dietary_restrictions = tk.Entry(user_frame,text=response[11])
    dietary_restrictions.pack()
    
    def submit():
        response[23] = str(datetime.datetime.now())
        response[11] = dietary_restrictions.get()
        reg_form.check_in(response[:25])
        
        tkinter.messagebox.showinfo(message=f"Successfully checked in {response[0]} {response[1]} ")
        phonebox.delete(0, tk.END)
        phonebox.insert(0, "")
        for widget in user_frame.winfo_children():
            widget.destroy()
        
    submit_button = tk.Button(user_frame, text="Submit!", command=submit)
    submit_button.pack()
        

search_button = tk.Button(text="search", command=search)
search_button.pack()
user_frame.pack()

window.mainloop()

