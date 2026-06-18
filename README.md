# HDIMS - Health Data Information Management System

HDIMS is a Python-based mobile application built with KivyMD that provides healthcare institutions with a centralized platform for managing and analyzing patient data across multiple hospitals.

## Project Overview

### Purpose
- Streamline healthcare data handling by consolidating records from different hospitals into one platform.

### Technology Stack
- **UI Framework:** Kivy + KivyMD (Material Design)
- **Data Processing:** Pandas, NumPy
- **Data Storage:** Excel files (`.xlsx`)
- **Visualization:** Matplotlib

## Core Components

### `hdims.py` - Main Application
- Multi-screen interface using `ScreenManager`
- Chart cards for data visualization
- Real-time analytics dashboard refresh support
- KivyMD mobile-first interface

### `data_manager.py` - Data Management Engine
- Excel-backed storage management
- CRUD operations for records
- Tracks:
  - Hospital Name
  - Patient Name
  - Disease Name
  - Doctor Name
- Analytics methods for hospital counts and total patients

## Key Features
- Centralized data integration from multiple hospitals
- Advanced analytics and visual summaries
- Patient data management (input/retrieval/update/delete)
- Disease and doctor tracking
- Scalable Excel-based data persistence
- Intuitive Material Design-based UI

## Dependencies
- `kivy`
- `kivymd`
- `pandas`
- `matplotlib`
- `numpy`
- `openpyxl`
