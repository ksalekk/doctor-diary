from services.choice_controller import ChoiceController
from services.model_manager import ModelManager
from services.user_interface import UserInterface


class App:
    """
    A class to manage the app running and dependencies.

    Attributes
    ----------
        model_manager: ModelManager
            service for patients and appointments managing (Model)
        user_interface: UserInterface
            service for user-app communication (View)
        choice_controller: ChoiceController
            service for app functions executing based on user choices (Controller)


    ! WARNING !
    The app is hard-coded for reading specified named and structured (json array) files.
    You shouldn't change data/patients.json, data/appointments.json files.
    If files were corrupted, create new 'patients.json', 'appointments.json' files
    in data directory and fill them only with '[]'.

    App architecture try to follow MVC pattern.
    """

    def __init__(self):
        self.model_manager = ModelManager("data/patients.json",
                                          "data/appointments.json")
        self.user_interface = UserInterface()
        self.choice_controller = ChoiceController(self.model_manager, self.user_interface)
        self.start_app()

    def start_app(self):
        """Start and stop app."""

        run_app = True
        while run_app:
            run_app = self.choice_controller.start()
