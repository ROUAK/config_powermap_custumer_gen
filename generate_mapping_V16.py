Bms_parameter_id = 401
FIRST_ADDRESS = '0640'
nb_range_soc = 7
nb_range_T = 15

adress_int = int(FIRST_ADDRESS, base=16)

f = open('mappingV16.e4s', 'w', encoding='UTF8', newline='')

for index_T in range(nb_range_T):
    for index_soc in range(nb_range_soc):
        adress_hex = ('0' + hex(adress_int).lstrip("0x")).upper()

        f.write(f"""
        <BMS_Parameters>
            <BMSParametersID>-{Bms_parameter_id}</BMSParametersID>
            <Nom>PAR_IMD_SOC{index_soc}_T{index_T}</Nom>
            <Key>{adress_hex}</Key>
            <Groupe>IMD</Groupe>
            <Commentaire>Full_Mid_Low_10bits</Commentaire>
            <Valeur>0</Valeur>
            <dateRW></dateRW>
            <ValeurHexa>00000000</ValeurHexa>
            <DisplayType>U32</DisplayType>
            <CfgFlags>CP;CC;</CfgFlags>
            <IsCloneable>true</IsCloneable>
        </BMS_Parameters>
        """)

        adress_int += 4
        Bms_parameter_id += 1
f.close()
