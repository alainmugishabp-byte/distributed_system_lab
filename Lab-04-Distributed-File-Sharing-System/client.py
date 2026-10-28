import json
import os
import urllib.request
import urllib.error
from urllib.parse import urlencode

COORDINATOR = "http://localhost:8000"

DEPARTMENTS = {
    "1": "IT",
    "2": "FINANCE",
    "3": "ADMIN",
}


def choose_department():
    print("\nSelect department:")
    print("1. IT")
    print("2. Finance")
    print("3. Administration")

    choice = input("Enter choice: ").strip()

    if choice not in DEPARTMENTS:
        print("Invalid department.")
        return None

    return DEPARTMENTS[choice]


def show_error(error):
    if isinstance(error, urllib.error.HTTPError):
        try:
            details = error.read().decode("utf-8")
            print(f"Request failed ({error.code}): {details}")
        except Exception:
            print(f"Request failed with HTTP status {error.code}.")
    else:
        print("Could not connect to the coordinator.")
        print("Details:", error)


def upload_file():
    department = choose_department()
    if not department:
        return

    filepath = input("Enter the full path of the file: ").strip()
    filepath = filepath.strip('"')

    if not os.path.isfile(filepath):
        print("File does not exist.")
        return

    filename = os.path.basename(filepath)

    if os.path.getsize(filepath) == 0:
        print("The file is empty; choose a non-empty file.")
        return

    if os.path.getsize(filepath) > 10 * 1024 * 1024:
        print("Maximum file size is 10 MB.")
        return

    with open(filepath, "rb") as file:
        content = file.read()

    query = urlencode({
        "department": department,
        "filename": filename,
    })

    request = urllib.request.Request(
        f"{COORDINATOR}/upload?{query}",
        data=content,
        headers={"Content-Type": "application/octet-stream"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            result = json.loads(response.read().decode("utf-8"))
            print("\nUpload successful!")
            print(json.dumps(result, indent=2))
    except (urllib.error.URLError, TimeoutError, OSError) as error:
        show_error(error)


def list_files():
    department = choose_department()
    if not department:
        return

    query = urlencode({"department": department})
    url = f"{COORDINATOR}/files?{query}"

    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            result = json.loads(response.read().decode("utf-8"))

        print(f"\nFiles stored for {department}:")
        files = result.get("files", [])

        if not files:
            print("No files found.")
        else:
            for filename in files:
                print("-", filename)

    except (urllib.error.URLError, TimeoutError, OSError) as error:
        show_error(error)


def download_file():
    department = choose_department()
    if not department:
        return

    filename = input("Enter the filename to download: ").strip()

    if (
        not filename
        or filename in (".", "..")
        or "/" in filename
        or "\\" in filename
    ):
        print("Enter a valid filename without a directory path.")
        return

    query = urlencode({
        "department": department,
        "filename": filename,
    })

    url = f"{COORDINATOR}/download?{query}"

    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            content = response.read()

        os.makedirs("downloads", exist_ok=True)
        output_path = os.path.join("downloads", filename)

        with open(output_path, "wb") as file:
            file.write(content)

        print("Download successful!")
        print("Saved to:", os.path.abspath(output_path))

    except (urllib.error.URLError, TimeoutError, OSError) as error:
        show_error(error)


def main():
    while True:
        print("\n=== DISTRIBUTED FILE SHARING SYSTEM ===")
        print("1. Upload file")
        print("2. List files")
        print("3. Download file")
        print("4. Exit")

        choice = input("Select an option: ").strip()

        if choice == "1":
            upload_file()
        elif choice == "2":
            list_files()
        elif choice == "3":
            download_file()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
