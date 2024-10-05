import random
import string
from cryptography.fernet import Fernet
from datetime import datetime

# Cargar o generar la clave de cifrado
try:
    with open('key.key', 'rb') as file:
        key = file.read()
except FileNotFoundError:
    key = Fernet.generate_key()
    with open('key.key', 'wb') as file:
        file.write(key)

cipher_suite = Fernet(key)

def password_gen(length=12):
    #Genera una contraseña aleatoria con la longitud especificada.
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def check_access():
    #Verifica si la contraseña ingresada es correcta para acceder al archivo.
    access_password = "mypassword"  # Cambia esta a tu contraseña
    entered_password = input('Enter the password to view pass.txt: ')
    return access_password == entered_password

def view_password_file():
    #Lee, descifra y muestra el contenido de pass.txt, si existe.
    try:
        with open('pass.txt', 'r') as file:
            content = file.readlines()
            if content:
                print("\nPasswords stored in pass.txt:\n")
                for line in content:
                    # Extraer la información de cada línea
                    timestamp, description, encrypted_password = line.strip().split(' - ')
                    # Descifrar la contraseña
                    decrypted_password = cipher_suite.decrypt(encrypted_password.encode()).decode()
                    print(f"{timestamp} - {description} - {decrypted_password}")
            else:
                print("\nNo passwords found in pass.txt.\n")
    except FileNotFoundError:
        print("\nThe file pass.txt does not exist yet.\n")

def save_password(description, password):
    #Guarda la nueva contraseña generada junto con la descripción y la fecha (cifrada).
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    encrypted_password = cipher_suite.encrypt(password.encode()).decode()  # Cifrar la contraseña
    with open('pass.txt', 'a') as file:
        file.write(f'{current_time} - {description} - {encrypted_password}\n')
    print('Password saved in pass.txt')

# Bloque principal
print('Welcome to the password generator')

# Verificar acceso solo para ver las contraseñas anteriores
if check_access():
    view_password_file()
else:
    print('Incorrect password')

# Bucle para solicitar una longitud válida
while True:
    try:
        long_length = int(input('Enter the length of the password (min 8): '))
        if long_length >= 8:
            break
        print('The password must be at least 8 characters long')
    except ValueError:
        print('Please enter a valid number')

# Generar la nueva contraseña
new_password = password_gen(long_length)
print(f'Your new password is: {new_password}')

# Solicitar una descripción para la contraseña
description = input('Enter a description for this password: ')

# Guardar la contraseña en el archivo (cifrada)
save_password(description, new_password)
