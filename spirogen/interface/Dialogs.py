"""
File: Dialogs.py
Author: Ryan McKay
Date: April 18, 2020

Purpose: These dialogs allow for extra functionality for the SpiroGen interface.
    They are all very simple with only a few widgets each
Input: All of the dialogs take a function to run upon submit except for the
    ListAvailableDialog, which takes the stringvar for the entry box for the
    name of the setting, which is set when a name is clicked on. it also takes
    the type of load/save as a string. This is the folder it is to list from.
Output:
    They all run the function that they are given when submit is clicked.
"""
from tkinter import Frame, Toplevel, StringVar, Label, Entry, Button, IntVar, \
    Radiobutton, Listbox
from spirogen.interface.Parameter import Parameter
import os
import re
from matplotlib.colors import rgb2hex, hex2color


class ShiftLightnessDialog(Frame):
    """
    This is the dialog for the lightness shift effect. It has just a single
    control.
    Args:
        func: the shift lightness function, which is run with the settings
            defined in the dialog when the apply button is clicked.
    """
    def __init__(self, func):
        super().__init__(Toplevel())
        self.master.title('Shift Lightness')
        self._func = func
        self.pack(padx=20, pady=20)

        self._amount = StringVar()
        self._amount.set(0)
        amtlabel = Label(self, text="Amount:")
        amtbox = Entry(self, width=5, textvariable=self._amount)
        applybtn = Button(self, text="Apply", command=self.apply)

        amtlabel.grid(row=38, column=3, columnspan=120, pady=10)
        amtbox.grid(row=38, column=125, columnspan=80)
        applybtn.grid(row=50, column=40)

    def apply(self):
        try:
            amt = round(float(self._amount.get()))
            if abs(amt) <= 255:
                self._func(amt)
                self.master.destroy()
            else:
                print("amount must be between -255 and 255.")
        except ValueError as error:
            print("Value must be numerical.")
            raise error


class RampLightnessDialog(Frame):
    """
    This is the dialog for the lightness ramp effect. It has just a few
    controls
    Args:
        func: the ramp lightness function, which is run with the settings
            defined in the dialog when the apply button is clicked.
    """
    def __init__(self, func):
        super().__init__(Toplevel())
        self.master.title('Ramp Lightness')
        self._func = func
        self.pack(padx=20, pady=20)

        self._amount = StringVar()
        self._direction = IntVar()
        self._goto = StringVar()

        self._amount.set(-255)
        self._direction.set(0)
        self._goto.set(50)

        # creating all of the controls and labels
        amtlabel = Label(self, text='Amount:')
        amtbox = Entry(self, width=5, textvariable=self._amount)
        directionlabel = Label(self, text='Direction:')
        leftbutton = Radiobutton(
            self, text='Left', width=8, indicatoron=False, value=0,
            variable=self._direction
        )
        rightbutton = Radiobutton(
            self, text='Right', width=8, indicatoron=False, value=1,
            variable=self._direction
        )
        gotolabel = Label(self, text='Go To %:')
        gotobox = Entry(self, width=5, textvariable=self._goto)
        applybtn = Button(self, text="Apply", command=self.apply)

        # and adding all controls and labels to the page
        amtlabel.grid(row=38, column=3, columnspan=120, pady=10)
        amtbox.grid(row=38, column=125, columnspan=80)
        directionlabel.grid(row=42, column=3, columnspan=90, pady=10)
        leftbutton.grid(row=42, column=100, columnspan=70)
        rightbutton.grid(row=42, column=180, columnspan=70)
        gotolabel.grid(row=46, column=3, columnspan=120, pady=10)
        gotobox.grid(row=46, column=130, columnspan=80)
        applybtn.grid(row=50, column=40)

    def apply(self):
        try:
            amt = round(float(self._amount.get()))
            direction = int(self._direction.get())
            goto = round(float(self._goto.get()))
            self._func(amt, direction, goto)
            self.master.destroy()
        except ValueError as error:
            print("one of the parameters in non-numerical.")
            raise error


class SaveDialog(Frame):
    """
    This is a simple dialog for saving settings. It has radiobuttons for
    selecting load type ('sessions', 'patterns', 'colors'), an entry box for the
    name you want to set for the current setting, and a button to save the
    current setting under the name in the entry box.
    Args:
         func: the function passed by Application to run when the load button
            is pressed.
    """
    def __init__(self, func, currentnames):
        super().__init__(Toplevel())
        self.master.title("Save")
        self.pack(padx=30, pady=30)

        self._current_names = currentnames

        # making controls to set the mode
        mode = StringVar()
        mode.set('sessions')
        session = Radiobutton(
            self, text="Session", width=8, indicatoron=False, value="sessions",
            variable=mode
        )
        pattern = Radiobutton(
            self, text="Pattern", width=8, indicatoron=False, value='patterns',
            variable=mode
        )
        colors = Radiobutton(
            self, text="Colors", width=8, indicatoron=False, value='colors',
            variable=mode
        )

        # creating the entry box
        name = StringVar()
        namelabel = Label(self, text="Name:")
        namebox = Entry(self, textvariable=name)

        self.fill_current_name(name, mode.get())
        mode.trace('w', lambda *x: self.fill_current_name(name, mode.get()))

        # making the button that runs the save function
        savebtn = Button(
            self, text="Save",
            command=lambda: func(mode.get(), name.get())
        )

        # adding everything to the page
        session.grid(row=10, column=9, columnspan=100)
        pattern.grid(row=10, column=120, columnspan=100, padx=20)
        colors.grid(row=10, column=230, columnspan=100)
        namelabel.grid(row=13, column=37, columnspan=100, pady=(20, 0))
        namebox.grid(row=15, column=10, columnspan=300, pady=(0, 20))
        savebtn.grid(row=20, column=250, columnspan=50, sticky='se')

    def fill_current_name(self, namevar, mode):
        if self._current_names[mode]:
            namevar.set(self._current_names[mode])


