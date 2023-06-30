import random
import tkinter as tk
from zxcvbn import zxcvbn

def password_generate(length):
    alphabet="abcdefghijklmnoperstuwxyzv"
    alphabet_big="ABCDEFGHIJKLMNOPERSTUWXYZV"
    numeric="0123456789"
    special="!@#$%&*()<>"

    password=""
    l=0

    while(l!=length):
        n=random.randint(0,100)
        if n%4==0:
            p=random.randint(0,len(alphabet)-1)
            p1=alphabet[p];
        if n%4==1:
            p=random.randint(0,len(alphabet_big)-1)
            p1=alphabet_big[p];
        if n%4==2:
            p=random.randint(0,len(numeric)-1)
            p1=numeric[p];
        if n%4==3:
            p=random.randint(0,len(special)-1)
            p1=special[p];
        password=password+p1
        l=l+1

    return password

def custom_messagebox(title, message,color):
    global messagebox_opened

    if messagebox_opened:
        return

    messagebox_opened = True

    messagebox = tk.Toplevel(window)
    messagebox.resizable(width=False, height=False)
    messagebox.title(title)
    messagebox.configure(bg=color)

    label = tk.Label(messagebox, text=message, bg=color, fg="white")
    label.pack(padx=20, pady=10)

    ok_button = tk.Button(messagebox, text="OK", command=lambda: close_messagebox(messagebox))
    ok_button.pack(pady=10)

    messagebox.update_idletasks()
    width = messagebox.winfo_width()
    height = messagebox.winfo_height()
    x = (messagebox.winfo_screenwidth() // 2) - (width // 2)
    y = (messagebox.winfo_screenheight() // 2) - (height // 2)
    messagebox.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    messagebox.mainloop()

def close_messagebox(messagebox):
    global messagebox_opened
    messagebox_opened = False
    messagebox.destroy()

def checker(password):
    results=zxcvbn(password)
    return results

def password_generator():
    length=length_entry.get()
    if not length.isdigit():
        custom_messagebox("Invalid Input", "Please enter a right length.", "red")
        return
    password=password_generate(int(length))
    results=checker(password)
    return message_results(results)
    
def password_checker():
    password = password_entry.get()
    if len(password) <= 0:
        custom_messagebox("Invalid Input", "Please enter correct word", "red")
        return
    results=checker(password)
    return message_results(results)

def message_results(results):
    message=f"Password: {results['password']}\n"+f"Score: {results['score']}\n"+f"Warning: {results['feedback']['warning']}\n"+f"Suggestions: {results['feedback']['suggestions']}\n"+f"Offline Fast Hashing (10B/s): {results['crack_times_display']['offline_fast_hashing_1e10_per_second']}\n"+f"Offline Slow Hashing (10k/s): {results['crack_times_display']['offline_slow_hashing_1e4_per_second']}\n"+f"Online No Throttling (10/s): {results['crack_times_display']['online_no_throttling_10_per_second']}\n"+f"Online Throttling (100/h): {results['crack_times_display']['online_throttling_100_per_hour']}"
    if results["score"]==0:
        color="#8B0000"
    elif results["score"]==1:
        color="red"
    elif results["score"]==2:
        color="#FFCCCB"
    elif results["score"]==3:
        color="#90EE90"
    else:
        color="green"
    custom_messagebox("Result",message,color)

def show_frame(frame):
    frame.tkraise()

def set_look_window():
    window.title("Password GeneratorOrChecker")
    window.resizable(width=False, height=False)

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width // 2) - (400 // 2)
    y = (screen_height // 2) - (400 // 2)

    window.geometry("400x400+{}+{}".format(x, y))


window = tk.Tk()
set_look_window()

messagebox_opened = False

container = tk.Frame(window)
container.pack(expand=True, padx=20, pady=20)

menu_frame = tk.Frame(container)
generate_password_frame = tk.Frame(container)
check_password_frame = tk.Frame(container)

for frame in (menu_frame, generate_password_frame, check_password_frame):
    frame.grid(row=0, column=0, sticky="nsew")


menu_label = tk.Label(menu_frame, text="Menu",font=("Arial", 13),)
menu_label.pack()

generate_button = tk.Button(menu_frame, text="Generate new password", command=lambda: show_frame(generate_password_frame),relief=tk.RAISED, bg="grey", fg="white")
generate_button.pack()

check_button = tk.Button(menu_frame, text="Check password's strength", command=lambda: show_frame(check_password_frame),relief=tk.RAISED, bg="grey", fg="white")
check_button.pack()

exit_button = tk.Button(menu_frame, text="Exit", command=window.destroy,relief=tk.RAISED, bg="red", fg="white")
exit_button.pack()

generate_password_label = tk.Label(generate_password_frame, text="Enter length of password:")
generate_password_label.pack()

length_entry = tk.Entry(generate_password_frame)
length_entry.pack()

generate_password_button = tk.Button(generate_password_frame, text="Generate Password", command=password_generator,relief=tk.RAISED, bg="green", fg="white")
generate_password_button.pack()

back_to_menu_button1 = tk.Button(generate_password_frame, text="Back to Menu", command=lambda: show_frame(menu_frame),relief=tk.RAISED, bg="red", fg="white")
back_to_menu_button1.pack()


check_password_label = tk.Label(check_password_frame, text="Enter password:")
check_password_label.pack()

password_entry = tk.Entry(check_password_frame)
password_entry.pack()

check_password_button = tk.Button(check_password_frame, text="Check Strength", command=password_checker,relief=tk.RAISED, bg="orange", fg="white")
check_password_button.pack()

back_to_menu_button2 = tk.Button(check_password_frame, text="Back to Menu", command=lambda: show_frame(menu_frame),relief=tk.RAISED, bg="red", fg="white")
back_to_menu_button2.pack()

show_frame(menu_frame)

window.mainloop()