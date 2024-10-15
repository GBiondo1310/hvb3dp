END_GCODE = """M106 S0 ;Turn-off fan
M104 S0 ;Turn-off hotend
M140 S0 ;Turn-off bed

M84 X Y E ;Disable all steppers but Z

M82 ;absolute extrusion mode
M104 S0
;End of Gcode"""


PRINTERS_JSON = """{
    "CUSTOM_PRINTER":{
        "name": "My custom printer",
        "x": 200,
        "y": 200,
        "z": 200,
        "nozzle_y_offset":50
    }
}"""
