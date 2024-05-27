class Patient:
    """
    A class that represents a patient.

    Attributes
    ----------
        pesel: str
            pesel of the patient
        firstname: str
            firstname of the patient
        lastname: str
            lastname of the patient
    """

    def __init__(self, pesel, firstname, lastname):
        self.pesel = pesel
        self.firstname = firstname
        self.lastname = lastname

    def __str__(self):
        return f"{self.firstname} {self.lastname},\tPESEL: {self.pesel}"


class Appointment:
    """
    A class that represents an appointment.
    Every instance is related to the specified patient with unique PESEL.

    Attributes
    ----------
        patient_pesel: str
            unique pesel of the appointed patient
        date: date
            [YYYY-MM-DD] formatted date of the appointment
        time: time
            [HH:MM:SS] formatted time of the appointment
        description: str
            short description of the appointment
    """

    def __init__(self, patient_pesel, date, time, description):
        self.patient_pesel = patient_pesel
        self.date = date
        self.time = time
        self.description = description

    def __str__(self):
        return f"[{self.date}\t{self.time.strftime('%H:%M')}] \n\t{self.description}"
