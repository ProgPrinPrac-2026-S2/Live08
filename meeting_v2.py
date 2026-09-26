# "Build a Python meeting-cost calculator 
# that calculates the financial cost of a meeting. 
# The user enters the number of participants, meeting duration (hours), 
# and hourly rate for each participant. 
# Display the total meeting cost."

def main():
    try:
        participant_count = int(input("Enter the number of participants: ").strip())
        if participant_count <= 0:
            raise ValueError("Participant count must be greater than zero.")

        duration_hours = float(input("Enter the meeting duration in hours: ").strip())
        if duration_hours <= 0:
            raise ValueError("Meeting duration must be greater than zero.")

        total_cost = 0.0

        for i in range(1, participant_count + 1):
            hourly_rate = float(input(f"Enter the hourly rate for participant {i}: ").strip())
            if hourly_rate < 0:
                raise ValueError("Hourly rate cannot be negative.")
            total_cost += hourly_rate

        meeting_cost = total_cost * duration_hours
        print(f"\nTotal meeting cost: ${meeting_cost:.2f}")

    except ValueError as exc:
        print(f"Error: {exc}")
    except Exception:
        print("Error: Invalid input. Please enter valid numbers.")


if __name__ == "__main__":
    main()