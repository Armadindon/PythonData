"""
Script permettant la conversion de fichier xls (Excel) vers csv
pour la lecture avec la librairie pandas
"""
import os
import csv
import xlrd

def conversion_num_dept(code_dept):
    """
    Convertit un département au bon format

    Args:
        code_dept (str): Code du département à convertir.

    Returns:
        code_dept (str): Code département au bon format.
    """
    if code_dept[-1] == '0':
        code_dept = code_dept[:-1]

        if code_dept[0] == '0':
            code_dept = code_dept[1]

    return code_dept


def main():
    """
    Fonction Principale
    """
    results = []
    result_depts = []

    for file in sorted(filter(lambda x: x.endswith(".xls"),
                              os.listdir(os.path.join("data", "RevenusFiscaux")))):
        workbook = xlrd.open_workbook(os.path.join("data", "RevenusFiscaux", file))
        started = False
        sheet = workbook.sheets()[0]
        dept = conversion_num_dept(file.replace(".xls", ""))

        for line in range(sheet.nrows):

            line_data = sheet.row(line)

            if line_data[2].value == "Commune":
                started = True
                continue

            if line_data[4].value == "Total":
                if not started:
                    result_depts.append({
                        "code_departement": dept,
                        "nom_departement": line_data[3].value,
                        "nbFoyerFiscaux": line_data[5].value
                        if line_data[5].value != "n.c." else "",
                        "revFiscalRefFoyers": line_data[6].value
                        if line_data[6].value != "n.c." else "",
                        "impotNet": line_data[7].value
                        if line_data[7].value != "n.c." else "",
                        "nbFoyersImposes": line_data[8].value
                        if line_data[8].value != "n.c." else "",
                        "revFiscalRefFoyersImpos": line_data[9].value
                        if line_data[9].value != "n.c." else ""
                    })
                else:
                    results.append({
                        "code_ville": dept + line_data[2].value,
                        "nom_commune": line_data[3].value,
                        "nbFoyerFiscaux": line_data[5].value
                        if line_data[5].value != "n.c." else "",
                        "revFiscalRefFoyers": line_data[6].value
                        if line_data[6].value != "n.c." else "",
                        "impotNet": line_data[7].value
                        if line_data[7].value != "n.c." else "",
                        "nbFoyersImposes": line_data[8].value
                        if line_data[8].value != "n.c." else "",
                        "revFiscalRefFoyersImpos": line_data[9].value
                        if line_data[9].value != "n.c." else ""
                    })

    with open(os.path.join("data", "revenuFiscauxDepts.csv"), "w+", encoding='utf-8') as file:
        fields = ["code_departement",
                  "nom_departement", "nbFoyerFiscaux",
                  "revFiscalRefFoyers", "impotNet",
                  "nbFoyersImposes", "revFiscalRefFoyersImpos"]
        writer = csv.DictWriter(file, fields)
        writer.writeheader()
        writer.writerows(result_depts)

    with open(os.path.join("data", "revenuFiscauxCommunes.csv"),
              "w+", encoding='utf-8') as file:
        fields = ["code_ville", "nom_commune",
                  "nbFoyerFiscaux", "revFiscalRefFoyers",
                  "impotNet", "nbFoyersImposes",
                  "revFiscalRefFoyersImpos"]
        writer = csv.DictWriter(file, fields)
        writer.writeheader()
        writer.writerows(results)


if __name__ == "__main__":
    main()
