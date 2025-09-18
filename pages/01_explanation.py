import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

# Set page configuration
st.set_page_config(
    page_title="Track Monitoring Explanation",
    page_icon="🚆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main content
st.title("🚆 Understanding Track Monitoring and Analysis")

st.markdown("""
## What is Track Monitoring?

Track monitoring is a critical process in railway maintenance that involves the systematic inspection and assessment of railway tracks to ensure their safety, reliability, and performance. The Indian Railways Integrated Track Monitoring System (ITMS) is designed to collect, analyze, and visualize track condition data to support maintenance decisions.

### Key Parameters Monitored

""")

# Create tabs for different parameter explanations
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Track Geometry", 
    "Acceleration", 
    "Rail Profile", 
    "Thresholds", 
    "Analysis Methods"
])

with tab1:
    st.header("Track Geometry Parameters")
    
    st.subheader("Gauge")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/1c/Rail_gauge_measurement.svg/640px-Rail_gauge_measurement.svg.png", width='stretch')
    with col2:
        st.markdown("""
        **Gauge** is the distance between the inner faces of the rails. The standard gauge used in many countries is 1435mm.
        
        - **Gauge Deviation**: Difference between measured gauge and nominal gauge
        - **Importance**: Incorrect gauge can lead to train derailment or excessive wheel wear
        - **Measurement**: Typically measured using track recording vehicles or manual gauge tools
        """)
    
    st.subheader("Alignment")
    col1, col2 = st.columns([1, 2])
    with col1:
        # Create a simple alignment visualization
        fig = go.Figure()
        x = np.linspace(0, 10, 100)
        y_ideal = np.zeros_like(x)
        y_actual = 0.2 * np.sin(x)
        
        fig.add_trace(go.Scatter(x=x, y=y_ideal, mode='lines', name='Ideal Alignment', line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=x, y=y_actual, mode='lines', name='Actual Alignment', line=dict(color='red')))
        
        fig.update_layout(
            title="Track Alignment Visualization",
            xaxis_title="Distance",
            yaxis_title="Lateral Deviation",
            height=300
        )
        st.plotly_chart(fig, width='stretch')
    with col2:
        st.markdown("""
        **Alignment** refers to the lateral position of the track. It measures how straight the track is in the horizontal plane.
        
        - **Left/Right Alignment**: Measures deviation on each rail
        - **Importance**: Poor alignment causes lateral forces, passenger discomfort, and increased wear
        - **Measurement**: Measured using chord-based systems or inertial measurement units
        """)
    
    st.subheader("Cross Level and Twist")
    col1, col2 = st.columns([1, 2])
    with col1:
        # Create a cross level visualization
        fig = go.Figure()
        
        # Draw rails
        fig.add_shape(type="line", x0=0, y0=0, x1=10, y1=0, line=dict(color="gray", width=10))
        fig.add_shape(type="line", x0=0, y0=1, x1=10, y1=2, line=dict(color="gray", width=10))
        
        # Add annotation
        fig.add_annotation(x=5, y=0.5, text="Cross Level", showarrow=True, arrowhead=2)
        
        fig.update_layout(
            title="Cross Level Visualization",
            xaxis_title="Distance",
            yaxis_title="Height",
            height=300,
            showlegend=False
        )
        st.plotly_chart(fig, width='stretch')
    with col2:
        st.markdown("""
        **Cross Level** is the height difference between the two rails at a specific point.
        
        **Twist** is the rate of change of cross level over a specified distance.
        
        - **Importance**: Excessive twist can lead to wheel unloading and derailment risk
        - **Measurement**: Measured using track geometry cars with optical or inertial systems
        - **Relationship**: Twist is calculated from cross level measurements at two points
        """)
    
    st.subheader("Unevenness")
    st.markdown("""
    **Unevenness** (also called surface or top) refers to the vertical deviations in the rail head surface.
    
    - **Left/Right Unevenness**: Measured for each rail
    - **Importance**: Affects ride quality, dynamic forces, and component fatigue
    - **Measurement**: Measured using accelerometers, optical systems, or chord-based methods
    - **Wavelength Bands**: Often analyzed in different wavelength bands (short, medium, long)
    """)

