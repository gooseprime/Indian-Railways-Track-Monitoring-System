

# 🚆 Indian Railways Integrated Track Monitoring System (ITMS)

This is a **prototype** of the **Indian Railways Integrated Track Monitoring System (ITMS)** built with **Streamlit**.  
The application provides **analysis and visualization of track monitoring data** to ensure safe and reliable railway operations.  

---

## ✨ Features
- 🔧 Data preprocessing with multiple filtering options  
- 📊 Analysis of track geometry parameters:  
  - Gauge deviation  
  - Alignment error  
  - Twist  
  - Cross level  
  - Unevenness  
- 📈 Acceleration measurements analysis  
- 🛤️ Rail profile and wear visualization  
- 🚨 Anomaly detection and flagging  
- 📍 Interactive chainage range selection  
- 💾 Data export in **CSV** and **JSON** formats  

---

## ⚙️ Installation
1. Clone this repository  
   ```bash
   git clone <repo-url>
   cd Indian-Railways-Track-Monitoring-System
````

2. Install the required packages

   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ Usage

Run the Streamlit application:

```bash
streamlit run app.py
```

The application will open in your default web browser.

---

## 📂 Data Input

You can either:

* Upload your own **CSV file** with track monitoring data
* Use the **provided sample data**

### Required CSV Columns:

* `chainage`: Distance along the track (m)
* `gauge`: Track gauge (mm)
* `alignment_left`, `alignment_right`: Track alignment (mm)
* `cross_level`: Cross level (mm)
* `twist`: Track twist (mm/m)
* `unevenness_left`, `unevenness_right`: Track unevenness (mm)
* `vertical_acceleration`, `lateral_acceleration`: Acceleration measurements (g)
* `rail_wear_left`, `rail_wear_right`: Rail wear measurements (mm)
* `component_condition`: Condition of track components (text)

---

## 🔎 Analysis Performed

* Gauge deviation from nominal value (**1435 mm standard gauge**)
* Alignment error calculation
* Twist error calculation
* Unevenness calculation
* Acceleration peak detection
* Automatic flagging of segments exceeding thresholds

---

## 📊 Visualization

The application provides the following interactive visualizations:

* Line charts of track parameters vs chainage
* Heatmap of parameter correlations
* Rail profile plot
* Flag distribution bar chart

---

## 🚨 Thresholds

The following thresholds are used for flagging anomalies:

| Parameter             | Threshold |
| --------------------- | --------- |
| Gauge deviation       | ±5.0 mm   |
| Alignment             | 10.0 mm   |
| Twist                 | 5.0 mm/m  |
| Cross level           | 7.0 mm    |
| Unevenness            | 7.0 mm    |
| Vertical acceleration | 0.7 g     |
| Lateral acceleration  | 0.5 g     |

*(These thresholds can be modified in the code as needed.)*

---

## 🏷️ Project Info

* **Name**: Indian Railways Integrated Track Monitoring System (ITMS)
* **Technology**: Python, Streamlit, Data Analysis, Visualization
* **Status**: Prototype

---

## 🙌 Acknowledgements

Special thanks to all contributors and the Indian Railways ecosystem inspiring this project.

---

# 🚀 Goodluck!

```

Would you like me to also **add screenshots & GIF placeholders** in the README (so your Streamlit app looks even more professional on GitHub)?
```
