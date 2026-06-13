# esphome-sensostar

**Custom ESPHome Component for Engelmann SensoStar Heat Meters**

This ESPHome integration enables reading detailed heat consumption data from Engelmann SensoStar U heat meters and makes it available in Home Assistant.

---

## 🔧 Features

- 📊 **Sensor Readings**
  - Energy consumption (kWh)
  - Flow rate (m³/h)
  - Volume (m³)
  - Power (W)
  - Flow temperature (°C)
  - Return temperature (°C)
  - Temperature difference (ΔT)
  - Meter status (text)
  - Battery voltage (via ADC)

- 🧠 **Home Assistant Integration**
  - Native API support
  - OTA updates
  - Web dashboard (optional)

- 🕹 **Controls**
  - Template button for instant battery reading
  - Template button for instant Wi-Fi signal strength reading (WiFi variants)
  - MQTT broker address, port, username, password configurable at runtime
  - MQTT enable/disable switch (persisted across reboots)

- 💡 **LED Indicators**
  - Flash programming
  - Wi-Fi / Ethernet link status
  - Heartbeat (device activity)
  - New data received from the SensoStar meter

---

## 🧩 Repository Structure

The firmware uses a **modular package architecture**. A thin device file selects the hardware variant and connectivity module; all shared logic lives in reusable packages.

```
esphome-sensostar/
├── sensostar_black.yaml        # Device file: ESP32-S3 / WiFi  (black PCB)
├── sensostar_red.yaml          # Device file: ESP32-C6 / WiFi  (red PCB)
├── sensostar_blue_WLAN.yaml    # Device file: ESP32-C6 / WiFi  (blue PCB)
├── sensostar_blue_LAN.yaml     # Device file: ESP32-C6 / Wired LAN via W5500 (blue PCB)
└── packages/
    ├── sensostar_base.yaml     # Shared: sensors, MQTT, scripts, LED outputs
    ├── sensostar_wifi.yaml     # Connectivity: WiFi + AP-mode blink
    └── sensostar_eth.yaml      # Connectivity: W5500 Ethernet
```

Each device file defines board-specific substitutions (chip, pin mapping) and then includes two packages:

```yaml
packages:
  base:         !include packages/sensostar_base.yaml
  connectivity: !include packages/sensostar_wifi.yaml   # or sensostar_eth.yaml
```

### Hardware Variants

| File | PCB | Chip | Connectivity |
|------|-----|------|-------------|
| `sensostar_black.yaml` | Black | ESP32-S3 | WiFi |
| `sensostar_red.yaml` | Red | ESP32-C6 | WiFi |
| `sensostar_blue_WLAN.yaml` | Blue | ESP32-C6 | WiFi |
| `sensostar_blue_LAN.yaml` | Blue | ESP32-C6 | Wired LAN (W5500) |

> The blue PCB is available in two variants: use `sensostar_blue_WLAN.yaml` for the WiFi-only version and `sensostar_blue_LAN.yaml` for the wired Ethernet expansion board (W5500 via FFC adapter).

---

## 🧪 Requirements

- ESPHome installed on your system
- Home Assistant (optional but recommended)
- Sensostar heat meter — the following have been confirmed to be working:
  - SensoStar U (Engelmann)
  - SensoStar E (Engelmann)
  - Volumess VI E (Wasser-Geräte)
  - microCLIMA EVO (Maddalena)
  - microCLIMA U (Maddalena)
  - Brummerhoop F90U3
  - Molline Wingman C3

**Check compatibility:** Only units with *Modul* are working.

