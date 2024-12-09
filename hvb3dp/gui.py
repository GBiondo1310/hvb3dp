import json
import tkinter as tk

from os import listdir
from tkinter import filedialog, messagebox, ttk, simpledialog
from platform import system

from .hv_multiple import HVMultiple
from .setup import default_printer


class HVB3DPGui(tk.Tk):
    """User Interface for HVB3D"""

    file_list = []  #: Holds user selected files
    printers_dict = {}  #: Holds printers stored in printers.json
    selected_printer = None  #: Holds selected printer
    printer_name = None  #: Holds selected printer name
    printer_x = None  #: Holds selected printer Max X
    printer_y = None  #: Holds selected printer Max Y
    printer_z = None  #: Holds selected printer Max Z
    printer_nozzle_offset = None  #: Holds selected printer nozzle - head offset

    def __init__(self):
        """Initializes UI"""
        super().__init__()

        self.title("HVB3DP - High Volume Batch (for) 3D Printing")
        self.geometry("1600x900")

        self.selected_printer = tk.StringVar()

        if "printers.json" not in listdir():
            default_printer()

        self.load_printers()
        self.setup()

    def load_printers(self):
        """Loads printers in printers.json in self.printers_dict
        and updates self.selected_printer"""
        with open("printers.json", mode="r") as printers_json:
            self.printers_dict = json.load(printers_json)
        if not any(self.printers_dict):
            default_printer()
            self.load_printers()
            return
        self.selected_printer.set(list(self.printers_dict.keys())[0])

    def setup(self):
        """Set up UI"""

        self.files_frame = tk.Frame(self)
        self.printer_frame = tk.Frame(self)
        self.btns_frame = tk.Frame(self)

        self.files_frame.place_configure(relx=0, rely=0, relheight=0.8, relwidth=0.7)
        self.printer_frame.place_configure(
            relx=0.7, rely=0, relheight=0.8, relwidth=0.3
        )
        self.btns_frame.place_configure(relx=0.5, rely=0.9, anchor="center")

        add_file_btn = tk.Button(
            self.btns_frame, text="Add gcode files", command=self.add_gcode
        )
        add_file_btn.grid(row=0, column=0, padx=5)

        generate_btn = tk.Button(
            self.btns_frame, text="Generate HVB gcode", command=self.generate
        )
        generate_btn.grid(row=0, column=1, padx=5)

        manage_printes_btn = tk.Button(
            self.btns_frame, text="Manage printers", command=self.manage_printers
        )
        manage_printes_btn.grid(row=0, column=2, padx=5)

        printers_menu = tk.OptionMenu(
            self.printer_frame, self.selected_printer, *list(self.printers_dict.keys())
        )
        printers_menu.pack(pady=20)

        self.update()

        self.selected_printer.trace_add("write", self.update)
        self.printer_name.pack()
        self.printer_x.pack()
        self.printer_y.pack()
        self.printer_z.pack()
        self.printer_nozzle_offset.pack()

    def update(self, *args, **kwargs):
        """Updates UI"""
        if self.printer_name:
            self.printer_name.destroy()
        self.printer_name = tk.Label(
            self.printer_frame,
            text=f"Printer name: {self.printers_dict.get(self.selected_printer.get()).get('name')}",
        )
        self.printer_name.pack(pady=5, anchor="nw", padx=5)

        if self.printer_x:
            self.printer_x.destroy()
        self.printer_x = tk.Label(
            self.printer_frame,
            text=f"Printer X: {self.printers_dict.get(self.selected_printer.get()).get('x')}",
        )
        self.printer_x.pack(pady=5, anchor="nw", padx=5)

        if self.printer_y:
            self.printer_y.destroy()
        self.printer_y = tk.Label(
            self.printer_frame,
            text=f"Printer Y: {self.printers_dict.get(self.selected_printer.get()).get('y')}",
        )
        self.printer_y.pack(pady=5, anchor="nw", padx=5)

        if self.printer_z:
            self.printer_z.destroy()
        self.printer_z = tk.Label(
            self.printer_frame,
            text=f"Printer Z: {self.printers_dict.get(self.selected_printer.get()).get('z')}",
        )
        self.printer_z.pack(pady=5, anchor="nw", padx=5)

        if self.printer_nozzle_offset:
            self.printer_nozzle_offset.destroy()
        self.printer_nozzle_offset = tk.Label(
            self.printer_frame,
            text=f"Printer nozzle offset: {self.printers_dict.get(self.selected_printer.get()).get('nozzle_y_offset')}",
        )
        self.printer_nozzle_offset.pack(pady=5, anchor="nw", padx=5)

    def add_gcode(self):
        paths = filedialog.askopenfilenames()
        if any(paths):
            for path in paths:
                row = len(self.file_list)
                file_label = tk.Label(self.files_frame, text=path)
                file_label.grid(row=row, column=0, sticky="w", padx=10, pady=20)

                spinbox = tk.Spinbox(
                    self.files_frame,
                    from_=1,
                    to=9999,
                    width=5,
                )
                spinbox.grid(row=row, column=1, padx=10, pady=5)

                move_up_btn = tk.Button(
                    self.files_frame,
                    text="Up",
                    command=lambda index=row: self.move_up(index),
                )
                move_up_btn.grid(row=row, column=2, padx=5)

                move_down_btn = tk.Button(
                    self.files_frame,
                    text="Down",
                    command=lambda index=row: self.move_down(index),
                )
                move_down_btn.grid(row=row, column=3, padx=5)

                delete_btn = tk.Button(
                    self.files_frame,
                    text="Remove object",
                    command=lambda index=row: self.delete_file(index),
                )
                delete_btn.grid(row=row, column=4, padx=5)

                self.file_list.append(
                    (path, file_label, spinbox, move_up_btn, move_down_btn, delete_btn)
                )

    def move_up(self, index):
        """Moves up a file in the list"""
        if index > 0:
            self.swap_rows(index, index - 1)

    def move_down(self, index):
        """Moves down a file in the list"""
        if index < len(self.file_list) - 1:
            self.swap_rows(index, index + 1)

    def delete_file(self, index):
        """Removes a file from the list"""
        _, file_label, spinbox, move_up_btn, move_down_btn, delete_btn = self.file_list[
            index
        ]

        file_label.grid_forget()
        spinbox.grid_forget()
        move_up_btn.grid_forget()
        move_down_btn.grid_forget()
        delete_btn.grid_forget()

        self.file_list.pop(index)

        self.refresh_grid()

    def swap_rows(self, index1, index2):
        """Swaps rows of a file in the file list"""
        self.file_list[index1], self.file_list[index2] = (
            self.file_list[index2],
            self.file_list[index1],
        )

        self.refresh_grid()

    def refresh_grid(self):
        for i, (_, file_label, spinbox, up_btn, down_btn, del_btn) in enumerate(
            self.file_list
        ):
            file_label.grid(row=i, column=0, sticky="w", padx=10, pady=20)
            spinbox.grid(row=i, column=1, padx=10, pady=5)
            up_btn.grid(row=i, column=2, padx=5)
            down_btn.grid(row=i, column=3, padx=5)
            del_btn.grid(row=i, column=4, padx=5)

            # Update button commands to reflect the new indices
            up_btn.config(command=lambda idx=i: self.move_up(idx))
            down_btn.config(command=lambda idx=i: self.move_down(idx))
            del_btn.config(command=lambda idx=i: self.delete_file(idx))

    def generate(self):
        """Generate HVB .gcode file"""
        if not any(self.file_list):
            messagebox.showerror(
                "No gcode added", "You need to add at least one gcode file first"
            )
            return

        message = tk.Toplevel(self)
        message.title("HVB3DP")
        message.geometry("800x450")

        objects = []
        for obj in self.file_list:
            name = None
            if system() == "Windows":
                name = obj[0].split("\\")[-1]
            elif system() == "Linux":
                name = obj[0].split("/")[-1]
            else:
                raise NotImplementedError

            objects.append({name: {"path": obj[0], "number": int(obj[2].get())}})

        hv = HVMultiple(objects, self.selected_printer.get())

        tk.Label(message, text="Export on progress..").pack()

        pbs = ttk.Progressbar(message, length=100, mode="indeterminate", value=0)
        pbs.pack()
        pbs.start()

        operation_var = tk.IntVar()
        operation_var.set(0)

        self.operation = tk.Label(message, text="Processing...")
        self.operation.pack()

        def update_operation(*args, **kw):
            self.operation.destroy()

            self.operation = tk.Label(
                message, text=f"Generating gcode for obj: {operation_var.get()}..."
            )
            self.operation.pack()
            message.update()

        operation_var.trace_add(mode="write", callback=update_operation)

        def generate():
            for x in hv.generate():
                if x == 0:
                    break
                operation_var.set(x)
                operation_var.get()

        generate()

        self.operation.destroy()
        self.operation = tk.Label(message, text="Exporting HVB gcode...")
        self.operation.pack()
        output = filedialog.asksaveasfilename()
        if output == "":
            message.destroy()
            return
        output = output + ".gcode"

        with open(output, mode="w") as hvb_file:
            hvb_file.write(hv.hvb_gcode)

        message.destroy()
        messagebox.showinfo("SUCCESS", f"File: {output} has been saved successfully")

        hv.hvb_gcode = ""
        for bumper in hv.bumpers:
            del bumper

        layer = 0
        with open(output, mode="r") as gcode_file:
            gcode = gcode_file.readlines()

        for index, line in enumerate(gcode):
            if line.startswith(";LAYER:"):
                gcode[index] = f";LAYER:{layer}\n"
                layer += 1

        layer -= 1

        first = True
        for index, line in enumerate(gcode):
            if line.startswith(";LAYER_COUNT:"):
                if first:
                    gcode[index] = f";LAYER_COUNT:{layer}\nG28\n"
                    first = False
                else:
                    gcode[index] = "G28\n"

        with open(output, mode="w") as gcode_file:
            gcode_file.writelines(gcode)

    def manage_printers(self):
        """Allows user to add, modify and delete printers"""

        manage_printers_menu = tk.Toplevel(self)
        manage_printers_menu.title("HVB3DP - Manage printers")
        manage_printers_menu.geometry("800x450")

        add_printer_btn = tk.Button(
            manage_printers_menu, text="Add printer", command=self.add_printer
        )
        modify_printer_btn = tk.Button(
            manage_printers_menu, text="Modify printer", command=self.modify_printers
        )
        remove_printer_btn = tk.Button(
            manage_printers_menu, text="Remove printer", command=self.delete_printer
        )

        add_printer_btn.pack(expand=True, pady=5)
        modify_printer_btn.pack(expand=True, pady=5)
        remove_printer_btn.pack(expand=True, pady=5)

    def add_printer(self):
        """User can add a new printer"""

        printer_name = simpledialog.askstring(
            title="HVB3DP - Add printer", prompt="Enter printer name"
        )
        printer_x = simpledialog.askinteger(
            title="HVB3DP - Add printer", prompt="Enter printer max X"
        )

        printer_y = simpledialog.askinteger(
            title="HVB3DP - Add printer", prompt="Enter printer max Y"
        )

        printer_z = simpledialog.askinteger(
            title="HVB3DP - Add printer", prompt="Enter printer max Z"
        )
        printer_nozzle_offset = simpledialog.askinteger(
            title="HVB3DP - Add printer",
            prompt="Enter printer nozzle - head offset",
        )
        printer_code = simpledialog.askstring(
            title="HVB3DP - Add printer", prompt="Enter printer shorthand name"
        )

        yn = messagebox.askokcancel(
            "HVB3DP - Add printer",
            message=f"""Printers details
Name: {printer_name}
Max X: {printer_x}
Max Y: {printer_y}
Max Z: {printer_z}
Nozzle - head offset: {printer_nozzle_offset}
Shorthand name: {printer_code}

Do you want to add this printer?""",
        )

        if yn:
            if "printers.json" not in listdir():
                with open("printers.json", mode="w") as printers_file:
                    json.dump("{}", printers_file)
            if self.printers_dict.get(printer_code):
                overwrite = messagebox.askokcancel(
                    "HVB3DP - Add printer",
                    f"A printer with shorthand name: {printer_code} already exists, do you want to replace it?",
                )
                if not overwrite:
                    return

            self.printers_dict.update(
                {
                    printer_code: {
                        "name": printer_name,
                        "x": printer_x,
                        "y": printer_y,
                        "z": printer_z,
                        "nozzle_y_offset": printer_nozzle_offset,
                    }
                }
            )

            with open("printers.json", mode="w") as printers_file:
                json.dump(self.printers_dict, printers_file, indent=4)

            messagebox.showinfo(
                title="HVB3DP - Add printer",
                message="New printer added",
            )

            self.files_frame.destroy()
            self.btns_frame.destroy()
            self.printer_frame.destroy()
            self.selected_printer.set(list(self.printers_dict.keys())[0])
            self.setup()

    def modify_printers(self):
        """User can modify printers"""
        message = tk.Toplevel(self)
        message.title("HVB3DP - Modify printer")
        message.geometry("800x450")

        selected_printer = tk.StringVar()
        selected_printer.set(list(self.printers_dict.keys())[0])

        printers_menu = tk.OptionMenu(
            message,
            selected_printer,
            *list(self.printers_dict.keys()),
        )

        printers_menu.pack(pady=20, padx=5)

        def modify():
            printer_name = simpledialog.askstring(
                title=f"HVB3DP - Modify {selected_printer.get()}",
                prompt="Enter printer name",
            )
            printer_x = simpledialog.askinteger(
                title=f"HVB3DP - Modify {selected_printer.get()}",
                prompt="Enter printer max X",
            )

            printer_y = simpledialog.askinteger(
                title=f"HVB3DP - Modify {selected_printer.get()}",
                prompt="Enter printer max Y",
            )

            printer_z = simpledialog.askinteger(
                title=f"HVB3DP - Modify {selected_printer.get()}",
                prompt="Enter printer max Y",
            )
            printer_nozzle_offset = simpledialog.askstring(
                title=f"HVB3DP - Modify {selected_printer.get()}",
                prompt="Enter printer nozzle - head offset",
            )

            yn = messagebox.askokcancel(
                f"HVB3DP - Modify {selected_printer.get()}",
                message=f"""Printers details
Name: {printer_name}
Max X: {printer_x}
Max Y: {printer_y}
Max Z: {printer_z}
Nozzle - head offset: {printer_nozzle_offset}
Shorthand name: {selected_printer.get()}

Do you want to modify this printer?""",
            )

            if yn:

                self.printers_dict.update(
                    {
                        selected_printer.get(): {
                            "name": printer_name,
                            "x": printer_x,
                            "y": printer_y,
                            "z": printer_z,
                            "nozzle_y_offset": printer_nozzle_offset,
                        }
                    }
                )

                with open("printers.json", mode="w") as printers_file:
                    json.dump(self.printers_dict, printers_file, indent=4)

                messagebox.showinfo(
                    title=f"HVB3DP - Modify {selected_printer.get()}",
                    message="Printer modified",
                )

            self.files_frame.destroy()
            self.btns_frame.destroy()
            self.printer_frame.destroy()
            self.selected_printer.set(list(self.printers_dict.keys())[0])
            self.setup()

            message.destroy()

        tk.Button(message, text="Modify printer", command=modify).pack(padx=5)
        tk.Button(message, text="Cancel", command=lambda _: message.destroy()).pack(
            padx=5
        )

    def delete_printer(self):
        """User can delete a printer"""
        if "printers.json" not in listdir():
            messagebox.showwarning("No printer added yet!")
            return

        message = tk.Toplevel(self)
        message.title("HVB3DP - Delete printer")
        message.geometry("800x450")

        selected_printer = tk.StringVar()
        selected_printer.set(list(self.printers_dict.keys())[0])

        printers_menu = tk.OptionMenu(
            message,
            selected_printer,
            *list(self.printers_dict.keys()),
        )

        printers_menu.pack(pady=20, padx=5)

        def delete():
            yn = messagebox.askokcancel(
                "HVB3DP - Delete printer",
                f"Do you really want to delete {selected_printer.get()} printer?",
            )
            if yn:
                self.printers_dict.pop(selected_printer.get())
                print(json.dumps(self.printers_dict, indent=4))

                with open("printers.json", mode="w") as printers_file:
                    json.dump(self.printers_dict, printers_file, indent=4)

                messagebox.showinfo(
                    title="HVB3DP - Delete printer",
                    message="Printed deleted",
                )

            self.files_frame.destroy()
            self.btns_frame.destroy()
            self.printer_frame.destroy()
            if not any(self.printers_dict):
                default_printer()

            self.load_printers()
            self.setup()
            message.destroy()

        tk.Button(message, text="Delete printer", command=delete).pack()
