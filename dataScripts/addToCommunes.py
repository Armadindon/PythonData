# -*- coding: utf-8 -*-

import os
from csv import writer

def append_missing_cities(file, city):
    with open(file, encoding='utf-8', mode='a+') as write_csv:
        csv_writer = writer(write_csv)
        csv_writer.writerow(city)

def main():
    Marseille=[13055,'MARSEILLE',13000,'MARSEILLE','',43.2755155435,5.42681101081,210,'','Marseille','Marseille',13,'Bouches-du-Rhône',93,'Provence-Alpes-Côte d\'Azur'
    ]
    Lyon=[69123,'LYON',69000,'LYON','',45.7699284397,4.82922464978,381,'','Lyon','Lyon',69,'Rhône',84,'Auvergne-Rhône-Alpes']
    Paris=[75056,'PARIS',75000,'PARIS','',48.8626304852,2.33629344655,101,'','Paris','Paris',75,'Paris',11,'Île-de-France']

    append_missing_cities(os.path.join('data', 'communes.csv'), Marseille)
    append_missing_cities(os.path.join('data', 'communes.csv'), Lyon)
    append_missing_cities(os.path.join('data', 'communes.csv'), Paris)

if __name__ == "__main__":
    main()