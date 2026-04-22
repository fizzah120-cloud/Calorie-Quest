import streamlit as st
import pandas as pd
from datetime import date
import matplotlib.pyplot as plt

st.set_page_config(page_title="Calorie Budget Game", layout="centered")

st.title("🎮 Calorie Budget Game Pro")

# ---------------- SESSION STATE ----------------
if "log" not in st.session_state:
    st.session_state.log = []

if "daily_total" not in st.session_state:
    st.session_state.daily_total = 0

if "streak" not in st.session_state:
    st.session_state.streak = 0

if "last_date" not in st.session_state:
    st.session_state.last_date = str(date.today())

# ---------------- USER INPUT ----------------
st.sidebar.header("⚙️ Settings")

budget = st.sidebar.number_input("Daily Calorie Budget", 1000, 4000, 1800)
protein_goal = st.sidebar.number_input("Protein Goal (g)", 20, 200, 60)
carb_goal = st.sidebar.number_input("Carbs Goal (g)", 50, 400, 200)
fat_goal = st.sidebar.number_input("Fat Goal (g)", 20, 150, 60)

# ---------------- NEW DAY RESET ----------------
today = str(date.today())

if today != st.session_state.last_date:
    if st.session_state.daily_total <= budget:
        st.session_state.streak += 1
    else:
        st.session_state.streak = 0

    st.session_state.daily_total = 0
    st.session_state.log = []
    st.session_state.last_date = today

# ---------------- FOOD ENTRY ----------------
st.subheader("🍔 Add Food")

col1, col2 = st.columns(2)

with col1:
    food = st.text_input("Food Name")

with col2:
    calories = st.number_input("Calories", min_value=0)

protein = st.number_input("Protein (g)", min_value=0)
carbs = st.number_input("Carbs (g)", min_value=0)
fat = st.number_input("Fat (g)", min_value=0)

if st.button("➕ Add Food"):
    entry = {
        "Food": food,
        "Calories": calories,
        "Protein": protein,
        "Carbs": carbs,
        "Fat": fat
    }
    st.session_state.log.append(entry)
    st.session_state.daily_total += calories
    st.success(f"{food} added!")

# ---------------- DISPLAY ----------------
st.subheader("📊 Daily Summary")

df = pd.DataFrame(st.session_state.log)

if not df.empty:
    st.dataframe(df)

total_protein = df["Protein"].sum() if not df.empty else 0
total_carbs = df["Carbs"].sum() if not df.empty else 0
total_fat = df["Fat"].sum() if not df.empty else 0

st.write(f"🔥 Calories: {st.session_state.daily_total} / {budget}")
st.write(f"🥩 Protein: {total_protein} / {protein_goal} g")
st.write(f"🍞 Carbs: {total_carbs} / {carb_goal} g")
st.write(f"🧈 Fat: {total_fat} / {fat_goal} g")

remaining = budget - st.session_state.daily_total
st.write(f"🎯 Remaining Calories (Points): {remaining}")

# Progress bar
progress = min(st.session_state.daily_total / budget, 1.0)
st.progress(progress)

# ---------------- CHART ----------------
st.subheader("📈 Macronutrient Breakdown")

fig, ax = plt.subplots()
labels = ["Protein", "Carbs", "Fat"]
values = [total_protein, total_carbs, total_fat]
ax.pie(values, labels=labels, autopct='%1.1f%%')
st.pyplot(fig)

# ---------------- GAME STATUS ----------------
st.subheader("🎯 Game Status")

if st.session_state.daily_total < budget:
    st.info("You're within your calorie budget!")
elif st.session_state.daily_total == budget:
    st.success("Perfect hit! 🏆")
else:
    st.error("You exceeded your budget! 💥")

# ---------------- STREAK ----------------
st.subheader("🔥 Streak System")
st.write(f"Current Streak: {st.session_state.streak} days")

# ---------------- LEVEL SYSTEM ----------------
st.subheader("🏆 Level")

if st.session_state.streak >= 7:
    level = "Elite 🔥"
elif st.session_state.streak >= 4:
    level = "Pro 💪"
elif st.session_state.streak >= 2:
    level = "Intermediate ⚡"
else:
    level = "Beginner 🌱"

st.write(f"Your Level: {level}")

# ---------------- BADGES ----------------
st.subheader("🎖️ Badges")

badges = []

if st.session_state.daily_total <= budget:
    badges.append("✅ Budget Master")

if total_protein >= protein_goal:
    badges.append("🥩 Protein King")

if total_fat < fat_goal:
    badges.append("🧈 Fat Controller")

if st.session_state.streak >= 3:
    badges.append("🔥 Consistency Champ")

if badges:
    for b in badges:
        st.success(b)
else:
    st.write("No badges yet!")

# ---------------- HEALTH FEEDBACK ----------------
st.subheader("🧠 Nutrition Feedback")

if total_protein < protein_goal:
    st.warning("Increase protein intake!")

if total_fat > fat_goal:
    st.warning("Reduce fat intake!")

if total_carbs > carb_goal:
    st.warning("High carb intake!")

if st.session_state.daily_total < 1200:
    st.warning("Calories too low!")

# ---------------- RESET ----------------
if st.button("🔄 Reset Day"):
    st.session_state.daily_total = 0
    st.session_state.log = []
    st.success("Day Reset!")
