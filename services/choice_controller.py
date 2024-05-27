from services.model_manager import ModelManager
from services.user_interface import UserInterface, Choice


class ChoiceController:
    """
    A class to represent mediator between user and model.
    Use UserInterface and ModelManager dependencies to manage data flowing.
    """

    def __init__(self, model_manager, user_interface):
        """
        Injection dependencies to controller and invoke printing welcome text for user.

        Arguments:
            model_manager (ModelManager): model managing dependency
            user_interface (UserInterface): user interface dependency
        """

        self.model_manager: ModelManager = model_manager
        self.user_interface: UserInterface = user_interface
        self.user_interface.print_welcome()

    def start(self):
        """
        Core of the app. Display menu interface, get user input data,
        invoke data processing functions and stop/keep app running.

        Returns:
            run (Bool): False if user wants to exit app, True otherwise
        """

        try:
            choice = self.user_interface.menu()
        except ValueError:
            self.user_interface.print_info("PODANA OPCJA NIE ISTNIEJE")
            return True

        if choice == Choice.EXIT:
            return False

        elif choice == Choice.ADD_PATIENT:
            self.add_patient()
            return True

        elif choice == Choice.ADD_APPOINTMENT:
            self.add_appointment()
            return True

        elif choice == Choice.PRINT_PATIENTS:
            self.print_all_patients()
            return True

        elif choice == Choice.PRINT_DAILY_APPOINTMENTS:
            self.print_day_appointments()
            return True

        elif choice == Choice.PRINT_PATIENT_APPOINTMENTS:
            self.print_patient_appointments()
            return True

        elif choice == Choice.DELETE_PATIENT:
            self.delete_patient()
            return True

        elif choice == Choice.CANCEL_APPOINTMENT:
            self.delete_appointment()
            return True

        elif choice == Choice.PRINT_ALL_APPOINTMENTS:
            self.print_all_appointments()
            return True

    def add_patient(self):
        """
        Display interface for user, get user input data, validate them,
        add new patient, write patients.json file and print operation status for user.
        """

        # ! WARNING !
        # Input data validation was commented (easier for testing).
        try:
            pesel = self.user_interface.get_patient_pesel()
            # Validator.pesel_validation(pesel)
            firstname, lastname = self.user_interface.get_patient_name()
            # Validator.name_validation(firstname)
            # Validator.name_validation(lastname)
        except ValueError:
            self.user_interface.print_info("NIEPRAWIDŁOWY FORMAT DANYCH")
            return

        status = self.model_manager.add_patient(pesel, firstname, lastname)
        self.model_manager.write_patients()
        self.user_interface.print_info(status)

    def add_appointment(self):
        """
        Display interface for user, get user input data, add new appointment,
        write appointments.json file and print operation status for user.
        """

        if self.model_manager.get_patients_count() == 0:
            self.user_interface.print_info("BRAK ZAREJESTROWANYCH PACJENTÓW")
            return

        pesel = self.user_interface.get_patient_pesel()
        if self.model_manager.get_patient_by_pesel(pesel) is None:
            self.user_interface.print_info("PACJENT O PODANYM PESEL NIE JEST ZAREJESTROWANY")
            return

        try:
            date = self.user_interface.get_date()
            time = self.user_interface.get_time()
            description = self.user_interface.get_appointment_description()
        except ValueError:
            self.user_interface.print_info("NIEPRAWIDŁOWY FORMAT DANYCH")
            return

        status = self.model_manager.add_appointment(pesel, date, time, description)
        self.model_manager.write_appointments()
        self.user_interface.print_info(status)

    def print_all_patients(self):
        """ Print all registered patients. """

        patients = self.model_manager.get_all_registered_patients()
        self.user_interface.print_patients(patients)

    def print_day_appointments(self):
        """ Display user interface, get input data and print appointments for specified date. """

        if self.model_manager.get_appointments_count() == 0:
            self.user_interface.print_info("BRAK UMÓWIONYCH WIZYT")
            return

        try:
            date = self.user_interface.get_date()
            appointments = self.model_manager.get_appointments_by_date(date)
            self.user_interface.print_appointments(appointments)
        except ValueError:
            self.user_interface.print_info("NIEPRAWIDŁOWY FORMAT DANYCH")
            return


    def print_patient_appointments(self):
        """ Display user interface, get input data and print appointments for specified patient """

        # ! WARNING !
        # Input data validation was commented (easier for testing):

        if self.model_manager.get_patients_count() == 0:
            self.user_interface.print_info("BRAK ZAREJESTROWANYCH PACJENTÓW")
            return

        pesel = self.user_interface.get_patient_pesel()
        # Validator.pesel_validation(pesel)
        appointments = self.model_manager.get_appointments_by_pesel(pesel)
        if appointments is None:
            self.user_interface.print_info("PACJENT O PODANYM PESEL NIE JEST ZAREJESTROWANY")
            return

        self.user_interface.print_appointments(appointments)

    def delete_patient(self):
        """
        Display interface for user, get user input data, validate them,
        delete specified patient and print operation status for user.
        """

        if self.model_manager.get_patients_count() == 0:
            self.user_interface.print_info("BRAK ZAREJESTROWANYCH PACJENTÓW")
            return

        patients = self.model_manager.get_all_registered_patients()
        self.user_interface.print_patients(patients)

        pesel = self.user_interface.get_patient_pesel()
        # Validator.pesel_validation(pesel)
        status = self.model_manager.delete_patient(pesel)
        self.user_interface.print_info(status)
        self.model_manager.write_patients()
        self.model_manager.write_appointments()

    def delete_appointment(self):
        """
        Display interface for user, get user input data, delete specified appointment,
        write appointments.json file and print operation status for user.
        """

        if self.model_manager.get_appointments_count() == 0:
            self.user_interface.print_info("BRAK UMÓWIONYCH WIZYT")
            return

        try:
            date = self.user_interface.get_date()
            time = self.user_interface.get_time()
        except ValueError:
            self.user_interface.print_info("NIEPRAWIDŁOWY FORMAT DANYCH")
            return

        status = self.model_manager.delete_appointment(date, time)
        self.model_manager.write_appointments()
        self.user_interface.print_info(status)

    def print_all_appointments(self):
        """ Print all booked appointments """
        appointments = self.model_manager.get_all_booked_appointments()
        self.user_interface.print_appointments(appointments)


class Validator:
    """ A class that share patient data validator services """

    @classmethod
    def name_validation(cls, name: str):
        """ Raise ValueError exception if name contains not only alphabetic chars

        Arguments:
            name (str): validated firstname or lastname
        """

        if name.isalpha():
            return
        raise ValueError("Invalid name")

    @classmethod
    def pesel_validation(cls, pesel: str):
        """ Raise ValueError exception if pesel contains not only numeric chars
        or length is not equal PESEL length (11)

        Arguments:
            pesel (str): validated PESEL number
        """

        if pesel.isdigit() and len(pesel) == 11:
            return
        raise ValueError("Invalid PESEL")
