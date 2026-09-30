#!/usr/bin/env python3
"""Summarize one week of clinic encounters and save the two report files."""

from pathlib import Path


from vitals_tools import (
    count_patients,
    mean_systolic,
    patients_at_or_above,
    systolic_readings,
)

DATA_PATH = Path("data") / "clinic_encounters.csv"
OUTPUT_DIR = Path("output")


def read_encounters(data_path):
    """TODO: describe what one usable encounter looks like.

    A data row is **usable** when all three of these hold:

    1. it splits into exactly three comma-separated fields;
    2. `int()` can read the third field; and
    3. the reading is from 60 to 250 mmHg inclusive. 
    Anything outside that range is a recording error, not a blood pressure.

    Give back two values: the list of usable encounters, and how many data
    rows you skipped. `main()` unpacks them the way the lecture unpacks a
    tuple, with two names on the left of the `=`.
    """
    # TODO: read the rows and skip the header line.
    # TODO: keep a row only when it has three fields, int() can read the
    #       systolic field, and the reading is plausible.
    # TODO: count every other data row as skipped, the blank line included,
    #       and print one line per skipped row so you can see what dropped out.
    # TODO: end with `return encounters, skipped`.

    with open(data_path, "r", encoding="utf-8") as csv_file:
        rows = csv_file.readlines()

        encounters = []
        skipped = 0

        for row in rows[1:]:                      # rows[0] is the header line
            if not row.strip():                   # an export often ends with a blank line
                skipped+= 1
                print("Skipping a blank row.")
                continue
            fields = row.strip().split(",")
            if len(fields) != 3:
                skipped+= 1
                print(f"Skipping a row with {len(fields)} fields: {row.strip()}")
                continue
            patient_id, visit_date, systolic = fields
            try:
                systolic = int(systolic)
            except ValueError as error:
                skipped+= 1
                print(f"Skipping {patient_id}: {error}")
                continue
            else:
                if 60 <= systolic <= 250:  #plausible range
                    encounters.append({
                        "patient_id": patient_id, 
                        "visit_date": visit_date, 
                        "systolic": systolic
                    })
                else:
                    skipped+= 1
                    print(f"Skipping a row of {patient_id}: {systolic} because the systolic value is not plausible")
        return encounters, skipped

def main():
    """TODO: describe the two artifacts this writes."""
    encounters, skipped = read_encounters(DATA_PATH)

    report_path = OUTPUT_DIR/"vitals_report.txt"
    with open(report_path, "w", encoding="utf-8") as output_report:
        output_report.write(f"Usable encounters: {len(encounters)}\n")
        output_report.write(f"Skipped rows: {skipped}\n")
        output_report.write(f"Patients seen: {count_patients(encounters)}\n")
        output_report.write(f"Mean systolic: {mean_systolic(systolic_readings(encounters)):.2f} mmHg\n")
        output_report.write(f"Highest systolic: {max(systolic_readings(encounters))} mmHg\n")
        output_report.write(f"Lowest systolic: {min(systolic_readings(encounters))} mmHg\n")
    # TODO: build the six report lines and write them to output/vitals_report.txt.
    # TODO: read the file back and print it, so you can see what was saved.
    # TODO: choose your follow-up cutoff, then write output/followup_list.txt
    #       with the Cutoff line, the Reason line, and one patient ID per line.

    followup_path = OUTPUT_DIR/"followup_list.txt"
    cutoff = 130
    with open(followup_path, "w", encoding="utf-8") as followup_list:
        followup_list.write(f"Cutoff: {cutoff} mmHg\n")
        followup_list.write(f"Reason: I chose a cutoff of {cutoff}mmHg because readings at or above it fall in stage 1 hypertension or higher, which needs monitoring.\n")
        for patient_id in patients_at_or_above(encounters, cutoff):
            followup_list.write(f"{patient_id}\n")
    

if __name__ == "__main__":
    main()