class LoadDialog(Frame):
    """
    This is a simple dialog for loading settings. It has radiobuttons for
    selecting load type ('sessions', 'patterns', 'colors'), an entry box
    for the name of the desired setting, a button to list and select available
    setting names, and a button to load whatever is in the entry box.
    Args:
         func: the function passed by Application to run when the load button
            is pressed.
    """
    def __init__(self, func):
        super().__init__(Toplevel())
        self.master.title("Load")
        self.pack(padx=30, pady=30)

        # controls for type of setting to load:
        mode = StringVar()
        mode.set('sessions')
        session = Radiobutton(
            self, text="Session", width=8, indicatoron=False, value="sessions",
            variable=mode
        )
        pattern = Radiobutton(
            self, text="Pattern", width=8, indicatoron=False, value='patterns',
            variable=mode
        )
        colors = Radiobutton(
            self, text="Colors", width=8, indicatoron=False, value='colors',
            variable=mode
        )

        # setting up the entry box for the name of setting:
        name = StringVar()
        namelabel = Label(self, text="Name:")
        namebox = Entry(self, textvariable=name)

        # making the button to show available settings
        listbtn = Button(
            self,
            text="List Available",
            command=lambda: self.open_list_dialog(name, mode)
        )

        # making button to run the passed loading function
        loadbtn = Button(
            self, text="Load",
            command=lambda: func(mode.get(), name.get())
        )

        # adding everything to the page:
        session.grid(row=10, column=9, columnspan=100)
        pattern.grid(row=10, column=120, columnspan=100, padx=20)
        colors.grid(row=10, column=230, columnspan=100)
        namelabel.grid(row=13, column=37, columnspan=100, pady=(20, 0))
        namebox.grid(row=15, column=10, columnspan=300, pady=(0, 20))
        listbtn.grid(row=20, column=9, columnspan=50, sticky='sw')
        loadbtn.grid(row=20, column=250, columnspan=50, sticky='se')

    @staticmethod
    def open_list_dialog(name, mode):
        ListAvailableDialog(name, mode.get())


class ListAvailableDialog(Frame):
    """
    This dialog is launched from the loading dialog. It lists the names that
    are available to load. Clicking on one of the names fills the entry box
    with that name.
    Args:
        namevar: the tk variable for the load dialog textbox. This is set based
            on the list item clicked.
        type: a string representing the type of object to load. must be
            'sessions', 'colors', or 'patterns'.
    """
    def __init__(self, namevar, type='sessions'):
        super().__init__(Toplevel())
        self.namevar = namevar
        self.master.title(f"Loadable {type.capitalize()[:-1]} Names")
        self.pack(padx=30, pady=30)

        files = os.listdir(
            f'./spirogen/interface/settings/{type}'
        )
        lbox = Listbox(self)

        endfiles = []
        for i, file in enumerate(files):
            name = file.replace('.json', '')
            # so that we don't show the names that are just generated id's:
            if 'from' in name and 'session' in name:
                endfiles.append(name)
            else:
                if not all(map(lambda x: x.isdigit(), name)):
                    lbox.insert(i, name)
        for i, file in enumerate(endfiles):
            lbox.insert(i + len(files), file)
        lbox.pack(fill="both")
        lbox.bind('<<ListboxSelect>>', self.get_value)

    def get_value(self, event):
        w = event.widget
        ind = int(w.curselection()[0])
        self.namevar.set(w.get(ind))


