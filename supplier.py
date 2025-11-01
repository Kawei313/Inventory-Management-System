from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from employees import connect_database

def delete_supplier(invoice, treeview):
  index = treeview.selection()
  if not index:
    messagebox.showerror('Error', 'No row is selected')
    return
  cursor, connection = connect_database()
  if not cursor or not connection:
    return
  try:
    cursor.execute("use inventory_system")
    cursor.execute('DELETE FROM supplier_data WHERE invoice=%s', invoice)
    connection.commit()
    treeview_data(treeview)
    messagebox.showinfo('Info', 'Record is deleted')
  except Exception as e:
    messagebox.showerror('Error', f'Error due to {e}')
  finally:
    cursor.close()
    connection.close()
    
def clear(invoice_entry, name_entry, contact_entry, description_text, treeview):
  invoice_entry.delete(0, END)
  name_entry.delete(0, END)
  contact_entry.delete(0, END)
  description_text.delete(1.0, END)
  treeview.selection_remove(treeview.selection())
  
def search_supplier(search_value, treeview):
  if search_value =='':
    messagebox.showerror('Error', 'Please enter invoice no.')
  else:
    cursor, connection = connect_database()
    if not cursor or not connection:
      return
    try:
      cursor.execute("use inventory_system")
      cursor.execute('SELECT * from supplier_data WHERE invoice=%s', (search_value))
      record = cursor.fetchone()
      if not record:
        messagebox.showerror('Error', f'No record found')
        return
      treeview.delete(*treeview.get_children())
      treeview.insert('', END,values=record)
    except Exception as e:
      messagebox.showerror('Error', f'Error due to {e}')
    finally:
      cursor.close()
      connection.close()
    
def show_all(treeview, search_entry):
  treeview_data(treeview)
  search_entry.delete(0, END)

def update_supplier(invoice, name, contact, description, treeview):
  index = treeview.selection()
  if not index:
    messagebox.showerror('Error', 'No row is selected')
    return
  
  cursor, connection = connect_database()
  if not cursor or not connection:
    return
  try:
    cursor.execute("use inventory_system")
    cursor.execute('SELECT * from supplier_data WHERE invoice=%s', (invoice,))
    current_data = cursor.fetchone()
    current_data=current_data[1:]
    print(current_data)
    
    new_data = (name, contact, description)
    print(new_data)
    if current_data == new_data:
      messagebox.showinfo('Info', "No changes detected")
      return
  
    cursor.execute('UPDATE supplier_data SET name=%s, contact=%s, description=%s WHERE invoice=%s', (name, contact, description, invoice))
    connection.commit()
    messagebox.showinfo('Info', 'Data is updated')
    treeview_data(treeview)
  except Exception as e:
    messagebox.showerror('Error', f'Error due to {e}')
  finally:
    cursor.close()
    connection.close()

def select_data(event,invoice_entry, name_entry, contact_entry, description_text, treeview):
  index = treeview.selection()
  content = treeview.item(index)
  actual_content = content['values']
  # print(actual_content)
  
  invoice_entry.delete(0, END)
  name_entry.delete(0, END)
  contact_entry.delete(0, END)
  description_text.delete(1.0, END)
  
  invoice_entry.insert(0, actual_content[0])
  name_entry.insert(0, actual_content[1])
  contact_entry.insert(0, actual_content[2])
  description_text.insert(1.0, actual_content[3])
  
  
def treeview_data(treeview):
  cursor, connection = connect_database()
  if not cursor or not connection:
    return
  try:
    cursor.execute("use inventory_system")
    cursor.execute('Select * from supplier_data')
    records = cursor.fetchall()
    treeview.delete(* treeview.get_children())
    for record in records:
      treeview.insert('', END, values=record)
  except Exception as e:
      messagebox.showerror('Error', f'Error due to {e}')
  finally:
    cursor.close()
    connection.close()

def add_supplier(invoice, name, contact, description, treeview):
  if invoice=='' or name=='' or contact=='' or description=='':
    messagebox.showerror('Error', 'All feilds are required')
  else:
    try:     
      cursor, connection = connect_database()
      if not cursor or not connection:
        return
      cursor.execute('use inventory_system')
      cursor.execute('SELECT * from supplier_data WHERE invoice=%s', invoice)
      if cursor.fetchone():
        messagebox.showerror('Error', 'Id already exists')
        return
      cursor.execute('INSERT INTO supplier_data VALUE(%s, %s, %s, %s)', (invoice, name, contact, description.strip()))
      connection.commit()
      messagebox.showinfo('Info', 'Data is inserted')
      treeview_data(treeview)
    except Exception as e:
      messagebox.showerror('Error', f'Error due to {e}')
    finally:
      cursor.close()
      connection.close()
    
