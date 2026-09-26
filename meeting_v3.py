# Prompt: "Build a Python meeting-cost calculator that:
#
# - Calculates total person-hours and financial cost
# - Supports online and in-person meetings
# - Estimates travel emissions for in-person meetings
# - Uses separate functions for each calculation
# - Validates user input
# - Produces a summary report"

def get_positive_int(prompt, minimum=1):
    while True:
        try:
            value = int(input(prompt).strip())
            if value >= minimum:
                return value
            print(f"Value must be at least {minimum}.")
        except ValueError:
            print("Please enter a valid integer.")


def get_non_negative_float(prompt):
    while True:
        try:
            value = float(input(prompt).strip())
            if value >= 0:
                return value
            print("Value cannot be negative.")
        except ValueError:
            print("Please enter a valid number.")


def collect_rates(participant_count):
    rates = []
    for i in range(1, participant_count + 1):
        rate = get_non_negative_float(f"Enter the hourly rate for participant {i} (USD/hr): ")
        rates.append(rate)
    return rates


def calculate_person_hours(participant_count, duration_hours):
    return participant_count * duration_hours


def calculate_labor_cost(rates, duration_hours):
    return sum(rate * duration_hours for rate in rates)


def calculate_online_cost(rates, duration_hours, platform_fee=0.0):
    return calculate_labor_cost(rates, duration_hours) + platform_fee


def estimate_travel_emissions(distance_km, participant_count, travel_mode):
    emission_factors = {
        "car": 0.21,      # kg CO2 per km per person
        "bus": 0.12,
        "train": 0.04,
        "bike": 0.0,
        "walk": 0.0
    }

    if travel_mode.lower() not in emission_factors:
        raise ValueError("Unsupported travel mode. Use car, bus, train, bike, or walk.")

    return distance_km * participant_count * emission_factors[travel_mode.lower()]


def calculate_in_person_cost(rates, duration_hours, room_cost, platform_fee, travel_distance_km, travel_mode):
    labor_cost = calculate_labor_cost(rates, duration_hours)
    travel_cost = travel_distance_km * 0.25  # estimated travel cost per km
    total_cost = labor_cost + room_cost + platform_fee + travel_cost
    emissions_kg = estimate_travel_emissions(travel_distance_km, len(rates), travel_mode)
    return total_cost, emissions_kg


def print_summary(meeting_type, participant_count, duration_hours, rates, total_cost, person_hours, emissions_kg=0.0):
    print("\n=== Meeting Summary ===")
    print(f"Meeting type: {meeting_type}")
    print(f"Participants: {participant_count}")
    print(f"Duration: {duration_hours:.2f} hours")
    print(f"Total person-hours: {person_hours:.2f}")
    print(f"Total labor cost: ${calculate_labor_cost(rates, duration_hours):.2f}")

    if meeting_type.lower() == "online":
        print(f"Total meeting cost: ${total_cost:.2f}")
    else:
        print(f"Estimated travel emissions: {emissions_kg:.2f} kg CO2")
        print(f"Total meeting cost: ${total_cost:.2f}")


def main():
    try:
        print("Meeting Cost Calculator")
        participant_count = get_positive_int("Enter the number of participants: ")

        duration_hours = get_non_negative_float("Enter the meeting duration in hours: ")
        if duration_hours <= 0:
            raise ValueError("Meeting duration must be greater than zero.")

        rates = collect_rates(participant_count)
        person_hours = calculate_person_hours(participant_count, duration_hours)

        meeting_type = input("Is this an online or in-person meeting? ").strip().lower()
        if meeting_type not in ("online", "in-person"):
            raise ValueError("Meeting type must be 'online' or 'in-person'.")

        if meeting_type == "online":
            platform_fee = get_non_negative_float("Enter the platform fee (USD): ")
            total_cost = calculate_online_cost(rates, duration_hours, platform_fee)
            print_summary("online", participant_count, duration_hours, rates, total_cost, person_hours)
        else:
            room_cost = get_non_negative_float("Enter the room cost (USD): ")
            platform_fee = get_non_negative_float("Enter the platform fee (USD): ")
            travel_distance_km = get_non_negative_float("Enter average one-way travel distance per participant (km): ")
            travel_mode = input("Enter travel mode (car, bus, train, bike, walk): ").strip().lower()

            total_cost, emissions_kg = calculate_in_person_cost(
                rates,
                duration_hours,
                room_cost,
                platform_fee,
                travel_distance_km,
                travel_mode
            )
            print_summary(
                "in-person",
                participant_count,
                duration_hours,
                rates,
                total_cost,
                person_hours,
                emissions_kg
            )

    except ValueError as exc:
        print(f"Error: {exc}")
    except Exception:
        print("Error: Invalid input. Please try again.")


if __name__ == "__main__":
    main()