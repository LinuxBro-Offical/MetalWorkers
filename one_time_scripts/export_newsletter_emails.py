import sys
from pathlib import Path
import csv

# Add the project root to sys.path to ensure modules can be imported
project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

from sqlmodel import Session, create_engine, select
from newsletter.models import Newsletter
from settings.settings import DATABASE_URL


def export_emails_to_csv(output_file: str = "newsletter_emails.csv"):
    engine = create_engine(DATABASE_URL)

    with Session(engine) as session:
        emails = session.exec(select(Newsletter)).all()

        if not emails:
            print("No newsletter emails found to export.")
            return

        with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = ["id", "email", "created_date"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for email_record in emails:
                writer.writerow({
                    "id": email_record.id,
                    "email": email_record.email,
                    "created_date": email_record.created_date.isoformat()
                })
        print(f"Successfully exported {len(emails)} emails to {output_file}")


if __name__ == "__main__":
    # You can change the output file name if needed
    export_emails_to_csv("newsletter_emails.csv") 