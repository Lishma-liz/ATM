import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
import pymysql
import random
import re


# Function for Login page
def open_login_page():
    def validate_pin():
        
        entered_pin=pin_entry_box.get()
        
        try:
            connection=pymysql.connect(
            host='localhost',
            user='root',
            password='1234',
            database='trust_atm_db'
            )
            cursor = connection.cursor()

            query="SELECT name FROM users WHERE pin=%s"
            cursor.execute(query,(entered_pin))
            result=cursor.fetchone()
            

            if result:
                name=result[0]
                messagebox.showinfo("Login Successful", f"Welcome, {name}!")
                login_window.destroy()
                open_dashboard(name)  # Navigate to the dashboard
            else:
                    messagebox.showerror("Login Failed", "Invalid PIN. Please try again.")

        except Exception as e:
             messagebox.showerror("Error", f"Database connection failed: {str(e)}")
        finally:
            if connection:
                connection.close()
                


    def open_dashboard(name):
            
        dashboard_window=tk.Toplevel(root)
        dashboard_window.title('login Confirmation')
        dashboard_window.geometry("500x300")
        
        dashboard_window.configure(bg='#981c4e')

        dashwelcome_label=tk.Label(dashboard_window, text=f"WELCOME {name}",font=('orbitron', 35), bg='#981c4e', fg='white')
        dashwelcome_label.pack(pady=40)
        
        tk.Label(dashboard_window, text=f"Please select the transaction:",font=('orbitron', 20), bg='#981c4e', fg='white').pack(pady=5)

        AccountInformation_button = tk.Button( dashboard_window, text="Account Information",font=("Orbitron", 18, "bold"),bg="#ffffff", fg="#981c4e", padx=20, pady=10,command=lambda:show_account_information(name))
        AccountInformation_button.pack(pady=10)

        Balace_button = tk.Button( dashboard_window, text="Balance", font=("Orbitron", 18, "bold"),bg="#ffffff", fg="#981c4e", padx=20, pady=10,command=lambda:show_check_balance(name))
        Balace_button.pack(pady=10)

        Deposit_button = tk.Button( dashboard_window, text="Deposite", font=("Orbitron", 18, "bold"),bg="#ffffff", fg="#981c4e", padx=20, pady=10,command=lambda:show_deposit(name))
        Deposit_button.pack(pady=10)

        Withdrawal_button = tk.Button( dashboard_window, text="Withdrawal", font=("Orbitron", 18, "bold"),bg="#ffffff", fg="#981c4e", padx=20, pady=10,command=lambda:show_withdraw(name))
        Withdrawal_button.pack(pady=10)

        pinchange_button = tk.Button( dashboard_window, text="Pin Change", font=("Orbitron", 18, "bold"),bg="#ffffff", fg="#981c4e", padx=20, pady=10,command=lambda:pin_check(name))
        pinchange_button.pack(pady=10)

        home_button=tk.Button(
                   dashboard_window,text='HOME',relief='raised',borderwidth=3,width=40,height=3,bg="#981c4e",fg="white",command=lambda: [dashboard_window.destroy(), home(root)])
        home_button.pack(pady=10)


        def show_account_information(name):
            try:
                connection = pymysql.connect(
                    host='localhost',
                    user='root',
                    password='1234',
                    database='trust_atm_db'
                )
                cursor = connection.cursor()
                query = "SELECT * FROM users WHERE name=%s"
                cursor.execute(query, (name,))
                result = cursor.fetchone()

                if result:
                   account_window = tk.Toplevel(root)
                   account_window.title("Account Information")
                   account_window.geometry("500x400")
                   account_window.configure(bg='#981c4e')

                   tk.Label(account_window, text="ACCOUNT INFORMATION", font=('orbitron', 28, 'bold'), bg='#981c4e', fg='white').pack(pady=50)
                   tk.Label(account_window, text=f"Name: {result[1]}", font=('orbitron', 20), bg='#981c4e', fg='white').pack(pady=5)
                   tk.Label(account_window, text=f"Account Number: {result[2]}", font=('orbitron', 20), bg='#981c4e', fg='white').pack(pady=5)
                   tk.Label(account_window, text=f"Contact: {result[3]}", font=('orbitron', 20), bg='#981c4e', fg='white').pack(pady=5)
                   tk.Label(account_window, text=f"Email: {result[4]}", font=('orbitron', 20), bg='#981c4e', fg='white').pack(pady=5)

                   back_button=tk.Button(
                   account_window,text='HOME',relief='raised',borderwidth=3,width=40,height=3,bg="#981c4e",fg="white",command=lambda: [account_window.destroy(), home(root)])
                   back_button.pack(pady=10)

                   #back_button=tk.Button(
                   #account_window,text='BACK',relief='raised',borderwidth=3,width=40,height=3,bg="#981c4e",fg="white",command=lambda: [show_account_information.destroy(), open_dashboard(root)])
                   #back_button.pack(pady=10)
                else:
                   messagebox.showerror("Error", "No account information found.")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to retrieve account information: {str(e)}")
            finally:
                if connection:
                   connection.close()

        def show_check_balance(name):
                try:
                    connection = pymysql.connect(
                        host='localhost',
                        user='root',
                        password='1234',
                        database='trust_atm_db'
                    )
                
                    cursor=connection.cursor()
                    query="SELECT balance FROM users WHERE name=%s"
                    cursor.execute( query,(name,))
                    result = cursor.fetchone()

                    if result:
                       balance_window = tk.Toplevel(root)
                       balance_window.title("Current Balance")
                       balance_window.geometry("500x400")
                       balance_window.configure(bg='#981c4e')

                       tk.Label(balance_window, text="BALANCE", font=('orbitron', 28, 'bold'), bg='#981c4e', fg='white').pack(pady=30)
                       tk.Label(balance_window, text=f"Your current balance is: {result[0]}", font=('orbitron', 20), bg='#981c4e', fg='white').pack(pady=5)
                       back_button=tk.Button(
                           balance_window,text='HOME',relief='raised',borderwidth=3,width=40,height=3,bg="#981c4e",fg="white",command=lambda: [balance_window.destroy(), home(root)])
                       back_button.pack(pady=10)

                    else:
                        messagebox.showinfo("Balance", f"zero balance")
                        
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to retrieve Balance information: {str(e)}")
                finally:
                    if connection:
                       connection.close()
                       
        def show_deposit(name):
            def process_deposit():
                            try:
                                
                                connection = pymysql.connect(
                                    host='localhost',
                                    user='root',
                                    password='1234',
                                    database='trust_atm_db'
                                )
                                cursor = connection.cursor()
                                amount = float(amount_entry.get())
                                query="UPDATE users SET balance = balance + %s WHERE name = %s"
                                cursor.execute(query,(amount,name))
                                connection.commit()

                                messagebox.showinfo("Success", f"₹{amount} deposited successfully!")
                                deposit_window.destroy()
                                
                            except Exception as e:
                                messagebox.showerror("Error", f"Deposit failed: {str(e)}")

                            finally:
                                if connection:
                                    connection.close()
            deposit_window = tk.Toplevel(dashboard_window)
            deposit_window.title("Deposit")
            deposit_window.geometry("400x200")
            deposit_window.configure(bg='#981c4e')

            tk.Label(deposit_window, text="DEPOSIT", font=('orbitron', 28, 'bold'), bg='#981c4e', fg='white').pack(pady=50)

            enddep_label=tk.Label(deposit_window, text="Enter amount to deposit:",font=("orbitron",13),bg="#981c4e",fg="white")
            enddep_label.pack(pady=10)
                    
            amount_entry = tk.Entry(deposit_window)
            amount_entry.pack(pady=5)

            deposit_button=tk.Button(deposit_window, text="DEPOSIT", command=lambda:process_deposit())
            deposit_button.pack(pady=10)

            back_button=tk.Button(
                   deposit_window,text='HOME',relief='raised',borderwidth=3,width=40,height=3,bg="#981c4e",fg="white",command=lambda: [deposit_window.destroy(), home(root)])
            back_button.pack(pady=10)


        def show_withdraw(name):
            def process_withdraw():
                try:
                                 
                    connection = pymysql.connect(
                        host='localhost',
                        user='root',
                        password='1234',
                        database='trust_atm_db'
                    )
                    
                    cursor = connection.cursor()
                    amount = float(withdraw_amount_entry.get())
                    query="SELECT balance from users WHERE name=%s"
                    cursor.execute(query,(name))
                    result = cursor.fetchone()
                    if result:
                        balance = result[0]                  
                        if amount > balance:
                            messagebox.showerror("Error", "Insufficient balance!")
                            
                        else:
                  
                            cursor.execute("UPDATE users SET balance = balance - %s WHERE name = %s", (amount, name))
                            connection.commit()
                            messagebox.showinfo("Success",f"\u20b9{amount} withdrawn successfully!")
                            withdraw_window.destroy()
                            
                    else:
                        messagebox.showerror("Error", "User not found!")
        
                except ValueError:
                    messagebox.showerror("Error", "Invalid amount entered!")
                except Exception as e:
                    messagebox.showerror("Error", str(e))
                finally:
                    connection.close()  

            withdraw_window=tk.Toplevel(dashboard_window)
            withdraw_window.title("Deposit")
            withdraw_window.geometry("400x200")
            withdraw_window.configure(bg='#981c4e')

            tk.Label(withdraw_window, text="WITHDRAW", font=('orbitron', 28, 'bold'), bg='#981c4e', fg='white').pack(pady=50)

            withdraw_label=tk.Label(withdraw_window, text="Enter amount to Withdraw:",font=("orbitron",13),bg="#981c4e",fg="white")
            withdraw_label.pack(pady=10)
                    
            withdraw_amount_entry = tk.Entry(withdraw_window)
            withdraw_amount_entry.pack(pady=5)

            withdraw_button=tk.Button(withdraw_window, text="WITHDRAW", command=lambda:process_withdraw())
            withdraw_button.pack(pady=10)

            back_button=tk.Button(
                   withdraw_window,text='HOME',relief='raised',borderwidth=3,width=40,height=3,bg="#981c4e",fg="white",command=lambda: [withdraw_window.destroy(), home(root)])
            back_button.pack(pady=10)



        def pin_check(name):
            def process_pin():
                try:
                                 
                    connection = pymysql.connect(
                        host='localhost',
                        user='root',
                        password='1234',
                        database='trust_atm_db'
                    )
                    
                    cursor = connection.cursor()
                    pin = pin_number_entry.get()
                    if not pin.isdigit() or len(pin) != 4:
                        messagebox.showerror("Error", "PIN must be exactly 4 digits!")
                        return

            
                    query = "SELECT pin FROM users WHERE name=%s"
                    cursor.execute(query, (name,))
                    result = cursor.fetchone()

                    if result is None:
                        messagebox.showerror("Error", "User not found!")
                        return

           
                    update_query = "UPDATE users SET pin = %s WHERE name = %s"
                    cursor.execute(update_query, (pin, name))
                    connection.commit()
                    messagebox.showinfo("Success", "PIN changed successfully!")
                    pin_change_window.destroy()

                except pymysql.Error as e:
                    messagebox.showerror("Database Error", f"An error occurred: {e}")
                finally:
                    if connection:
                        connection.close()

            
            pin_change_window=tk.Toplevel(dashboard_window)
            pin_change_window.title("Deposit")
            pin_change_window.geometry("400x200")
            pin_change_window.configure(bg='#981c4e')

            tk.Label(pin_change_window, text="PIN CHANGE", font=('orbitron', 28, 'bold'), bg='#981c4e', fg='white').pack(pady=50)


            pin_label=tk.Label(pin_change_window, text="Enter the pin to change",font=("orbitron",20),bg="#981c4e",fg="white")
            pin_label.pack(pady=10)
                    
            pin_number_entry = tk.Entry(pin_change_window)
            pin_number_entry.pack(pady=5)
            pin_button=tk.Button(pin_change_window, text="PIN CHANGE", command=lambda:process_pin())
            pin_button.pack(pady=10)
            back_button=tk.Button(
            pin_change_window,text='HOME',relief='raised',borderwidth=3,width=40,height=3,bg="#981c4e",fg="white",command=lambda: [account_window.destroy(), home(root)])
            back_button.pack(pady=10)
            
            
        
                    
                  
    
    login_window = tk.Toplevel(root)
    login_window.title("Login")
    login_window.geometry("500x300")
    login_window.configure(bg='#981c4e')
    
    loghead_label=tk.Label(login_window  ,text='LOGIN  FORM',font=('orbitron',25,'bold'),fg='white',bg='#981c4e')
    loghead_label.pack(pady=40)

    space_label=tk.Label(login_window,bg='#981c4e')
    space_label.pack()

    pin_label=tk.Label(login_window,text="Enter Your PIN",font=("orbitron",13),bg="#981c4e",fg="white")
    pin_label.pack(pady=10)

    my_password=tk.IntVar
    
    pin_entry_box=tk.Entry(login_window,textvariable=my_password,font=('orbitron',12),width=22)
    pin_entry_box.pack(ipady=7)
    
    enter_button=tk.Button(login_window,text='Enter',relief='raised',borderwidth=3,width=40,height=3,command=validate_pin)
    enter_button.pack(pady=10)

    back_button=tk.Button(
    login_window,text='HOME',relief='raised',borderwidth=3,width=40,height=3,command=lambda: [login_window.destroy(), home(root)])
    back_button.pack(pady=10)

        

 # Function for Registration page
