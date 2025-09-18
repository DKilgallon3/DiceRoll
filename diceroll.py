import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os

data_file = "dice_rolls.csv"

# Ensure the file exists and has headers
if not os.path.exists(data_file) or os.path.getsize(data_file) == 0:
    pd.DataFrame(columns=["sum"]).to_csv(data_file, index=False)

# Now safely read the file
df = pd.read_csv(data_file)


# File to store roll data
data_file = "dice_rolls.csv"

# Initialize or load data

if os.path.exists(data_file) and os.path.getsize(data_file) > 0:
    df = pd.read_csv(data_file)
else:
    df = pd.DataFrame(columns=["sum"])

st.title("🎲 Live Dice Roll Distribution")
st.markdown("Enter the sum of your two 10-sided dice rolls (2–20):")

# User input
roll = st.number_input("Dice Roll Sum", min_value=2, max_value=20, step=1)

if st.button("Submit Roll"):
    df = pd.concat([df, pd.DataFrame([{"sum": roll}])], ignore_index=True)
    df.to_csv(data_file, index=False)
    st.success("Roll submitted!")

# Display histogram with normal distribution overlay
if not df.empty:
    mean = df["sum"].astype(float).mean()
    std = df["sum"].astype(float).std()

    # Histogram
    fig = px.histogram(df, x="sum", nbins=19, histnorm='probability density',
                       title="Distribution of Dice Roll Sums")

    # Normal distribution curve
    x_vals = np.linspace(2, 20, 100)
    y_vals = (1 / (std * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x_vals - mean) / std) ** 2)
    fig.add_scatter(x=x_vals, y=y_vals, mode='lines', name='Normal Curve')

    st.plotly_chart(fig)
    st.write(f"Total Rolls: {len(df)} | Mean: {mean:.2f} | Std Dev: {std:.2f}")
else:
    st.info("No rolls submitted yet. Be the first!")


