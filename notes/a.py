import polars as pl

# Example DataFrame
df = pl.DataFrame({"size": [5, 3, 4], "content": ["hello", "cat", "dogs"]})

# Check if size equals length of content in all rows
all_match = (df["size"] == df["content"].str.len_chars()).all()

print(all_match)


def classify_content(value: str) -> str:
    if value.isdigit():
        return "numeric"
    elif value.isalpha():
        return "alpha"
    elif "@" in value:
        return "email"
    elif len(value) > 10:
        return "long"
    else:
        return "other"


df = pl.DataFrame(
    {"content": ["12345", "hello", "test@example.com", "short", "averylongstring"]}
)

df = df.with_columns([df["content"].map_elements(classify_content).alias("type")])

df = df.with_columns(
    [
        pl.when(pl.col("content").str.contains(r"^\d+$"))
        .then(pl.lit("numeric"))
        .when(pl.col("content").str.contains(r"^[a-zA-Z]+$"))
        .then(pl.lit("alpha"))
        .when(pl.col("content").str.contains(r"@"))
        .then(pl.lit("email"))
        .when(pl.col("content").str.len_chars() > 10)
        .then(pl.lit("long"))
        .otherwise(pl.lit("other"))
        .alias("type")
    ]
)
print(df)


df = pl.DataFrame(
    {
        "content": [
            "valid_entry",
            "also_valid",
            "broken__entry_here",
            "___broken",
            "still__ok",
            "no_issues",
        ]
    }
)

# Filter out rows with 3 or more underscores
df_clean = df.filter(~pl.col("content").str.contains(r"(.*_){3,}"))

print(df_clean)


df = pl.DataFrame({"x": [1, 2, 3, 4], "y": [10, 20, 30, 25]})
df.plot.scatter(x="x", y="y")
