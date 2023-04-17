import csv
from tkinter import *
import math
from tkinter.ttk import Notebook

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("config_PowerMap_Custumer_Gen")
window.config(padx=20, pady=20)

# ---------------------------- Constants and global variables ------------------------------- #
index_parameter = 0
FIRST_ADDRESS = '0640'
adress_int = int(FIRST_ADDRESS, base=16)
entries = {}
entries_mid_power = {}
entries_low_power = {}
entries_soc = {}
entries_T = {}
tableheight = 15
tablewidth = 7
header = []
seuils_soc_labels = {}
seuils_soc_mid_labels = {}
seuils_soc_low_labels = {}
seuils_T_labels = {}
seuils_T_mid_labels = {}
seuils_T_low_labels = {}
WIDTH_ENTRIES = 7
seuils_soc = [5, 10, 15, 20, 30, 35]
seuils_Temperature = [-15, -10, -5, 0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]

############################################### Ajout des seuils Soc##############################################


def generate_header_soc(seuils_soc_var):
    global adress_int
    global index_parameter
    global header

    header = []
    index_parameter = 0
    adress_int = int(FIRST_ADDRESS, base=16)
    seuils_soc_comment = ''
    range_seuil_soc = 1

    if len(seuils_soc_var) <= 4:
        range_seuil_soc = 1
    elif len(seuils_soc_var) <= 8:
        range_seuil_soc = 2
    elif len(seuils_soc_var) <= 12:
        range_seuil_soc = 3
    elif len(seuils_soc_var) <= 16:
        range_seuil_soc = 4
    else:
        range_seuil_soc = 5

    len_seuils_soc = len(seuils_soc_var)
    for seuil_soc in range(range_seuil_soc):
        adress_hex = ('0' + hex(adress_int).lstrip("0x")).upper()
        if int(len_seuils_soc/4) != 0:
            seuils_soc_comment = f'Seuil{4*seuil_soc+3}_{4*seuil_soc+2}_{4*seuil_soc+1}_{4*seuil_soc}'
            param_int = int('0b00' + bin(seuils_soc_var[4*seuil_soc+3])[2:].zfill(8) + bin(seuils_soc_var[4*seuil_soc+2])[
                2:].zfill(8) + bin(seuils_soc_var[4*seuil_soc+1])[2:].zfill(8) + bin(seuils_soc_var[4*seuil_soc])[
                2:].zfill(8), base=2)
        else:
            if (len(seuils_soc_var) % 4) == 2:
                seuils_soc_comment = f'Seuilx_x_{4*seuil_soc+1}_{4*seuil_soc}'
                param_int = int('0b00' + bin(seuils_soc_var[4*seuil_soc+1])[2:].zfill(8) + bin(seuils_soc_var[4*seuil_soc])[
                    2:].zfill(8), base=2)
            elif (len(seuils_soc_var) % 4) == 3:
                seuils_soc_comment = f'Seuilx_{4*seuil_soc+2}_{4*seuil_soc+1}_{4*seuil_soc}'
                param_int = int('0b00' + bin(seuils_soc_var[4*seuil_soc+2])[
                    2:].zfill(8) + bin(seuils_soc_var[4*seuil_soc+1])[2:].zfill(8) + bin(seuils_soc_var[4*seuil_soc])[
                    2:].zfill(8), base=2)
            elif (len(seuils_soc_var) % 4) == 1:
                seuils_soc_comment = f'Seuilx_x_x_{4*seuil_soc}'
                param_int = int('0b00' + bin(seuils_soc_var[4*seuil_soc])[
                    2:].zfill(8), base=2)
            else:
                seuils_soc_comment = f'Seuilx_x_x_x'
                param_int = 0

        param_hex = hex(param_int).lstrip("0x").zfill(8).upper()

        header.append([str(index_parameter),
                       f'PAR_IMD_SOC{seuil_soc}', adress_hex, 'IMD', seuils_soc_comment, str(param_int), '', param_hex])
        index_parameter += 1
        adress_int += 4
        len_seuils_soc -= 4


############################################### Ajout des seuils Temperatures ##############################################


