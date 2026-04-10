import pandas as pd

# ─────────────────────────────────────────
# STEP 1: LOAD THE RAW DATA
# ─────────────────────────────────────────
df = pd.read_csv("books_data.csv", encoding="utf-8")

print("=== RAW DATA OVERVIEW ===")
print(f"Shape: {df.shape}")          # (rows, columns)
print(f"\nColumn types:\n{df.dtypes}")
print(f"\nMissing values:\n{df.isnull().sum()}")
print(f"\nFirst 3 rows:\n{df.head(3)}")


# ─────────────────────────────────────────
# STEP 2: CLEAN COLUMN NAMES
# Lowercase all column headers and strip any accidental spaces
# ─────────────────────────────────────────
df.columns = df.columns.str.strip().str.lower()
print(f"\nCleaned column names: {list(df.columns)}")


# ─────────────────────────────────────────
# STEP 3: STRIP WHITESPACE FROM TEXT COLUMNS
# Raw scraped text often has leading/trailing spaces
# ─────────────────────────────────────────
text_columns = ["title", "category", "rating", "availability", "description"]

for col in text_columns:
    df[col] = df[col].str.strip()

print("\nWhitespace stripped from text columns.")


# ─────────────────────────────────────────
# STEP 4: CLEAN AND CONVERT THE PRICE COLUMN
# Price comes in as "£12.99" — strip the symbol and convert to float
# ─────────────────────────────────────────
df["price"] = df["price"].str.replace("£", "", regex=False)
df["price"] = df["price"].str.replace("Â", "", regex=False)  # Sometimes appears with encoding issues
df["price"] = df["price"].str.strip()
df["price"] = pd.to_numeric(df["price"], errors="coerce")  # Convert to number; invalid values become NaN

print(f"\nPrice column after cleaning (sample): {df['price'].head().tolist()}")
print(f"Price column type: {df['price'].dtype}")


# ─────────────────────────────────────────
# STEP 5: NORMALISE THE RATING COLUMN
# Rating comes as words: "One", "Two", "Three", "Four", "Five"
# Convert to numbers: 1, 2, 3, 4, 5
# ─────────────────────────────────────────
rating_map = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

df["rating"] = df["rating"].map(rating_map)

print(f"\nRating column after normalising (sample): {df['rating'].head().tolist()}")


# ─────────────────────────────────────────
# STEP 6: HANDLE MISSING VALUES
# Fill missing descriptions with a clear placeholder
# Drop rows where critical fields (title, price, url) are missing
# ─────────────────────────────────────────
df["description"] = df["description"].fillna("No description available")

rows_before = len(df)
df = df.dropna(subset=["title", "price", "url"])
rows_after = len(df)

print(f"\nDropped {rows_before - rows_after} rows with missing critical fields.")


# ─────────────────────────────────────────
# STEP 7: REMOVE DUPLICATE ROWS
# Duplicates can sneak in when pagination overlaps
# ─────────────────────────────────────────
dupes_before = len(df)
df = df.drop_duplicates(subset=["url"])  # URL is the unique identifier for each book
dupes_after = len(df)

print(f"Removed {dupes_before - dupes_after} duplicate rows.")


# ─────────────────────────────────────────
# STEP 8: VALIDATE REQUIRED FIELDS
# Check that no critical column is empty after all cleaning
# ─────────────────────────────────────────
print("\n=== POST-CLEANING VALIDATION ===")
print(f"Remaining missing values:\n{df.isnull().sum()}")
print(f"Final dataset shape: {df.shape}")
print(f"\nSample of clean data:\n{df.head(3)}")


# ─────────────────────────────────────────
# STEP 9: REORDER COLUMNS FOR CLEAN PRESENTATION
# ─────────────────────────────────────────
df = df[["title", "category", "rating", "price", "availability", "description", "url"]]


# ─────────────────────────────────────────
# STEP 10: EXPORT TO CLEAN CSV
# ─────────────────────────────────────────
df.to_csv("books_clean.csv", index=False, encoding="utf-8")
print("\nExported: books_clean.csv")


# ─────────────────────────────────────────
# STEP 11: EXPORT TO JSON
# orient="records" means each row becomes one JSON object
# indent=2 makes it human-readable
# ─────────────────────────────────────────
df.to_json("books_clean.json", orient="records", indent=2, force_ascii=False)
print("Exported: books_clean.json")


print("\n✅ Cleaning complete.")