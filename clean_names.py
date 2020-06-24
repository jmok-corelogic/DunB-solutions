#!/usr/bin/python3

RAW_NAMES = [
'SPV Inc., DBA: Super Company',
'Michael Forsky LLC d.b.a F/B Burgers .',
'*** Youthful You Aesthetics ***',
'Aruna Indika (dba. NGXess)',
'Diot SA, - D. B. A. *Diot-Technologies*',
'PERFECT PRIVACY, LLC, d-b-a Perfection,',
'PostgreSQL DB Analytics',
'/JAYE INC/',
' ETABLISSEMENTS SCHEPENS /D.B.A./ ETS_SCHEPENS',
'DUIKERSTRAINING OOSTENDE | D.B.A.: D.T.O. '
]

CLEANED_NAME_PAIRS = [
('SPV Inc', 'Super Company'),
('Michael Forsky LLC', 'F/B Burgers'),
('Youthful You Aesthetics',None),
('Aruna Indika', 'NGXess'),
('Diot SA', 'Diot-Technologies'),
('PERFECT PRIVACY, LLC', 'Perfection'),
('PostgreSQL DB Analytics',None),
('JAYE INC',None),
('ETABLISSEMENTS SCHEPENS', 'ETS SCHEPENS'),
('DUIKERSTRAINING OOSTENDE', 'D.T.O')
]

def clean_names(raw_names):

    clean_name_pairs = []

    remove_characters = "|*:()/"

    dba_variants =["d.b.a", "dba.","D.B.A.", "d-b-a", "D.B.A", "D. B. A.", "DBA.", "DBA"]

    for n in raw_names:

        for ch in remove_characters:
            n = n.replace(ch ,'')

        n = n.replace(" - ","")  # another string that serve no purpose
        n = n.replace("_"," ")   # replace underscore with space
        n = n.replace("FB", "F/B")  # put the /exception case back into the string

        for v in dba_variants:
            n = n.replace(v, "|")  # replace dba variant with | as delimiter

        name_pairs = n.split("|")
        name_pairs = [x.rstrip("., ").lstrip() for x in name_pairs] # strip trailing comma,dot and spaces(leading too)

        # add empty None if has no dba name
        if len(name_pairs) == 1:
            name_pairs.append(None)

        clean_name_pairs.append(tuple(name_pairs))

    return clean_name_pairs

# write your code here
if __name__ == "__main__":
#    print(clean_names(RAW_NAMES))
#    print(CLEANED_NAME_PAIRS)
    assert clean_names(RAW_NAMES) == CLEANED_NAME_PAIRS
