import csv
from tkinter import *
import math
from tkinter.ttk import Notebook

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("config_PowerMap_Custumer_Gen")
window.config(padx=20, pady=20)

# ---------------------------- Constants and global variables ------------------------------- #
FIRST_ADDRESS = '0640'
adress_int = int(FIRST_ADDRESS, base=16)
entries = {}
entries_mid_power = {}
entries_low_power = {}
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

############################################### Ajout des de la table powermap 105 ##############################################


powermap_low = [
    [0,   0,   0,   0,   0,   0,   0],
    [0,   0,   0,   0,   0,   0,   0],
    [0,   0,   0,   0,   0,   0,   0],
    [0,   0,   0,   0,   0,   0,   0],
    [0,   0,   0,   0,   0,   0,   0],
    [0,   0,   0,   0,   0,   0,   0],
    [0,   0,   0,   0,   0,   0,   0],
    [0,   0,   0,   0,   0,   0,   0],
    [0,   0,   0,   0,   0,   0,   0],
    [0,   0,   0,   0,   0,   0,   0],
    [0,   0,   0,   0,   0,   0,   0],
    [0,   0,   0,   0,   0,   0,   0],
    [0,   0, 200, 200, 200, 200, 200],
    [0,   0, 125, 125, 125, 125, 125],
    [0,   0, 125, 125, 125, 125, 125],
]

powermap_mid = [
    [0,   0,   0,   0,   0,   0,   0],
    [0,   0,   0,   0,   0,   0,   0],
    [0,   0,   0,   0,   0,   0,   0],
    [0,   0,   0,   0,   0,   0,   0],
    [0,   0,   0,   0,   0,   0,   0],
    [0,   0,   0,   0,   0,   0,   0],
    [0,   0,   0,   0,   0,   0,   0],
    [0,   0,   0,   0,   0,   0,   0],
    [0,   0,   0,   0,   0,   0,   0],
    [0,   0,   0,   0,   0,   0,   0],
    [0,   0,   0,   0,   0,   0,   0],
    [0,   0,   0,   0,   0,   0,   0],
    [0,   0,   0,   0,   0,   0,   0],
    [0,   0,   0,   0,   0,   0,   0],
    [0,   0,   0,   0,   0,   0,   0],
]

powermap_full = [
    [0,   0,  0,    0,   0,   0,   0],
    [0,   0,  0,    0,   0,   0,   0],
    [0,   0,  0,    0,   0,   0,   0],
    [0,   0,  0,    0,   0,   0,   0],
    [0,   0,  0,    0,   0,   0,   0],
    [0,   0,  0,    0,   0,   0,   0],
    [0, 250, 250, 500, 500,   0,   0],
    [0, 250, 250, 500, 500,   0,   0],
    [0, 250, 250, 500, 500,   0,   0],
    [0, 250, 250, 500, 500,   0,   0],
    [0, 250, 250, 500, 500,   0,   0],
    [0, 250, 250, 500, 500,   0,   0],
    [0,   0, 200, 300, 300, 300, 300],
    [0,   0, 125, 300, 300, 300, 300],
    [0,   0, 125, 300, 300, 300, 300],
]

######################################################## Generate csv file ##################################################


def generate_csv_file():
    global header

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

            data.append([f'{134+index_T*6+index_soc}', f'PAR_IMD_SOC{index_soc}_T{index_T}', adress_hex,
                        'IMD', 'Full_Mid_Low_10bits', str(param_int), '', param_hex])

            adress_int_data += 4

    with open('powermap_client_105.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f, delimiter=';')

        # write multiple rows
        writer.writerows(data)

    # Close opend file
    f.close()

################################################ Reset Powermap  ########################################################


def reset_powermap_to_Goupil():
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


def reset_powermap_to_Zero():
    counter = 0
    for row in range(tableheight):
        for column in range(tablewidth):
            entries[counter].delete(0, END)
            entries[counter].insert(0, string='0')
            entries_mid_power[counter].delete(0, END)
            entries_mid_power[counter].insert(
                0, '0')
            entries_low_power[counter].delete(0, END)
            entries_low_power[counter].insert(
                0, string='0')
            counter += 1


###################################################################################################################################
# ---------------------------- Layout GUI ------------------------------- #
reset_button = Button(text="Reset Powermap to Goupil",
                      command=reset_powermap_to_Goupil)
reset_button.grid(row=0, column=0, columnspan=4, pady=5)

reset_button = Button(text="Reset Powermap to Zero",
                      command=reset_powermap_to_Zero)
reset_button.grid(row=0, column=4, columnspan=4, pady=5)

# Add entries validation to accept only digits and ignore the rest


def callback_digits(P):
    if str.isdigit(P) or P == "":
        return True
    else:
        return False


vcmd_digits = (window.register(callback_digits))

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
        entries[counter] = Entry(
            full_powermap_tab, width=WIDTH_ENTRIES, validate='all', validatecommand=(vcmd_digits, '%P'), justify=CENTER)
        entries[counter].insert(END, string=powermap_full[row][column])
        entries[counter].grid(row=row+1, column=column+1)
        counter += 1

# add data entries for mid power
counter = 0
for row in range(tableheight):
    for column in range(tablewidth):
        entries_mid_power[counter] = Entry(
            mid_powermap_tab, width=WIDTH_ENTRIES, validate='all', validatecommand=(vcmd_digits, '%P'), justify=CENTER)
        entries_mid_power[counter].insert(
            END, string=powermap_mid[row][column])
        entries_mid_power[counter].grid(row=row+1, column=column+1)
        counter += 1

# add data entries for low power
counter = 0
for row in range(tableheight):
    for column in range(tablewidth):
        entries_low_power[counter] = Entry(
            low_powermap_tab, width=WIDTH_ENTRIES, validate='all', validatecommand=(vcmd_digits, '%P'), justify=CENTER)
        entries_low_power[counter].insert(
            END, string=powermap_low[row][column])
        entries_low_power[counter].grid(row=row+1, column=column+1)
        counter += 1

##################################################################################################################################


window.mainloop()
