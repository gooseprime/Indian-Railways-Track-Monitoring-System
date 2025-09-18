import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
import base64
from PIL import Image
import io

# Set page configuration
st.set_page_config(
    page_title="Track Video Sync",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main content
st.title("🎥 Track Video Sync")

st.markdown("""
This page allows you to synchronize track footage with track monitoring data. 
Select a chainage range to view the corresponding track footage and parameter values.
""")

# Function to load data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("track_data.csv")
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# Function to get image for a specific chainage
def get_image_for_chainage(chainage):
    """
    This function would normally retrieve the actual image corresponding to the chainage.
    For this prototype, we'll simulate this by generating a placeholder image with chainage info.
    """
    # In a real system, you would have a mapping between chainage and image files
    # For now, we'll use sample images from the test directory if available
    
    # Check if we have any images in the test directory
    defective_dir = os.path.join("test", "Defective")
    non_defective_dir = os.path.join("test", "Non defective")
    
    all_images = []
    
    if os.path.exists(defective_dir):
        all_images.extend([os.path.join(defective_dir, f) for f in os.listdir(defective_dir) if f.endswith(('.jpg', '.jpeg', '.png'))])
    
    if os.path.exists(non_defective_dir):
        all_images.extend([os.path.join(non_defective_dir, f) for f in os.listdir(non_defective_dir) if f.endswith(('.jpg', '.jpeg', '.png'))])
    
    if all_images:
        # Use chainage to deterministically select an image
        image_index = int(chainage / 100) % len(all_images)
        image_path = all_images[image_index]
        
        try:
            img = Image.open(image_path)
            # Add chainage info to the image
            return img, image_path
        except Exception as e:
            st.error(f"Error loading image: {e}")
            return None, None
    else:
        # If no images are available, return None
        return None, None

# Function to display track parameters for a specific chainage
def display_track_parameters(df, chainage):
    """Display track parameters for the selected chainage"""
    # Find the closest chainage in the dataset
    closest_idx = (df['chainage'] - chainage).abs().idxmin()
    closest_data = df.iloc[closest_idx]
    
    st.subheader(f"Track Parameters at Chainage {closest_data['chainage']:.1f}m")
    
    # Create columns for parameters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Gauge", f"{closest_data['gauge']:.2f} mm", 
                 f"{closest_data['gauge'] - 1435:.2f} mm from nominal")
        st.metric("Cross Level", f"{closest_data['cross_level']:.2f} mm")
        st.metric("Vertical Acceleration", f"{closest_data['vertical_acceleration']:.3f} g")
    
    with col2:
        st.metric("Alignment Left", f"{closest_data['alignment_left']:.2f} mm")
        st.metric("Alignment Right", f"{closest_data['alignment_right']:.2f} mm")
        st.metric("Lateral Acceleration", f"{closest_data['lateral_acceleration']:.3f} g")
    
    with col3:
        st.metric("Twist", f"{closest_data['twist']:.2f} mm/m")
        st.metric("Unevenness Left", f"{closest_data['unevenness_left']:.2f} mm")
        st.metric("Unevenness Right", f"{closest_data['unevenness_right']:.2f} mm")
    
    # Display component condition
    st.info(f"Component Condition: {closest_data['component_condition']}")
    
    # Check if any parameters exceed thresholds
    flags = []
    if abs(closest_data['gauge'] - 1435) > 5.0:
        flags.append("Gauge Deviation")
    if abs(closest_data['alignment_left']) > 10.0 or abs(closest_data['alignment_right']) > 10.0:
        flags.append("Alignment")
    if abs(closest_data['twist']) > 5.0:
        flags.append("Twist")
    if abs(closest_data['cross_level']) > 7.0:
        flags.append("Cross Level")
    if abs(closest_data['vertical_acceleration']) > 0.7:
        flags.append("Vertical Acceleration")
    if abs(closest_data['lateral_acceleration']) > 0.5:
        flags.append("Lateral Acceleration")
    
    if flags:
        st.warning(f"⚠️ Flagged Parameters: {', '.join(flags)}")

# Function to create a plot for a parameter around the selected chainage
def create_parameter_plot(df, chainage, parameter, window=500):
    """Create a plot for a parameter around the selected chainage"""
    # Filter data around the selected chainage
    min_chainage = max(0, chainage - window)
    max_chainage = chainage + window
    
    filtered_df = df[(df['chainage'] >= min_chainage) & (df['chainage'] <= max_chainage)]
    
    # Create the plot
    fig = px.line(filtered_df, x='chainage', y=parameter, title=f"{parameter.capitalize()} vs Chainage")
    
    # Add a vertical line at the selected chainage
    fig.add_vline(x=chainage, line_dash="dash", line_color="red")
    
    # Add a point at the selected chainage
    closest_idx = (df['chainage'] - chainage).abs().idxmin()
    closest_chainage = df.iloc[closest_idx]['chainage']
    closest_value = df.iloc[closest_idx][parameter]
    
    fig.add_trace(go.Scatter(
        x=[closest_chainage],
        y=[closest_value],
        mode='markers',
        marker=dict(color='red', size=10),
        name='Selected Point'
    ))
    
    fig.update_layout(
        xaxis_title='Chainage (m)',
        yaxis_title=parameter.capitalize(),
        height=300
    )
    
    return fig

