#  Smart Campus Environment Monitoring Dashboard
### IoT Internship Project — Task 3: IoT Data Monitoring Dashboard
**DecodeLabs IoT Internship Track**

---

## Project Overview

This project implements a real-time IoT Data Monitoring Dashboard that simulates environmental sensors deployed across a university campus. Sensor data (temperature, humidity, CO₂ levels, and noise) is continuously generated, checked against safety thresholds, logged to a CSV file, and displayed on a live-updating multi-panel chart.

This fulfills the following requirements:
- Show sensor readings visually (live line charts per zone)
- Update data periodically (every 2 seconds)
- Use charts and tables (matplotlib live dashboard + CSV log)

---

## System Architecture

```
Sensor Simulation Layer
  └─ Temperature / Humidity / CO₂ / Noise generators
        │
        ▼
Data Collection Thread (background)
  └─ Reads all zones every 2 s
  └─ Writes rows to campus_sensor_log.csv
  └─ Checks alert thresholds → prints warnings
        │
        ▼
Live Dashboard (matplotlib animation)
  └─ 4-panel chart (one per sensor type)
  └─ One line per campus zone
  └─ Red dashed line = alert threshold
  └─ Latest values displayed per chart
```

**Campus Zones monitored:** Library · Lab A · Cafeteria · Lecture Hall

---

## Technologies Used

| Tool | Purpose |
|------|---------|
| Python 3.x | Core language |
| `threading` | Concurrent sensor polling |
| `matplotlib` | Live animated dashboard |
| `csv` / `os` | Data logging & file management |
| `collections.deque` | Rolling window of sensor history |
| `random` | Sensor value simulation with anomalies |

---

## Getting Started

### Prerequisites
```bash
pip install matplotlib
```

### Run the dashboard
```bash
python smart_campus_dashboard.py
```

A live chart window opens. Sensor data updates every **2 seconds**.  
Close the chart window to end the session.

---

## Dashboard Preview

The dashboard displays 4 live charts:

| Chart | Sensor | Alert Threshold |
|-------|--------|----------------|
| Top-left | Temperature (°C) | > 30 °C |
| Top-right | Humidity (%) | > 70 % |
| Bottom-left | CO₂ (ppm) | > 1000 ppm |
| Bottom-right | Noise Level (dB) | > 80 dB |

Each chart overlays all 4 campus zones as separate colored lines.

---

## Output Files

| File | Description |
|------|-------------|
| `smart_campus_dashboard.py` | Main application |
| `campus_sensor_log.csv` | Auto-generated log (timestamp, zone, all readings) |

### Sample CSV Output
```
timestamp,zone,temperature,humidity,co2,noise
2025-05-27 10:00:02,Library,24.3,52.1,640,55
2025-05-27 10:00:02,Lab A,26.7,48.9,870,63
...
```

---

## Configuration

Edit the constants at the top of `smart_campus_dashboard.py`:

```python
UPDATE_INTERVAL = 2       # seconds between sensor polls
MAX_HISTORY     = 30      # number of data points shown on chart
RUNTIME_SECONDS = 120     # total simulation time
```

---

## Alert System

If any reading exceeds a safe threshold, a warning is printed to the console:
```
[ALERT] Lab A | CO2 HIGH: 1143
[ALERT] Cafeteria | TEMPERATURE HIGH: 31.4
```

---

## Key IoT Concepts Demonstrated

- **Sensor data simulation** — realistic readings with occasional anomalies
- **Periodic polling** — background thread collects data at fixed intervals
- **Data logging** — all readings persisted to CSV for offline analysis
- **Real-time visualization** — live dashboard with animated charts
- **Multi-zone monitoring** — independent sensor streams per location
- **Threshold-based alerting** — safety limit checks on every reading

---

## Author

**[Fatma Abdelbadie]**  
DecodeLabs IoT Internship — 2026  
GitHub: [fatmaabdebadie]
