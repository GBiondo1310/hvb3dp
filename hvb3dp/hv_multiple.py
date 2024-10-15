from datetime import datetime
from .bumper import Bumper, Analyzer
from ._funcs import seconds_to_timespan
from ._consts import END_GCODE


class HVMultiple:
    """Class that generates the high volume gcode for multiple objects"""

    bumpers: list[list[Bumper, int, str]] = []
    hvb_gcode: str = ""

    def __init__(self, objects: list[dict], printer: str):
        """Initializes a new HVMultiple object

        :param objects: A list of objects infos
            >>> [
            >>>     {%object_name%:{
            >>>         "path": %file_path%,
            >>>         "number": %object_number%,
            >>>     }},
            >>>    {%object_name_2%:{
            >>>         "path": %file_path_2%,
            >>>         "number": %object2_number%
            >>>     }}
            >>> ]
        :type objects: list[dict]
        :param printer: The selected printer
        :type printer: str"""

        self.bumpers = []
        for obj in objects:
            name = list(obj.keys())[0]
            path = obj.get(name).get("path")
            number = obj.get(name).get("number")

            self.bumpers.append([Bumper(path, printer), number, name])

    def generate_header(self) -> str:
        """Generates custom header for the gcode

        :rtype: str"""
        new_header = [
            ";# ============== HVB3DP ============== #"
            ";Created with HVB3DP version: 0.4.0.dev0",
            f";Date: {datetime.now().strftime('%d/%m/%Y')}",
            ";Print list:",
        ]
        total_meters = 0
        total_grams = 0
        total_time = 0

        for obj in self.bumpers:
            time = obj[0].analyzer.print_time * obj[1]
            meters = obj[0].analyzer.meters * obj[1]
            grams = obj[0].analyzer.grams * obj[1]
            new_header.append(f";\t- {obj[2]} x {obj[1]} Pcs:")
            new_header.append(f";\t\t- Print time: {seconds_to_timespan(time)}")
            new_header.append(f";\t\t- Filament meters: {round(meters)} meters")
            new_header.append(f";\t\t- Filament grams: {round(grams)} grams\n")
            total_meters += meters
            total_time += time
            total_grams += grams

        new_header.append(";# ============== HVB3DP ============== #")

        original_header_lines = self.bumpers[0][0].analyzer.header.split("\n")

        for line in original_header_lines:
            if line.startswith(";TIME:"):
                line = f";TIME: {total_time}"
                new_header.append(line)

            elif line.startswith(";Filament used:"):
                line = f";Filament used: {round(total_meters)}m"
                new_header.append(line)

            elif line.startswith(";Generated with"):
                new_header.append(line)

        return "\n".join(new_header)

    def generate(self):
        """Generates and sets ``self.hvb_gcode``"""

        gcode = self.generate_header()
        objects_number = 0
        for obj in self.bumpers:
            for i in range(0, obj[1]):
                gcode = gcode + f"\n;Object: {obj[2]} number {i}\n"
                gcode = gcode + (obj[0].analyzer.core_gcode) + "\n"
                gcode = gcode + "# ===== BUMPER GCODE ===== #\n"
                gcode = gcode + f"{obj[0].bumper_gcode()}\n"
                gcode = gcode + "# ===== BUMPER GCODE ===== #\n"
                objects_number += 1

                yield objects_number

        gcode = gcode + END_GCODE
        self.hvb_gcode = gcode
        yield 0
