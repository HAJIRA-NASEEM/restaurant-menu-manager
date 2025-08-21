import streamlit as st
import pandas as pd
import json

SAVE_FILE = "menu.json"

DEFAULT_MENU = {
    'Burger': ('Main', 10.5),
    'Soup': ('Appetizer', 5.0),
    'Ice Cream': ('Dessert', 4.0),
    'Salad': ('Appetizer', 6.5)
}

def load_menu():
    try:
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return DEFAULT_MENU.copy()

def save_menu(menu):
    with open(SAVE_FILE, "w") as f:
        json.dump(menu, f)

if "menu" not in st.session_state:
    st.session_state.menu = load_menu()

menu = st.session_state.menu

st.markdown("""
    <style>
    body { background-color: #000; color: #fff; }
    .stApp { background-color: #000; }
    h1, h2, h3, h4 { color: #FFD700; }
    .stTable, .stDataFrame { background-color: #1c1c1c; color: #fff; border-radius: 10px; padding: 10px; }
    .stButton>button { background-color: #FFD700; color: black; font-weight: bold; border-radius: 10px; padding: 10px 20px; }
    .stButton>button:hover { background-color: #FFB700; color: white; }
    </style>
""", unsafe_allow_html=True)


st.title("🍴 Welcome to Golden Spoon Restaurant")
st.markdown("---")

st.subheader("📋 Our Delicious Menu")
if menu:
    df = pd.DataFrame([(dish, dish_type, price) for dish, (dish_type, price) in menu.items()],
                      columns=["Dish", "Type", "Price ($)"])
    st.table(df)
else:
    st.info("No dishes available.")

st.markdown("---")

st.subheader("📊 Menu Overview")
type_counts = {}
for dish_type, _ in menu.values():
    type_counts[dish_type] = type_counts.get(dish_type, 0) + 1

if type_counts:
    st.bar_chart(pd.DataFrame.from_dict(type_counts, orient="index", columns=["Count"]))
else:
    st.info("No dish types to display.")

st.markdown("---")

st.subheader("➕ Add a New Dish")
with st.form("add_form"):
    new_dish = st.text_input("🍽️ Dish Name")
    dish_type = st.selectbox("🥗 Dish Type", ["Main", "Appetizer", "Dessert", "Drink"])
    price = st.number_input("💲 Price", min_value=0.0, step=0.5)
    submitted = st.form_submit_button("Add Dish")
    if submitted and new_dish:
        if new_dish in menu:
            st.warning(f"{new_dish} already exists!")
        else:
            menu[new_dish] = (dish_type, price)
            st.success(f"{new_dish} added to the menu! 🎉")

st.markdown("---")

st.subheader("➖ Remove a Dish")
remove_dish = st.selectbox("Select dish to remove", [""] + list(menu.keys()))
if st.button("Remove Dish"):
    if remove_dish:
        menu.pop(remove_dish, None)
        st.success(f"{remove_dish} removed from the menu ❌")

st.markdown("---")

st.subheader("💲 Update Dish Price")
update_dish = st.selectbox("Select dish to update", [""] + list(menu.keys()))
new_price = st.number_input("Enter new price", min_value=0.0, step=0.5, key="update_price")
if st.button("Update Price"):
    if update_dish:
        dish_type, _ = menu[update_dish]
        menu[update_dish] = (dish_type, new_price)
        st.success(f"Price of {update_dish} updated to ${new_price:.2f} ✅")

st.markdown("---")

st.subheader("💾 Save or Reset Menu")
col1, col2 = st.columns(2)

with col1:
    if st.button("✅ Save Menu"):
        save_menu(menu)
        st.success("Menu saved! Changes will stay after refresh.")

with col2:
    if st.button("♻️ Reset Menu"):
        menu.clear()
        menu.update(DEFAULT_MENU.copy())
        save_menu(menu)
        st.warning("Menu reset to default dishes.")
