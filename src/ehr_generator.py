
import argparse
from pathlib import Path

import numpy as np
import pandas as pd


DEPARTMENTS = {
    "Registration": "Front Desk",
    "Triage": "Triage",
    "Doctor Consultation": "Emergency Medicine",
    "Lab Test": "Laboratory",
    "X-Ray": "Radiology",
    "Treatment": "Treatment Area",
    "Observation": "Observation Unit",
    "Discharge": "Front Desk",
    "Admission": "Inpatient Admissions",
}


def generate_event_log(number_of_visits=500, seed=42):
    if number_of_visits < 1:
        raise ValueError("Number of visits must be at least 1")

    rng = np.random.default_rng(seed)
    events = []

    for visit in range(1, number_of_visits + 1):
        case_id = f"CASE{visit:06d}"
        patient_id = (
            f"PAT{rng.integers(1, max(2, number_of_visits // 2) + 1):06d}"
        )

        current_time = pd.Timestamp("2026-01-01") + pd.Timedelta(
            minutes=int(rng.integers(0, 90 * 24 * 60))
        )

        journey = [
            "Registration",
            "Triage",
            "Doctor Consultation",
        ]

        if rng.random() < 0.50:
            journey.append("Lab Test")

        if rng.random() < 0.35:
            journey.append("X-Ray")

        if rng.random() < 0.15:
            journey.extend(["Triage", "Doctor Consultation"])

        journey.append("Treatment")

        if rng.random() < 0.25:
            journey.append("Observation")

        journey.append(
            "Admission" if rng.random() < 0.12 else "Discharge"
        )

        for sequence, activity in enumerate(journey, start=1):
            if sequence > 1:
                current_time += pd.Timedelta(
                    minutes=int(rng.integers(5, 61))
                )

            events.append({
                "case_id": case_id,
                "patient_id": patient_id,
                "event_id": f"{case_id}-EVT{sequence:02d}",
                "activity": activity,
                "timestamp": current_time,
                "department": DEPARTMENTS[activity],
                "event_sequence": sequence,
                "is_repeat": (
                    activity == "Triage"
                    and journey[:sequence].count("Triage") > 1
                ),
            })

    df = pd.DataFrame(events)
    df = df.sort_values(
        ["case_id", "timestamp", "event_sequence"]
    ).reset_index(drop=True)

    return df


def main():
    parser = argparse.ArgumentParser(
        description="Generate a synthetic emergency-room event log."
    )
    parser.add_argument("--visits", type=int, default=500)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument(
        "--output",
        default="data/raw/er_event_log.csv",
    )
    args = parser.parse_args()

    df = generate_event_log(args.visits, args.seed)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df["timestamp"] = df["timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S")
    df.to_csv(output_path, index=False)

    print(f"Generated events: {len(df)}")
    print(f"Patient visits: {df['case_id'].nunique()}")
    print(f"Unique patients: {df['patient_id'].nunique()}")
    print(f"Saved to: {output_path}")
    print("\nSample events:")
    print(df.head(10).to_string(index=False))


if __name__ == "__main__":
    main()