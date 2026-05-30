import random
import time
import csv
import os
import threading
import datetime
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque

ZONES = ["Library", "Lab A", "Cafeteria", "Lecture Hall"]
UPDATE_INTERVAL = 2          # seconds between sensor reads
MAX_HISTORY = 30             # data points shown on charts
LOG_FILE = "campus_sensor_log.csv"
RUNTIME_SECONDS = 120        # total simulation runtime

SENSOR_RANGES = {
    "temperature": (18.0, 32.0),   # °C
    "humidity":    (30.0, 75.0),   # %
    "co2":         (400, 1200),     # ppm
    "noise":       (30, 90),        # dB
}

ALERT_THRESHOLDS = {
    "temperature": {"low": 18.0, "high": 30.0},
    "humidity":    {"low": 35.0, "high": 70.0},
    "co2":         {"low": 0,    "high": 1000},
    "noise":       {"low": 0,    "high": 80},
}

history = {
    zone: {
        "temperature": deque(maxlen=MAX_HISTORY),
        "humidity":    deque(maxlen=MAX_HISTORY),
        "co2":         deque(maxlen=MAX_HISTORY),
        "noise":       deque(maxlen=MAX_HISTORY),
    }
    for zone in ZONES
}
latest = {zone: {} for zone in ZONES}
alerts = []
data_lock = threading.Lock()
running = True

def simulate_sensor(sensor_type):
    """Generate a realistic sensor reading with occasional anomalies."""
    lo, hi = SENSOR_RANGES[sensor_type]
    # 10% chance of anomaly reading
    if random.random() < 0.10:
        if sensor_type == "temperature":
            return round(random.uniform(hi, hi + 5), 1)
        elif sensor_type == "co2":
            return random.randint(hi, hi + 300)
        elif sensor_type == "noise":
            return random.randint(hi, hi + 15)
    if isinstance(lo, float):
        return round(random.uniform(lo, hi), 1)
    return random.randint(lo, hi)


def check_alerts(zone, sensor, value):
    """Check if a reading exceeds safe thresholds and log an alert."""
    thresholds = ALERT_THRESHOLDS[sensor]
    if value > thresholds["high"]:
        msg = f"[ALERT] {zone} | {sensor.upper()} HIGH: {value}"
        alerts.append((datetime.datetime.now().strftime("%H:%M:%S"), msg))
        print(msg)
    elif value < thresholds["low"] and thresholds["low"] > 0:
        msg = f"[ALERT] {zone} | {sensor.upper()} LOW: {value}"
        alerts.append((datetime.datetime.now().strftime("%H:%M:%S"), msg))
        print(msg)

def data_collection_loop():
    """Continuously polls simulated sensors and writes to CSV log."""
    global running

    # Initialise CSV file with headers
    file_exists = os.path.isfile(LOG_FILE)
    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "zone", "temperature",
                             "humidity", "co2", "noise"])

    while running:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with data_lock:
            for zone in ZONES:
                readings = {s: simulate_sensor(s) for s in SENSOR_RANGES}
                latest[zone] = readings

                for sensor, value in readings.items():
                    history[zone][sensor].append(value)
                    check_alerts(zone, sensor, value)

                # Write row to CSV
                with open(LOG_FILE, "a", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow([
                        timestamp, zone,
                        readings["temperature"], readings["humidity"],
                        readings["co2"], readings["noise"]
                    ])

        time.sleep(UPDATE_INTERVAL)

def build_dashboard():
    """Create and animate the live IoT monitoring dashboard."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 8))
    fig.patch.set_facecolor("#1e1e2e")
    fig.suptitle("Smart Campus Environment Monitor  |  Live IoT Dashboard",
                 fontsize=15, fontweight="bold", color="white", y=0.98)

    sensor_axes = {
        "temperature": axes[0][0],
        "humidity":    axes[0][1],
        "co2":         axes[1][0],
        "noise":       axes[1][1],
    }
    sensor_labels = {
        "temperature": "Temperature (°C)",
        "humidity":    "Humidity (%)",
        "co2":         "CO₂ (ppm)",
        "noise":       "Noise Level (dB)",
    }
    colors = ["#74c7ec", "#a6e3a1", "#fab387", "#cba6f7"]

    for ax in axes.flat:
        ax.set_facecolor("#181825")
        ax.tick_params(colors="white")
        for spine in ax.spines.values():
            spine.set_edgecolor("#45475a")

    def update(_frame):
        with data_lock:
            for sensor, ax in sensor_axes.items():
                ax.cla()
                ax.set_facecolor("#181825")
                ax.tick_params(colors="white")
                ax.set_title(sensor_labels[sensor],
                             color="white", fontsize=10, pad=6)
                ax.set_xlabel("Samples", color="#6c7086", fontsize=8)
                ax.axhline(y=ALERT_THRESHOLDS[sensor]["high"],
                           color="#f38ba8", linestyle="--",
                           alpha=0.6, linewidth=1, label="High Threshold")
                for spine in ax.spines.values():
                    spine.set_edgecolor("#45475a")

                for i, zone in enumerate(ZONES):
                    data = list(history[zone][sensor])
                    if data:
                        ax.plot(data, label=zone,
                                color=colors[i], linewidth=1.8,
                                marker="o", markersize=3)

                ax.legend(fontsize=7, facecolor="#313244",
                         labelcolor="white", loc="upper left")

                # Show latest values in corner
                latest_text = "  ".join(
                    f"{z[:3]}: {latest[z].get(sensor, '--')}"
                    for z in ZONES
                )
                ax.set_xlabel(latest_text, color="#a6adc8", fontsize=7.5)

        fig.tight_layout(rect=[0, 0, 1, 0.96])

    ani = animation.FuncAnimation(fig, update, interval=UPDATE_INTERVAL * 1000,
                                  cache_frame_data=False)
    plt.show()
    return ani

def main():
    global running

    print("=" * 55)
    print("  Smart Campus IoT Environment Dashboard")
    print(f"  Monitoring zones: {', '.join(ZONES)}")
    print(f"  Logging to: {LOG_FILE}")
    print("=" * 55)

    # Start background data collection thread
    collector = threading.Thread(target=data_collection_loop, daemon=True)
    collector.start()

    # Give sensors a moment to populate initial data
    time.sleep(UPDATE_INTERVAL + 0.5)

    print("\nDashboard running. Close the chart window to stop.\n")

    try:
        ani = build_dashboard()  # blocks until window closed
    except KeyboardInterrupt:
        pass

    running = False
    print("\n[INFO] Simulation ended.")
    print(f"[INFO] {len(alerts)} alert(s) triggered during session.")
    print(f"[INFO] Data saved to '{LOG_FILE}'")


if __name__ == "__main__":
    main()
