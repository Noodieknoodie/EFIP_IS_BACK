# Application settings
APP_NAME = "Retirement Planning Tool"
VERSION = "1.0.0"

# Client data structure
CLIENT_SCHEMA = {
    "personal_info": [
        "client_first_name",
        "client_last_name",
        "client_dob",
        "is_retired",
        "retirement_age",
        "spouse_first_name",
        "spouse_last_name",
        "spouse_dob",
        "spouse_is_retired",
        "spouse_retirement_age"
    ],
    "asset_categories": [
        "taxable",
        "tax_deferred",
        "tax_free",
        "personal_property"
    ],
    # Structure for individual assets
    "asset_properties": [
        "name",
        "value",
        "is_managed",
        "include_in_nest_egg"
    ],
    "income_sources": [
        "salary",
        "pension",
        "social_security",
        "rental_income",
        "other_income"
    ],
    "expense_categories": [
        "essential",
        "discretionary",
        "healthcare",
        "long_term_care"
    ]
}

# Default asset categories
DEFAULT_ASSET_CATEGORIES = {
    "taxable": "Taxable Accounts",
    "tax_deferred": "Tax-Deferred Accounts",
    "tax_free": "Tax-Free Accounts",
    "personal_property": "Personal Property"
}
