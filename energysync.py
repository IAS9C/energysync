import datetime
import math
import argparse

# Constants
CAFFEINE_HALFLIFE_HOURS = 5
MAX_SCORE = 100

# Variables
energy_drink = 80  # mg of caffeine in a typical energy drink
coffee = 95  # mg of caffeine in a typical cup of coffee
tea = 47  # mg of caffeine in a typical cup of tea
cola = 20  # mg of caffeine in a typical can of cola

# Calculate remaining caffeine based on intake time
def caffeine_remaining(caffeine_mg, hours_since_intake):
    return caffeine_mg * (0.5 ** (hours_since_intake / CAFFEINE_HALFLIFE_HOURS))

def productivity_score(sleep_hours, sleep_quality, caffeine_mg, hours_since_caffeine, hour_of_day):
    # Circadian rhythm: peak hours between 9-12 & 15-17
    if 9 <= hour_of_day <= 12 or 15 <= hour_of_day <= 17:
        circadian_boost = 10
    else:
        circadian_boost = -5

    # Caffeine contribution
    caffeine_now = caffeine_remaining(caffeine_mg, hours_since_caffeine)
    caffeine_score = min(caffeine_now / 4, 20)  # Up to 20 points

    # Sleep contribution
    sleep_score = min(sleep_hours * 7 + sleep_quality * 1.5, 40)  # Up to 40 points

    # Final productivity score
    total = max(0, min(MAX_SCORE, sleep_score + caffeine_score + circadian_boost))
    return total

def productivity_mood(score):
    if score >= 80:
        return "🚀 Peak mode! Perfect time to focus."
    elif score >= 60:
        return "⚡ Productive window open. Ride the wave!"
    elif score >= 40:
        return "😐 Moderate focus. Maybe hydrate or take a quick break."
    else:
        return "🌙 Low energy. Consider resting or minimizing distractions."

def caffeine_effect_level(caffeine_mg, hours_since_intake, target_hour=22, current_hour=None):
    """
    Returns a tuple: (effect_level, hours_until_wearoff)
    effect_level: "none", "small", "mild", "heavy"
    hours_until_wearoff: estimated hours until caffeine < 10mg
    """
    if current_hour is None:
        now = datetime.datetime.now()
        current_hour = now.hour

    # Calculate hours from now until 22h
    if current_hour <= target_hour:
        hours_to_22 = target_hour - current_hour
    else:
        hours_to_22 = 24 - (current_hour - target_hour)

    caffeine_at_22 = caffeine_remaining(caffeine_mg, hours_since_intake + hours_to_22)

    # Determine effect level at 22h
    if caffeine_at_22 >= 100:
        effect = "heavy"
    elif caffeine_at_22 >= 40:
        effect = "mild"
    elif caffeine_at_22 >= 15:
        effect = "small"
    else:
        effect = "none"

    # Estimate when caffeine drops below 10mg
    if caffeine_mg <= 0:
        hours_until_wearoff = 0
    else:
        try:
            hours_until_wearoff = math.log(10 / caffeine_mg, 0.5) * CAFFEINE_HALFLIFE_HOURS
            hours_until_wearoff = max(0, hours_until_wearoff - hours_since_intake)
        except ValueError:
            hours_until_wearoff = 0

    return effect, hours_until_wearoff

def main():
    print("-----ENERGYSYNC-----\n")
    print("☕🔋Estimate your productivity based on sleep and caffeine 🔋☕\n")
    print("Caffeine reference values (mg):")
    print(f"  1 cup coffee = {coffee} mg")
    print(f"  1 energy drink = {energy_drink} mg")
    print(f"  1 cup tea = {tea} mg")
    print(f"  1 can cola = {cola} mg\n")
    while True:
        try:
            print("Enter your caffeine intake below. You can enter the number of drinks or total mg.\n")
            coffee_cups = input(f"☕ How many cups of coffee? (press Enter for 0): ")
            energy_drinks = input(f"🔋 How many energy drinks? (press Enter for 0): ")
            tea_cups = input(f"🍵 How many cups of tea? (press Enter for 0): ")
            cola_cans = input(f"🥤 How many cans of cola? (press Enter for 0): ")
            extra_caffeine = input("⬜ Any extra caffeine (mg)? (press Enter for 0): ")

            total_caffeine = (
                (int(coffee_cups) if coffee_cups.strip() else 0) * coffee +
                (int(energy_drinks) if energy_drinks.strip() else 0) * energy_drink +
                (int(tea_cups) if tea_cups.strip() else 0) * tea +
                (int(cola_cans) if cola_cans.strip() else 0) * cola +
                (int(extra_caffeine) if extra_caffeine.strip() else 0)
            )

            sleep_hours = float(input("Hours you slept last night: "))
            sleep_quality = int(input("Sleep quality (1-10): "))
            hours_since_caffeine = float(input("Hours since you had caffeine: "))
            hour_input = input("Current hour (24h format, optional, press Enter to use current hour): ")
            if hour_input.strip() == "":
                hour_of_day = datetime.datetime.now().hour
            else:
                hour_of_day = int(hour_input)
            break
        except ValueError:
            print("Invalid input. Please enter the values again.\n")

    score = productivity_score(
        sleep_hours,
        sleep_quality,
        total_caffeine,
        hours_since_caffeine,
        hour_of_day
    )

    print(f"\n🔋 Estimated Productivity Score: {score:.1f}/100")
    print(productivity_mood(score))

    # Caffeine warning for 22h
    effect, hours_until_wearoff = caffeine_effect_level(
        total_caffeine, hours_since_caffeine, target_hour=22, current_hour=hour_of_day
    )
    if effect != "none":
        print(f"\n🔺WARNING: At 22:00, caffeine in your system will likely have a {effect} effect.")
    else:
        print("\n✅ By 22:00, caffeine should have little to no effect.")

    if hours_until_wearoff > 0:
        wearoff_time = datetime.datetime.now() + datetime.timedelta(hours=hours_until_wearoff)
        print(f"☕ Caffeine should wear off in about {hours_until_wearoff:.1f} hours (around {wearoff_time.strftime('%H:%M')}).")
    else:
        print("☕ Caffeine is already mostly out of your system.")

if __name__ == "__main__":
    main()
