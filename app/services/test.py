from app.models.hr_contact import HRContact
from app.services.email_service import generate_outreach_email

def test_generate_email():
    # Mock HR Contact Data matching the schema
    hr_contact = HRContact(
        Name="aryaman singh",
        Email="jane.doe@techsolutions.com",
        Title="HR Manager",
        Company="Tech Solutions Inc."
    )

    # User profile summary
    user_summary = (
        "A passionate Software Developer with 3+ years of experience specializing in AI and Python development. "
        "Proficient in building scalable full-stack applications and collaborating with cross-functional teams."
    )

    # Job Seeker's Name
    user_name = "John Smith"

    print("Generating Outreach Email...\n")
    email_content = generate_outreach_email(hr_contact, user_summary, user_name)
    print(email_content)


if __name__ == "__main__":
    test_generate_email()