with tab2:
    st.header("Acceleration Measurements")
    
    st.markdown("""
    Acceleration measurements capture the dynamic response of the track-vehicle system during train passage.
    
    ### Vertical Acceleration
    
    - Measures the up-and-down movement of the track or vehicle
    - High values indicate track dips, joints, or poor support conditions
    - Typically measured in g units (1g = 9.81 m/s²)
    - Critical for identifying track defects that affect ride quality
    
    ### Lateral Acceleration
    
    - Measures side-to-side movement
    - High values indicate alignment issues, gauge variations, or curve problems
    - Important for safety assessment, especially in curves
    - Can indicate risk of derailment when excessive
    
    ### Measurement Methods
    
    - **Track-based**: Accelerometers mounted on sleepers or rails
    - **Vehicle-based**: Sensors on bogies or car body
    - **Frequency Analysis**: Often analyzed in different frequency bands
    """)
    
    # Create a sample acceleration plot
    fig = go.Figure()
    x = np.linspace(0, 100, 1000)
    y_vert = 0.1 * np.sin(0.5 * x) + 0.05 * np.random.randn(len(x))
    y_lat = 0.08 * np.sin(0.3 * x) + 0.03 * np.random.randn(len(x))
    
    fig.add_trace(go.Scatter(x=x, y=y_vert, mode='lines', name='Vertical Acceleration'))
    fig.add_trace(go.Scatter(x=x, y=y_lat, mode='lines', name='Lateral Acceleration'))
    
    fig.update_layout(
        title="Sample Acceleration Measurements",
        xaxis_title="Distance (m)",
        yaxis_title="Acceleration (g)",
        height=400
    )
    st.plotly_chart(fig, width='stretch')

with tab3:
    st.header("Rail Profile and Wear")
    
    st.markdown("""
    Rail profile monitoring tracks the shape and wear of the rail head over time.
    
    ### Rail Wear Types
    
    - **Vertical Wear**: Reduction in rail height
    - **Side Wear**: Loss of material on the gauge face
    - **Head Loss**: Combined vertical and side wear
    - **Rolling Contact Fatigue (RCF)**: Surface cracks and spalling
    
    ### Importance of Rail Profile Monitoring
    
    - Predicts rail life and replacement needs
    - Identifies locations requiring grinding or maintenance
    - Ensures proper wheel-rail contact
    - Prevents excessive forces and wear
    
    ### Measurement Methods
    
    - Manual profile gauges
    - Optical/laser profile measurement systems
    - Vehicle-mounted automated systems
    """)
    
    # Create a rail profile visualization
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("New Rail Profile")
        # Simple rail profile visualization
        fig = go.Figure()
        
        # Create a simplified rail profile shape
        x = np.linspace(-30, 30, 100)
        y = -0.01 * x**2 + 20
        y[x < -15] = -0.05 * (x[x < -15] + 15)**2 + 15
        y[x > 15] = -0.05 * (x[x > 15] - 15)**2 + 15
        
        fig.add_trace(go.Scatter(x=x, y=y, fill='tozeroy', fillcolor='rgba(100, 100, 100, 0.8)', 
                                line=dict(color='black'), name='New Rail'))
        
        fig.update_layout(
            title="New Rail Cross-Section",
            xaxis_title="Width (mm)",
            yaxis_title="Height (mm)",
            height=300,
            showlegend=False
        )
        st.plotly_chart(fig, width='stretch')
    
    with col2:
        st.subheader("Worn Rail Profile")
        # Worn rail profile visualization
        fig = go.Figure()
        
        # Create a simplified worn rail profile shape
        x = np.linspace(-30, 30, 100)
        y = -0.01 * x**2 + 20
        y[x < -15] = -0.05 * (x[x < -15] + 15)**2 + 15
        y[x > 15] = -0.05 * (x[x > 15] - 15)**2 + 15
        
        # Add wear on the top and side
        y[abs(x) < 10] -= 3 * np.exp(-(x[abs(x) < 10])**2/20)
        y[(x > 10) & (x < 20)] -= 5 * np.exp(-((x[(x > 10) & (x < 20)]-15)**2)/10)
        
        fig.add_trace(go.Scatter(x=x, y=y, fill='tozeroy', fillcolor='rgba(100, 100, 100, 0.8)', 
                                line=dict(color='black'), name='Worn Rail'))
        
        fig.update_layout(
            title="Worn Rail Cross-Section",
            xaxis_title="Width (mm)",
            yaxis_title="Height (mm)",
            height=300,
            showlegend=False
        )
        st.plotly_chart(fig, width='stretch')