[![SensoStar compatible devices](https://github.com/STB3/esphome-sensostar/raw/main/pictures/sensostar_compatibility.png)](pictures/sensostar_compatibility.png)

---

## 🔌 Hardware Wiring

The SensoStar meter uses a 12-pin internal connector for communication and power. Below is the pinout and how to wire it to the ESP:

| Pin | Function | Connection |
|-----|----------|-----------|
| 1 | NC | — |
| 2 | GND | Connect to ESP GND |
| 3 | VCC | Connected to the internal battery of the meter |
| 4 | NC | — |
| 5 | RX | Connect to ESP UART TX |
| 6 | TX | Connect to ESP UART RX |
| 7 | NC | — |
| 8 | NC | — |
| 9 | NC | — |
| 10 | HW Detect (56 kΩ to GND) | Connect a 56 kΩ resistor to GND |
| 11 | NC | — |
| 12 | GND | Connect to ESP GND |

> **Note:** "NC" means *Not Connected*. Be sure to use level shifting or protective circuitry if needed, depending on your ESP model and power requirements.

[![SensoStar internal connector](https://github.com/STB3/esphome-sensostar/raw/main/pictures/Sensostar_internal_connector.png)](pictures/Sensostar_internal_connector.png)

---

## 📷 Example Hardware

### Version 1 — Black PCB (ESP32-S3)

[![SensoStar Hardware V1](https://github.com/STB3/esphome-sensostar/raw/main/pictures/Sensostar_w_ESP32_Sensostar.png)](pictures/Sensostar_w_ESP32_Sensostar.png)

[![SensoStar Hardware V1 detail](https://github.com/STB3/esphome-sensostar/raw/main/pictures/ESP_Sensostar.png)](pictures/ESP_Sensostar.png)

### Version 2 — Red PCB (ESP32-C6 / WiFi)

[![SensoStar Hardware V2](https://github.com/STB3/esphome-sensostar/raw/main/pictures/ESP_Sensostar_V2.png)](pictures/ESP_Sensostar_V2.png)

### Version 3 — Blue PCB (ESP32-C6 / WiFi or Wired LAN)

<!-- 📸 PLACEHOLDER: Photo of the blue PCB (WiFi variant) — e.g. pictures/ESP_Sensostar_V3_WLAN.png -->

<!-- 📸 PLACEHOLDER: Photo of the blue PCB with W5500 LAN expansion board — e.g. pictures/ESP_Sensostar_V3_LAN.png -->

---

## 🗺 Schematics

### Version 1 — Black PCB

[![Schematic V1](https://github.com/STB3/esphome-sensostar/raw/main/pictures/ESP32_Sensostar.png)](pictures/ESP32_Sensostar.png)

### Version 2 — Red PCB

[![Schematic V2](https://github.com/STB3/esphome-sensostar/raw/main/pictures/ESP32_Sensostar_V2.png)](pictures/ESP32_Sensostar_V2.png)

### Version 3 — Blue PCB (LAN variant)

<!-- 📸 PLACEHOLDER: Schematic of the blue PCB with W5500 SPI wiring — e.g. pictures/ESP32_Sensostar_V3_LAN.png -->

---

## 🌐 Interfaces

### Web Interface

[![SensoStar Web Interface](https://github.com/STB3/esphome-sensostar/raw/main/pictures/Sensostar_ESP_WebIF.png)](pictures/Sensostar_ESP_WebIF.png)

### Home Assistant Dashboard

[![SensoStar Home Assistant Integration](https://github.com/STB3/esphome-sensostar/raw/main/pictures/HA_Dash_Sensostar.png)](pictures/HA_Dash_Sensostar.png)

---

## 🚀 Setup Instructions

### 1. Install ESPHome

[ESPHome installation guide](https://esphome.io/guides/installing_esphome.html)

### 2. Clone this repository

```bash
git clone https://github.com/STB3/esphome-sensostar.git
cd esphome-sensostar
```

The `external_components` block is already included in `packages/sensostar_base.yaml` — no manual configuration needed:

```yaml
external_components:
  - source:
      type: git
      url: https://github.com/STB3/esphome-sensostar
      ref: main
    components: [ SensoStar_MBus ]
```

### 3. Create a `secrets.yaml` file

Place a `secrets.yaml` file in the same directory as the device YAML files:

```yaml
# secrets.yaml
wifi_ssid: "YourSSID"
wifi_password: "YourPassword"
api_encryption_key: "YourAPIKey"  # Generate with: openssl rand -base64 32
```

[Generate an API key online](https://www.cryptool.org/en/cto/openssl/)

### 4. Flash the firmware

Choose the file matching your hardware:

**Black PCB (ESP32-S3 / WiFi)**
```bash
esphome run sensostar_black.yaml
```

**Red PCB (ESP32-C6 / WiFi)**
```bash
esphome run sensostar_red.yaml
```

**Blue PCB — WiFi**
```bash
esphome run sensostar_blue_WLAN.yaml
```

**Blue PCB — Wired LAN (W5500)**
```bash
esphome run sensostar_blue_LAN.yaml
```

### 5. First-boot fallback (WiFi variants)

If no WiFi credentials are stored, the device opens an access point named **Sensostar**. Connect to it and enter your SSID and password via the captive portal. The AP-mode LED blinks rapidly until a connection is established.

### 6. Configure MQTT (optional)

MQTT is disabled by default. After the device appears in Home Assistant or the web interface, set the broker parameters under **Controls**:

1. Enter **MQTT address**, **MQTT port** (default: 1883), **MQTT username**, **MQTT password**
2. Enable the **MQTT Enabled** switch

All settings are stored in NVS and survive reboots.

---

## 📦 Repository Contents

| Path | Description |
|------|-------------|
| `components/SensoStar_MBus/` | Custom ESPHome component for M-Bus communication |
| `packages/sensostar_base.yaml` | Shared base: sensors, MQTT, scripts, LED outputs |
| `packages/sensostar_wifi.yaml` | WiFi connectivity module |
| `packages/sensostar_eth.yaml` | Wired LAN (W5500) connectivity module |
| `sensostar_black.yaml` | Device file: Black PCB, ESP32-S3, WiFi |
| `sensostar_red.yaml` | Device file: Red PCB, ESP32-C6, WiFi |
| `sensostar_blue_WLAN.yaml` | Device file: Blue PCB, ESP32-C6, WiFi |
| `sensostar_blue_LAN.yaml` | Device file: Blue PCB, ESP32-C6, Wired LAN |

---

## 🔐 Security Note

This repository **does not** contain any private configurations. Be sure to:

- Use `secrets.yaml` to keep credentials out of your main config
- Add a `.gitignore` to exclude secrets from being committed

```ini
# .gitignore
secrets.yaml
*.key
*.pem
```

---

## 📫 Contact

Maintained by **STB3**  
For issues or feature requests, open an issue in the [GitHub repository](https://github.com/STB3/esphome-sensostar/issues).

---

## 📝 License

This project is open-source and licensed under the MIT License.
