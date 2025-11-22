from helpers import (
    _kill_chrome,
    _generate_resume,
    _generate_cover_letter,
    _get_information,
    _send_email               # NEW – import the mail helper
)
from classes.Providers.Indeed import Indeed
from classes.Database import Database
from termcolor import colored
import os

def main() -> None:
    _kill_chrome()
    db = Database()
    db.create_table()

    me = _get_information()

    # Define WFH-focused queries
    job_queries = [
        "Freelance Writer",
        "Data Entry",
        "Academic Writer",
        "Content Writer",
        "Copywriter",
        "Ghostwriter",
        "Typing",
        "Assignment Helper"
    ]
    place_query = "Remote"

    all_jobs = []

    for query in job_queries:
        print(colored(f"\n🔎  Searching for: {query} ({place_query})", "magenta"))
        try:
            indeed = Indeed(db=db,
                            job_query=query,
                            place_query=place_query)
            indeed.search(advanced=True)
            # Collect jobs from this search instance
            # Note: indeed.jobs is populated by search()
            all_jobs.extend(indeed.jobs)
        except Exception as e:
            print(colored(f"⚠️  Search failed for '{query}': {e}", "red"))

    # Get all jobs from DB (deduplicated by ID in DB)
    jobs = db.get_jobs()
    print(f"🔍  Scraped {len(jobs)} jobs")

    # 1. build résumé once
    resume_path = _generate_resume(info=me)
    if not resume_path or not os.path.exists(resume_path):
        print(colored("❌  Resume not found – stopping pipeline.", "red"))
        return

    # 2. apply + e-mail loop
    for idx, job in enumerate(jobs, 1):
        print(colored(f"\n[{idx}/{len(jobs)}]  Applying to ::  {job.get('title', 'N/A')}", "cyan"))

        cover_letter_path = _generate_cover_letter(job["job_description_markdown"], me)
        if not cover_letter_path:
            print(colored("⚠️  Cover-letter failed – skipping.", "yellow"))
            continue

        # ---- Indeed apply-button click (optional) ----
        try:
            indeed.apply(job["id"], cover_letter_path, resume_path)
        except Exception as e:
            print(colored(f"⚠️  Indeed apply-button blocked :: {e}", "yellow"))

        # ---- ALWAYS send e-mail (HR address from job page or fallback) ----
        hr_email = job.get("hr_email") or "hr@example.com"   # scrape or fallback
        mail_subj = f"Application for {job.get('title', 'Software Engineer')}"
        _send_email(hr_email, mail_subj, cover_letter_path, resume_path)

    print(colored("\n✅  Pipeline finished – all applications mailed.", "green"))

if __name__ == "__main__":
    main()
