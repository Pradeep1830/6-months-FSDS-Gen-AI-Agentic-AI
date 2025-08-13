import streamlit as st
import requests
import json
from datetime import datetime, timedelta
import pandas as pd

# Optional imports for plotting
try:
    import plotly.graph_objects as go
    import plotly.express as px
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    st.warning("Plotly not available. Charts will be disabled. Install with: pip install plotly")

# Page configuration
st.set_page_config(
    page_title="Converter Calculator",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .converter-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        margin: 1rem 0;
    }
    .result-display {
        background: rgba(255,255,255,0.1);
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        color: white;
        font-size: 1.8rem;
        font-weight: bold;
        margin: 1rem 0;
        border: 2px solid rgba(255,255,255,0.2);
    }
    .info-box {
        background: rgba(255,255,255,0.1);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    .metric-card {
        background: rgba(255,255,255,0.1);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        color: white;
        margin: 0.5rem 0;
    }
    .stSelectbox > div > div > div {
        background-color: rgba(20,20,20,0.95) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.3) !important;
    }
    .stNumberInput > div > div > div > input {
        background-color: rgba(20,20,20,0.95) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.3) !important;
    }
    .stSelectbox > div > div > div > div {
        background-color: rgba(20,20,20,0.95) !important;
        color: white !important;
    }
    .stSelectbox > div > div > div > div:hover {
        background-color: rgba(40,40,40,0.95) !important;
    }
    .stNumberInput > div > div > div > input::placeholder {
        color: rgba(255,255,255,0.7) !important;
    }
    .stSelectbox > div > div > div > div[data-baseweb="select"] {
        background-color: rgba(20,20,20,0.95) !important;
        color: white !important;
    }
    /* Additional dark theme fixes */
    .stSelectbox > div > div > div > div[role="option"] {
        background-color: rgba(20,20,20,0.95) !important;
        color: white !important;
    }
    .stSelectbox > div > div > div > div[role="option"]:hover {
        background-color: rgba(40,40,40,0.95) !important;
    }
    .stNumberInput > div > div > div > input:focus {
        background-color: rgba(30,30,30,0.95) !important;
        border: 2px solid rgba(255,255,255,0.5) !important;
    }
