class AnalyzerCrealityPrint:

    info: str
    core_gcode: str
    xyz: list[float]
    meters: float
    grams: float
    print_time: float
    header: str

    def __init__(self, filename: str):
        """Initializes the Analyzer and extract vaues"""
        self.filename = filename
        self.get_info()
        self.get_header()
        self.extract_values()

    def get_info(self):
        """Gets gcode info cutting out thumbnail"""
        lines = []
        is_thumbnail = False
        with open(self.filename, mode="r") as gcode_file:
            while True:
                line = gcode_file.readline()
                if "EXECUTABLE_BLOCK_START" in line:
                    break
                if "THUMBNAIL_BLOCK_START" in line:
                    is_thumbnail = True
                if "THUMBNAIL_BLOCK_END" in line:
                    is_thumbnail = False
                    continue

                if not is_thumbnail:
                    lines.append(line)
        self.info = lines

    def get_header(self):
        """Gets gcode header"""

        self.header = ""
        for line in self.info:
            if line.startswith(";"):
                self.header = self.header + line

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
                case "; MINX":
                    min_x = float(line.split("; MINX = ")[1])
                case "; MAXX":
                    max_x = float(line.split("; MAXX = ")[1])
                case "; MAXY":
                    max_y = float(line.split("; MAXY = ")[1])
                case "; MAXZ":
                    max_z = float(line.split("; MAXZ = ")[1])

        avg_x = (max_x + min_x) / 2

        if not max_z:
            raise ValueError("Can't find Max Z value")
        if not max_y:
            raise ValueError("Can't find Max Y value")
        if not avg_x:
            raise ValueError("Can't find Avg X value")

        self.xyz = [avg_x, max_y, max_z]