def open_register_page():
        def submit_to_database():
            name=name_entry_box.get()
            account=account_entry_box.get()
            contact=contact_entry_box.get()
            email=email_entry_box.get()

            #validation
            if len(account)!=10 or not account.isdigit():
                messagebox.showerror("error",'Account number must be exactly 10 digit')
                return
            if len(contact)!=10 or not contact.isdigit():
                messagebox.showerror("error","Contact number must be exactly 10 digit")
                return
            email_regex=r'^[a-zA-Z0-9_.+-]+@[a-zA_Z0-9-]+\.[a-zA-Z0-9-.]+$'
            if not re.match(email_regex,email):
                messagebox.showerror("Error",'invalid email address format!')
                return

            pin=random.randint(1000,9999)
            try:
                connection=pymysql.connect(
                        host='localhost',
                        user='root',
                        password='1234',
                        database='trust_atm_db'

                    )
                cursor=connection.cursor()


                #insert data into table
                query="""
                INSERT INTO users(name,account_number,contact_number,email,pin)
                VALUES (%s,%s,%s,%s,%s)
                """
                cursor.execute(query,(name,account,contact,email,pin))
                connection.commit()
                
                messagebox.showinfo("success",f"Registration Successful!Your PIN is {pin}")
                display_user_data(name,account,contact,email,pin)
                #register_window.destroy()

            
            except Exception as e:
                messagebox.showerror("Error",f"error inserting data: {str(e)}")
            finally:
                if connection:
                    connection.close()
                register_window.destroy()
                
        def display_user_data(name,account,contact,email,pin):
            confirmation_window=tk.Toplevel(root)
            confirmation_window.title('Registration Confirmation')
            confirmation_window.geometry("500x300")
            confirmation_window.configure(bg='#981c4e')

            tk.Label(confirmation_window, text=f"Hai{name} Your Registration Confirmed",font=('orbitron', 12), bg='#981c4e', fg='white').pack(pady=5)
           #tk.Label(confirmation_window, text=f"Account Number:{account}",font=('orbitron', 12), bg='#981c4e', fg='white').pack(pady=5)
            #tk.Label(confirmation_window, text=f"Contact:{contact}",font=('orbitron', 12), bg='#981c4e', fg='white').pack(pady=5)
            #tk.Label(confirmation_window, text=f"Email:{email}",font=('orbitron', 12), bg='#981c4e', fg='white').pack(pady=5)
            tk.Label(confirmation_window, text=f"Your PIN :{pin}",font=('orbitron', 12), bg='#981c4e', fg='white').pack(pady=20)
            
            
            login_button = tk.Button(confirmation_window, text="Login", font=("Orbitron", 18, "bold"),bg="#981c4e", fg="#ffffff", padx=20, pady=10, command=open_login_page)
            login_button.pack(pady=10)  

            back_button = tk.Button(confirmation_window, text="Back to Home", relief='raised', borderwidth=3, width=40, height=3, command=lambda: [confirmation_window.destroy(), home(root)])
            back_button.pack(pady=10)
        
                
        register_window = tk.Toplevel(root)
        register_window.title("Register")
        register_window.geometry("500x300")
        register_window.configure(bg='#981c4e')

        Reghead_label=tk.Label(register_window ,text='REGISTER FORM',font=('orbitron',25,'bold'),fg='white',bg='#981c4e')
        Reghead_label.pack(pady=40)

        space_label=tk.Label(register_window ,bg='#981c4e')
        space_label.pack()

        name_label=tk.Label(register_window ,text="Enter Your Name",font=("orbitron",13),bg="#981c4e",fg="white")
        name_label.pack(pady=10)

        name_entry_box=tk.Entry(register_window,font=('orbitron',12),width=22)
        name_entry_box.pack(ipady=7)
        
        account_label=tk.Label(register_window ,text="Enter Account Number",font=("orbitron",13),bg="#981c4e",fg="white")
        account_label.pack(pady=10)

        account_entry_box=tk.Entry(register_window,font=('orbitron',12),width=22)
        account_entry_box.pack(ipady=7)

        contact_label=tk.Label(register_window ,text="Enter Contact Number",font=("orbitron",13),bg="#981c4e",fg="white")
        contact_label.pack(pady=10)

        contact_entry_box=tk.Entry(register_window,font=('orbitron',12),width=22)
        contact_entry_box.pack(ipady=7)
        

        email_label=tk.Label(register_window ,text="Enter Email Address",font=("orbitron",13),bg="#981c4e",fg="white")
        email_label.pack(pady=10)

        email_entry_box=tk.Entry(register_window,font=('orbitron',12),width=22)
        email_entry_box.pack(ipady=7)


        Submit_button=tk.Button(register_window,text='SUBMITTED',relief='raised',borderwidth=3,width=40,height=3,bg="#981c4e",fg="white",command=lambda: submit_to_database())
        Submit_button.pack(pady=10)

        back_button=tk.Button(
        register_window,text='HOME',relief='raised',borderwidth=3,width=40,height=3,bg="#981c4e",fg="white",command=lambda: [register_window.destroy(), home(root)])
        back_button.pack(pady=10)

   
  
