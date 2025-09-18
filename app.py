import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from scipy import signal
import io
import json
import base64

# Set page configuration
st.set_page_config(
    page_title="Indian Railways Track Monitoring System",
    page_icon="🚆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define constants
NOMINAL_GAUGE = 1435.0  # Standard gauge in mm
GAUGE_THRESHOLD = 5.0  # mm deviation threshold
ALIGNMENT_THRESHOLD = 10.0  # mm threshold
TWIST_THRESHOLD = 5.0  # mm/m threshold
CROSS_LEVEL_THRESHOLD = 7.0  # mm threshold
UNEVENNESS_THRESHOLD = 7.0  # mm threshold
VERTICAL_ACC_THRESHOLD = 0.7  # g threshold
LATERAL_ACC_THRESHOLD = 0.5  # g threshold

# Preprocessing functions
def load_data(file):
    """Load data from uploaded CSV file"""
    try:
        df = pd.read_csv(file)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

def handle_missing_values(df):
    """Handle missing values in the dataframe"""
    # Fill numeric columns with their median values
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    for col in numeric_cols:
        df[col] = df[col].fillna(df[col].median())
    
    # Fill categorical columns with mode
    categorical_cols = df.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        df[col] = df[col].fillna(df[col].mode()[0] if not df[col].mode().empty else "Unknown")
    
    return df

def apply_filter(df, column, filter_type='rolling', window_size=5, order=3):
    """Apply noise filtering to a column"""
    if filter_type == 'rolling':
        # Simple rolling average
        df[f"{column}_filtered"] = df[column].rolling(window=window_size, center=True).mean()
        # Fill NaN values at the edges
        df[f"{column}_filtered"] = df[f"{column}_filtered"].fillna(df[column])
    
    elif filter_type == 'butterworth':
        # Butterworth filter
        b, a = signal.butter(order, 1/window_size)
        df[f"{column}_filtered"] = signal.filtfilt(b, a, df[column])
    
    elif filter_type == 'savgol':
        # Savitzky-Golay filter
        # Ensure polyorder (order) is less than window_size
        if order >= window_size:
            order = window_size - 1
        # Ensure window_size is odd
        if window_size % 2 == 0:
            window_size += 1
        df[f"{column}_filtered"] = signal.savgol_filter(df[column], window_size, order)
    
    return df

# Analysis functions
def compute_gauge_deviation(df):
    """Compute gauge deviation from nominal value"""
    df['gauge_deviation'] = df['gauge'] - NOMINAL_GAUGE
    df['gauge_deviation_flag'] = np.abs(df['gauge_deviation']) > GAUGE_THRESHOLD
    return df

def compute_alignment_error(df):
    """Compute alignment error"""
    # Combine left and right alignment for total error
    df['alignment_total'] = np.sqrt(df['alignment_left']**2 + df['alignment_right']**2)
    df['alignment_flag'] = df['alignment_total'] > ALIGNMENT_THRESHOLD
    return df

def compute_twist_error(df):
    """Compute twist error"""
    df['twist_flag'] = np.abs(df['twist']) > TWIST_THRESHOLD
    return df

def compute_unevenness(df):
    """Compute unevenness"""
    df['unevenness_total'] = (df['unevenness_left'] + df['unevenness_right']) / 2
    df['unevenness_flag'] = df['unevenness_total'] > UNEVENNESS_THRESHOLD
    return df

def compute_acceleration_peaks(df):
    """Compute peak acceleration values"""
    df['vertical_acc_flag'] = df['vertical_acceleration'] > VERTICAL_ACC_THRESHOLD
    df['lateral_acc_flag'] = df['lateral_acceleration'] > LATERAL_ACC_THRESHOLD
    return df

def flag_segments(df):
    """Flag segments that exceed thresholds"""
    # Create a combined flag column
    df['flagged'] = (
        df['gauge_deviation_flag'] | 
        df['alignment_flag'] | 
        df['twist_flag'] | 
        df['unevenness_flag'] | 
        df['vertical_acc_flag'] | 
        df['lateral_acc_flag']
    )
    return df

# Visualization functions
def plot_parameter_vs_chainage(df, parameter, title, y_label, threshold=None):
    """Create a line chart of parameter vs chainage"""
    fig = px.line(df, x='chainage', y=parameter, title=title)
    
    # Add threshold lines if provided
    if threshold is not None:
        fig.add_hline(y=threshold, line_dash="dash", line_color="red", annotation_text=f"Threshold: {threshold}")
        fig.add_hline(y=-threshold, line_dash="dash", line_color="red")
    
    # Add markers for flagged points
    flag_column = f"{parameter}_flag" if f"{parameter}_flag" in df.columns else None
    if flag_column and flag_column in df.columns:
        flagged_points = df[df[flag_column]]
        if not flagged_points.empty:
            fig.add_trace(go.Scatter(
                x=flagged_points['chainage'],
                y=flagged_points[parameter],
                mode='markers',
                marker=dict(color='red', size=8),
                name='Flagged Points'
            ))
    
    fig.update_layout(
        xaxis_title='Chainage (m)',
        yaxis_title=y_label,
        height=400
    )
    return fig

def plot_heatmap(df):
    """Create a heatmap of track parameters"""
    # Select numeric columns for heatmap
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    # Exclude chainage and flag columns
    cols_to_plot = [col for col in numeric_cols if 'flag' not in col and col != 'chainage']
    
    # Create a correlation matrix
    corr_matrix = df[cols_to_plot].corr()
    
    fig = px.imshow(
        corr_matrix,
        text_auto=True,
        aspect="auto",
        color_continuous_scale='RdBu_r',
        title="Parameter Correlation Heatmap"
    )
    
    fig.update_layout(height=600)
    return fig

def plot_rail_profile(df):
    """Create a rail profile plot if data is available"""
    if 'rail_wear_left' in df.columns and 'rail_wear_right' in df.columns:
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df['chainage'],
            y=df['rail_wear_left'],
            mode='lines',
            name='Left Rail Wear'
        ))
        
        fig.add_trace(go.Scatter(
            x=df['chainage'],
            y=df['rail_wear_right'],
            mode='lines',
            name='Right Rail Wear'
        ))
        
        fig.update_layout(
            title="Rail Wear Profile",
            xaxis_title='Chainage (m)',
            yaxis_title='Rail Wear (mm)',
            height=400
        )
        return fig
    else:
        return None

