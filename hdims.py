from __future__ import annotations

from pathlib import Path
from typing import Dict

import matplotlib.pyplot as plt
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp

from data_manager import HDIMSDataManager

KV = """
ScreenManager:
    DashboardScreen:
    RecordScreen:

<DashboardScreen>:
    name: "dashboard"

    MDBoxLayout:
        orientation: "vertical"
        spacing: "12dp"
        padding: "12dp"

        MDTopAppBar:
            title: "HDIMS Dashboard"
            right_action_items: [["refresh", lambda x: root.refresh_metrics()]]

        MDGridLayout:
            cols: 2
            adaptive_height: True
            spacing: "12dp"

            MDCard:
                orientation: "vertical"
                padding: "10dp"
                radius: [12, 12, 12, 12]
                MDLabel:
                    text: "Total Patients"
                    halign: "center"
                MDLabel:
                    id: total_patients_label
                    text: "0"
                    halign: "center"
                    theme_text_color: "Primary"
                    font_style: "H5"

            MDCard:
                orientation: "vertical"
                padding: "10dp"
                radius: [12, 12, 12, 12]
                MDLabel:
                    text: "Hospitals Covered"
                    halign: "center"
                MDLabel:
                    id: hospital_count_label
                    text: "0"
                    halign: "center"
                    theme_text_color: "Primary"
                    font_style: "H5"

        MDCard:
            orientation: "vertical"
            padding: "10dp"
            radius: [12, 12, 12, 12]
            size_hint_y: None
            height: "260dp"
            MDLabel:
                text: "Hospital Distribution (Chart Card)"
                halign: "center"
            Image:
                id: chart_image
                allow_stretch: True
                keep_ratio: True
            MDLabel:
                id: chart_summary_label
                text: "No data available"
                halign: "center"

        MDRaisedButton:
            text: "Manage Records"
            pos_hint: {"center_x": .5}
            on_release: app.root.current = "records"

<RecordScreen>:
    name: "records"

    MDBoxLayout:
        orientation: "vertical"
        spacing: "10dp"
        padding: "12dp"

        MDTopAppBar:
            title: "Patient Data Management"
            left_action_items: [["arrow-left", lambda x: app.root.get_screen("dashboard").refresh_metrics() or setattr(app.root, "current", "dashboard")]]

        MDTextField:
            id: hospital_input
            hint_text: "Hospital Name"

        MDTextField:
            id: patient_input
            hint_text: "Patient Name"

        MDTextField:
            id: disease_input
            hint_text: "Disease Name"

        MDTextField:
            id: doctor_input
            hint_text: "Doctor Name"

        MDRaisedButton:
            text: "Add Record"
            pos_hint: {"center_x": .5}
            on_release: root.add_record()

        MDLabel:
            id: status_label
            text: ""
            halign: "center"
"""


class DashboardScreen(Screen):
    def refresh_metrics(self) -> None:
        app = MDApp.get_running_app()
        if app is None:
            return

        hospital_counts = app.data_manager.get_hospital_counts()
        total_patients = app.data_manager.get_total_patients()

        self.ids.total_patients_label.text = str(total_patients)
        self.ids.hospital_count_label.text = str(len(hospital_counts))
        self.ids.chart_summary_label.text = (
            ", ".join(f"{name}: {count}" for name, count in hospital_counts.items())
            if hospital_counts
            else "No data available"
        )
        app.build_hospital_chart(hospital_counts, self.ids.chart_image)


class RecordScreen(Screen):
    def add_record(self) -> None:
        app = MDApp.get_running_app()
        if app is None:
            return

        hospital_name = self.ids.hospital_input.text.strip()
        patient_name = self.ids.patient_input.text.strip()
        disease_name = self.ids.disease_input.text.strip()
        doctor_name = self.ids.doctor_input.text.strip()

        if not all([hospital_name, patient_name, disease_name, doctor_name]):
            self.ids.status_label.text = "Please fill all fields."
            return

        app.data_manager.add_record(
            hospital_name=hospital_name,
            patient_name=patient_name,
            disease_name=disease_name,
            doctor_name=doctor_name,
        )

        for field_id in ("hospital_input", "patient_input", "disease_input", "doctor_input"):
            self.ids[field_id].text = ""

        self.ids.status_label.text = "Record added successfully."


class HDIMSApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_manager = HDIMSDataManager()
        self.chart_path = Path("/tmp/hdims_hospital_chart.png")

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        return Builder.load_string(KV)

    def on_start(self) -> None:
        self.root.get_screen("dashboard").refresh_metrics()

    def build_hospital_chart(self, hospital_counts: Dict[str, int], image_widget=None) -> None:
        if not hospital_counts:
            if image_widget is not None:
                image_widget.source = ""
            return

        figure, axis = plt.subplots(figsize=(4, 2.5))
        axis.bar(list(hospital_counts.keys()), list(hospital_counts.values()))
        axis.set_title("Patients by Hospital")
        axis.set_ylabel("Patients")
        axis.tick_params(axis="x", rotation=20)
        figure.tight_layout()
        figure.savefig(self.chart_path)
        plt.close(figure)

        if image_widget is not None:
            image_widget.source = str(self.chart_path)
            image_widget.reload()


if __name__ == "__main__":
    HDIMSApp().run()
