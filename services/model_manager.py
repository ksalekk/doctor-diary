import json

import services.model_entities as model_entities
import helper_classes.json_service as json_service


def load_patients(filename):
    """
    Load registered patients from json file and convert them into Patient objects.

    Arguments:
        filename (str): relative path for patients.json file

    Returns:
        patients (Patient[]): list of registered patients
    """

    with open(filename, "rt", encoding="utf8") as patients_file:
        json_patients = json.loads(patients_file.read())

    patients = []
    for json_patient in json_patients:
        object_patient = model_entities.Patient(**json_patient)
        patients.append(object_patient)

    return patients


def load_appointments(filename):
    """
    Load booked appointments from json file and convert them into Appointment objects.

    Arguments:
        filename (str): relative path for appointments.json file

    Returns:
        appointments (Appointment[]): list of booked appointments
    """

    with open(filename, "rt", encoding="utf8") as appointments_file:
        json_appointments = json.loads(appointments_file.read(),
                                       object_hook=json_service.json_deserializer)

    appointments = []
    for json_appointment in json_appointments:
        object_appointment = model_entities.Appointment(**json_appointment)
        appointments.append(object_appointment)

    return appointments


class ModelManager:
    """
    A class to share model data (patients, appointments) manage services.

    Attributes
    ----------
        patients_filename: str
            relative path for patients.json file
        appointments_filename: str
            relative path for appointments.json file
        patients: Patient[]
            list of registered patients
        appointments: Appointment[]
            list of booked appointments
    """

    def __init__(self, patients_filename, appointments_filename):
        """
        Loads registered patients and booked appointments from json files to object lists.

        Arguments:
            patients_filename (str): relative path for patients.json file
            appointments_filename (str): relative path for appointments.json file
        """

        self.patients_filename = patients_filename
        self.appointments_filename = appointments_filename
        self.patients = load_patients(patients_filename)
        self.appointments = load_appointments(appointments_filename)

    def write_patients(self):
        """ Save Patients list as json file"""

        with open(self.patients_filename, "wt", encoding="utf8") as patients_file:
            json.dump(self.patients, patients_file,
                      default=json_service.json_serializer, indent=4)

    def write_appointments(self):
        """ Save Appointments list as json file."""

        with open(self.appointments_filename, "wt", encoding="utf8") as appointments_file:
            json.dump(self.appointments, appointments_file,
                      default=json_service.json_serializer, indent=4)

    def add_patient(self, pesel, firstname, lastname):
        """
        Add new patient and return info about operation status.

        Arguments:
            pesel (str): patient PESEL
            firstname (str): patient firstname
            lastname (str): patient lastname

        Returns:
            status (str): info about operation status
        """

        exist = self.get_patient_by_pesel(pesel)
        if exist is not None:
            return "PACJENT O PODANYM PESEL ZOSTAŁ JUŻ ZAREJESTROWANY"

        new_patient = model_entities.Patient(pesel, firstname, lastname)
        self.patients.append(new_patient)
        return "PACJENT ZOSTAŁ DODANY"

    def add_appointment(self, patient_pesel, date, time, description):
        """
        Add new appointment and return info about operation status.

        Arguments:
            patient_pesel (str): patient PESEL
            date (date): appointment date
            time (time): appointment time
            description (str): appointment description

        Returns:
            status (str): info about operation status
        """

        exist = self.get_patient_by_pesel(patient_pesel)
        if exist is None:
            return "PACJENT O PODANYM PESEL NIE JEST ZAREJESTROWANY"

        busy = self.get_busy_appointment(date, time)
        if busy is not None:
            return "WYBRANY TERMIN JEST JUŻ ZAJĘTY"

        new_appointment = model_entities.Appointment(patient_pesel, date, time, description)
        self.appointments.append(new_appointment)
        return "WIZYTA ZOSTAŁA DODANA"

    def delete_patient(self, pesel):
        """
        Delete patient and set pesel in her/his appointments as 'patient_deleted'
        Return info about operation status.

        Arguments:
            pesel (str): patient PESEL

        Returns:
            status (str): info about operation status
        """

        exist = self.get_patient_by_pesel(pesel)
        if exist is None:
            return "PACJENT O PODANYM PESEL NIE JEST ZAREJESTROWANY"

        patient_appointments = self.get_appointments_by_pesel(pesel)
        for appointment in patient_appointments:
            appointment.patient_pesel = "patient_deleted"

        self.patients.remove(exist)
        return "PACJENT ZOSTAŁ USUNIĘTY"

    def delete_appointment(self, date, time):
        """
        Delete appointment and return info about operation status.

        Arguments:
            date (date): date of the deleted appointment
            time (time): time of the deleted appointment

        Returns:
            status (str): info about operation status
        """

        busy = self.get_busy_appointment(date, time)
        if busy is None:
            return "WYBRANY TERMIN NIE POSIADA ZAREJESTROWANEJ WIZYTY"

        self.appointments.remove(busy)
        return "WIZYTA ZOSTAŁA ANULOWANA"

    def get_patient_by_pesel(self, pesel):
        """
        Get patient by his PESEL

        Arguments:
            pesel (str): patient PESEL

        Returns:
            patient (Patient | None): patient for specified PESEL
            or None if patient with specified PESEL is not registered
        """

        for patient in self.patients:
            if patient.pesel == pesel:
                return patient
        return None

    def get_appointments_by_pesel(self, pesel):
        """
        Get appointments for patient specified by his PESEL.

        Arguments:
            pesel (str): patient PESEL

        Returns:
            patient_appointments (Appointment[] | None): list of appointments for specified patient
            or None if patient with specified PESEL is not registered
        """

        patient_appointments = []

        exist = self.get_patient_by_pesel(pesel)
        if exist is None:
            return None

        for appointment in self.appointments:
            if appointment.patient_pesel == pesel:
                patient_appointments.append(appointment)

        return patient_appointments

    def get_appointments_by_date(self, date):
        """
        Get appointments for specified date.

        Arguments:
            date (date): [YYYY-MM-DD] formatted date of the appointment

        Returns:
            day_appointments (Appointment[]): list of appointments for specified date
        """

        patient_appointments = []

        for appointment in self.appointments:
            if appointment.date == date:
                patient_appointments.append(appointment)

        return patient_appointments

    def get_busy_appointment(self, date, time):
        """
        Get appointment booked in specified date, time.

        Arguments:
            date (date): [YYYY-MM-DD] formatted date
            time (time): [HH:MM:SS] specified time

        Returns:
             appointment (Appointment): appointment which occupied specified date, time
             or None if appointment with specified date, time is not busy
        """

        day_appointments = self.get_appointments_by_date(date)
        for appointment in day_appointments:
            if appointment.time == time:
                return appointment
        return None

    def get_patients_count(self):
        """
        Get number of all registered patients.

        Returns:
             patients_count (int): number of all registered patients
        """

        return len(self.patients)

    def get_all_registered_patients(self):
        """
        Get all registered patients.

        Returns:
            patients (Patient[]): list of all registered patients
        """

        return self.patients

    def get_appointments_count(self):
        """
        Get number of all booked appointments.

        Returns:
             appointments_count (int): number of all booked appointments patients
        """

        return len(self.appointments)

    def get_all_booked_appointments(self):
        """
        Get all booked appointments.

        Returns:
            appointments (Appointment[]): list of all booked appointments
        """

        return self.appointments
