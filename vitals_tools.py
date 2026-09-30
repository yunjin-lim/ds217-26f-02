"""Reusable helpers for summarizing clinic systolic readings."""


def systolic_readings(encounters):
    """TODO: describe what this pulls out of the encounter records."""
    """collect the systolic value of every encounter into one list"""
    # TODO: collect the systolic value of every encounter into one list.
    readings = []
    for encounter in encounters:
        readings.append(encounter["systolic"])
    return readings


def mean_systolic(readings):
    """TODO: describe what this returns, including the empty-list result."""
    """getting the average of systolic values of every encounter"""
    # TODO: return None when there is nothing to average, then sum() / len().
    if not readings:
        return None
    else:
        return sum(readings)/len(readings)


def count_patients(encounters):
    """TODO: describe what this counts."""
    """count the number of dinstinct patients"""
    # TODO: collect the patient IDs and keep only the distinct ones.
    distinct_patient = set()
    for encounter in encounters:
        distinct_patient.add(encounter["patient_id"])
    return len(distinct_patient)


def patients_at_or_above(encounters, cutoff):
    """TODO: describe which patient IDs come back."""
    """print each distinct patient IDs whose systolic value is at or above cutoff
    and need to come back to the clinic for follow-up
    """
    # TODO: keep each patient whose systolic reading is at or above cutoff.
    followup_set = set()
    for encounter in encounters:
        if encounter["systolic"] >= cutoff:
            followup_set.add(encounter["patient_id"])
    return followup_set
   