import datetime
from enum import Enum


class Choice(Enum):
    """
    An Enum class to represent user choices in if/switch statements.

    Possible values:
        - EXIT: exit app
        - ADD_PATIENT: add new patient
        - ADD_APPOINTMENT: add new appointment for registered patient
        - PRINT_PATIENTS: print all registered patients
        - PRINT_DAILY_APPOINTMENTS: print all appointments for specified date [YYYY-MM-DD]
        - PRINT_PATIENT_APPOINTMENTS: print all appointments for specified patient
        - DELETE_PATIENT: delete registered patient
        - CANCEL_APPOINTMENT: cancel booked appointment
        - PRINT_ALL_APPOINTMENTS: print all booked appointments in the app
    """

    EXIT = 0
    ADD_PATIENT = 1
    ADD_APPOINTMENT = 2
    PRINT_PATIENTS = 3
    PRINT_DAILY_APPOINTMENTS = 4
    PRINT_PATIENT_APPOINTMENTS = 5
    DELETE_PATIENT = 6
    CANCEL_APPOINTMENT = 7
    PRINT_ALL_APPOINTMENTS = 8


class UserInterface:
    """
    A class to represent interface between user and controller.
    Send data from user to controller and display data on console.

    Attributes
    ----------
        welcome: str
            welcome text printed on console
        menu_choices: str
            menu text printed on console
    """

    def __init__(self):
        self.welcome = """
        |=============================================|
        |             WITAMY W APLIKACJI!             |
        |      WYBIERZ SPOŚRÓD DOSTĘPNYCH OPCJI.      |
        |=============================================| """

        self.menu_choices = """
        |=============================================|
        | 1 |   DODAJ NOWEGO PACJENTA                 |
        | 2 |   UMÓW WIZYTĘ                           |
        | 3 |   WYŚWIETL PACJENTÓW                    |
        | 4 |   WYŚWIETL WIZYTY W DNIU                |
        | 5 |   WYŚWIETL WIZYTY PACJENTA              |
        | 6 |   USUŃ PACJENTA Z LISTY                 |
        | 7 |   ANULUJ WIZYTĘ                         |
        | 8 |   WYŚWIETL WSZYSTKIE WIZYTY             |
        |---------------------------------------------|
        | 0 |   WYJDŹ                                 |
        |=============================================|"""

    def print_welcome(self):
        """Print welcome text on console."""

        print(self.welcome)

    def menu(self):
        """
        Display menu interface to get user choice and return it as an enum Choice object.

        Returns:
            user_choice (Choice): enum object which represents user choice
        """

        print(self.menu_choices)
        user_choice = input("\nWYBIERAM OPCJĘ: ")
        user_choice = int(user_choice)
        return Choice(user_choice)

    def get_patient_pesel(self):
        """
        Display interface for get patient PESEL from user.

        Returns:
            pesel (str): patient PESEL
        """

        pesel = input("\nPESEL PACJENTA: ")
        return pesel

    def get_patient_name(self):
        """
        Display interface for get patient firstname and lastname from user.

        Returns:
            name_tuple (str, str): patient firstname and lastname in tuple
        """

        firstname = input("IMIĘ PACJENTA: ")
        lastname = input("NAZWISKO PACJENTA: ")
        return firstname, lastname

    def get_date(self):
        """
        Display interface for get the appointment date from user.

        Returns:
            date (date): [YYYY-MM-DD] formatted date of the appointment
        """

        print("\nPODAJ DATĘ WIZYTY")
        year = int(input("ROK [YYYY]: "))
        month = int(input("MIESIĄC [MM]: "))
        day = int(input("DZIEŃ [DD]: "))
        date = datetime.date(year, month, day)
        return date

    def get_time(self):
        """
        Display interface for get the appointment time from user.

        Returns:
            time (time): [HH:MM:SS] formatted time of the appointment
        """

        print("\nPODAJ CZAS WIZYTY: ")
        hour = int(input("GODZINA [HH]: "))
        minute = int(input("MINUTA [MM]: "))
        time = datetime.time(hour, minute, 0)
        return time

    def get_appointment_description(self):
        """
        Display interface for get the appointment description.

        Returns:
            description (str): description of the appointment
        """

        description = input("\nOPIS WIZYTY: ")
        return description

    def print_patients(self, patients):
        """
        Print patients list received in function argument.

        Arguments:
            patients (Patient[]): list of patients printed for user
        """

        if len(patients) == 0:
            self.print_info("BRAK ZAREJESTROWAYNCH PACJENTÓW")
            return

        print("\nPACJENCI ZAREJESTROWANI W PLACÓWCE: ")
        for patient in patients:
            print(patient)

    def print_appointments(self, appointments):
        """
        Print appointments list received in function argument.

        Arguments:
            appointments (Appointment[]): list of appointments printed for user
        """

        if len(appointments) == 0:
            self.print_info("BRAK UMÓWIONYCH WIZYT")
            return

        print("\nUMÓWIONE WIZYTY: ")
        for appointment in appointments:
            print(appointment)

    def print_info(self, info: str):
        """Print extra info for user."""

        print(f"[---{info.upper()}---]")