with tab4:
    st.header("Threshold Values and Standards")
    
    st.markdown("""
    Track parameters are evaluated against established thresholds that define acceptable limits for safe operation.
    
    ### Common Standards
    
    - **EN 13848**: European standard for track geometry quality
    - **RDSO**: Indian Railways standards for track parameters
    - **FRA Track Safety Standards**: U.S. Federal Railroad Administration standards
    
    ### Threshold Categories
    
    Most standards define multiple threshold levels:
    
    - **Alert Limit (AL)**: Early warning, plan maintenance
    - **Intervention Limit (IL)**: Maintenance required soon
    - **Immediate Action Limit (IAL)**: Immediate action required, possible speed restrictions
    
    ### Speed-Based Thresholds
    
    Thresholds typically vary based on line speed:
    - Higher speeds require tighter tolerances
    - Lower speed lines may have more relaxed limits
    """)
    
    # Create a table of sample thresholds
    st.subheader("Sample Threshold Values")
    
    threshold_data = {
        'Parameter': ['Gauge Deviation', 'Alignment (35m)', 'Twist (3m)', 'Cross Level', 'Vertical Acceleration', 'Lateral Acceleration'],
        'Alert Limit': ['±3 mm', '8 mm', '3 mm/m', '5 mm', '0.35g', '0.25g'],
        'Intervention Limit': ['±5 mm', '10 mm', '5 mm/m', '7 mm', '0.5g', '0.35g'],
        'Immediate Action Limit': ['±10 mm', '16 mm', '7 mm/m', '12 mm', '0.7g', '0.5g']
    }
    
    df_thresholds = pd.DataFrame(threshold_data)
    st.table(df_thresholds)
    
    st.info("Note: These are sample values for illustration. Actual thresholds vary by railway administration, track class, and operating speed.")

with tab5:
    st.header("Analysis Methods")
    
    st.markdown("""
    Track data analysis involves various techniques to extract meaningful information from raw measurements.
    
    ### Preprocessing Techniques
    
    - **Missing Value Handling**: Interpolation, median filling
    - **Noise Filtering**: Removing measurement noise while preserving defect signals
    - **Signal Processing**: Converting time-domain to distance-domain data
    
    ### Filtering Methods
    
    - **Rolling Average**: Simple moving average to smooth data
    - **Butterworth Filter**: Low-pass filter that removes high-frequency noise
    - **Savitzky-Golay Filter**: Preserves peaks and valleys while removing noise
    
    ### Advanced Analysis
    
    - **Wavelength Analysis**: Identifying defects by their characteristic wavelengths
    - **Pattern Recognition**: Detecting specific defect patterns
    - **Trend Analysis**: Tracking parameter degradation over time
    - **Machine Learning**: Predicting maintenance needs and defect development
    """)
    
    # Create a visualization of different filtering methods
    st.subheader("Comparison of Filtering Methods")
    
    # Generate noisy data
    np.random.seed(42)
    x = np.linspace(0, 10, 500)
    y_true = np.sin(x) + 0.2 * np.sin(5 * x)
    y_noisy = y_true + 0.2 * np.random.randn(len(x))
    
    # Apply different filters
    y_rolling = pd.Series(y_noisy).rolling(window=15, center=True).mean().values
    
    # Create plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y_true, mode='lines', name='True Signal', line=dict(color='black')))
    fig.add_trace(go.Scatter(x=x, y=y_noisy, mode='lines', name='Noisy Data', line=dict(color='gray', width=1)))
    fig.add_trace(go.Scatter(x=x, y=y_rolling, mode='lines', name='Rolling Average', line=dict(color='blue')))
    
    fig.update_layout(
        title="Effect of Filtering on Noisy Track Data",
        xaxis_title="Distance",
        yaxis_title="Measurement Value",
        height=400
    )
    st.plotly_chart(fig, width='stretch')

# Additional information section
st.header("Benefits of Track Monitoring")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### Safety
    - Early detection of defects
    - Prevention of derailments
    - Identification of hazardous conditions
    - Compliance with safety standards
    """)

with col2:
    st.markdown("""
    ### Maintenance Optimization
    - Condition-based maintenance
    - Prioritization of critical areas
    - Reduced unnecessary interventions
    - Extended asset life
    """)

with col3:
    st.markdown("""
    ### Operational Benefits
    - Increased track availability
    - Higher permissible speeds
    - Improved ride comfort
    - Reduced energy consumption
    """)

# References section
st.header("References and Further Reading")

st.markdown("""
- EN 13848 series: "Railway applications - Track - Track geometry quality"
- UIC 518: "Testing and approval of railway vehicles from the point of view of their dynamic behaviour"
- RDSO Guidelines for Track Monitoring and Maintenance
- Esveld, C. (2001). Modern Railway Track. MRT-Productions.
- Mundrey, J.S. (2017). Railway Track Engineering. Tata McGraw-Hill Education.
""")

# Footer
st.markdown("---")
st.markdown("Indian Railways Integrated Track Monitoring System (ITMS) - Explanation Page")