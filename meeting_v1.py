# Prompt 1: "Build a meeting-cost calculator."


from __future__ import annotations

import argparse
from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Attendee:
    name: str
    hourly_rate: float


def calculate_meeting_cost(
    duration_minutes: float,
    attendees: List[Attendee],
    room_cost_per_hour: float = 0.0,
    platform_cost: float = 0.0,
    overhead_cost: float = 0.0,
) -> float:
    """
    Calculate the total cost of a meeting.

    Formula:
      attendee_cost + room_cost + platform_cost + overhead_cost
    where:
      attendee_cost = sum(attendee.hourly_rate * duration_hours)
      room_cost = room_cost_per_hour * duration_hours

    Args:
        duration_minutes: Meeting length in minutes.
        attendees: List of attendees with their hourly rates.
        room_cost_per_hour: Facility or room rental cost per hour.
        platform_cost: Flat fee for virtual meeting tools, etc.
        overhead_cost: Additional fixed costs (travel, snacks, etc.).

    Returns:
        Total meeting cost rounded to 2 decimal places.
    """
    if duration_minutes < 0:
        raise ValueError("Duration cannot be negative.")

    if not attendees:
        raise ValueError("At least one attendee is required.")

    hours = duration_minutes / 60.0
    attendee_cost = sum(attendee.hourly_rate * hours for attendee in attendees)
    room_cost = room_cost_per_hour * hours
    total = attendee_cost + room_cost + platform_cost + overhead_cost

    return round(total, 2)


def prompt_for_attendees() -> List[Attendee]:
    attendee_count = int(input("How many attendees are in the meeting? ").strip())
    if attendee_count <= 0:
        raise ValueError("Attendee count must be greater than zero.")

    attendees: List[Attendee] = []
    for index in range(1, attendee_count + 1):
        name = input(f"Name for attendee {index}: ").strip() or f"Attendee {index}"
        hourly_rate = float(input(f"Hourly rate for {name} (USD/hr): ").strip())
        attendees.append(Attendee(name=name, hourly_rate=hourly_rate))

    return attendees


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Calculate the cost of a meeting.")
    parser.add_argument("--minutes", type=float, help="Meeting duration in minutes.")
    parser.add_argument(
        "--rates",
        nargs="*",
        type=float,
        help="Hourly rates for attendees, e.g. --rates 65 90 120",
    )
    parser.add_argument(
        "--room-cost-per-hour",
        type=float,
        default=0.0,
        help="Room or facility cost per hour.",
    )
    parser.add_argument(
        "--platform-cost",
        type=float,
        default=0.0,
        help="Flat software or platform cost for the meeting.",
    )
    parser.add_argument(
        "--overhead-cost",
        type=float,
        default=0.0,
        help="Any additional fixed meeting costs.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.minutes is not None:
        if args.rates:
            attendees = [
                Attendee(name=f"Attendee {i + 1}", hourly_rate=rate)
                for i, rate in enumerate(args.rates)
            ]
        else:
            attendees = prompt_for_attendees()

        total_cost = calculate_meeting_cost(
            duration_minutes=args.minutes,
            attendees=attendees,
            room_cost_per_hour=args.room_cost_per_hour,
            platform_cost=args.platform_cost,
            overhead_cost=args.overhead_cost,
        )
    else:
        duration_minutes = float(input("Meeting duration in minutes: ").strip())
        attendees = prompt_for_attendees()
        room_cost_per_hour = float(input("Room cost per hour (USD/hr): ").strip() or "0")
        platform_cost = float(input("Platform cost (USD): ").strip() or "0")
        overhead_cost = float(input("Overhead cost (USD): ").strip() or "0")

        total_cost = calculate_meeting_cost(
            duration_minutes=duration_minutes,
            attendees=attendees,
            room_cost_per_hour=room_cost_per_hour,
            platform_cost=platform_cost,
            overhead_cost=overhead_cost,
        )

    print(f"\nTotal meeting cost: ${total_cost:.2f}")


if __name__ == "__main__":
    try:
        main()
    except ValueError as exc:
        print(f"Error: {exc}")