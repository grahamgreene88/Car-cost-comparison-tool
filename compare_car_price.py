# Import libraries
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Title and description
st.title("Cost of Ownership Comparison: ICE vs. EV")
st.write(
    "This app compares the total cost of ownership of an internal combustion \
    engine (ICE) and an electric vehicle (EV) over a 15-year period. Only \
    the purchase price and fuel/electricity costs are considered."
)

# Input fields
st.header("Input Parameters")
ev_price = st.number_input("EV after-tax purchase price ($)", value=25000, step=5000)
ice_price = st.number_input("ICE after-tax purchase price ($)", value=None, step=5000)
annual_km = st.number_input(
    "Annual Distance Driven (km)",
    value=None,
    step=500,
    placeholder="The average annual distance traveled by car in Canada is about 15000 km.",
)
ev_efficiency = st.number_input(
    "EV Efficiency (kWh per 100 km)",
    value=None,
    step=1,
    placeholder="A typical EV efficiency is 15 kWh/100km",
)
electricity_cost = st.number_input(
    "Electricity Cost (cents/kWh)",
    value=None,
    step=0.2,
    placeholder="A typical electricity cost overnight in Ontario is 2.8cents/kWh",
)
ice_efficiency = st.number_input(
    "ICE Fuel Efficiency (L per 100 km)",
    value=None,
    step=0.2,
    placeholder="The fuel efficiency of a 2024 Honda Civic Sedan is 6.9L/100km",
)
gasoline_cost = st.number_input(
    "Gasoline Cost (cents/L)",
    value=None,
    step=10,
    placeholder="A typical fuel price in Ontario Nov 2024 is 150 cents/L",
)


# Define calculation function
def calculate_costs(
    ev_price,
    ice_price,
    annual_km,
    ev_efficiency,
    electricity_cost,
    ice_efficiency,
    gasoline_cost,
):
    """This function takes in the variables defined for the EV and ICE by the user
    and calculates the cost for each option after each year.

    Args:
        ev_price (int): _description_
        ice_price (int): _description_
        annual_km (int): _description_
        ev_efficiency (int): _description_
        electricity_cost (float): _description_
        ice_efficiency (float): _description_
        gasoline_cost (int): _description_
    """
    years = np.arange(1, 16)
    ev_fuel_cost = (
        annual_km / 100 * ev_efficiency * electricity_cost * 1 / 100
    )  # Convert cents to $
    ice_fuel_cost = (
        annual_km / 100 * ice_efficiency * gasoline_cost * 1 / 100
    )  # Convert cents to $

    ev_total_cost = ev_price + ev_fuel_cost * years
    ice_total_cost = ice_price + ice_fuel_cost * years

    return years, ev_total_cost, ice_total_cost


# ev_price = 40000
# ice_price = 30000
# annual_km = 15000
# ev_efficiency = 15
# electricity_cost = 2.8
# ice_efficiency = 6.9
# gasoline_cost = 150
# Perform calculation
years, ev_total_cost, ice_total_cost = calculate_costs(
    ev_price,
    ice_price,
    annual_km,
    ev_efficiency,
    electricity_cost,
    ice_efficiency,
    gasoline_cost,
)

# Display Graph
st.header(" Cost of Ownership Over Time")
fig, ax = plt.subplots()
ax.plot(years, ice_total_cost, label="ICE Total Cost", color="red", marker="o")
ax.plot(years, ev_total_cost, label="EVTotal Cost", color="blue", marker="o")
ax.set_title("Cost of Ownership Over 15 Years")
ax.set_xlabel("Years")
ax.set_ylabel("Total Cost ($)")
ax.legend()
ax.grid(True)

st.pyplot(fig)

# Results Summary
st.header("Results Summary")
st.write(f"EV Fuel Cost per Year: ${ev_total_cost[0] - ev_price:.2f}")
st.write(f"ICE Fuel Cost per Year: ${ice_total_cost[0] - ice_price:.2f}")
st.write("Break-even Analysis:")
if ev_total_cost[-1] < ice_total_cost[-1]:
    st.write(
        f"Over 15 years, the EV is cheaper by ${ice_total_cost[-1] - ev_total_cost[-1]:.2f}."
    )
else:
    st.write(
        f"Over 15 years, the ICE car is cheaper by ${ev_total_cost[-1] - ice_total_cost[-1]:.2f}."
    )
