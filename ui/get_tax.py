import requests
import json


def get_taxid_from_nc(nc_number):
    url = f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=nuccore&id={nc_number}&retmode=json'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        first_key, first_value = next(iter(data['result'].items()))

        # Extract the 'taxid' from the first item
        taxid = data['result'][first_value[0]]['taxid']
        return taxid
    else:
        print(f"Error: Unable to retrieve TaxID for {nc_number}")
        return None


# Replace 'Your_NC_Number' with the actual NC number
# nc_number = 'MW160272'
# taxid = get_taxid_from_nc(nc_number)
#
# if taxid:
#     print(f'TaxID for {nc_number}: {taxid}')
