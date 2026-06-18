from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd


class HDIMSDataManager:
    """Excel-backed data manager for HDIMS records and analytics."""

    COLUMNS = [
        "Hospital Name",
        "Patient Name",
        "Disease Name",
        "Doctor Name",
    ]

    def __init__(self, file_path: str = "hdims_data.xlsx") -> None:
        self.file_path = Path(file_path)
        self._ensure_storage()

    def _ensure_storage(self) -> None:
        if not self.file_path.exists():
            pd.DataFrame(columns=self.COLUMNS).to_excel(self.file_path, index=False)

    def _load_dataframe(self) -> pd.DataFrame:
        dataframe = pd.read_excel(self.file_path, engine="openpyxl")
        for column in self.COLUMNS:
            if column not in dataframe.columns:
                dataframe[column] = ""
        return dataframe[self.COLUMNS]

    def _save_dataframe(self, dataframe: pd.DataFrame) -> None:
        dataframe.to_excel(self.file_path, index=False)

    def add_record(
        self,
        hospital_name: str,
        patient_name: str,
        disease_name: str,
        doctor_name: str,
    ) -> Dict[str, str]:
        dataframe = self._load_dataframe()
        record = {
            "Hospital Name": hospital_name,
            "Patient Name": patient_name,
            "Disease Name": disease_name,
            "Doctor Name": doctor_name,
        }
        dataframe = pd.concat([dataframe, pd.DataFrame([record])], ignore_index=True)
        self._save_dataframe(dataframe)
        return record

    def get_all_records(self) -> List[Dict[str, str]]:
        dataframe = self._load_dataframe()
        return dataframe.fillna("").to_dict(orient="records")

    def update_record(
        self,
        index: int,
        hospital_name: Optional[str] = None,
        patient_name: Optional[str] = None,
        disease_name: Optional[str] = None,
        doctor_name: Optional[str] = None,
    ) -> bool:
        dataframe = self._load_dataframe()
        if index < 0 or index >= len(dataframe):
            return False

        if hospital_name is not None:
            dataframe.at[index, "Hospital Name"] = hospital_name
        if patient_name is not None:
            dataframe.at[index, "Patient Name"] = patient_name
        if disease_name is not None:
            dataframe.at[index, "Disease Name"] = disease_name
        if doctor_name is not None:
            dataframe.at[index, "Doctor Name"] = doctor_name

        self._save_dataframe(dataframe)
        return True

    def delete_record(self, index: int) -> bool:
        dataframe = self._load_dataframe()
        if index < 0 or index >= len(dataframe):
            return False

        dataframe = dataframe.drop(index=index).reset_index(drop=True)
        self._save_dataframe(dataframe)
        return True

    def get_total_patients(self) -> int:
        return len(self._load_dataframe())

    def get_hospital_counts(self) -> Dict[str, int]:
        dataframe = self._load_dataframe()
        if dataframe.empty:
            return {}
        counts = dataframe.groupby("Hospital Name").size().to_dict()
        return {str(name): int(count) for name, count in counts.items() if str(name).strip() != ""}

    def get_disease_counts(self) -> Dict[str, int]:
        dataframe = self._load_dataframe()
        if dataframe.empty:
            return {}
        counts = dataframe.groupby("Disease Name").size().to_dict()
        return {str(name): int(count) for name, count in counts.items() if str(name).strip() != ""}
