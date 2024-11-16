import os
from agents.intent_parser import parse_intent
from agents.search_agent import search_hotels
from agents.question_agent import answer_question
from agents.booking_agent import book_hotel


def main():
    print("Agent Testing CLI")
    while True:
        user_input = input("\nEnter your message (or type 'exit' to quit): ")
        if user_input.lower() == "exit":
            break

        # Parse the user's intent
        intent, data, next_step = parse_intent(user_input)
        if not intent:
            print("Could not determine intent.")
            continue

        print(f"Intent: {intent}")
        print(f"Data: {data}")
        print(f"Next Step: {next_step}")

        # Handle the next step based on the intent
        if next_step == "search":
            # Assuming search_hotels function takes the parsed data as input
            search_results = search_hotels(data)
            print(f"Search Results: {search_results}")
        elif next_step == "qa":
            # Assuming answer_question function takes context and question as input
            context = data.get("context", "")
            question = data.get("question", "")
            answer = answer_question(context, question)
            print(f"Answer: {answer}")
        elif next_step == "booking":
            # Assuming book_hotel function takes booking details as input
            booking_details = data.get("booking_details", {})
            booking_confirmation = book_hotel(booking_details)
            print(f"Booking Confirmation: {booking_confirmation}")
        else:
            print("Unhandled next step.")


if __name__ == "__main__":
    main()
