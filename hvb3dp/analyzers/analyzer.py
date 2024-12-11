class Analyzer:
    """Class that analyzes the chosed gcode and extracts needed info"""

    info: str
    core_gcode: str
    xyz: list[float]
    meters: float
    grams: float
    print_time: float
    header: str
    slicer:str

    def __init__(self, filename: str):
        """Initializes the Analyzer and extracts needed infods

        :param filename: The name of the gcode file to analyze
        :type filename: str"""

        self.filename = filename

    def 