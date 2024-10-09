class Analyzer:
    """Object that analyzes the chosen gcode and extracts needed values"""

    info: str
    core_gcode: str
    xyz: list[float]
    meters: float
    grams: float
    print_time: float

    def __init__(self, filename: str):
        """Initializes the Analyzer and extracts values

        :param filename: The name of the gcode file to analyze
        :type filename: str
        """

        self.filename = filename
        self.get_info()
        self.extract_values()
        self.extract_print_time()
        self.extract_filament_amount()
        self.extract_core_gcode()

    def get_info(self) -> str:
        """Extracts the first 300 from the gcode file as it's usually enough
        to cover print info

        :rtype: str"""

        with open(self.filename, mode="r") as gcode_file:
            self.info = gcode_file.readlines(300)

    def extract_values(self):
        """Extracts the following from a gcode file:

        :Avg X: The average X position of the print
        :Max Y: The maximum Y position of the print
        :Max Z: The maximum Z position of the print"""

        max_z = None
        max_y = None
        min_x = None
        max_x = None
        avg_x = None

        for line in self.info:

            match line[:6]:
                case ";MINX:":
                    min_x = float(line.split(";MINX:")[1])
                case ";MAXX:":
                    max_x = float(line.split(";MAXX:")[1])
                case ";MAXY:":
                    max_y = float(line.split(";MAXY:")[1])
                case ";MAXZ:":
                    max_z = float(line.split(";MAXZ:")[1])

        avg_x = (max_x + min_x) / 2

        if not max_z:
            raise ValueError("Can't find Max Z value")
        if not max_y:
            raise ValueError("Can't find Max Y value")
        if not avg_x:
            raise ValueError("Can't find Avg X value")

        self.xyz = [avg_x, max_y, max_z]

    def extract_filament_amount(self):
        """Extracts filament amount from gcode file"""

        for line in self.info:
            if ";Filament used:" in line:
                self.meters = float(line.split(": ")[1].replace("m", ""))
                self.grams = (
                    1000 * self.meters
                ) / 330  # 1Kg of PLA is about 330 meters

    def extract_print_time(self):
        """Extracts print time from gcode file"""

        for line in self.info:
            if ";TIME:" in line:
                self.print_time = float(line.split(":")[1])

    def extract_core_gcode(self):
        """Extracts the core gcode of the object"""

        with open(self.filename, mode="r") as gcode_file:
            gcode = gcode_file.readlines()

        self.core_gcode = []

        for line in gcode:
            if line.startswith(";End of"):
                self.core_gcode = "".join(self.core_gcode)

            if not line.startswith(";"):
                self.core_gcode.append(line)