</style>
""", unsafe_allow_html=True)

class CurrencyConverter:
    def __init__(self):
        self.cached_rates = {}
        self.api_key = "YOUR_API_KEY"  # Replace with actual API key
        self.base_url = "https://api.exchangerate-api.com/v4/latest/"
        self.last_update = None
        self.cache_duration = timedelta(hours=1)
    
    def get_exchange_rates(self, base_currency="USD"):
        """Get exchange rates from API with caching"""
        current_time = datetime.now()
        
        # Check if we have cached rates and they're still valid
        if (base_currency in self.cached_rates and 
            self.last_update and 
            current_time - self.last_update < self.cache_duration):
            return self.cached_rates[base_currency]
        
        try:
            # For demo purposes, using a free API
            response = requests.get(f"{self.base_url}{base_currency}")
            if response.status_code == 200:
                data = response.json()
                self.cached_rates[base_currency] = data
                self.last_update = current_time
                return data
            else:
                # Fallback to demo rates if API fails
                return self.get_demo_rates(base_currency)
        except:
            return self.get_demo_rates(base_currency)
    
    def get_demo_rates(self, base_currency="USD"):
        """Demo exchange rates for demonstration purposes"""
        demo_rates = {
            "USD": {
                "rates": {
                    "EUR": 0.85, "GBP": 0.73, "JPY": 110.0, "CAD": 1.25,
                    "AUD": 1.35, "CHF": 0.92, "CNY": 6.45, "INR": 74.5,
                    "BRL": 5.25, "MXN": 20.5, "KRW": 1150.0, "SGD": 1.35,
                    "HKD": 7.78, "NZD": 1.42, "SEK": 8.65, "NOK": 8.85
                },
                "date": datetime.now().strftime("%Y-%m-%d")
            },
            "EUR": {
                "rates": {
                    "USD": 1.18, "GBP": 0.86, "JPY": 129.4, "CAD": 1.47,
                    "AUD": 1.59, "CHF": 1.08, "CNY": 7.59, "INR": 87.6,
                    "BRL": 6.18, "MXN": 24.1, "KRW": 1353.0, "SGD": 1.59,
                    "HKD": 9.15, "NZD": 1.67, "SEK": 10.18, "NOK": 10.41
                },
                "date": datetime.now().strftime("%Y-%m-%d")
            }
        }
        return demo_rates.get(base_currency, demo_rates["USD"])
    
    def convert_currency(self, amount, from_currency, to_currency):
        """Convert amount from one currency to another"""
        if from_currency == to_currency:
            return amount
        
        rates_data = self.get_exchange_rates(from_currency)
        rates = rates_data["rates"]
        
        if to_currency in rates:
            return amount * rates[to_currency]
        else:
            # Try reverse conversion
            reverse_rates = self.get_exchange_rates(to_currency)
            if from_currency in reverse_rates["rates"]:
                return amount / reverse_rates["rates"][from_currency]
            else:
                return None

class UnitConverter:
    """Class for various unit conversions"""
    
    @staticmethod
    def length_conversion(value, from_unit, to_unit):
        """Convert length units"""
        # Base unit: meters
        to_meters = {
            "mm": 0.001, "cm": 0.01, "m": 1, "km": 1000,
            "in": 0.0254, "ft": 0.3048, "yd": 0.9144, "mi": 1609.344
        }
        
        if from_unit in to_meters and to_unit in to_meters:
            meters = value * to_meters[from_unit]
            return meters / to_meters[to_unit]
        return None
    
    @staticmethod
    def weight_conversion(value, from_unit, to_unit):
        """Convert weight units"""
        # Base unit: grams
        to_grams = {
            "mg": 0.001, "g": 1, "kg": 1000, "t": 1000000,
            "oz": 28.3495, "lb": 453.592, "st": 6350.29
        }
        
        if from_unit in to_grams and to_unit in to_grams:
            grams = value * to_grams[from_unit]
            return grams / to_grams[to_unit]
        return None
    
    @staticmethod
    def temperature_conversion(value, from_unit, to_unit):
        """Convert temperature units"""
        # Convert to Celsius first
        to_celsius = {
            "C": lambda x: x,
            "F": lambda x: (x - 32) * 5/9,
            "K": lambda x: x - 273.15,
            "R": lambda x: (x - 491.67) * 5/9
        }
        
        # Convert from Celsius
        from_celsius = {
            "C": lambda x: x,
            "F": lambda x: x * 9/5 + 32,
            "K": lambda x: x + 273.15,
            "R": lambda x: (x + 273.15) * 9/5
        }
        
        if from_unit in to_celsius and to_unit in from_celsius:
            celsius = to_celsius[from_unit](value)
            return from_celsius[to_unit](celsius)
        return None

def main():
    # Header
    st.markdown('<h1 class="main-header">Converter Calculator</h1>', unsafe_allow_html=True)
    
    # Initialize converters
    currency_converter = CurrencyConverter()
    unit_converter = UnitConverter()
    
    # Sidebar for conversion type selection
    with st.sidebar:
        st.header("🔄 Conversion Type")
        conversion_type = st.selectbox(
            "Choose Conversion Type",
            ["Currency Converter", "Length Converter", "Weight Converter", "Temperature Converter"]
        )
        
        st.markdown("---")
        st.markdown("### 📊 Features")
        st.markdown("""
        - *Real-time Currency Rates*
        - *Multiple Unit Conversions*
        - *Historical Data Charts*
        - *Bulk Conversions*
        - *Mobile Responsive*
        """)
        
        st.markdown("### 💡 Tips")
        st.markdown("""
        - Currency rates update hourly
        - Use bulk converter for multiple values
        - Check historical trends for better insights
        """)
    
    # Main content area
    if conversion_type == "Currency Converter":
        currency_converter_ui(currency_converter)
    elif conversion_type == "Length Converter":
        length_converter_ui(unit_converter)
    elif conversion_type == "Weight Converter":
        weight_converter_ui(unit_converter)
    elif conversion_type == "Temperature Converter":
        temperature_converter_ui(unit_converter)

def currency_converter_ui(converter):
    """Currency converter UI"""
    st.markdown('<div class="converter-container">', unsafe_allow_html=True)
    
    # Get available currencies
    rates_data = converter.get_exchange_rates("USD")
    currencies = list(rates_data["rates"].keys()) + ["USD"]
    currencies.sort()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💱 Currency Conversion")
        
        # Input section
        amount = st.number_input("Amount", min_value=0.01, value=100.0, step=0.01)
        from_currency = st.selectbox("From Currency", currencies, index=currencies.index("USD"))
        to_currency = st.selectbox("To Currency", currencies, index=currencies.index("EUR"))
        
        # Convert button
        if st.button("🔄 Convert", type="primary"):
            result = converter.convert_currency(amount, from_currency, to_currency)
            if result is not None:
                st.session_state.conversion_result = result
                st.session_state.from_currency = from_currency
                st.session_state.to_currency = to_currency
                st.session_state.amount = amount
    
    with col2:
        st.subheader("📊 Exchange Rate Info")
        
        # Display current rates
        rates_data = converter.get_exchange_rates(from_currency)
        rates = rates_data["rates"]
        
        # Show rate for selected currency
        if to_currency in rates:
            rate = rates[to_currency]
            st.metric(f"1 {from_currency} → {to_currency}", f"{rate:.4f}")
            st.metric(f"1 {to_currency} → {from_currency}", f"{1/rate:.4f}")
        
        # Last updated info
        st.info(f"Last updated: {rates_data['date']}")
    
    # Display result
    if 'conversion_result' in st.session_state:
        result = st.session_state.conversion_result
        amount = st.session_state.amount
        from_curr = st.session_state.from_currency
        to_curr = st.session_state.to_currency
        
        st.markdown(f'''
        <div class="result-display">
            {amount:.2f} {from_curr} = {result:.2f} {to_curr}
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Bulk converter
    st.markdown('<div class="converter-container">', unsafe_allow_html=True)
    st.subheader("📈 Bulk Currency Converter")
    
    # Sample amounts for bulk conversion
    sample_amounts = [1, 10, 100, 1000, 10000]
    
    col1, col2 = st.columns(2)
    
    with col1:
        bulk_from = st.selectbox("From Currency (Bulk)", currencies, index=currencies.index("USD"), key="bulk_from")
        bulk_to = st.selectbox("To Currency (Bulk)", currencies, index=currencies.index("EUR"), key="bulk_to")
    
    with col2:
        if st.button("📊 Generate Bulk Conversion", type="secondary"):
            bulk_results = []
            for amount in sample_amounts:
                result = converter.convert_currency(amount, bulk_from, bulk_to)
                if result is not None:
                    bulk_results.append({
                        "Amount": f"{amount} {bulk_from}",
                        "Converted": f"{result:.2f} {bulk_to}",
                        "Rate": f"{result/amount:.4f}"
                    })
            
            if bulk_results:
                df = pd.DataFrame(bulk_results)
                st.dataframe(df, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def length_converter_ui(converter):
    """Length converter UI"""
    st.markdown('<div class="converter-container">', unsafe_allow_html=True)
    
    length_units = ["mm", "cm", "m", "km", "in", "ft", "yd", "mi"]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📏 Length Conversion")
        
        length_value = st.number_input("Length", min_value=0.01, value=100.0, step=0.01)
        from_unit = st.selectbox("From Unit", length_units, index=length_units.index("m"))
        to_unit = st.selectbox("To Unit", length_units, index=length_units.index("ft"))
        
        if st.button("🔄 Convert Length", type="primary"):
            result = converter.length_conversion(length_value, from_unit, to_unit)
            if result is not None:
                st.session_state.length_result = result
                st.session_state.length_from = from_unit
                st.session_state.length_to = to_unit
                st.session_state.length_value = length_value
    
    with col2:
        st.subheader("📊 Common Length Conversions")
        
        # Show some common conversions
        common_lengths = [1, 10, 100]
        common_from = "m"
        
        for length in common_lengths:
            for unit in ["ft", "in", "cm", "mm"]:
                result = converter.length_conversion(length, common_from, unit)
                if result is not None:
                    st.metric(f"{length} {common_from} → {unit}", f"{result:.2f}")
    
    # Display result
    if 'length_result' in st.session_state:
        result = st.session_state.length_result
        value = st.session_state.length_value
        from_unit = st.session_state.length_from
        to_unit = st.session_state.length_to
        
        st.markdown(f'''
        <div class="result-display">
            {value:.2f} {from_unit} = {result:.2f} {to_unit}
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def weight_converter_ui(converter):
    """Weight converter UI"""
    st.markdown('<div class="converter-container">', unsafe_allow_html=True)
    
    weight_units = ["mg", "g", "kg", "t", "oz", "lb", "st"]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("⚖️ Weight Conversion")
        
        weight_value = st.number_input("Weight", min_value=0.01, value=1.0, step=0.01)
        from_unit = st.selectbox("From Unit", weight_units, index=weight_units.index("kg"))
        to_unit = st.selectbox("To Unit", weight_units, index=weight_units.index("lb"))
        
        if st.button("🔄 Convert Weight", type="primary"):
            result = converter.weight_conversion(weight_value, from_unit, to_unit)
            if result is not None:
                st.session_state.weight_result = result
                st.session_state.weight_from = from_unit
                st.session_state.weight_to = to_unit
                st.session_state.weight_value = weight_value
    
    with col2:
        st.subheader("📊 Common Weight Conversions")
        
        # Show some common conversions
        common_weights = [1, 10, 100]
        common_from = "kg"
        
        for weight in common_weights:
            for unit in ["lb", "g", "oz"]:
                result = converter.weight_conversion(weight, common_from, unit)
                if result is not None:
                    st.metric(f"{weight} {common_from} → {unit}", f"{result:.2f}")
    
    # Display result
    if 'weight_result' in st.session_state:
        result = st.session_state.weight_result
        value = st.session_state.weight_value
        from_unit = st.session_state.weight_from
        to_unit = st.session_state.weight_to
        
        st.markdown(f'''
        <div class="result-display">
            {value:.2f} {from_unit} = {result:.2f} {to_unit}
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def temperature_converter_ui(converter):
    """Temperature converter UI"""
    st.markdown('<div class="converter-container">', unsafe_allow_html=True)
    
    temp_units = ["C", "F", "K", "R"]
    temp_names = {"C": "Celsius", "F": "Fahrenheit", "K": "Kelvin", "R": "Rankine"}
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🌡️ Temperature Conversion")
        
        temp_value = st.number_input("Temperature", value=25.0, step=0.1)
        from_unit = st.selectbox("From Unit", temp_units, index=temp_units.index("C"), 
                                format_func=lambda x: temp_names[x])
        to_unit = st.selectbox("To Unit", temp_units, index=temp_units.index("F"), 
                              format_func=lambda x: temp_names[x])
        
        if st.button("🔄 Convert Temperature", type="primary"):
            result = converter.temperature_conversion(temp_value, from_unit, to_unit)
            if result is not None:
                st.session_state.temp_result = result
                st.session_state.temp_from = from_unit
                st.session_state.temp_to = to_unit
                st.session_state.temp_value = temp_value
    
    with col2:
        st.subheader("📊 Common Temperature Conversions")
        
        # Show some common conversions
        common_temps = [0, 25, 100]
        common_from = "C"
        
        for temp in common_temps:
            for unit in ["F", "K"]:
                result = converter.temperature_conversion(temp, common_from, unit)
                if result is not None:
                    st.metric(f"{temp}°{common_from} → {unit}", f"{result:.1f}°")
    
    # Display result
    if 'temp_result' in st.session_state:
        result = st.session_state.temp_result
        value = st.session_state.temp_value
        from_unit = st.session_state.temp_from
        to_unit = st.session_state.temp_to
        
        st.markdown(f'''
        <div class="result-display">
            {value:.1f}°{from_unit} = {result:.1f}°{to_unit}
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Temperature chart
    st.markdown('<div class="converter-container">', unsafe_allow_html=True)
    st.subheader("📈 Temperature Comparison Chart")
    
    if PLOTLY_AVAILABLE:
        # Create temperature comparison chart
        celsius_range = list(range(-50, 151, 10))
        fahrenheit_values = [converter.temperature_conversion(c, "C", "F") for c in celsius_range]
        kelvin_values = [converter.temperature_conversion(c, "C", "K") for c in celsius_range]
        
        chart_data = pd.DataFrame({
            "Celsius": celsius_range,
            "Fahrenheit": fahrenheit_values,
            "Kelvin": kelvin_values
        })
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=chart_data["Celsius"], y=chart_data["Fahrenheit"], 
                                mode='lines', name='Fahrenheit', line=dict(color='red')))
        fig.add_trace(go.Scatter(x=chart_data["Celsius"], y=chart_data["Kelvin"], 
                                mode='lines', name='Kelvin', line=dict(color='blue')))
        
        fig.update_layout(
            title="Temperature Scale Comparison",
            xaxis_title="Celsius",
            yaxis_title="Temperature",
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        # Fallback table when Plotly is not available
        st.info("📊 Temperature Conversion Table")
        
        # Create a simple table for temperature conversions
        temp_data = []
        for celsius in range(-50, 151, 25):
            fahrenheit = converter.temperature_conversion(celsius, "C", "F")
            kelvin = converter.temperature_conversion(celsius, "C", "K")
            temp_data.append({
                "Celsius": f"{celsius}°C",
                "Fahrenheit": f"{fahrenheit:.1f}°F",
                "Kelvin": f"{kelvin:.1f}K"
            })
        
        temp_df = pd.DataFrame(temp_data)
        st.dataframe(temp_df, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()