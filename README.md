# EnergySync

**EnergySync** is a simple Python tool that estimates your productivity score based on your sleep, caffeine intake, and the time of day. It uses a basic model of circadian rhythms and caffeine metabolism to help you understand when you might be most productive.

## Features

- Calculates remaining caffeine in your system based on intake time and amount.
- Considers sleep duration and quality.
- Accounts for circadian rhythm peaks.
- Provides a productivity score (0–100) and a motivational message.

## Usage

1. Make sure you have Python 3 installed.
2. Run the script:

   ```sh
   python energysync.py
   ```

Enter the following when prompted:

Hours you slept last night (e.g., 7.5)
Sleep quality (1–10)
Total caffeine consumed (in mg, e.g., 200)
Hours since your last caffeine intake (e.g., 3)
Current hour (24h format, optional; press Enter to use your system's current hour)
The script will display your estimated productivity score and a message.

## Example

```markdown
Estimate your productivity based on sleep and caffeine ☕

Hours you slept last night: 7
Sleep quality (1-10): 8
Total caffeine you drank (in mg): 150
Hours since you had caffeine: 2
Current hour (24h format, optional, press Enter to use current hour):

🔋 Estimated Productivity Score: 78.2/100
⚡ Productive window open. Ride the wave!
```
