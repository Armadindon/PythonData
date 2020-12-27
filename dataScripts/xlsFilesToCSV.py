import xlrd
import os
import csv

def conversionNumDept(codeDept):

    if codeDept[-1] == '0':
        codeDept = codeDept[:-1]

        if codeDept[0] == '0':
            codeDept = codeDept[1]

    return codeDept



results = []
resultDepts = []

for file in sorted(filter(lambda x: x.endswith(".xls") ,os.listdir(os.path.join(os.getcwd(), "data", "RevenusFiscaux")))):
    wb = xlrd.open_workbook(os.path.join(os.getcwd(), "data", "RevenusFiscaux", file))
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
                    "nbFoyerFiscaux": lineData[5].value,
                    "revFiscalRefFoyers": lineData[6].value,
                    "impotNet": lineData[7].value,
                    "nbFoyersImposes": lineData[8].value,
                    "revFiscalRefFoyersImpos": lineData[9].value
                })
            else:
                results.append({
                    "code_ville": dept + lineData[2].value,
                    "nom_commune": lineData[3].value,
                    "nbFoyerFiscaux": lineData[5].value,
                    "revFiscalRefFoyers": lineData[6].value,
                    "impotNet": lineData[7].value,
                    "nbFoyersImposes": lineData[8].value,
                    "revFiscalRefFoyersImpos": lineData[9].value
                })

with open(os.path.join(os.getcwd(), "data", "revenuFiscauxDepts.csv"), "w+") as f:
    fields = ["code_departement", "nom_departement", "nbFoyerFiscaux", "revFiscalRefFoyers", "impotNet", "nbFoyersImposes", "revFiscalRefFoyersImpos"]
    writer = csv.DictWriter(f, fields)
    writer.writeheader()
    writer.writerows(resultDepts)

with open(os.path.join(os.getcwd(), "data", "revenuFiscauxCommunes.csv"), "w+") as f:
    fields = ["code_ville", "nom_commune", "nbFoyerFiscaux", "revFiscalRefFoyers", "impotNet", "nbFoyersImposes", "revFiscalRefFoyersImpos"]
    writer = csv.DictWriter(f, fields)
    writer.writeheader()
    writer.writerows(results)