def supplier_form(window):
  global back_image
  supplier_frame=Frame(window, width=1070, height=567, bg="white")
  supplier_frame.place(x=200, y=100)
  
  heading_label = Label(supplier_frame, text="Manage Supplier Details", font=("Times New Roman", 16, "bold"), bg="#0f4d7d", fg="white")
  heading_label.place(x=0, y=0, relwidth=1) 
  
  
  back_image=PhotoImage(file=r"helpers/icons/back_button.png")
  back_button = Button(supplier_frame, image=back_image, cursor="hand2", bd=0,bg="white", command=lambda:supplier_frame.place_forget()) #lambda: hàm không tên
  back_button.place(x=10, y=30)
  
  left_frame = Frame(supplier_frame, bg='white')
  left_frame.place(x=10, y=100)
  
  invoice_label = Label(left_frame, text = 'Invoice No.', font=('Time New Roman', 14, 'bold'), bg="white")
  invoice_label.grid(row=0, column=0, padx=(20,40), sticky='w')
  invoice_entry = Entry(left_frame, font=('Time New Roman', 14, 'bold'), bg="lightyellow")
  invoice_entry.grid(row=0, column=1, sticky="w")
  
  name_label = Label(left_frame, text = 'Supplier Name', font=('Time New Roman', 14, 'bold'), bg="white")
  name_label.grid(row=1, column=0, padx=(20,40), pady=20, sticky='w')
  name_entry = Entry(left_frame, font=('Time New Roman', 14, 'bold'), bg="lightyellow")
  name_entry.grid(row=1, column=1, sticky="w")
  
  contact_label = Label(left_frame, text = 'Supplier Contact', font=('Time New Roman', 14, 'bold'), bg="white")
  contact_label.grid(row=2, column=0, padx=(20,40), pady=20, sticky='w')
  contact_entry = Entry(left_frame,font=('Time New Roman', 14, 'bold'), bg="lightyellow")
  contact_entry.grid(row=2, column=1, sticky="w")
  
  description_label = Label(left_frame, text = 'Description', font=('Time New Roman', 14, 'bold'), bg="white")
  description_label.grid(row=3, column=0, padx=(20,40), pady=25, sticky='nw')
  description_text=Text(left_frame, width=25, height=6, bd=2)
  description_text.grid(row=3, column=1,  sticky="w")
  
  button_frame = Frame(left_frame, bg='white')
  button_frame.grid(row=4, column=0, columnspan=2, pady=20)
  
  add_button=Button(button_frame, text="Add", font=("Times New Roman", 14), width=8, cursor="hand2", fg="white", bg="#0f4d7d", command=lambda: add_supplier(invoice_entry.get(), name_entry.get(), contact_entry.get(), description_text.get(1.0, END).strip(), treeview))
  add_button.grid(row=0, column=0, padx=20)
  
  update_button=Button(button_frame, text="Update", font=("Times New Roman", 14), width=8, cursor="hand2", fg="white", bg="#0f4d7d", command=lambda: update_supplier(invoice_entry.get(), name_entry.get(), contact_entry.get(), description_text.get(1.0, END).strip(), treeview))
  update_button.grid(row=0, column=1, padx=20)
  
  delete_button=Button(button_frame, text="Delete", font=("Times New Roman", 14), width=8, cursor="hand2", fg="white", bg="#0f4d7d", command=lambda: delete_supplier(invoice_entry.get(), treeview))
  delete_button.grid(row=0, column=2, padx=20)
  
  clear_button=Button(button_frame, text="Clear", font=("Times New Roman", 14), width=8, cursor="hand2", fg="white", bg="#0f4d7d", command=lambda:clear(invoice_entry, name_entry, contact_entry, description_text, treeview))
  clear_button.grid(row=0, column=3, padx=20)
  
  right_frame = Frame(supplier_frame, bg='white')
  right_frame.place(x=520, y=95, width=500, height=350)
  
  search_frame=Frame(right_frame)
  search_frame.pack(pady=(0,20))
  
  num_label = Label(search_frame, text = 'Invoice No.', font=('Time New Roman', 14, 'bold'), bg="white")
  num_label.grid(row=0, column=0, padx=(0,15), sticky='w')
  search_entry = Entry(search_frame, font=('Time New Roman', 14, 'bold'), bg="lightyellow", width=12)
  search_entry.grid(row=0, column=1, sticky="w")
  
  search_button=Button(search_frame, text="Search", font=("Times New Roman", 14), width=8, cursor="hand2", fg="white", bg="#0f4d7d", command=lambda :search_supplier(search_entry.get(), treeview))
  search_button.grid(row=0, column=2, padx=20)
  
  show_button=Button(search_frame, text="Show All", font=("Times New Roman", 14), width=8, cursor="hand2", fg="white", bg="#0f4d7d", command=lambda: show_all(treeview, search_entry))
  show_button.grid(row=0, column=3)
  

  treeview = ttk.Treeview(right_frame, columns=('invoice', 'name', 'contact', 'description'), show='headings')
  treeview.pack()
  treeview.heading('invoice', text='Invoice Id')
  treeview.heading('name', text='Supplier Name')
  treeview.heading('contact', text='Supplier Contact')
  treeview.heading('description', text='Description')
  
  x_scroll = ttk.Scrollbar(right_frame, orient=HORIZONTAL, command=treeview.xview)
  treeview.configure(xscrollcommand=x_scroll.set)
  x_scroll.pack(fill=X)

  #Thêm thanh cuộn dọc 
  
  treeview.bind('<Button-1>', lambda e: 'break' if treeview.identify_region(e.x, e.y) == "separator" else None)

  treeview.column('invoice', width=80)
  treeview.column('name', width=160)
  treeview.column('contact', width=100)
  treeview.column('description', width=300)
  
  treeview_data(treeview)
  treeview.bind('<ButtonRelease-1>', lambda event:select_data(event,invoice_entry, name_entry, contact_entry, description_text, treeview))