import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.title("Advanced Unit Converter")

# Import dictionaries from units.py
from units import length_units, weight_units, area_units, temperature_units, time_units, volume_units

# Category selection
category = st.selectbox("Choose Category", ["Length", "Weight", "Volume", "Temperature", "Area", "Time"])

# Define units and current dictionary based on category
if category == "Length":
    units = list(length_units.keys())
    current_dict = {k: v for k, v in length_units.items() if v is not None}
elif category == "Weight":
    units = list(weight_units.keys())
    current_dict = {k: v for k, v in weight_units.items() if v is not None}
elif category == "Volume":
    units = list(volume_units.keys())
    current_dict = {k: v for k, v in volume_units.items() if v is not None}
elif category == "Temperature":
    units = list(temperature_units.keys())
    current_dict = {k: v for k, v in temperature_units.items() if v is not None}
elif category == "Area":
    units = list(area_units.keys())
    current_dict = {k: v for k, v in area_units.items() if v is not None}
elif category == "Time":
    units = list(time_units.keys())
    current_dict = {k: v for k, v in time_units.items() if v is not None}
else:
    units = []
    current_dict = {}

# General conversion function
def convert(value, from_unit, to_unit, category, units_dict):
    if category == "Temperature":
        if from_unit == "celsius":
            celsius = value
        elif from_unit == "fahrenheit":
            celsius = (value - 32) * 5 / 9
        elif from_unit == "kelvin":
            celsius = value - 273.15
        
        if to_unit == "celsius":
            return celsius
        elif to_unit == "fahrenheit":
            return (celsius * 9 / 5) + 32
        elif to_unit == "kelvin":
            return celsius + 273.15
    else:
        return value * units_dict[from_unit] / units_dict[to_unit]

# User inputs
value = st.number_input("Enter Value", min_value=0.0)
from_unit = st.selectbox("From Unit", units)
to_unit = st.selectbox("To Unit", units)

# Conversion trigger and output
if st.button("Convert"):
    if from_unit == to_unit:
        st.warning("Same units selected! No conversion needed.")
    else:
        try:
            result = convert(value, from_unit, to_unit, category, current_dict)
            st.write(f"{value} {from_unit} = {result:.2f} {to_unit}")
        except KeyError:
            st.error("Error: Invalid unit selection.")
        except ZeroDivisionError:
            st.error("Error: Division by zero occurred.")

# Visualization with Plotly
if st.checkbox("Show Visualization"):
    if from_unit == to_unit:
        st.warning("No visualization needed for same units.")
    else:
        try:
            # Generate data for plot
            x = np.linspace(0, value * 2, 100)
            y = [convert(val, from_unit, to_unit, category, current_dict) for val in x]

            # Create Plotly figure
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name=f"{from_unit} to {to_unit}"))
            fig.update_layout(
                title=f"Conversion from {from_unit} to {to_unit}",
                xaxis_title=f"{from_unit}",
                yaxis_title=f"{to_unit}",
                showlegend=True,
                template="plotly_white",
                width=800,
                height=400
            )
            fig.update_traces(hovertemplate="%{x:.2f} " + from_unit + " = %{y:.2f} " + to_unit)

            # Display in Streamlit
            st.write("Generating interactive plot...")
            st.plotly_chart(fig, use_container_width=True)

        except KeyError:
            st.error("Error: Invalid unit selection for visualization.")
        except ZeroDivisionError:
            st.error("Error: Division by zero in visualization.")