def generate_header_T(seuils_T_var):
    global adress_int
    global index_parameter
    global header

    seuils_Temperature_comment = ''
    range_seuil_Temperature = 1

    for seuil_T_idx in range(len(seuils_T_var)):
        if seuils_T_var[seuil_T_idx] < 0:
            seuils_T_var[seuil_T_idx] += 256

    if len(seuils_T_var) <= 4:
        range_seuil_Temperature = 1
    elif len(seuils_T_var) <= 8:
        range_seuil_Temperature = 2
    elif len(seuils_T_var) <= 12:
        range_seuil_Temperature = 3
    elif len(seuils_T_var) <= 16:
        range_seuil_Temperature = 4
    else:
        range_seuil_Temperature = 5

    len_seuils_Temperature = len(seuils_T_var)
    for seuil_Temperature in range(range_seuil_Temperature):
        adress_hex = ('0' + hex(adress_int).lstrip("0x")).upper()
        if int(len_seuils_Temperature/4) != 0:
            seuils_Temperature_comment = f'Seuil{4*seuil_Temperature+3}_{4*seuil_Temperature+2}_{4*seuil_Temperature+1}_{4*seuil_Temperature}'
            param_int = int('0b00' + bin(seuils_T_var[4*seuil_Temperature+3])[2:].zfill(8) + bin(seuils_T_var[4*seuil_Temperature+2])[
                2:].zfill(8) + bin(seuils_T_var[4*seuil_Temperature+1])[2:].zfill(8) + bin(seuils_T_var[4*seuil_Temperature])[
                2:].zfill(8), base=2)
        else:
            if (len(seuils_T_var) % 4) == 2:
                seuils_Temperature_comment = f'Seuilx_x_{4*seuil_Temperature+1}_{4*seuil_Temperature}'
                param_int = int('0b00' + bin(seuils_T_var[4*seuil_Temperature+1])[2:].zfill(8) + bin(seuils_T_var[4*seuil_Temperature])[
                    2:].zfill(8), base=2)
            elif (len(seuils_T_var) % 4) == 3:
                seuils_Temperature_comment = f'Seuilx_{4*seuil_Temperature+2}_{4*seuil_Temperature+1}_{4*seuil_Temperature}'
                param_int = int('0b00' + bin(seuils_T_var[4*seuil_Temperature+2])[
                    2:].zfill(8) + bin(seuils_T_var[4*seuil_Temperature+1])[2:].zfill(8) + bin(seuils_T_var[4*seuil_Temperature])[
                    2:].zfill(8), base=2)
            elif (len(seuils_T_var) % 4) == 1:
                seuils_Temperature_comment = f'Seuilx_x_x_{4*seuil_Temperature}'
                param_int = int('0b00' + bin(seuils_T_var[4*seuil_Temperature])[
                    2:].zfill(8), base=2)
            else:
                seuils_Temperature_comment = f'Seuilx_x_x_x'
                param_int = 0

        param_hex = hex(param_int).lstrip("0x").zfill(8).upper()

        header.append([str(index_parameter),
                       f'PAR_IMD_T{seuil_Temperature}', adress_hex, 'IMD', seuils_Temperature_comment, str(param_int), '', param_hex])
        index_parameter += 1
        adress_int += 4
        len_seuils_Temperature -= 4


############################################### Ajout des de la table powermap 105 ##############################################


powermap_low = [
    [3,  6,  12, 19, 25,  50,  50],
    [5,  6,  12, 19, 25,  50,  50],
    [6,  13, 25, 38, 50,  50,  50],
    [10, 19, 37, 44, 50,  50,  50],
    [12, 25, 50, 53, 56,  56,  56],
    [12, 25, 50, 75, 100, 100, 100],
    [14, 25, 50, 75, 100, 100, 100],
    [17, 34, 68, 84, 100, 100, 100],
    [18, 36, 72, 86, 100, 100, 100],
    [19, 38, 75, 88, 100, 100, 100],
    [19, 38, 75, 88, 100, 100, 100],
    [19, 38, 75, 88, 100, 100, 100],
    [19, 38, 75, 88, 100, 100, 100],
    [19, 38, 75, 88, 100, 100, 100],
    [19, 38, 75, 88, 100, 100, 100],
]

