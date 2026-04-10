import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# ─────────────────────────────────────────
# STEP 1: AUTHENTICATE WITH GOOGLE
# ─────────────────────────────────────────

# Define the scopes — what permissions your script needs
scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Load your credentials from the downloaded JSON file
creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)

# Connect to Google Sheets
client = gspread.authorize(creds)

print("Authenticated with Google successfully.")


# ─────────────────────────────────────────
# STEP 2: OPEN YOUR GOOGLE SHEET
# Replace the string below with YOUR Sheet ID from the URL
# ─────────────────────────────────────────
SHEET_ID = "1gih35UZeVQIiImziEZ17Vd7Z7q_YSugsJ2XS8JVGlzU"

spreadsheet = client.open_by_key(SHEET_ID)
worksheet = spreadsheet.sheet1  # Uses the first tab

print("Google Sheet opened successfully.")


# ─────────────────────────────────────────
# STEP 3: LOAD YOUR CLEAN DATA
# ─────────────────────────────────────────
df = pd.read_csv("books_clean.csv")

# Replace NaN values with empty string — Sheets doesn't accept NaN
df = df.fillna("")

print(f"Loaded {len(df)} rows of clean data.")


# ─────────────────────────────────────────
# STEP 4: CLEAR THE SHEET AND WRITE FRESH DATA
# ─────────────────────────────────────────
worksheet.clear()  # Wipe any existing content first

# Convert the dataframe to a list of lists (rows)
# First row = headers, remaining rows = data
headers = df.columns.tolist()
rows = df.values.tolist()

all_data = [headers] + rows

# Write everything in one call — much faster than row by row
worksheet.update(all_data)

print(f"Written {len(rows)} rows + header to Google Sheets.")
print("✅ Done. Open your Google Sheet to verify the data.")