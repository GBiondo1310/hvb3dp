from .bumper import Bumper, Analyzer
from ._funcs import seconds_to_timespan
from ._consts import END_GCODE


class HVSingle:
    """Class that generates the high volume gcode for a single object"""

    def __init__(self, filename: str, printer: str, objects_number: int):
        """Initializes a new HVSingle object

        :param filename: The name of the gcode to analyze
        :type filename: str
        :param printer: Name of the printer to use (saved in "printers.json" file)
        :type printer: str
        :param objects_numer: Number of objects to print
        :type objects_number: int
        """
        self.bumper = Bumper(filename, printer)
        self.objects_number = objects_number

    @property
    def analyzer(self) -> Analyzer:
        """Exposes ``self.bumper.analyzer``

        :rtype: Analyzer"""
        return self.bumper.analyzer

    def generate_header(self) -> str:
        """Generates the custom header for the gcode"""

        new_header = [";Created with HVB3DP version: 0.2.0.dev0"]
        time = seconds_to_timespan(self.analyzer.print_time * self.objects_number)
        meters = self.analyzer.meters * self.objects_number
        grams = self.analyzer.grams * self.objects_number
        original_header_lines = self.analyzer.header.split("\n")
        for line in original_header_lines:
            new_line = line
            if new_line.startswith(";TIME:"):
                new_line = f";TIME: {time}"
            elif new_line.startswith(";Filament used:"):
                new_line = (
                    f";Filament used: {round(meters)} meters - {round(grams)} grams"
                )
            new_header.append(new_line)

        return "\n".join(new_header)

    def generate_gcode(self, output: str):
        """Generates the gcode fot the high volume print

        :param output: The name of the output file
        :type output: str"""

        with open(f"{output}.gcode", mode="w") as output_gcode:
            output_gcode.write(self.generate_header())
            for i in range(0, self.objects_number):
                output_gcode.write(f";Piece number: {i + 1}\n")
                output_gcode.write(self.analyzer.core_gcode)
                output_gcode.write(";BUMPER GCODE")
                output_gcode.write(f"\n{self.bumper.bumper_gcode()}\n")
            output_gcode.write(END_GCODE)