# Load data
df = load_data()

if df is not None:
    # Sidebar for chainage selection
    st.sidebar.header("Chainage Selection")
    
    min_chainage = float(df['chainage'].min())
    max_chainage = float(df['chainage'].max())
    
    selected_chainage = st.sidebar.slider(
        "Select chainage",
        min_value=min_chainage,
        max_value=max_chainage,
        value=(min_chainage + max_chainage) / 2,
        step=100.0
    )
    
    # Option to automatically advance through chainages
    auto_advance = st.sidebar.checkbox("Auto-advance through chainages", value=False)
    
    if auto_advance:
        speed = st.sidebar.slider("Speed (seconds per 100m)", 1, 10, 3)
        
        # Use a placeholder to update the chainage
        chainage_placeholder = st.empty()
        
        # Get the current chainage from the session state or use the selected one
        if 'current_chainage' not in st.session_state:
            st.session_state.current_chainage = selected_chainage
        
        # Update the chainage in the session state
        current_chainage = st.session_state.current_chainage
        
        # Advance the chainage
        if st.sidebar.button("Start Auto-Advance"):
            for chainage in range(int(current_chainage), int(max_chainage), 100):
                st.session_state.current_chainage = chainage
                chainage_placeholder.text(f"Current Chainage: {chainage}m")
                
                # Display the image and parameters for this chainage
                img, img_path = get_image_for_chainage(chainage)
                if img:
                    st.image(img, caption=f"Track at Chainage {chainage}m (Image: {os.path.basename(img_path)})", width='stretch')
                else:
                    st.image("https://via.placeholder.com/800x400?text=No+Track+Image+Available", width='stretch')
                
                display_track_parameters(df, chainage)
                
                # Sleep for the specified time
                import time
                time.sleep(speed)
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader(f"Track Footage at Chainage {selected_chainage:.1f}m")
        
        # Get and display the image for the selected chainage
        img, img_path = get_image_for_chainage(selected_chainage)
        if img:
            st.image(img, caption=f"Track at Chainage {selected_chainage}m (Image: {os.path.basename(img_path)})", width='stretch')
        else:
            st.image("https://via.placeholder.com/800x400?text=No+Track+Image+Available", width='stretch')
    
    with col2:
        # Display track parameters
        display_track_parameters(df, selected_chainage)
    
    # Create plots for key parameters
    st.subheader("Parameter Trends Around Selected Chainage")
    
    tab1, tab2, tab3 = st.tabs(["Geometry", "Acceleration", "Rail Wear"])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            gauge_fig = create_parameter_plot(df, selected_chainage, 'gauge')
            st.plotly_chart(gauge_fig, width='stretch')
            
            twist_fig = create_parameter_plot(df, selected_chainage, 'twist')
            st.plotly_chart(twist_fig, width='stretch')
        
        with col2:
            alignment_left_fig = create_parameter_plot(df, selected_chainage, 'alignment_left')
            st.plotly_chart(alignment_left_fig, width='stretch')
            
            cross_level_fig = create_parameter_plot(df, selected_chainage, 'cross_level')
            st.plotly_chart(cross_level_fig, width='stretch')
    
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            vert_acc_fig = create_parameter_plot(df, selected_chainage, 'vertical_acceleration')
            st.plotly_chart(vert_acc_fig, width='stretch')
        
        with col2:
            lat_acc_fig = create_parameter_plot(df, selected_chainage, 'lateral_acceleration')
            st.plotly_chart(lat_acc_fig, width='stretch')
    
    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            rail_wear_left_fig = create_parameter_plot(df, selected_chainage, 'rail_wear_left')
            st.plotly_chart(rail_wear_left_fig, width='stretch')
        
        with col2:
            rail_wear_right_fig = create_parameter_plot(df, selected_chainage, 'rail_wear_right')
            st.plotly_chart(rail_wear_right_fig, width='stretch')
    
    # Information about video sync
    st.info("""
    ### About Video Sync
    
    In a production environment, this feature would:
    
    1. Use GPS-tagged video footage from track inspection vehicles
    2. Synchronize video frames with precise chainage values
    3. Allow frame-by-frame inspection of track conditions
    4. Support multiple camera angles (top-down, side view, etc.)
    5. Provide augmented reality overlays of parameter values on video
    
    For this prototype, we're simulating the functionality using sample images.
    """)
else:
    st.error("Failed to load track data. Please ensure track_data.csv is available.")

# Footer
st.markdown("---")
st.markdown("Indian Railways Integrated Track Monitoring System (ITMS) - Video Sync Page")