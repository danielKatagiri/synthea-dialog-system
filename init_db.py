from synthea_dialog_system.database.populate_conditions import run_conditions
from synthea_dialog_system.database.populate_patients import run_patients

if __name__ == "__main__":
    run_patients()
    run_conditions()
