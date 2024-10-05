import random
import string
import tkinter as tk
from tkinter import messagebox, simpledialog
from cryptography.fernet import Fernet
from datetime import datetime

# Cargar o generar la clave de cifrado
try:
    with open('password_to_passtxt.key', 'rb') as file:
        key = file.read()
except FileNotFoundError:
    key = Fernet.generate_key()
    with open('password_to_passtxt.key', 'wb') as file:
        file.write(key)

cipher_suite = Fernet(key)

def password_gen(length=12):
    """Genera una contraseña aleatoria con la longitud especificada."""
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def check_access(root):
    """Verifica si la contraseña ingresada es correcta para acceder al archivo."""
    access_password = "mypassword"  # Cambia esta a tu contraseña
    entered_password = simpledialog.askstring("Access Password", "Enter the password to view pass.txt:", parent=root)
    return access_password == entered_password

def view_password_file(root):
    """Lee, descifra y muestra el contenido de pass.txt, si existe."""
    try:
        with open('pass.txt', 'r') as file:
            content = file.readlines()
            if content:
                result = ""
                for line in content:
                    # Extraer la información de cada línea
                    timestamp, description, encrypted_password = line.strip().split(' - ')
                    # Descifrar la contraseña
                    decrypted_password = cipher_suite.decrypt(encrypted_password.encode()).decode()
                    result += f"{timestamp} - {description} - {decrypted_password}\n"
                messagebox.showinfo("Stored Passwords", result, parent=root)
            else:
                messagebox.showinfo("Stored Passwords", "No passwords found in pass.txt.", parent=root)
    except FileNotFoundError:
        messagebox.showwarning("File Not Found", "The file pass.txt does not exist yet.", parent=root)

def save_password(description, password, root):
    """Guarda la nueva contraseña generada junto con la descripción y la fecha (cifrada)."""
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    encrypted_password = cipher_suite.encrypt(password.encode()).decode()  # Cifrar la contraseña
    with open('pass.txt', 'a') as file:
        file.write(f'{current_time} - {description} - {encrypted_password}\n')
    messagebox.showinfo("Success", "Password saved in pass.txt", parent=root)

def generate_password(root):
    """Genera una nueva contraseña y la guarda."""
    long_length = simpledialog.askinteger("Password Length", "Enter the length of the password (min 8):", minvalue=8, parent=root)
    if long_length:
        new_password = password_gen(long_length)
        description = simpledialog.askstring("Password Description", "Enter a description for this password:", parent=root)
        save_password(description, new_password, root)

def main():
    """Configura la ventana principal de la aplicación."""
    root = tk.Tk()
    root.title("Password Generator")
    
    # Establecer tamaño de la ventana
    window_width = 400
    window_height = 300
    root.geometry(f"{window_width}x{window_height}")  # Ancho x Alto en píxeles

    # Calcular la posición para centrar la ventana
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    # Establecer la posición de la ventana
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Botones
    generate_button = tk.Button(root, text="Generate Password", command=lambda: generate_password(root))
    generate_button.pack(pady=10)

    view_button = tk.Button(root, text="View Stored Passwords", command=lambda: check_access(root) and view_password_file(root))
    view_button.pack(pady=10)

    exit_button = tk.Button(root, text="Exit", command=root.quit)
    exit_button.pack(pady=10)

    root.mainloop()

# Ejecutar la aplicación
if __name__ == "__main__":
    main()
