import json
from .analyzer import Analyzer


class Bumper:
    """Class that contains object bumping logic"""

    _printer: str
    printer_x: float
    printer_y: float
    printer_z: float
    printer_nozzle_y_offset: float

    def __init__(self, filename: str, printer: str):
        """Initializes a Bumper isntance

        :param filename: The name of the gcode to analyze
        :type filename: str
        """
        self.filename = filename
        self.printer = printer

    def get_printer_data(self):
        """Retreives printer data from ``printers.json`` file"""

        with open("printers.json", mode="r") as printers_file:
            printers = json.load(printers_file)

        self.printer_x = printers.get(self._printer).get("x")
        self.printer_y = printers.get(self._printer).get("y")
        self.printer_z = printers.get(self._printer).get("z")
        self.printer_nozzle_y_offset = printers.get(self._printer).get(
            "nozzle_y_offset"
        )

    @property
    def printer(self) -> str:
        """Returns ``self._printer``
        :rtype: str"""

        return self._printer

    @printer.setter
    def printer(self, new_printer: str):
        """Setter used to retreive printers data on printer change"""
        self._printer = new_printer
        self.get_printer_data()

    @property
    def filename(self) -> str:
        """Exposes ``self.analyzer.filename

        :rtype: str"""
        return self.analyzer.filename

    @filename.setter
    def filename(self, filename: str):
        """Setting new filename also creates a new Analyzer for this instance"""
        self.analyzer = Analyzer(filename)

    @property
    def x(self) -> float:
        """Returns bumper movements x

        :rtype: float"""
        return self.analyzer.xyz[0]

    @property
    def y(self) -> float:
        """Calculates and returns bumper movement y

        :rtype: float"""
        return (
            self.analyzer.xyz[1] + self.printer_nozzle_y_offset + 2
        )  # Add nozzle offset + 2mm so head does not crush into the object

    @property
    def z(self) -> float:
        """Calculates and returns bumper movement z

        :rtype: float"""
        return (
            self.analyzer.xyz[2] + 5
        )  # Add 5mm so head does not scratch object's top surface

    def is_operable(self) -> bool:
        """Calculates wether the bumping action can be performed or not

        :rtype: bool"""

        return all([self.y < self.printer_y, self.z < self.printer_z])

    def bumper_gcode(self) -> str:
        """Returns bumper gcode
        This gcode will be executed as soon as the printer finished printing the object
        :rtype: str"""

        return f"""\nG1 X{self.x} Y{self.y} Z{self.z} F3000
G1 X{self.x} Y{self.y} Z1 F3000
G1 X{self.x} Y1 Z1 2400\n"""
