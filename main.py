import datetime
import math
import argparse

# Constants
CAFFEINE_HALFLIFE_HOURS = 5
MAX_SCORE = 100

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

def main():
    parser = argparse.ArgumentParser(description="Estimate your productivity based on sleep and caffeine ☕")
    parser.add_argument("--sleep-hours", type=float, required=True, help="Hours you slept last night")
    parser.add_argument("--sleep-quality", type=int, required=True, help="Sleep quality (1-10)")
    parser.add_argument("--caffeine-mg", type=int, required=True, help="Total caffeine you drank (in mg)")
    parser.add_argument("--hours-since-caffeine", type=float, required=True, help="Hours since you had caffeine")
    parser.add_argument("--hour", type=int, help="Current hour (24h format, optional)")

    args = parser.parse_args()
    hour_of_day = args.hour if args.hour is not None else datetime.datetime.now().hour

    score = productivity_score(
        args.sleep_hours,
        args.sleep_quality,
        args.caffeine_mg,
        args.hours_since_caffeine,
        hour_of_day
    )

    print(f"\n🔋 Estimated Productivity Score: {score:.1f}/100")
    print(productivity_mood(score))

if __name__ == "__main__":
    main()
