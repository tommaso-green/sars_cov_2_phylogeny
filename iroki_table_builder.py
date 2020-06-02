from Bio import SeqIO


def get_dict_of_nations(filename):
    sequences = list(SeqIO.parse(filename, "fasta"))
    offset = 10
    sequences_by_nation = {}
    nations = []
    for sequence in sequences:
        code_start = sequence.description.find("ISL")  # find index where ISL is
        sequence_code = sequence.description[code_start:code_start + offset]  # get substring ISL_XXXXXX
        sequence_nation = sequence.description.split("/")[1]
        if sequence_nation in ['Wuhan', 'Wuhan-Hu-1', 'Shanghai', 'NanChang', 'Fujian', 'Guangdong']:
            sequence_nation = "China"
        if sequence_nation in ['England', 'Wales', 'Scotland']:
            sequence_nation = "UK"
        if sequence_nation not in nations:
            nations.append(sequence_nation)
        sequences_by_nation[sequence_code] = sequence_nation
    print("Found the following %d nations:" % len(nations))
    print(nations)
    return nations, sequences_by_nation


def create_iroki_table():
    nations, sequences_by_nation = get_dict_of_nations("fasta_files/allsequences.fasta")
    nations_by_color = dict.fromkeys(nations)
    lines = ["name\tbranch_color\tnew_name\n"]
    nations_by_color["China"] = "k_red"
    nations_by_color["Colombia"] = "k_yellow"
    nations_by_color["France"] = "royalblue"
    nations_by_color["Italy"] = "r_lightgreen"
    nations_by_color["Germany"] = "k_reddish_orange"
    nations_by_color["Japan"] = "k_violet"
    nations_by_color["Russia"] = "darkmagenta"
    nations_by_color["Spain"] = "palevioletred"
    nations_by_color["UK"] = "darksalmon"
    nations_by_color["USA"] = "r_cadetblue2"
    emojis_by_nation = {"China": "🇨🇳", "Colombia": "🇨🇴", "France": "🇫🇷", "Italy": "🇮🇹", "Germany": "🇩🇪",
                        "Japan": "🇯🇵", "Russia": "🇷🇺", "Spain": "🇪🇸", "UK": "🇬🇧", "USA": "🇺🇸"}
    for element in list(sequences_by_nation.items()):
        sequence = element[0]
        nation = element[1]
        color = nations_by_color[nation]
        lines.append(sequence + "\t" + color + "\t" + sequence + "\n")
    file = open("colormatrix.txt", "w+")
    file.writelines(lines)
    file.close()


create_iroki_table()