class ColorSwatchDialog(Frame):
    """
    This dialog is for editing colors directly. It is launched by clicking on
    a color swatch on the color scheme page.
    Args:
        targetswatch: the swatched that was clicked to open the dialog. This is
            the swatch that will be updated.
        curcolors: the current bank of colors in the session
        defaultcolors: the bank of default, full spectrum, colors
    """
    def __init__(self, targetswatch, curcolors, defaultcolors):
        super().__init__(Toplevel())
        self.master.title('Update Color')
        self.pack(padx=10, pady=10)
        self.targetbox = targetswatch
        self.targetvars = targetswatch.targets
        self.curcolors = curcolors
        self.defaultcolors = defaultcolors

        self.colorview = Frame(self, width=200, height=200, bg=targetswatch.color)
        self.colorview.grid(column=5, row=5, rowspan=200, columnspan=200)

        rscale = Parameter(
            self, width=200, from_=0, to=255, row=210, pady=0,
            troughcolor='red', activebackground='red',
            command=lambda *x: self.update_color('r')
        )
        gscale = Parameter(
            self, width=200, from_=0, to=255, row=220, pady=0,
            troughcolor='#0F0', activebackground='#0F0',
            command=lambda *x: self.update_color('g')
        )
        bscale = Parameter(
            self, width=200, from_=0, to=255, row=230, pady=0,
            troughcolor='blue', activebackground='blue',
            command=lambda *x: self.update_color('b')
        )
        self.colorparams = {'r': rscale, 'g': gscale, 'b': bscale}
        for color in self.targetvars:
            try:
                val = round(float(self.targetvars[color].get()))
            except ValueError:
                print('color values must be numeric and between 0 and 255')
                val = 0
            self.colorparams[color].set(val)
        self.swatch_area = Frame(self)
        self.swatch_area.grid(column=0, row=5, padx=10, rowspan=250)

        self.hexvar = StringVar()
        self.hexvar.set(
            rgb2hex((rscale.get()/255, gscale.get()/255, bscale.get()/255))
        )
        hexlabel = Label(self, text='Hex:')
        hexbox = Entry(self, width=20, textvariable=self.hexvar)
        hexlabel.grid(row=260, column=5)
        hexbox.grid(row=279, column=5, columnspan=195)
        self.hexvar.trace('w', self.set_from_hex)

        self.setup_swatch_selection()

    def update_color(self, color):
        rgb = []
        indexloc = {'r': 0, 'g': 1, 'b': 2}
        for k in self.colorparams:
            param = self.colorparams[k]
            val = round(float(param.get()))
            if color == k:
                self.targetvars[k].set(val)
                singlecolor = [0, 0, 0]
                singlecolor[indexloc[k]] = val
                singlecolor = self.rgb_tk(singlecolor)
                param.configure(activebackground=singlecolor)
            rgb.append(val)
        rgb = self.rgb_tk(rgb)
        self.colorview.configure(bg=rgb)
        self.targetbox.configure(bg=rgb)

    def setup_swatch_selection(self):
        current = self.curcolors
        defaultcolors = self.defaultcolors
        length = len(self.curcolors['r'])
        black = SelectableColorSwatch(
            self.swatch_area, color=(0, 0, 0), func=self.grab_swatch_color
        )
        black.grid(row=5, column=10, padx=2, pady=(0, 15))
        white = SelectableColorSwatch(
            self.swatch_area, color=(255, 255, 255),
            func=self.grab_swatch_color, highlightbackground='black',
            highlightthickness=1
        )
        white.grid(row=5, column=20, padx=2, pady=(0, 15))
        for i in range(length):
            rgb = tuple(current[k][i] for k in ['r', 'g', 'b'])
            swatch = SelectableColorSwatch(
                self.swatch_area, color=rgb, func=self.grab_swatch_color,
                highlightbackground='black', highlightthickness=1
            )
            swatch.grid(row=10*(i+1), column=10, padx=2)

            rgb = tuple(defaultcolors[k][i] for k in ['r', 'g', 'b'])
            swatch = SelectableColorSwatch(
                self.swatch_area, rgb, self.grab_swatch_color,
                highlightbackground='black', highlightthickness=1
            )
            swatch.grid(row=10 * (i + 1), column=20, padx=2, pady=4)

    def grab_swatch_color(self, color):
        color = {'r': color[0], 'g': color[1], 'b': color[2]}
        for k in color:
            self.colorparams[k].set(color[k])

    def set_from_hex(self, *args):
        hex = self.hexvar.get()
        if '#' in hex and (len(hex) == 7 or len(hex) == 4):
            match = re.search('^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$', hex)
            if match:
                rgb = tuple(round(i * 255) for i in (hex2color(hex)))
                indicies = {'r': 0, 'g': 1, 'b': 2}
                for k in self.colorparams:
                    self.colorparams[k].set(rgb[indicies[k]])


    @staticmethod
    def hex_to_rgb(hexstr):
        hexstr = hexstr.strip('#')
        hlen = len(hexstr)
        return tuple(int(hexstr[i:i+hlen//3], 16) for i in range(0, hlen, hlen//3))

    @staticmethod
    def rgb_tk(rgb):
        rgb = tuple([round(float(i)) for i in rgb])
        output = "#%02x%02x%02x" % rgb
        return output


class SelectableColorSwatch(Frame):
    """
    This is the class of swatches used in the color editing dialog. The point
    is to be selectable. It's just a thin wrapper around Frame that binds
    click events to the passed function.
    """
    def __init__(self, master, color, func, **kwargs):
        self.color = color
        super().__init__(
            master, bg=self.rgb_tk(self.color), height=25, width=30, **kwargs
        )
        self.bind("<Button-1>", lambda *x: func(color))

    @staticmethod
    def rgb_tk(rgb):
        rgb = tuple([round(float(i)) for i in rgb])
        output = "#%02x%02x%02x" % rgb
        return output
