

# 🚆 Indian Railways Integrated Track Monitoring System (ITMS)

<div align="center">
  <img src="https://upload.wikimedia.org/wikipedia/en/thumb/8/83/Indian_Railways.svg/1200px-Indian_Railways.svg.png" alt="Indian Railways Logo" width="200"/>
  <h3>A Comprehensive Track Monitoring and Analysis Solution</h3>
</div>

## 📋 Table of Contents
- [Overview](#-overview)
- [System Architecture](#-system-architecture)
- [Features](#-features)
- [Installation](#%EF%B8%8F-installation)
- [Usage](#%EF%B8%8F-usage)
- [Smart India Hackathon Context](#-smart-india-hackathon-context)

## 🔍 Overview

The Indian Railways Integrated Track Monitoring System (ITMS) is a comprehensive solution designed to monitor, analyze, and visualize railway track conditions in real-time. This system combines advanced sensor technology, data processing algorithms, and an intuitive user interface to provide actionable insights for railway maintenance teams.

## 🏗️ System Architecture

### Hardware Components

Below is the Mermaid diagram code showing the hardware architecture:

```mermaid
graph TD
    subgraph "Track Monitoring Vehicle"
        A[GPS Receiver] --> D[Central Processing Unit]
        B[Inertial Measurement Units] --> D
        C[Optical Sensors] --> D
        E[High-Resolution Cameras] --> D
        F[Accelerometers] --> D
        G[Distance Measurement System] --> D
    end
    
    D --> H[Data Storage]
    D --> I[Real-time Transmission System]
    I --> J[Central Data Server]
    J --> K[ITMS Software Platform]
    
    style D fill:#f9f,stroke:#333,stroke-width:2px
    style J fill:#bbf,stroke:#333,stroke-width:2px
    style K fill:#bfb,stroke:#333,stroke-width:2px
```

### Software Components

Below is the Mermaid diagram code showing the software architecture:

```mermaid
graph TD
    A[Data Acquisition Module] --> B[Data Preprocessing]
    B --> C[Parameter Analysis]
    B --> D[Video Processing]
    
    C --> E[Anomaly Detection]
    D --> F[Video-Data Synchronization]
    
    E --> G[Alert Generation]
    E --> H[Visualization Engine]
    F --> H
    
    H --> I[Streamlit Dashboard]
    G --> J[Maintenance Recommendation System]
    
    style A fill:#f9f,stroke:#333,stroke-width:2px
    style E fill:#bbf,stroke:#333,stroke-width:2px
    style H fill:#bfb,stroke:#333,stroke-width:2px
    style I fill:#fbb,stroke:#333,stroke-width:2px
```

### Data Flow

Below is the Mermaid diagram code showing the data flow:

```mermaid
sequenceDiagram
    participant S as Sensors
    participant P as Preprocessing
    participant A as Analysis
    participant D as Database
    participant V as Visualization
    participant U as User Interface
    
    S->>P: Raw sensor data
    S->>P: Video footage
    P->>A: Filtered data
    A->>D: Processed parameters
    A->>D: Anomaly flags
    D->>V: Query results
    V->>U: Interactive visualizations
    U->>D: User queries
    U->>A: Parameter thresholds
```

## ✨ Features

- 🔧 **Track Parameter Monitoring**: 
  - Gauge, alignment, twist, cross level, unevenness
  - Acceleration measurements (vertical and lateral)
  - Rail profile and wear

- 📊 **Advanced Analytics**: 
  - Anomaly detection based on thresholds
  - Trend analysis over distance
  - Hotspot identification for maintenance

- 📈 **Interactive Visualization**:
  - Parameter vs. chainage plots
  - Anomaly highlighting with red markers
  - Video synchronization with parameter data
  - Heatmap of parameter correlations

- 💾 **Reporting and Export**:
  - Data export in CSV and JSON formats
  - Flagged segments in tabular format

## ⚙️ Installation

1. Clone this repository
   ```bash
   git clone <repo-url>
   cd Indian-Railways-Track-Monitoring-System
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   streamlit run app.py
   ```

## ▶️ Usage

The application consists of multiple pages:

1. **Main Dashboard**: 
   - Upload data or use sample data
   - Apply preprocessing filters
   - View track parameter analysis
   - Identify flagged segments

2. **Video Sync Page**: 
   - View track footage synchronized with parameter data
   - See real-time parameter values at selected chainage
   - Auto-advance through the track with adjustable speed

3. **Explanation Page**: 
   - Learn about track monitoring concepts
   - Understand parameter definitions and significance

4. **Documentation Page**:
   - Access comprehensive system documentation
   - View architecture diagrams and data flow

## 🏆 Smart India Hackathon Context

This project aligns perfectly with the Smart India Hackathon's focus on leveraging technology to solve real-world problems in India's infrastructure. The potential impacts include:

- **Safety Enhancement**: Early detection of track defects to prevent accidents
- **Maintenance Optimization**: Data-driven maintenance planning
- **Service Reliability**: Fewer delays due to track issues
- **Resource Allocation**: Prioritize maintenance based on actual conditions

---

<div align="center">
  <h3>Best of luck to all Smart India Hackathon participants!</h3>
  <p>Your innovative solutions have the potential to transform India's railway infrastructure and improve the lives of millions of passengers.</p>
</div>

For more detailed information, please see the [COMPREHENSIVE_README.md](./COMPREHENSIVE_README.md) file.