powermap_mid = [
    [3,  6,  12, 19, 25,  50,  50],
    [5,  6,  12, 19, 25,  50,  50],
    [6,  13, 25, 38, 50,  50,  50],
    [10, 19, 37, 44, 50,  50,  50],
    [12, 25, 50, 53, 56,  56,  56],
    [12, 25, 50, 75, 100, 100, 100],
    [14, 25, 50, 75, 100, 100, 100],
    [17, 34, 68, 84, 100, 100, 100],
    [18, 36, 72, 86, 100, 100, 100],
    [19, 38, 75, 88, 100, 100, 100],
    [19, 38, 75, 88, 100, 100, 100],
    [19, 38, 75, 88, 100, 100, 100],
    [19, 38, 75, 88, 100, 100, 100],
    [19, 38, 75, 88, 100, 100, 100],
    [19, 38, 75, 88, 100, 100, 100],
]

powermap_full = [
    [3,  6,  12, 19,  25,  50,  50],
    [4,  6,  25, 25,  25,  50,  50],
    [9,  12, 50, 56,  62,  120, 120],
    [13, 25, 56, 75,  100, 212, 212],
    [14, 28, 62, 81,  106, 218, 218],
    [16, 31, 66, 87,  112, 225, 225],
    [16, 33, 68, 94,  112, 243, 243],
    [17, 34, 72, 100, 132, 263, 263],
    [18, 36, 72, 107, 141, 282, 282],
    [19, 38, 75, 113, 150, 300, 300],
    [19, 38, 75, 113, 150, 300, 300],
    [19, 38, 75, 113, 150, 300, 300],
    [19, 38, 75, 113, 150, 300, 300],
    [19, 38, 75, 113, 150, 300, 300],
    [19, 38, 75, 113, 150, 300, 300],
]

######################################################## Generate csv file ##################################################


