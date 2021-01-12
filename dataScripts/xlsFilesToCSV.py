import xlrd
import os
import csv

def conversionNumDept(codeDept):

    if codeDept[-1] == '0':
        codeDept = codeDept[:-1]

        if codeDept[0] == '0':
            codeDept = codeDept[1]

    return codeDept


def main():
    results = []
    resultDepts = []

    for file in sorted(filter(lambda x: x.endswith(".xls") ,os.listdir(os.path.join("data", "RevenusFiscaux")))):
        wb = xlrd.open_workbook(os.path.join("data", "RevenusFiscaux", file))
        started = False
        sheet = wb.sheets()[0]
        dept = conversionNumDept(file.replace(".xls",""))
        
        for line in range(sheet.nrows):

            lineData = sheet.row(line)

            if lineData[2].value == "Commune":
                started = True
                continue

            if lineData[4].value == "Total":
                if not started:
                    resultDepts.append({
                        "code_departement": dept,
                        "nom_departement": lineData[3].value,
                        "nbFoyerFiscaux": lineData[5].value if lineData[5].value != "n.c." else "",
                        "revFiscalRefFoyers": lineData[6].value if lineData[6].value != "n.c." else "",
                        "impotNet": lineData[7].value if lineData[7].value != "n.c." else "",
                        "nbFoyersImposes": lineData[8].value if lineData[8].value != "n.c." else "",
                        "revFiscalRefFoyersImpos": lineData[9].value if lineData[9].value != "n.c." else ""
                    })
                else:
                    results.append({
                        "code_ville": dept + lineData[2].value,
                        "nom_commune": lineData[3].value,
                        "nbFoyerFiscaux": lineData[5].value if lineData[5].value != "n.c." else "",
                        "revFiscalRefFoyers": lineData[6].value if lineData[6].value != "n.c." else "",
                        "impotNet": lineData[7].value if lineData[7].value != "n.c." else "",
                        "nbFoyersImposes": lineData[8].value if lineData[8].value != "n.c." else "",
                        "revFiscalRefFoyersImpos": lineData[9].value if lineData[9].value != "n.c." else ""
                    })

    with open(os.path.join("data", "revenuFiscauxDepts.csv"), "w+") as f:
        fields = ["code_departement", "nom_departement", "nbFoyerFiscaux", "revFiscalRefFoyers", "impotNet", "nbFoyersImposes", "revFiscalRefFoyersImpos"]
        writer = csv.DictWriter(f, fields)
        writer.writeheader()
        writer.writerows(resultDepts)

    with open(os.path.join("data", "revenuFiscauxCommunes.csv"), "w+") as f:
        fields = ["code_ville", "nom_commune", "nbFoyerFiscaux", "revFiscalRefFoyers", "impotNet", "nbFoyersImposes", "revFiscalRefFoyersImpos"]
        writer = csv.DictWriter(f, fields)
        writer.writeheader()
        writer.writerows(results)

if __name__ == "__main__":
    main()
