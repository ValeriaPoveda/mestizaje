import json
import os
import csv
import unittest

DATASET_PATH = os.path.join("data", "dataset.json")
OUTPUT_CSV = "missing_paths_report.csv"

class TestImagePaths(unittest.TestCase):

    def test_artwork_paths_exist(self):

        with open(DATASET_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)

        missing = []
        rows = []

        for country in data["countries"]:
            for artist in country["artists"]:
                for art in artist["artworks"]:

                    rel_path = art["path"]  
                    full_path = os.path.join(".", rel_path)

                    country_folder = rel_path.split("/")[1]
                    artist_folder  = rel_path.split("/")[2]
                    file_name      = rel_path.split("/")[-1]

                    country_exists = os.path.isdir(os.path.join("artworks", country_folder))
                    artist_exists  = os.path.isdir(os.path.join("artworks", country_folder, artist_folder))
                    file_exists    = os.path.isfile(full_path)

                    if not file_exists:
                        missing.append(full_path)

                        rows.append({
                            "expected_full_path": full_path,
                            "country_folder": country_folder,
                            "country_folder_exists": country_exists,
                            "artist_folder": artist_folder,
                            "artist_folder_exists": artist_exists,
                            "file_name": file_name,
                            "file_exists": file_exists
                        })

        # Write CSV report
        with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)

        print("\n===== PATH CHECK SUMMARY =====")
        print(f"Missing files: {len(missing)}")
        print(f"CSV report saved to: {OUTPUT_CSV}\n")

        if missing:
            print("Open missing_paths_report.csv for details.\n")

        self.assertEqual(len(missing), 0, "Some artwork paths do NOT exist.")

if __name__ == "__main__":
    unittest.main()
