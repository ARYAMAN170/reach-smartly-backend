import camelot
import pandas as pd
from typing import List
from app.models.hr_contact import HRContact

def parse_hr_contacts_pdf(pdf_path: str) -> List[HRContact]:
    """
    Extracts HR contact information from a PDF with a grid-like table.
    This version is more robust and does not depend on the PDF's header row.
    """
    hr_contacts = []
    tables = camelot.read_pdf(pdf_path, pages='all', flavor='lattice')

    if not tables:
        return []

    # Define the column names directly to prevent errors
    expected_columns = ['SNo', 'Name', 'Email', 'Title', 'Company']

    for table in tables:
        df = table.df
        # Ensure the table has the right number of columns
        if df.shape[1] != len(expected_columns):
            continue

        # Skip the header row from the PDF file
        df_data = df.iloc[1:]
        # Assign the predefined column names
        df_data.columns = expected_columns

        # Iterate over each data row in the DataFrame
        for index, row in df_data.iterrows():
            try:
                # Direct mapping from columns is now more reliable
                name = str(row['Name']).strip()
                email = str(row['Email']).strip()
                title = str(row['Title']).strip()
                company = str(row['Company']).strip()

                if name and email and title and company:
                    contact = HRContact(
                        Name=name,
                        Email=email,
                        Title=title,
                        Company=company
                    )
                    hr_contacts.append(contact)

            except (KeyError, IndexError, ValueError) as e:
                print(f"Skipping malformed row {index}. Error: {e}")
                continue

    return hr_contacts