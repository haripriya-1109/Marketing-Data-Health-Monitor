def get_issue_severity(record):

    high_priority = [
        "missing_email",
        "invalid_email",
        "duplicate_email"
    ]

    medium_priority = [
        "missing_company_name",
        "missing_campaign_name",
        "company_inconsistent"
    ]

    low_priority = [
        "missing_job_title"
    ]

    for column in high_priority:
        if column in record and record[column] == 1:
            return "High"

    for column in medium_priority:
        if column in record and record[column] == 1:
            return "Medium"

    for column in low_priority:
        if column in record and record[column] == 1:
            return "Low"

    return "No Issue"



def get_all_issue_details(record):

    issue_details = {
        "missing_email": (
            "Missing Email",
            "Contact cannot be reached through email."
        ),
        "invalid_email": (
            "Invalid Email",
            "Email format is invalid and may prevent delivery."
        ),
        "duplicate_email": (
            "Duplicate Email",
            "The email appears in multiple records."
        ),
        "missing_company_name": (
            "Missing Company",
            "Company-level reporting may be incomplete."
        ),
        "missing_campaign_name": (
            "Missing Campaign",
            "Campaign attribution may be incomplete."
        ),
        "missing_job_title": (
            "Missing Job Title",
            "Role-based segmentation may be limited."
        ),
        "company_inconsistent": (
            "Company Name Inconsistency",
            "Company naming variations may fragment reporting."
        )
    }

    detected_issues = []

    for column, details in issue_details.items():

        if column in record and record[column] == 1:
            detected_issues.append(details)

    return detected_issues


def get_recommended_action(issue_type):

    actions = {
        "Missing Email": "Enrich the record with a verified email address.",
        "Invalid Email": "Validate and correct the email address.",
        "Duplicate Email": "Review duplicate records and apply deduplication rules.",
        "Missing Company": "Enrich the record with the correct company name.",
        "Missing Campaign": "Identify and populate the correct campaign.",
        "Missing Job Title": "Enrich the record with the contact's job title.",
        "Company Name Inconsistency": "Standardize the company name using a canonical naming convention."
    }

    return actions.get(issue_type, "Review the record manually.")