def create_download_link(df, filename, link_text):
    """Create a download link for the processed data"""
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{link_text}</a>'
    return href

def create_download_link_json(df, filename, link_text):
    """Create a download link for JSON data"""
    json_str = df.to_json(orient='records')
    b64 = base64.b64encode(json_str.encode()).decode()
    href = f'<a href="data:file/json;base64,{b64}" download="{filename}">{link_text}</a>'
    return href

# Main application
def main():
    # Add a title and description
    st.title("🚆 Indian Railways Integrated Track Monitoring System")
    st.markdown("""
    This dashboard provides analysis and visualization of track monitoring data.
    Upload your CSV file with track parameters to begin analysis.
    """)
    
    # Sidebar for file upload and parameter selection
    st.sidebar.header("Data Input")
    uploaded_file = st.sidebar.file_uploader("Upload CSV file", type=["csv"])
    
    # Default to sample data if no file is uploaded
    use_sample_data = st.sidebar.checkbox("Use sample data", value=True if not uploaded_file else False)
    
    # Load data
    df = None
    if uploaded_file:
        df = load_data(uploaded_file)
    elif use_sample_data:
        df = pd.read_csv("track_data.csv")
    
    if df is not None:
        # Display raw data
        st.sidebar.header("Data Preview")
        if st.sidebar.checkbox("Show raw data", value=False):
            st.subheader("Raw Data")
            st.dataframe(df.head(10))
        
        # Preprocessing options
        st.sidebar.header("Preprocessing")
        handle_missing = st.sidebar.checkbox("Handle missing values", value=True)
        
        filter_type = st.sidebar.selectbox(
            "Filter type",
            ["None", "rolling", "butterworth", "savgol"],
            index=1
        )
        
        window_size = st.sidebar.slider("Filter window size", 3, 21, 5, step=2)
        filter_order = st.sidebar.slider("Filter order (for Butterworth/Savgol)", 1, 5, 3)
        
        # Apply preprocessing
        if handle_missing:
            df = handle_missing_values(df)
        
        # Apply filtering to selected columns
        if filter_type != "None":
            # Get available numeric columns
            available_numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
            
            # Set default columns for filtering, ensuring they exist in the dataset
            default_cols = []
            for col in ['gauge', 'alignment_left', 'alignment_right', 'twist', 'cross_level']:
                if col in available_numeric_cols:
                    default_cols.append(col)
            
            # If no default columns are available, don't set a default
            if not default_cols:
                default_cols = []
            
            filter_columns = st.sidebar.multiselect(
                "Select columns to filter",
                available_numeric_cols,
                default=default_cols
            )
            
            for col in filter_columns:
                df = apply_filter(df, col, filter_type, window_size, filter_order)
        
        # Analysis options
        st.sidebar.header("Analysis")
        run_analysis = st.sidebar.checkbox("Run analysis", value=True)
        
        if run_analysis:
            # Compute analysis metrics
            df = compute_gauge_deviation(df)
            df = compute_alignment_error(df)
            df = compute_twist_error(df)
            df = compute_unevenness(df)
            df = compute_acceleration_peaks(df)
            df = flag_segments(df)
            
            # Chainage range selection
            st.sidebar.header("Chainage Range")
            min_chainage = float(df['chainage'].min())
            max_chainage = float(df['chainage'].max())
            
            chainage_range = st.sidebar.slider(
                "Select chainage range",
                min_value=min_chainage,
                max_value=max_chainage,
                value=(min_chainage, max_chainage)
            )
            
            # Filter data based on selected chainage range
            filtered_df = df[(df['chainage'] >= chainage_range[0]) & (df['chainage'] <= chainage_range[1])]
            
            # Display analysis results
            st.header("Track Analysis Results")
            
            # Create tabs for different visualizations
            tab1, tab2, tab3, tab4 = st.tabs(["Geometry Parameters", "Acceleration", "Rail Profile", "Anomalies"])
            
            with tab1:
                st.subheader("Track Geometry Parameters")
                
                # Create two columns for charts
                col1, col2 = st.columns(2)
                
                with col1:
                    # Gauge deviation plot
                    gauge_fig = plot_parameter_vs_chainage(
                        filtered_df, 'gauge_deviation', 
                        'Gauge Deviation vs Chainage', 
                        'Deviation (mm)', 
                        GAUGE_THRESHOLD
                    )
                    st.plotly_chart(gauge_fig, width='stretch')
                    
                    # Cross level plot
                    cross_level_fig = plot_parameter_vs_chainage(
                        filtered_df, 'cross_level', 
                        'Cross Level vs Chainage', 
                        'Cross Level (mm)', 
                        CROSS_LEVEL_THRESHOLD
                    )
                    st.plotly_chart(cross_level_fig, width='stretch')
                
                with col2:
                    # Alignment plot
                    alignment_fig = plot_parameter_vs_chainage(
                        filtered_df, 'alignment_total', 
                        'Alignment Error vs Chainage', 
                        'Alignment Error (mm)', 
                        ALIGNMENT_THRESHOLD
                    )
                    st.plotly_chart(alignment_fig, width='stretch')
                    
                    # Twist plot
                    twist_fig = plot_parameter_vs_chainage(
                        filtered_df, 'twist', 
                        'Twist vs Chainage', 
                        'Twist (mm/m)', 
                        TWIST_THRESHOLD
                    )
                    st.plotly_chart(twist_fig, width='stretch')
            
            with tab2:
                st.subheader("Acceleration Measurements")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Vertical acceleration plot
                    vert_acc_fig = plot_parameter_vs_chainage(
                        filtered_df, 'vertical_acceleration', 
                        'Vertical Acceleration vs Chainage', 
                        'Acceleration (g)', 
                        VERTICAL_ACC_THRESHOLD
                    )
                    st.plotly_chart(vert_acc_fig, width='stretch')
                
                with col2:
                    # Lateral acceleration plot
                    lat_acc_fig = plot_parameter_vs_chainage(
                        filtered_df, 'lateral_acceleration', 
                        'Lateral Acceleration vs Chainage', 
                        'Acceleration (g)', 
                        LATERAL_ACC_THRESHOLD
                    )
                    st.plotly_chart(lat_acc_fig, width='stretch')
            
            with tab3:
                st.subheader("Rail Profile and Wear")
                
                # Rail profile plot
                rail_profile_fig = plot_rail_profile(filtered_df)
                if rail_profile_fig:
                    st.plotly_chart(rail_profile_fig, width='stretch')
                else:
                    st.info("Rail profile data not available in the dataset.")
                
                # Unevenness plot
                unevenness_fig = plot_parameter_vs_chainage(
                    filtered_df, 'unevenness_total', 
                    'Track Unevenness vs Chainage', 
                    'Unevenness (mm)', 
                    UNEVENNESS_THRESHOLD
                )
                st.plotly_chart(unevenness_fig, width='stretch')
            
            with tab4:
                st.subheader("Anomaly Detection")
                
                # Heatmap
                heatmap_fig = plot_heatmap(filtered_df)
                st.plotly_chart(heatmap_fig, width='stretch')
                
                # Flagged segments table
                st.subheader("Flagged Track Segments")
                flagged_segments = filtered_df[filtered_df['flagged']]
                
                if not flagged_segments.empty:
                    # Display only relevant columns
                    display_cols = ['chainage', 'gauge_deviation', 'alignment_total', 
                                   'twist', 'cross_level', 'unevenness_total',
                                   'vertical_acceleration', 'lateral_acceleration']
                    
                    st.dataframe(flagged_segments[display_cols])
                    
                    # Count of different types of flags
                    st.subheader("Flag Distribution")
                    flag_counts = {
                        'Gauge Deviation': flagged_segments['gauge_deviation_flag'].sum(),
                        'Alignment': flagged_segments['alignment_flag'].sum(),
                        'Twist': flagged_segments['twist_flag'].sum(),
                        'Unevenness': flagged_segments['unevenness_flag'].sum(),
                        'Vertical Acceleration': flagged_segments['vertical_acc_flag'].sum(),
                        'Lateral Acceleration': flagged_segments['lateral_acc_flag'].sum()
                    }
                    
                    fig = px.bar(
                        x=list(flag_counts.keys()),
                        y=list(flag_counts.values()),
                        labels={'x': 'Parameter', 'y': 'Count'},
                        title='Number of Flagged Segments by Parameter'
                    )
                    st.plotly_chart(fig, width='stretch')
                else:
                    st.info("No flagged segments found in the selected chainage range.")
            
            # Video placeholder
            st.header("Track Video Sync")
            st.info("Video sync feature would display track footage corresponding to selected chainage.")
            
            # Placeholder for video
            st.image("https://via.placeholder.com/800x400?text=Track+Video+Placeholder", width='stretch')
            
            # Export options
            st.header("Export Data")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(create_download_link(filtered_df, "processed_track_data.csv", "Download CSV"), unsafe_allow_html=True)
            
            with col2:
                st.markdown(create_download_link_json(filtered_df, "processed_track_data.json", "Download JSON"), unsafe_allow_html=True)
    else:
        st.info("Please upload a CSV file or use the sample data to begin analysis.")

if __name__ == "__main__":
    main()