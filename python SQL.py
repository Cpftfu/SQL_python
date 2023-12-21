import sqlite3

# моя предмедная область по БД это регистратура в больнице, ее и сюда тоже пихнула
#bim bim  bam bam
#тут идет создание классов и определение атрибутов

class DataBase:
    conn = sqlite3.connect('hospital_database.db')
    cursor = conn.cursor()

    @classmethod
    def create_tables(cls):
        cls.cursor.execute('''
                CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY,
                password TEXT NOT NULL,
                role TEXT NOT NULL,
                full_name TEXT NOT NULL
            )
        ''')
        cls.cursor.execute('''
                CREATE TABLE IF NOT EXISTS Patients (
                id INTEGER PRIMARY KEY,
                patient_id INTEGER,
                name TEXT NOT NULL,
                surname TEXT NOT NULL,
                middlename TEXT,
                phone TEXT NOT NULL,
                email TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        cls.cursor.execute('''
                CREATE TABLE IF NOT EXISTS Doctors (
                id INTEGER PRIMARY KEY,
                doctor_id INTEGER,
                name TEXT NOT NULL,
                surname TEXT NOT NULL,
                middlename TEXT,
                specialisation TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')

        cls.cursor.execute('''
                CREATE TABLE IF NOT EXISTS Registrators (
                id INTEGER PRIMARY KEY,
                registrator_id INTEGER,
                name TEXT NOT NULL,
                surname TEXT NOT NULL,
                middlename TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        cls.conn.commit()

    @classmethod
    def add_user(cls, user):
        cls.cursor.execute('''
            INSERT INTO users (password, role, full_name)
            VALUES (?, ?, ?)
        ''', 
        (user.password, user.role, user.full_name))
        cls.conn.commit()

    @classmethod
    def add_patients(cls, patient):
        cls.cursor.execute('''
            INSERT INTO orders (patient_id, name, surname, middlename, phone, email)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', 
        (patient.user.id, patient.name, patient.surname, patient.middlename, patient.phone, patient.email))
        cls.conn.commit()

    @classmethod
    def add_doctors(cls, doctor):
        cls.cursor.execute('''
            INSERT INTO tovars (doctor_id, name, surname, middlename, specialisation)
            VALUES (?, ?, ?, ?, ?)
        ''', 
        (doctor.user.id, doctor.name, doctor.surname, doctor.middlename, doctor.specialisation))
        cls.conn.commit()

    @classmethod
    def add_registrators(cls, registrator):
        cls.cursor.execute('''
            INSERT INTO orders (registrator_id, name, surname, middlename)
            VALUES (?, ?, ?, ?)
        ''', 
        (registrator.user.id, registrator.name, registrator.surname, registrator.middlename))
        cls.conn.commit()

    @classmethod
    def fetch_user(cls, password, role, full_name):
        cls.cursor.execute('''
            SELECT * FROM Users
            WHERE password = ? AND role = ? AND full_name = ?
        ''', (password, role, full_name))
        user_data = cls.cursor.fetchone()

        if user_data:
            user_id, password, role, full_name = user_data
            return User(user_id, password, role, full_name)
        else:
            return None

class User:
    def __init__(self, user_id, password, role, full_name):
        self.id = user_id
        self.password = password
        self.role = role
        self.full_name = full_name

class Patients:
    def __init__(self, patient_id, user, name, surname, middlename, phone, email):
        self.id = patient_id
        self.user = user
        self.name = name
        self.surname = surname
        self.middlename = middlename
        self.phone = phone
        self.email = email

class Doctors:
    def __init__(self, doctor_id, user, name, surname, middlename, specialisation ):
        self.id = doctor_id
        self.user = user
        self.name = name
        self.surname = surname
        self.middlename = middlename
        self.specialisation = specialisation

class Registrators :
    def __init__(self, registrator_id, user, name, surname, middlename,):
        self.id = registrator_id
        self.user = user
        self.name = name
        self.surname = surname
        self.middlename = middlename

class Interface:
    @staticmethod
    def registration():
        password = input("Введите паролик: ")
        role = input("Выберите свою роль (Пациент/ Регистратор/ Доктор): ")
        full_name = input("Введите ваше полное имечко: ")

        user = User(None, password, role, full_name)
        DataBase.add_user(user)
        print("Ура! Вы успешно зарегестрировались. ") 

    @staticmethod
    def login():
        password = input("Введите пароль: ")
        role = input("Введите свою роль (Пациент/Регистротор/Доктор):")
        full_name = input("Введите свое полное имечко:")
        user = DataBase.fetch_user(password, role, full_name) 

        if user:
            return user
        else:
            print("Увы! Неверный паролик.")
            return None

    @classmethod
    def main(cls):
        pass

    @staticmethod
    def add_patients(cls, patient):
        cls.cursor.execute('''
            INSERT INTO orders (patient_id, name, surname, middlename, phone, email)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', 
        (patient.user.id, patient.name, patient.surname, patient.middlename, patient.phone, patient.email))
        cls.conn.commit()
        
    @staticmethod
    def view_patients():
        DataBase.cursor.execute("SELECT * FROM Patients")
        peoples = DataBase.cursor.fetchall()
        if peoples:
            print("Список: ")
            for people in peoples:
                patient_id, name, surname, middlename, phone, email = people
                print(f"ID: {patient_id}, Имечко: {name}, Фамилия: {surname}, Отчество: {middlename}, Телефон: {phone}, Почта: {email}")
        else:
            print("Не найдено.")


    @classmethod
    def change_patients(cls, patient_id, update_patients):
        cls.cursor.execute('''
                UPDATE Patients
                SET name = ?
                SET surname = ?
                SET middlename = ?
                SET phone = ?
                SET email = ?                      
                WHERE id = ?
            ''', 
            (update_patients, patient_id))
        cls.conn.commit()

    @staticmethod
    def change_patients():
        patient_id = input("Введите ID клиента, которого хотите изменить в базе данных: ")

        DataBase.cursor.execute("SELECT * FROM Patients WHERE id = ?", (patient_id,))
        patient = DataBase.cursor.fetchone()

        if patient:
            patient_id, name, surname, middlename, phone, email = patient
            print(f"Текущие данные выглядят так: \nИмя: {name}, Фамилия: {surname}, Отчество: {middlename}, Номер телефона: {phone}, Почта: {email}")

            new_name = input("Введите новое имя пациента (или Enter, чтобы оставить без изменений):")
            new_surname = input("Введите новую фамилию пациента (или Enter, чтобы оставить без изменений):")
            new_middlename = input("Введите новое отчество пациента (или Enter, чтобы оставить без изменений):")
            new_phone = input("Введите новый номер телефона пациента (или Enter, чтобы оставить без изменений):")
            new_email = input("Введите новую почту пациента (или Enter, чтобы оставить без изменений):")
            
            if new_name:
                patient = (new_name, new_surname, new_middlename, new_phone, new_email)
                DataBase.cursor.execute('''
                    UPDATE Patients
                    SET name = ?, surname = ? middlename = ?, phone = ?, email = ?
                    WHERE id = ?
                ''', patient)
                DataBase.conn.commit()

            print("Пациент успешно изменен!")
        else:
            print("Увы, такого не найдено.")

    @classmethod
    def delete_patients(patient_id):
        DataBase.cursor.execute('''
                      DELETE FROM Patients
                      WHERE id = ?
                  ''', 
                  (patient_id,))
        DataBase.conn.commit()

    @classmethod
    def delete_patients(cls):
        patient_id = input("Введите ID пациента, которого хотите удалить из базы данных: ")

        DataBase.cursor.execute("SELECT * FROM orders WHERE id = ?", (patient_id,))
        patient = DataBase.cursor.fetchone()

        if patient:
            cls.delete_patient_by_id(patient_id)
            print("Пациент успешно удален из базы данных.")
        else:
            print("Такого, увы, не найдено.")
            return


        @staticmethod
        def Doctors_interface():
            print("Добро пожаловать в роль Доктора!")
            while True:
                choice = input("1. Посмотреть пациентов\n2. Добавить новых пациентов \n3. Изменить существующих пациентов\n4. Удалить существующих пациентов\n5. Выйти из менюшки\nВыберите какое действие хотите совершить (введите цифорки): ")
                match choice:
                    case "1":
                        Interface.view_patients()
                    case "2":
                        Interface.add_patients()
                    case "3":
                        Interface.change_patients()
                    case "4":
                        Interface.add_patients()
                    case "5":
                        return
                    case _:
                        print("Что-то пошло не так!.")
                        return


    @staticmethod
    def main():
        while True:
            choice = input("1. Регистрация\n2. Авторизация\n3. Выход из программы\nВыберите действие: ")

            if choice == "1":
                Interface.registration()
            elif choice == "2":
                user = Interface.login()
                if user and user.role == "Пациент" or "пациент":
                    print("Это конечно круто, но для него не хватило сил сделать интерфейс...")
                elif user and user.role == "Доктор" or "доктор":
                    Interface.Doctors_interface()
                elif user and user.role == "Регистратор" or "регистратор":
                    print("Это конечно круто, но для него не хватило сил сделать интерфейс...")
                break
            else:
                print("Неверный ввод. Пожалуйста, выберите корректное действие.")
Interface.main()

# если быть честной то эта ЕРУНДА работает ужасно криво, косо, но сил это делать супер идеально уже просто НЕТУ
# это просто крик души