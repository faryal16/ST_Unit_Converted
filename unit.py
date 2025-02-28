import streamlit as st
import requests

# 🎯 Page Configuration
st.set_page_config(page_title="Universal Unit Converter", page_icon="🔄", layout="centered")

# Initialize session state for conversion history
if "history" not in st.session_state:
    st.session_state.history = []

# 📌 Predefined Currency List
currency_codes = ["USD", "EUR", "PKR", "GBP", "INR", "AUD", "CAD", "CNY", "JPY", "AED"]


# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []
if "show_categories" not in st.session_state:
    st.session_state.show_categories = False
if "expanded_categories" not in st.session_state:
    st.session_state.expanded_categories = {category: False for category in [
        "Length 📏", "Speed 🚗", "Time ⏳", "Temperature 🌡️", "Weight ⚖️", "Volume 🧪", "Area 📐", "Currency 💰"
    ]}

# 📌 Unit Categories and Conversion Factors
unit_categories = {
    "Length 📏": {
        "Meter (m)": 1, "Kilometer (km)": 1000, "Centimeter (cm)": 0.01, "Millimeter (mm)": 0.001,
        "Mile (mi)": 1609.34, "Yard (yd)": 0.9144, "Foot (ft)": 0.3048, "Inch (in)": 0.0254,
    },
    "Speed 🚗": {
        "Meter per second (m/s)": 1, "Kilometer per hour (km/h)": 0.277778,
        "Miles per hour (mph)": 0.44704, "Feet per second (ft/s)": 0.3048,
    },
    "Time ⏳": {
        "Second (s)": 1, "Minute (min)": 60, "Hour (h)": 3600, "Day (d)": 86400,
    },
    "Temperature 🌡️": {"Celsius (°C)": "C", "Fahrenheit (°F)": "F", "Kelvin (K)": "K"},
    "Weight ⚖️": {
        "Kilogram (kg)": 1, "Gram (g)": 0.001, "Pound (lb)": 0.453592, "Ounce (oz)": 0.0283495, "Ton (t)": 1000,
    },
    "Volume 🧪": {
        "Liter (L)": 1, "Milliliter (mL)": 0.001, "Cubic Meter (m³)": 1000,
        "Gallon (gal)": 3.78541, "Cup (cup)": 0.236588,
    },
    "Area 📐": {
        "Square Meter (m²)": 1, "Square Kilometer (km²)": 1_000_000,
        "Hectare (ha)": 10_000, "Acre (ac)": 4046.86,
        "Square Foot (ft²)": 0.092903, "Square Yard (yd²)": 0.836127,
    },
    "Currency 💰": "Live Exchange Rates",
}

# 🎯 Main User Interface
st.title("🔄 Universal Unit Converter")

## 🔹 Sidebar Section
with st.sidebar:
    # ℹ️ About Section
    st.subheader("🎎About This App")
    st.write("This universal unit converter supports various measurement categories.")

    # 📌 Show/Hide Categories
    if st.button("Wanna Know?"):
        st.session_state.show_categories = not st.session_state.show_categories

    # 📌 Display Categories when button is clicked
    if st.session_state.show_categories:
        st.subheader("📌 Supported Categories")
        for category in unit_categories.keys():
            # Toggle each category on click
            if st.button(category):
                st.session_state.expanded_categories[category] = not st.session_state.expanded_categories[category]

            # Show units only if the category is expanded
            if st.session_state.expanded_categories[category]:
                if isinstance(unit_categories[category], dict):
                    st.write(", ".join(unit_categories[category]))
                else:
                    st.write(unit_categories[category])  # For Currency case

    # ⚙️ Settings Section
    st.subheader("⚙️ Settings")
    if st.button("Clear History ❌"):
        st.session_state.history = []
        st.success("History cleared!")

        


# 📌 User Selection
category = st.selectbox("Select a Category", list(unit_categories.keys()))

# 🏷️ Currency Conversion (Special Case)
if category == "Currency 💰":
    st.write("💱 **Live Currency Exchange Converter**")
    amount = st.number_input("Enter amount", min_value=0.0, format="%.2f")
    from_currency = st.selectbox("From Currency", currency_codes, index=currency_codes.index("USD"))
    to_currency = st.selectbox("To Currency", currency_codes, index=currency_codes.index("PKR"))

    if st.button("Convert 💰"):
        url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
        try:
            response = requests.get(url).json()
            if to_currency in response["rates"]:
                converted_amount = amount * response["rates"][to_currency]
                result = f"💲 {amount} {from_currency} = {converted_amount:.2f} {to_currency}"
                st.session_state.history.append(result)
                st.success(result)
            else:
                st.error("❌ Invalid currency code.")
        except:
            st.error("⚠️ Error fetching exchange rates.")

else:
    # 🎛️ Standard Unit Conversion
    units = list(unit_categories[category].keys())
    from_unit = st.selectbox("Convert from", units)
    to_unit = st.selectbox("Convert to", units)
    value = st.number_input("Enter Value", format="%.2f")

    converted_value = None  # Initialize before using
    if st.button("Convert 🔄"):
        if category == "Temperature 🌡️":
            # 🌡️ Special Case for Temperature Conversion
            def convert_temperature(val, from_u, to_u):
                if from_u == to_u:
                    return val
                if from_u == "Celsius (°C)":
                    return val * 9/5 + 32 if to_u == "Fahrenheit (°F)" else val + 273.15
                if from_u == "Fahrenheit (°F)":
                    return (val - 32) * 5/9 if to_u == "Celsius (°C)" else (val - 32) * 5/9 + 273.15
                if from_u == "Kelvin (K)":
                    return val - 273.15 if to_u == "Celsius (°C)" else (val - 273.15) * 9/5 + 32
            
            converted_value = convert_temperature(value, from_unit, to_unit)
        else:
            # Standard Conversion
            converted_value = value * (unit_categories[category][from_unit] / unit_categories[category][to_unit])

        result = f"✅ {value} {from_unit} = {converted_value:.4f} {to_unit}"
        st.session_state.history.append(result)
        st.success(result)

# 📝 Summary Section
st.write("---")
st.write("📊 **Summary of Your Conversion:**")
st.write(f"🔹 **Category:** {category}")
if category == "Currency 💰":
    if 'converted_amount' in locals():
        st.write(f"🔹 **Amount:** {amount} {from_currency} ➝ {converted_amount:.2f} {to_currency}")
else:
    if converted_value is not None:
        st.write(f"🔹 **Converted:** {value} {from_unit} ➝ {converted_value:.4f} {to_unit}")
    else:
        st.write("🔹 **Converted:** N/A")

# 📜 **Conversion History**
st.write("---")
st.subheader("📜 Conversion History")
if st.session_state.history:
    for entry in st.session_state.history[::-1]:  # Show latest first
        st.write(entry)
else:
    st.write("No conversions yet. Start converting! 🔄")
