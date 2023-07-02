from cryptography.fernet import Fernet
import json


class PasswordManager:
    def __init__(self, file_path, key):
        self.file_path = file_path
        self.key = key
        self.fernet = Fernet(key)
        self.data = {}

    def encrypt(self, data):
        json_data = json.dumps(data)
        encrypted_data = self.fernet.encrypt(json_data.encode())
        return encrypted_data

    def decrypt(self, encrypted_data):
        decrypted_data = self.fernet.decrypt(encrypted_data).decode()
        data = json.loads(decrypted_data)
        return data

    def load_data(self):
        try:
            with open(self.file_path, 'rb') as file:
                encrypted_data = file.read()
            if encrypted_data:
                decrypted_data = self.decrypt(encrypted_data)
                self.data = decrypted_data
        except FileNotFoundError:
            pass

    def save_data(self):
        encrypted_data = self.encrypt(self.data)
        with open(self.file_path, 'wb') as file:
            file.write(encrypted_data)

    def add_password(self, website, username, password):
        self.load_data()
        if website in self.data:
            print(f"Password for {website} already exists.")
        else:
            self.data[website] = {"username": username, "password": password}
            self.save_data()
            print(f"Password for {website} added successfully.")

    def get_password(self, website):
        self.load_data()
        if website in self.data:
            return self.data[website]
        else:
            return None

    def print_passwords(self):
        self.load_data()
        for website, data in self.data.items():
            print(f"Website: {website}")
            print(f"Username: {data['username']}")
            print(f"Password: {data['password']}")
            print("------------------------")


# Main program
def main():
    file_path = 'passwords.txt'  # File to store the encrypted passwords
    key = Fernet.generate_key()  # Generate a random encryption key

    password_manager = PasswordManager(file_path, key)

    print("Password Manager")
    print("------------------------")
    print("1. Add a password")
    print("2. Get a password")
    print("3. Print all passwords")
    print("------------------------")

    while True:
        choice = input("Enter your choice (1-3): ")
        if choice == '1':
            website = input("Enter website: ")
            username = input("Enter username: ")
            password = input("Enter password: ")
            password_manager.add_password(website, username, password)
        elif choice == '2':
            website = input("Enter website: ")
            password_data = password_manager.get_password(website)
            if password_data:
                print(f"Website: {website}")
                print(f"Username: {password_data['username']}")
                print(f"Password: {password_data['password']}")
            else:
                print(f"No password found for {website}")
        elif choice == '3':
            password_manager.print_passwords()
        else:
            break


if __name__ == '__main__':
    main()