def generate_csv_file():
    global header

    entries_soc_list = []
    for column in range(tablewidth-1):
        entries_soc_list.append(int(entries_soc[column].get()))
    generate_header_soc(entries_soc_list)

    entries_T_list = []
    for row in range(tableheight-1):
        entries_T_list.append(int(entries_T[row].get()))
    generate_header_T(entries_T_list)

    adress_int_data = int(FIRST_ADDRESS, base=16)
    adress_int_data += len(header) * 4

    data = []
    data = header.copy()

    for index_T in range(len(powermap_full)):
        for index_soc in range(len(powermap_full[0])):
            adress_hex = ('0' + hex(adress_int_data).lstrip("0x")).upper()
            param_int = int('0b00' + bin(int(entries[index_T * tablewidth + index_soc].get()))[2:].zfill(10) + bin(int(
                entries_mid_power[index_T * tablewidth + index_soc].get()))[2:].zfill(10) + bin(int(entries_low_power[index_T * tablewidth + index_soc].get()))[2:].zfill(10), base=2)
            param_hex = hex(param_int).lstrip("0x").zfill(8).upper()

            data.append([f'{6+index_T*6+index_soc}', f'PAR_IMD_SOC{index_soc}_T{index_T}', adress_hex,
                        'IMD', 'Full_Mid_Low_10bits', str(param_int), '', param_hex])

            adress_int_data += 4

    with open('powermap_client_105.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f, delimiter=';')

        # write multiple rows
        writer.writerows(data)

    update_threshold_labels()

    # Close opend file
    f.close()

################################################ Reset Powermap to EVE ########################################################


def reset_powermap_to_EVE():
    counter = 0
    for row in range(tableheight):
        for column in range(tablewidth):
            entries[counter].delete(0, END)
            entries[counter].insert(0, string=powermap_full[row][column])
            entries_mid_power[counter].delete(0, END)
            entries_mid_power[counter].insert(
                0, string=powermap_mid[row][column])
            entries_low_power[counter].delete(0, END)
            entries_low_power[counter].insert(
                0, string=powermap_low[row][column])
            counter += 1

    counter = 0
    for column in range(len(seuils_Temperature)):
        entries_T[counter].delete(0, END)
        if seuils_Temperature[column] > 127:
            entries_T[counter].insert(
                END, string=seuils_Temperature[column] - 256)
        else:
            entries_T[counter].insert(END, string=seuils_Temperature[column])
        counter += 1

    counter = 0
    for column in range(len(seuils_soc)):
        entries_soc[counter].delete(0, END)
        entries_soc[counter].insert(END, string=seuils_soc[column])
        counter += 1

    update_threshold_labels()

################################################### Update thresholds labels ######################################################


def update_threshold_labels():

    counter = 0
    for column in range(tablewidth):
        if column == 0:
            seuils_soc_labels[counter].config(
                text="0.." + str(entries_soc[column].get()))
            seuils_soc_mid_labels[counter].config(
                text="0.." + str(entries_soc[column].get()))
            seuils_soc_low_labels[counter].config(
                text="0.." + str(entries_soc[column].get()))
        elif column == (tablewidth - 1):
            seuils_soc_labels[counter].config(
                text=str(entries_soc[column-1].get())+"..100")
            seuils_soc_mid_labels[counter].config(
                text=str(entries_soc[column-1].get())+"..100")
            seuils_soc_low_labels[counter].config(
                text=str(entries_soc[column-1].get())+"..100")
        else:
            seuils_soc_labels[counter].config(
                text=str(entries_soc[column-1].get()) + ".." + str(entries_soc[column].get()))
            seuils_soc_mid_labels[counter].config(
                text=str(entries_soc[column-1].get()) + ".." + str(entries_soc[column].get()))
            seuils_soc_low_labels[counter].config(
                text=str(entries_soc[column-1].get()) + ".." + str(entries_soc[column].get()))
        counter += 1

    counter = 0
    for row in range(tableheight):
        if row == 0:
            if int(entries_T[row].get()) > 127:
                seuils_T_labels[counter].config(
                    text="-20.." + str(int(entries_T[row].get()) - 256))
                seuils_T_mid_labels[counter].config(
                    text="-20.." + str(int(entries_T[row].get()) - 256))
                seuils_T_low_labels[counter].config(
                    text="-20.." + str(int(entries_T[row].get()) - 256))
            else:
                seuils_T_labels[counter].config(
                    text="-20.." + entries_T[row].get())
                seuils_T_mid_labels[counter].config(
                    text="-20.." + entries_T[row].get())
                seuils_T_low_labels[counter].config(
                    text="-20.." + entries_T[row].get())
        elif row == (tableheight - 1):
            if int(entries_T[row-1].get()) > 127:
                seuils_T_labels[counter].config(
                    text=str(int(entries_T[row-1].get()) - 256)+"..53")
                seuils_T_mid_labels[counter].config(
                    text=str(int(entries_T[row-1].get()) - 256)+"..53")
                seuils_T_low_labels[counter].config(
                    text=str(int(entries_T[row-1].get()) - 256)+"..53")
            else:
                seuils_T_labels[counter].config(
                    text=entries_T[row-1].get()+"..53")
                seuils_T_mid_labels[counter].config(
                    text=entries_T[row-1].get()+"..53")
                seuils_T_low_labels[counter].config(
                    text=entries_T[row-1].get()+"..53")
        else:
            if (int(entries_T[row-1].get()) > 127) and (int(entries_T[row].get() > 127)):
                seuils_T_labels[counter].config(text=str(
                    int(entries_T[row-1].get())-256) + ".." + str(int(entries_T[row].get())-256))
                seuils_T_mid_labels[counter].config(text=str(
                    int(entries_T[row-1].get())-256) + ".." + str(int(entries_T[row].get())-256))
                seuils_T_low_labels[counter].config(text=str(
                    int(entries_T[row-1].get())-256) + ".." + str(int(entries_T[row].get())-256))
            elif ((int(entries_T[row-1].get()) <= 127) and (int(entries_T[row].get()) > 127)):
                seuils_T_labels[counter].config(
                    text=str(entries_T[row-1].get()) + ".." + str(int(entries_T[row].get())-256))
                seuils_T_mid_labels[counter].config(
                    text=str(entries_T[row-1].get()) + ".." + str(int(entries_T[row].get())-256))
                seuils_T_low_labels[counter].config(
                    text=str(entries_T[row-1].get()) + ".." + str(int(entries_T[row].get())-256))
            elif ((int(entries_T[row-1].get()) > 127) and (int(entries_T[row].get()) <= 127)):
                seuils_T_labels[counter].config(
                    text=str(int(entries_T[row-1].get())-256) + ".." + entries_T[row].get())
                seuils_T_mid_labels[counter].config(
                    text=str(int(entries_T[row-1].get())-256) + ".." + entries_T[row].get())
                seuils_T_low_labels[counter].config(
                    text=str(int(entries_T[row-1].get())-256) + ".." + entries_T[row].get())
            else:
                seuils_T_labels[counter].config(
                    text=entries_T[row-1].get() + ".." + entries_T[row].get())
                seuils_T_mid_labels[counter].config(
                    text=entries_T[row-1].get() + ".." + entries_T[row].get())
                seuils_T_low_labels[counter].config(
                    text=entries_T[row-1].get() + ".." + entries_T[row].get())

        counter += 1


###################################################################################################################################
# ---------------------------- Layout GUI ------------------------------- #
reset_button = Button(text="Reset Powermap to EVE",
                      command=reset_powermap_to_EVE)
reset_button.grid(row=0, columnspan=tablewidth+1, pady=5)

# add soc threshold entries and label
label_soc_values = Label(text="Gauge (%)")
label_soc_values.grid(row=1, column=0)

counter = 0
for column in range(len(seuils_soc)):
    entries_soc[counter] = Entry(width=WIDTH_ENTRIES)
    entries_soc[counter].insert(END, string=seuils_soc[column])
    entries_soc[counter].grid(row=1, column=column+1)
    counter += 1

# add T threshold entries and label
label_T_values = Label(text="Temp (°C)")
label_T_values.grid(row=2, column=0)
counter = 0
for column in range(len(seuils_Temperature)):
    entries_T[counter] = Entry(width=WIDTH_ENTRIES)
    if seuils_Temperature[column] > 127:
        entries_T[counter].insert(END, string=seuils_Temperature[column] - 256)
    else:
        entries_T[counter].insert(END, string=seuils_Temperature[column])
    entries_T[counter].grid(
        row=2 + math.floor(column/tablewidth), column=column % tablewidth + 1)
    counter += 1

# add tabs for choosing power
tabs = Notebook(window)

full_powermap_tab = Frame(tabs)
mid_powermap_tab = Frame(tabs)
low_powermap_tab = Frame(tabs)

tabs.add(full_powermap_tab, text="Full power")
tabs.add(mid_powermap_tab, text="Mid power")
tabs.add(low_powermap_tab, text="Low power")

tabs.grid(row=4, column=0, columnspan=8, pady=10)

# generate csv button
generate_csv_button = Button(text="Generate CSV", command=generate_csv_file)
generate_csv_button.grid(row=5, columnspan=tablewidth+1, pady=5)

#####################################################################################################################################
# add soc thresholds labels for full power
counter = 0
for column in range(tablewidth):
    if column == 0:
        seuils_soc_labels[counter] = Label(full_powermap_tab,
                                           text="0.." + str(seuils_soc[column]))
    elif column == (tablewidth - 1):
        seuils_soc_labels[counter] = Label(full_powermap_tab,
                                           text=str(seuils_soc[column-1])+"..100")
    else:
        seuils_soc_labels[counter] = Label(full_powermap_tab,
                                           text=str(seuils_soc[column-1]) + ".." + str(seuils_soc[column]))
    seuils_soc_labels[counter].grid(row=0, column=column+1)
    counter += 1

# add soc thresholds labels for mid power
counter = 0
for column in range(tablewidth):
    if column == 0:
        seuils_soc_mid_labels[counter] = Label(mid_powermap_tab,
                                               text="0.." + str(seuils_soc[column]))
    elif column == (tablewidth - 1):
        seuils_soc_mid_labels[counter] = Label(mid_powermap_tab,
                                               text=str(seuils_soc[column-1])+"..100")
    else:
        seuils_soc_mid_labels[counter] = Label(mid_powermap_tab,
                                               text=str(seuils_soc[column-1]) + ".." + str(seuils_soc[column]))
    seuils_soc_mid_labels[counter].grid(row=0, column=column+1)
    counter += 1

# add soc thresholds labels for low power
counter = 0
for column in range(tablewidth):
    if column == 0:
        seuils_soc_low_labels[counter] = Label(low_powermap_tab,
                                               text="0.." + str(seuils_soc[column]))
    elif column == (tablewidth - 1):
        seuils_soc_low_labels[counter] = Label(low_powermap_tab,
                                               text=str(seuils_soc[column-1])+"..100")
    else:
        seuils_soc_low_labels[counter] = Label(low_powermap_tab,
                                               text=str(seuils_soc[column-1]) + ".." + str(seuils_soc[column]))
    seuils_soc_low_labels[counter].grid(row=0, column=column+1)
    counter += 1

################################################################################################################################
# add Temperature thresholds labels for full power
counter = 0
for row in range(tableheight):
    if row == 0:
        if seuils_Temperature[row] > 127:
            seuils_T_labels[counter] = Label(full_powermap_tab,
                                             text="-20.." + str(seuils_Temperature[row] - 256))
        else:
            seuils_T_labels[counter] = Label(full_powermap_tab,
                                             text="-20.." + str(seuils_Temperature[row]))
    elif row == (tableheight - 1):
        if seuils_Temperature[row-1] > 127:
            seuils_T_labels[counter] = Label(full_powermap_tab,
                                             text=str(seuils_Temperature[row-1] - 256)+"..53")
        else:
            seuils_T_labels[counter] = Label(full_powermap_tab,
                                             text=str(seuils_Temperature[row-1])+"..53")
    else:
        if (seuils_Temperature[row-1] > 127) and (seuils_Temperature[row] > 127):
            seuils_T_labels[counter] = Label(full_powermap_tab, text=str(
                seuils_Temperature[row-1]-256) + ".." + str(seuils_Temperature[row]-256))
        elif (seuils_Temperature[row-1] <= 127) and (seuils_Temperature[row] > 127):
            seuils_T_labels[counter] = Label(full_powermap_tab,
                                             text=str(seuils_Temperature[row-1]) + ".." + str(seuils_Temperature[row]-256))
        elif (seuils_Temperature[row-1] > 127) and (seuils_Temperature[row] <= 127):
            seuils_T_labels[counter] = Label(full_powermap_tab,
                                             text=str(seuils_Temperature[row-1]-256) + ".." + str(seuils_Temperature[row]))
        else:
            seuils_T_labels[counter] = Label(full_powermap_tab,
                                             text=str(seuils_Temperature[row-1]) + ".." + str(seuils_Temperature[row]))

    seuils_T_labels[counter].grid(row=row+1, column=0)
    counter += 1

# add Temperature thresholds labels for mid power
counter = 0
for row in range(tableheight):
    if row == 0:
        if seuils_Temperature[row] > 127:
            seuils_T_mid_labels[counter] = Label(mid_powermap_tab,
                                                 text="-20.." + str(seuils_Temperature[row] - 256))
        else:
            seuils_T_mid_labels[counter] = Label(mid_powermap_tab,
                                                 text="-20.." + str(seuils_Temperature[row]))
    elif row == (tableheight - 1):
        if seuils_Temperature[row-1] > 127:
            seuils_T_mid_labels[counter] = Label(mid_powermap_tab,
                                                 text=str(seuils_Temperature[row-1] - 256)+"..53")
        else:
            seuils_T_mid_labels[counter] = Label(mid_powermap_tab,
                                                 text=str(seuils_Temperature[row-1])+"..53")
    else:
        if (seuils_Temperature[row-1] > 127) and (seuils_Temperature[row] > 127):
            seuils_T_mid_labels[counter] = Label(mid_powermap_tab, text=str(
                seuils_Temperature[row-1]-256) + ".." + str(seuils_Temperature[row]-256))
        elif (seuils_Temperature[row-1] <= 127) and (seuils_Temperature[row] > 127):
            seuils_T_mid_labels[counter] = Label(mid_powermap_tab,
                                                 text=str(seuils_Temperature[row-1]) + ".." + str(seuils_Temperature[row]-256))
        elif (seuils_Temperature[row-1] > 127) and (seuils_Temperature[row] <= 127):
            seuils_T_mid_labels[counter] = Label(mid_powermap_tab,
                                                 text=str(seuils_Temperature[row-1]-256) + ".." + str(seuils_Temperature[row]))
        else:
            seuils_T_mid_labels[counter] = Label(mid_powermap_tab,
                                                 text=str(seuils_Temperature[row-1]) + ".." + str(seuils_Temperature[row]))

    seuils_T_mid_labels[counter].grid(row=row+1, column=0)
    counter += 1

# add Temperature thresholds labels for low power
counter = 0
for row in range(tableheight):
    if row == 0:
        if seuils_Temperature[row] > 127:
            seuils_T_low_labels[counter] = Label(low_powermap_tab,
                                                 text="-20.." + str(seuils_Temperature[row] - 256))
        else:
            seuils_T_low_labels[counter] = Label(low_powermap_tab,
                                                 text="-20.." + str(seuils_Temperature[row]))
    elif row == (tableheight - 1):
        if seuils_Temperature[row-1] > 127:
            seuils_T_low_labels[counter] = Label(low_powermap_tab,
                                                 text=str(seuils_Temperature[row-1] - 256)+"..53")
        else:
            seuils_T_low_labels[counter] = Label(low_powermap_tab,
                                                 text=str(seuils_Temperature[row-1])+"..53")
    else:
        if (seuils_Temperature[row-1] > 127) and (seuils_Temperature[row] > 127):
            seuils_T_low_labels[counter] = Label(low_powermap_tab, text=str(
                seuils_Temperature[row-1]-256) + ".." + str(seuils_Temperature[row]-256))
        elif (seuils_Temperature[row-1] <= 127) and (seuils_Temperature[row] > 127):
            seuils_T_low_labels[counter] = Label(low_powermap_tab,
                                                 text=str(seuils_Temperature[row-1]) + ".." + str(seuils_Temperature[row]-256))
        elif (seuils_Temperature[row-1] > 127) and (seuils_Temperature[row] <= 127):
            seuils_T_low_labels[counter] = Label(low_powermap_tab,
                                                 text=str(seuils_Temperature[row-1]-256) + ".." + str(seuils_Temperature[row]))
        else:
            seuils_T_low_labels[counter] = Label(low_powermap_tab,
                                                 text=str(seuils_Temperature[row-1]) + ".." + str(seuils_Temperature[row]))

    seuils_T_low_labels[counter].grid(row=row+1, column=0)
    counter += 1

#################################################################################################################################
# add data entries for full power
counter = 0
for row in range(tableheight):
    for column in range(tablewidth):
        entries[counter] = Entry(full_powermap_tab, width=WIDTH_ENTRIES)
        entries[counter].insert(END, string=powermap_full[row][column])
        entries[counter].grid(row=row+1, column=column+1)
        counter += 1

# add data entries for mid power
counter = 0
for row in range(tableheight):
    for column in range(tablewidth):
        entries_mid_power[counter] = Entry(
            mid_powermap_tab, width=WIDTH_ENTRIES)
        entries_mid_power[counter].insert(
            END, string=powermap_mid[row][column])
        entries_mid_power[counter].grid(row=row+1, column=column+1)
        counter += 1

# add data entries for low power
counter = 0
for row in range(tableheight):
    for column in range(tablewidth):
        entries_low_power[counter] = Entry(
            low_powermap_tab, width=WIDTH_ENTRIES)
        entries_low_power[counter].insert(
            END, string=powermap_low[row][column])
        entries_low_power[counter].grid(row=row+1, column=column+1)
        counter += 1

##################################################################################################################################


window.mainloop()
