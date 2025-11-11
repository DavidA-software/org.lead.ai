import re

from datetime import datetime



class SchedulingChatbot:

    """

    A simulated AI Chatbot focused on NLP-driven scheduling tasks.



    This class simulates the core logic of intent recognition, entity extraction,

    and managing a simple calendar. In a production system, 'extract_intent'

    and 'extract_entities' would be powered by advanced NLP models (e.g., PyTorch,

    spaCy, or Hugging Face Transformers) to handle complex and ambiguous user language.

    """

    def __init__(self):

        # A simple dictionary to store scheduled events (simulated calendar)

        # Key: Date string (e.g., "2025-11-05"), Value: List of events/descriptions

        self.calendar = {}

        print("🤖 Scheduling Chatbot initialized. Ready to process input.")



    def extract_intent(self, text: str) -> str:

        """

        Determines the user's intent from the input text.

        (Simulated NLP Intent Classification)



        Args:

            text: The raw user input string.



        Returns:

            The determined intent ('add_event', 'check_schedule', 'suggestion', 'unknown').

        """

        text_lower = text.lower()

        if any(keyword in text_lower for keyword in ["schedule", "add", "put in", "book"]):

            return 'add_event'

        if any(keyword in text_lower for keyword in ["what is", "show me", "check my", "agenda", "calendar"]):

            return 'check_schedule'

        if any(keyword in text_lower for keyword in ["suggest", "advice", "free time", "help me plan"]):

            return 'suggestion'

        return 'unknown'



    def extract_entities(self, text: str) -> dict:

        """

        Extracts key entities (date, time, event name) from the text.

        (Simulated NLP Named Entity Recognition - NER)



        Args:

            text: The raw user input string.



        Returns:

            A dictionary of extracted entities.

        """

        entities = {'event': None, 'date': None, 'time': None}



        # Simple date pattern simulation (e.g., "tomorrow", "Nov 15", "today")

        date_match = re.search(r'on (.*?)(?: at |$)', text, re.IGNORECASE)

        if date_match:

            entities['date'] = date_match.group(1).strip()

            # Simple simulation to convert common dates

            if 'today' in entities['date'].lower():

                 entities['date'] = datetime.now().strftime('%Y-%m-%d')

            elif 'tomorrow' in entities['date'].lower():

                entities['date'] = (datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')

            # For demonstration, we assume a clean date format is provided or derived



        # Simple time pattern simulation (e.g., "at 3pm", "14:00")

        time_match = re.search(r'at (\d{1,2}(?::\d{2})?\s?(?:am|pm|o\'clock)?)', text, re.IGNORECASE)

        if time_match:

            entities['time'] = time_match.group(1).strip()



        # Simple event extraction (the rest of the text, typically)

        # This is very basic and would be handled better by a token-based model

        event_match = re.search(r'to (.*?)(?: on |$)', text, re.IGNORECASE)

        if event_match:

            entities['event'] = event_match.group(1).strip()



        return entities



    def add_event(self, date: str, event_details: str) -> str:

        """Adds a new event to the calendar."""

        if not date or not event_details:

            return "❌ Error: I need a date and details to add an event."



        if date not in self.calendar:

            self.calendar[date] = []



        self.calendar[date].append(event_details)

        return f"✅ Success! Event '{event_details}' scheduled for {date}."



    def get_schedule(self, date: str) -> str:

        """Retrieves the schedule for a given date."""

        if not date:

            return "❌ Error: Please specify a date to check the schedule."



        if date in self.calendar and self.calendar[date]:

            events = "\n  - " + "\n  - ".join(self.calendar[date])

            return f"🗓️ Your schedule for {date}:\n{events}"

        else:

            return f"✨ You have no events scheduled for {date}. Free day!"



    def make_suggestion(self) -> str:

        """Offers a scheduling suggestion based on the current calendar state."""

        # Simple suggestion: find the day with the fewest events

        if not self.calendar:

            return "💡 Your calendar is empty! Why not schedule a break or a learning session?"



        day_counts = {date: len(events) for date, events in self.calendar.items()}

        # Find the day with the minimum number of events

        lightest_day = min(day_counts, key=day_counts.get)

        min_events = day_counts[lightest_day]



        if min_events == 0:

            return f"💡 I see {lightest_day} is completely free. That would be a great time for a deep work session or a fitness class."

        elif min_events <= 1:

            return f"💡 {lightest_day} only has {min_events} event(s). I suggest blocking out two hours that day for a high-priority task."

        else:

            return "💡 Your calendar looks pretty packed this week. Make sure to schedule short breaks between your meetings!"



    def process_input(self, user_input: str) -> str:

        """

        The main processing pipeline: intent -> entities -> action.

        """

        intent = self.extract_intent(user_input)

        entities = self.extract_entities(user_input)

        response = ""



        print(f"\n[DEBUG] Input: '{user_input}'")

        print(f"[DEBUG] Intent Detected: {intent}")

        print(f"[DEBUG] Entities Extracted: {entities}")



        if intent == 'add_event':

            event = entities.get('event')

            date_time = f"{entities.get('date', 'Unknown Date')} at {entities.get('time', 'Unknown Time')}"



            if event and entities.get('date'):

                response = self.add_event(entities['date'], f"{event} ({entities.get('time', 'Time unspecified')})")

            else:

                response = "🤔 I need more details to schedule that. Please tell me the event and the date/time."



        elif intent == 'check_schedule':

            date_to_check = entities.get('date', datetime.now().strftime('%Y-%m-%d')) # Default to today

            response = self.get_schedule(date_to_check)



        elif intent == 'suggestion':

            response = self.make_suggestion()



        else:

            response = "I'm sorry, I only handle scheduling and suggestion requests. Try asking to 'schedule a meeting' or 'check my calendar'."



        return response



if __name__ == '__main__':

    # Initialize and run the demonstration

    bot = SchedulingChatbot()

    print("-" * 50)

    print("DEMO: Enter commands to test the chatbot.")

    print("-" * 50)



    # 1. Add an event

    input_1 = "I need to add a meeting to finalize the project proposal to the calendar on 2025-11-15 at 3pm"

    print(f"User: {input_1}")

    print(f"Bot: {bot.process_input(input_1)}")

    print("-" * 20)



    # 2. Add another event (using today shortcut)

    input_2 = "Can you schedule a deep work session on today at 10:00am"

    print(f"User: {input_2}")

    print(f"Bot: {bot.process_input(input_2)}")

    print("-" * 20)



    # 3. Check the schedule

    input_3 = "What is my agenda for 2025-11-15?"

    print(f"User: {input_3}")

    print(f"Bot: {bot.process_input(input_3)}")

    print("-" * 20)



    # 4. Get a suggestion

    input_4 = "Can you suggest when I have free time?"

    print(f"User: {input_4}")

    print(f"Bot: {bot.process_input(input_4)}")

    print("-" * 50)



    # 5. Check today's schedule

    input_5 = "Show me what I have today."

    print(f"User: {input_5}")

    print(f"Bot: {bot.process_input(input_5)}")

    print("-" * 50)
