"""
GPS Interface

This runs without GPS hardware by using simulated GPS readings.
Later, we need to replace get_demo_gps_data() with data received from the GPS module
or from the main processor over USB/serial.
"""

import random
import tkinter as tk
from tkinter import ttk
from datetime import datetime


class GPSInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("ECEN 4013 - GPS Status")
        self.root.geometry("560x390")
        self.root.minsize(500, 350)

        self.running = False
        self.after_id = None

        self.demo_lat = 36.1156
        self.demo_lon = -97.0584
        self.demo_elevation = 300.0

        ttk.Label(
            root,
            text="GPS Monitoring Interface",
            font=("Segoe UI", 18, "bold"),
        ).pack(pady=(18, 4))

        ttk.Label(
            root,
            text="DEMO MODE — simulated readings; no GPS hardware connected",
            foreground="#8a5a00",
        ).pack(pady=(0, 14))

        status_frame = ttk.LabelFrame(root, text="GPS Status", padding=12)
        status_frame.pack(fill="x", padx=20, pady=6)

        self.status_var = tk.StringVar(value="Not started")
        self.status_label = ttk.Label(
            status_frame,
            textvariable=self.status_var,
            font=("Segoe UI", 12, "bold"),
        )
        self.status_label.pack(anchor="w")

        readings = ttk.LabelFrame(root, text="GPS Data", padding=12)
        readings.pack(fill="both", expand=True, padx=20, pady=8)

        self.values = {}
        fields = [
            ("Latitude", "latitude"),
            ("Longitude", "longitude"),
            ("Elevation (demo MSL)", "elevation"),
            ("Locked satellites", "satellites"),
            ("Last update", "updated"),
        ]

        for row, (label_text, key) in enumerate(fields):
            ttk.Label(readings, text=label_text + ":").grid(
                row=row, column=0, sticky="w", padx=(0, 18), pady=5
            )
            self.values[key] = tk.StringVar(value="—")
            ttk.Label(
                readings,
                textvariable=self.values[key],
                font=("Consolas", 11),
            ).grid(row=row, column=1, sticky="w", pady=5)

        buttons = ttk.Frame(root)
        buttons.pack(pady=(4, 14))

        self.start_button = ttk.Button(
            buttons, text="Start Display", command=self.start_display
        )
        self.start_button.grid(row=0, column=0, padx=6)

        self.stop_button = ttk.Button(
            buttons,
            text="End Display",
            command=self.stop_display,
            state="disabled",
        )
        self.stop_button.grid(row=0, column=1, padx=6)

        ttk.Button(
            buttons, text="Close", command=self.close_app
        ).grid(row=0, column=2, padx=6)

        self.root.protocol("WM_DELETE_WINDOW", self.close_app)
        
    def get_demo_gps_data(self):
        """Generate simulated GPS readings."""
        satellites = random.randint(0, 12)

        if satellites >= 4:
            self.demo_lat += random.uniform(-0.00003, 0.00003)
            self.demo_lon += random.uniform(-0.00003, 0.00003)
            self.demo_elevation += random.uniform(-0.3, 0.3)

            return {
                "latitude": self.demo_lat,
                "longitude": self.demo_lon,
                "elevation": self.demo_elevation,
                "satellites": satellites,
            }

        return {
            "latitude": None,
            "longitude": None,
            "elevation": None,
            "satellites": satellites,
        }

    def start_display(self):
        if not self.running:
            self.running = True
            self.start_button.config(state="disabled")
            self.stop_button.config(state="normal")
            self.update_readings()

    def update_readings(self):
        if not self.running:
            return

        data = self.get_demo_gps_data()
        satellites = data["satellites"]

        self.values["satellites"].set(str(satellites))
        self.values["updated"].set(datetime.now().strftime("%H:%M:%S"))

        if satellites >= 4:
            self.status_var.set("GPS LOCKED (DEMO)")
            self.status_label.configure(foreground="green")
            self.values["latitude"].set(
                f'{data["latitude"]:.6f}'
            )
            self.values["longitude"].set(
                f'{data["longitude"]:.6f}'
            )
            self.values["elevation"].set(
                f'{data["elevation"]:.1f} m (MSL demo)'
            )
        else:
            self.status_var.set("SEARCHING FOR SATELLITES (DEMO)")
            self.status_label.configure(foreground="#a35a00")
            self.values["latitude"].set("Waiting for fix")
            self.values["longitude"].set("Waiting for fix")
            self.values["elevation"].set("Waiting for fix")

        self.root.after(1000, self.update_readings)

    def stop_display(self):
        self.running = False
        self.status_var.set("Display ended")
        self.status_label.configure(foreground="black")
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")

    def close_app(self):
        self.running = False
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = GPSInterface(root)
    root.mainloop()

