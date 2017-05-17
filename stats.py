import argparse
import requests
from datetime import datetime
import pandas as pd
from dateutil import parser
from bs4 import BeautifulSoup

URLS = {'base': r'http://ecss2006.com/topos/kik/Was_Zuletzt_Vergeben.asp',
        # this also appears to have all the site ids
        'patients': r'http://ecss2006.com/topos/kik/KF_Display_Patients_Per_Month.asp',
        'totals': r'http://ecss2006.com/topos/kik/KF_Display_Farmaka_Per_Month.asp',
        }

BASE_TABLE_COLS = ['SiteID', 'Num', 'Drug', 'ExpirationDate', 'PatientID', 'DispensationDate']

KNOWN_SITES = {5551: 'HERCULES',
               5532: 'N. CHRANIS',
               5543: 'NIREAS',
               5514: 'OREFEAS SKOTINAS',
               5547: 'STONE',
               4623: 'PAIONIA',
               4531: 'STATE HOSPITAL KATERINI',
               5519: 'TRANSFORMATION'
               }


def get_all_site_ids():
    patient_pg_content = requests.get(URLS['patients'])
    soup = BeautifulSoup(patient_pg_content.text)
    all_site_ids = set()
    for tr in soup.findAll('tr'):
        try:
            possible_id = tr.findAll('td')[2].text
            all_site_ids.add(int(possible_id))
        except ValueError:
            print('Discarding non-int value {}'.format(possible_id))
        except IndexError:
            print('No tds found in tr: {}'.format(tr))
    print('Found {} site ids'.format(len(all_site_ids)))
    return all_site_ids


def get_drugs_for_site(site_id):
    print('Parsing drug records for site_id {}'.format(site_id))
    site_pg_content = requests.get(URLS['base'], params={'myID': site_id})
    soup = BeautifulSoup(site_pg_content.text)
    rows = []
    for tr in soup.findAll('tr'):
        row_vals = [site_id] + [td.text for td in tr.findAll('td')]
        try:
            assert len(row_vals) == len(BASE_TABLE_COLS)
            assert row_vals[4][:2] == "ID"
            row_vals[5] = parser.parse(row_vals[5], dayfirst=True).date()
            rows.append(row_vals)
        except AssertionError:
            print('Discarding row: {}'.format(row_vals))

    print('Parsed {} drug records for site_id {}'.format(len(rows), site_id))
    return pd.DataFrame(rows, columns=BASE_TABLE_COLS)


def get_drugs_for_all_sites(site_ids=None, outfile=None):
    if not site_ids:
        site_ids = get_all_site_ids()
    vals = [get_drugs_for_site(sid) for sid in site_ids]
    all_vals = pd.concat(vals)
    if outfile:
        print('Writing output csv to {}'.format(outfile))
        all_vals.to_csv(outfile)
    else:
        print(all_vals)

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-o', '--outfile', default='social_pharma_{}.csv'.format(datetime.today().date().isoformat()))
    argparser.add_argument('-s', '--site_ids', type=int, nargs='*')
    args = argparser.parse_args()

    get_drugs_for_all_sites(args.site_ids, args.outfile)
