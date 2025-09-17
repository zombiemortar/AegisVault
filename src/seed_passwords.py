import argparse
import sys
import os
from typing import List

from database import init_db, store_password, get_total_stored_passwords, get_all_stored_urls, get_app_data_dir
from encryption import encrypt_data, decrypt_data  # Import encryption functions instead of generate_key
from password_generator import PasswordGenerator


def generate_unique_websites(desired_count: int, existing_urls: List[str]) -> List[str]:
    """
    Generate a list of unique website hostnames that do not collide with
    existing records in the database. Uses a deterministic seed pattern
    to ensure uniqueness (e.g., seed-001.example.com).
    """
    unique_sites: List[str] = []
    existing_set = set(existing_urls)

    index = 1
    while len(unique_sites) < desired_count:
        hostname = f"seed-{index:03d}.example.com"
        if hostname not in existing_set:
            unique_sites.append(hostname)
        index += 1

    return unique_sites


def seed_passwords(count: int = 50) -> None:
    """
    Seed the credentials table with approximately `count` entries.

    - Generates strong passwords using PasswordGenerator
    - Ensures unique website values to avoid UPSERT collisions
    - Uses deterministic hostnames so reruns add new entries without duplication
    """
    try:
        # Ensure data directory exists and DB/encryption key are initialized
        data_dir = get_app_data_dir()
        print(f"📁 Using data directory: {data_dir}")
        
        init_db()
        # Note: Encryption key is automatically generated when encryption module is imported

        existing_urls = get_all_stored_urls()
        websites = generate_unique_websites(count, existing_urls)

        password_generator = PasswordGenerator()

        created = 0
        for i, site in enumerate(websites, start=1):
            username = f"user{i:03d}@{site}"
            password = password_generator.generate_password(
                length=16,
                include_lowercase=True,
                include_uppercase=True,
                include_digits=True,
                include_symbols=True,
                avoid_similar=True,
                avoid_ambiguous=True,
            )

            store_password(site, username, password)
            created += 1

        total = get_total_stored_passwords()
        print(f"✅ Seed complete: created {created} credential(s).")
        print(f"📦 Total active credentials in DB: {total}")
        
    except Exception as e:
        print(f"❌ Error during seeding: {e}")
        raise


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser(description="Seed the Aegis Vault credentials with sample entries")
    parser.add_argument("-n", "--num", type=int, default=50, help="Number of credentials to insert (default: 50)")
    args = parser.parse_args(argv)

    if args.num <= 0:
        print("Nothing to do: --num must be > 0")
        return 0

    try:
        print(f"🌱 Starting to seed {args.num} credentials...")
        seed_passwords(args.num)
        return 0
    except Exception as e:
        print(f"❌ Failed to seed passwords: {e}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))


