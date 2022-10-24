from tkinter import *
import sqlite3

root = Tk()
root.title('Address Book App')
root.geometry("430x700")

# Create db connection
conn = sqlite3.connect("address_book.db")

# Create cursor
c = conn.cursor()

# Create a table for DB
def createAddress_table():
    c.execute("""CREATE TABLE address(
                first_name text,
                last_name text,
                address text,
                city text,
                state text,
                zipcode integer
        )""")

# Create a submit function for the DB Table
def submit_record():
    # Create db connecion
    conn = sqlite3.connect("address_book.db")

    # Create cursor
    c = conn.cursor()

    # Insert into DB Table
    c.execute("INSERT INTO address VALUES (:f_name, :l_name, :address, :city, :state, :zipcode)",
              {
                  'f_name': f_name.get(),
                  'l_name': l_name.get(),
                  'address': address.get(),
                  'city': city.get(),
                  'state': state.get(),
                  'zipcode': zipcode.get(),
              })
    # Create a commit
    conn.commit()

    # Close a connection
    conn.close()

    # clear the text box
    f_name.delete(0, END)
    l_name.delete(0, END)
    address.delete(0, END)
    city.delete(0, END)
    state.delete(0, END)
    zipcode.delete(0, END)


# query from DB Table
def query_record():
    # Create db connecion
    conn = sqlite3.connect("address_book.db")

    # Create cursor
    c = conn.cursor()

    # query db Table
    c.execute("SELECT rowid,* FROM address")

    print_address_info = ''

    address_info = c.fetchall()
    for i in address_info:
        print_address_info += str(i) + "\n"

    screen_label = Label(root, text=print_address_info, pady=12)
    screen_label.grid(row=11, column=0, columnspan=2)

    # Create a commit
    conn.commit()

    # Close a connection
    conn.close()


# delete record from DB Table
def delete_record():
    # Create db connecion
    conn = sqlite3.connect("address_book.db")

    # Create cursor
    c = conn.cursor()

    recordId = selectBox.get()

    # Delete from DB table
    c.execute("DELETE from address WHERE rowid = " + recordId)

    selectBox.delete(0, END)

    # Create a commit
    conn.commit()

    # Close a connection
    conn.close()


# Update changes to DB Table
def edit_record():
    global editor
    editor = Tk()
    editor.title('Edit Window')
    editor.geometry("400x400")
    editor.resizable(False, False)

    # Create db connection
    conn = sqlite3.connect("address_book.db")

    # Create cursor
    c = conn.cursor()

    global f_name_editor
    global l_name_editor
    global address_editor
    global city_editor
    global state_editor
    global zipcode_editor

    # Create Text boxes
    f_name_editor = Entry(editor, width=40)
    f_name_editor.grid(row=0, column=1, padx=20, pady=12)

    l_name_editor = Entry(editor, width=40)
    l_name_editor.grid(row=1, column=1, pady=12),

    address_editor = Entry(editor, width=40)
    address_editor.grid(row=2, column=1, pady=12)

    city_editor = Entry(editor, width=40)
    city_editor.grid(row=3, column=1, pady=12)

    state_editor = Entry(editor, width=40)
    state_editor.grid(row=4, column=1, pady=12)

    zipcode_editor = Entry(editor, width=40)
    zipcode_editor.grid(row=5, column=1, pady=12)

    # Create a text box labels
    f_name_label = Label(editor, text="First Name:")
    f_name_label.grid(row=0, column=0)

    l_name_label = Label(editor, text="Last Name:")
    l_name_label.grid(row=1, column=0)

    address_label = Label(editor, text="Address:")
    address_label.grid(row=2, column=0)

    city_label = Label(editor, text="City:")
    city_label.grid(row=3, column=0)

    state_label = Label(editor, text="State:")
    state_label.grid(row=4, column=0)

    zipcode_label = Label(editor, text="Zipcode")
    zipcode_label.grid(row=5, column=0)

    # Create a save button to save edited record
    save_button = Button(editor, text="Save Record", command=update_record)
    save_button.grid(row=6, column=0, columnspan=2,
                     pady=10, padx=10, ipadx=138)

    recordId = selectBox.get()

    # Getting records from DB Table to insert into the Edit window to update the DB Table
    c.execute("SELECT * FROM address WHERE rowid = " + recordId)
    records = c.fetchall()

    for record in records:
        f_name_editor.insert(0, record[0]),
        l_name_editor.insert(0, record[1]),
        address_editor.insert(0, record[2]),
        city_editor.insert(0, record[3]),
        state_editor.insert(0, record[4]),
        zipcode_editor.insert(0, record[5])

    # Create a commit
    conn.commit()

    # Close a connection
    conn.close()

# Updating the DB Table
def update_record():
    # Create db connection
    conn = sqlite3.connect("address_book.db")

    # Create cursor
    c = conn.cursor()

    recordId = selectBox.get()

    c.execute("""UPDATE address SET
                first_name = :first,
                last_name = :last,
                address = :address,
                city    = :city,
                state   = :state,
                zipcode = :zipcode

                WHERE rowid = :rowid""",
              {
                  "first": f_name_editor.get(),
                  "last": l_name_editor.get(),
                  "address": address_editor.get(),
                  "city": city_editor.get(), 
                  "state": state_editor.get(),
                  "zipcode": zipcode_editor.get(),
                  "rowid": recordId
              })

    # Create a commit
    conn.commit()

    # Close a connection
    conn.close()

    #Close the Edit window
    editor.destroy()

# Create Text boxes
f_name = Entry(root, width=40)
f_name.grid(row=0, column=1, padx=20, pady=12)

l_name = Entry(root, width=40)
l_name.grid(row=1, column=1, pady=12),

address = Entry(root, width=40)
address.grid(row=2, column=1, pady=12)

city = Entry(root, width=40)
city.grid(row=3, column=1, pady=12)

state = Entry(root, width=40)
state.grid(row=4, column=1, pady=12)

zipcode = Entry(root, width=40)
zipcode.grid(row=5, column=1, pady=12)

selectBox = Entry(root, width=40)
selectBox.grid(row=8, column=1, pady=12)


# Create a text box labels
f_name_label = Label(root, text="First Name:")
f_name_label.grid(row=0, column=0)

l_name_label = Label(root, text="Last Name:")
l_name_label.grid(row=1, column=0)

address_label = Label(root, text="Address:")
address_label.grid(row=2, column=0)

city_label = Label(root, text="City:")
city_label.grid(row=3, column=0)

state_label = Label(root, text="State:")
state_label.grid(row=4, column=0)

zipcode_label = Label(root, text="Zipcode")
zipcode_label.grid(row=5, column=0)

selectBox_label = Label(root, text="Select ID:")
selectBox_label.grid(row=8, column=0)

# Create a submit button
submit_button = Button(
    root, text="Add Record to Database", command=submit_record)
submit_button.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

# Create a query button
query_button = Button(root, text="Show Record", command=query_record)
query_button.grid(row=7, column=0, columnspan=2, pady=10, padx=10, ipadx=130)

# Create a Delete button
delete_button = Button(root, text="Delete Record", command=delete_record)
delete_button.grid(row=9, column=0, columnspan=2, pady=10, padx=10, ipadx=130)

# Create AN Update button
update_button = Button(root, text="Edit Record", command=edit_record)
update_button.grid(row=10, column=0, columnspan=2, pady=10, padx=10, ipadx=136)

# Create a commit
conn.commit()

# Close a connection
conn.close()

root.mainloop()