def home(root):
    # Clear previous widgets, if any
    for widget in root.winfo_children():
        widget.destroy()

    # Header
    tk.Label(
        root, text="TrustATM", font=("Helvetica", 36, "bold"),
        bg="#981c4e", fg="#ffffff", pady=50
    ).pack(fill=tk.X)

    # Sub-header
    tk.Label(
        root, text="Welcome to TrustATM", font=("orbitron", 50, "bold"),
        bg="#ffffff", fg="#981c4e", pady=60
    ).pack(fill=tk.X)

    # Sub-text
    sub_text = tk.Text(
        root, font=("orbitron", 20), bg="#ffffff", fg="#981c4e",
        wrap="word", height=5, borderwidth=0
    )
    sub_text.insert("3.0", "Get started by choosing an option below:\n\n")
    sub_text.insert("end", "Login", "bold")
    sub_text.insert("end", " if you already have an account or ")
    sub_text.insert("end", "Register", "bold")
    sub_text.insert("end", " to join our community today!")
    sub_text.tag_config("bold", font=("orbitron", 20, "bold"), foreground="#981c4e")
    sub_text.config(state="disabled")
    sub_text.pack(fill=tk.X)

    # Buttons
    button_frame = tk.Frame(root, bg="#ffffff")
    button_frame.pack(pady=10)

    login_button = tk.Button(
        button_frame, text="Login", font=("Orbitron", 18, "bold"),
        bg="#981c4e", fg="#ffffff", padx=20, pady=10, command=open_login_page
    )
    login_button.grid(row=0, column=0, padx=20)

    register_button = tk.Button(
        button_frame, text="Register", font=("Orbitron", 18, "bold"),
        bg="#981c4e", fg="#ffffff", padx=20, pady=10, command=open_register_page
    )
    register_button.grid(row=0, column=1, padx=20)

    # Logo
    try:
        logo_image = Image.open("E:/Python Projects/Python/Logo1.png").resize((150, 140), Image.Resampling.LANCZOS)
        logo_photo = ImageTk.PhotoImage(logo_image)
        logo_label = tk.Label(root, image=logo_photo)
        logo_label.image = logo_photo  # Keep a reference to avoid garbage collection
        logo_label.place(x=10, y=10)
    except FileNotFoundError:
        tk.Label(root, text="Logo not found!", font=("Arial", 16), fg="red").pack(pady=20)

# Main execution
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    root.title("TrustATM")
    home(root)  # Call the home function to render the GUI
    root.mainloop()
