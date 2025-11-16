import re
from datetime import datetime, timedelta
from typing import Optional, Dict

from datetime import datetime, timedelta



class SchedulingChatbot:
    """
    An enhanced AI Chatbot with advanced NLP-driven scheduling capabilities.
    """
    
    def __init__(self):
        self.calendar = {}
        self.event_id_counter = 0
        print("🤖 Enhanced Scheduling Chatbot initialized and ready!")
        print("💬 Try: 'Schedule team meeting tomorrow at 2pm'\n")

    def extract_intent(self, text: str) -> str:
        """Advanced intent classification."""
        text_lower = text.lower()
        
        if any(kw in text_lower for kw in ["delete", "cancel", "remove", "clear"]):
            return 'delete_event'
        
        if any(kw in text_lower for kw in ["update", "modify", "change", "move", "reschedule"]):
            return 'update_event'
        
        if any(kw in text_lower for kw in ["schedule", "add", "book", "put in", "setup", 
                                            "create", "plan", "arrange", "meeting", "appointment"]):
            return 'add_event'
        
        if any(kw in text_lower for kw in ["what", "show", "check", "view", "see", "list",
                                            "agenda", "calendar", "schedule for", "what's on",
                                            "do i have", "am i free", "any events"]):
            return 'check_schedule'
        
        if any(kw in text_lower for kw in ["suggest", "recommend", "advice", "free time", 
                                            "when should", "help me plan", "available"]):
            return 'suggestion'
        
        if any(kw in text_lower for kw in ["help", "what can you do", "how do i", "commands"]):
            return 'help'
        
        return 'unknown'

    def parse_date(self, text: str) -> Optional[str]:
        """Enhanced date parsing."""
        text_lower = text.lower()
        today = datetime.now()
        
        if 'today' in text_lower:
            return today.strftime('%Y-%m-%d')
        if 'tomorrow' in text_lower:
            return (today + timedelta(days=1)).strftime('%Y-%m-%d')
        if 'yesterday' in text_lower:
            return (today - timedelta(days=1)).strftime('%Y-%m-%d')
        
        weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        for i, day in enumerate(weekdays):
            if day in text_lower:
                days_ahead = i - today.weekday()
                if days_ahead <= 0:
                    days_ahead += 7
                return (today + timedelta(days=days_ahead)).strftime('%Y-%m-%d')
        
        match = re.search(r'in (\d+) days?', text_lower)
        if match:
            days = int(match.group(1))
            return (today + timedelta(days=days)).strftime('%Y-%m-%d')
        
        date_patterns = [
            (r'(\d{4})-(\d{1,2})-(\d{1,2})', lambda m: f"{m.group(1)}-{m.group(2).zfill(2)}-{m.group(3).zfill(2)}"),
            (r'(\d{1,2})/(\d{1,2})/(\d{4})', lambda m: f"{m.group(3)}-{m.group(1).zfill(2)}-{m.group(2).zfill(2)}"),
            (r'(\d{1,2})/(\d{1,2})(?!/)', lambda m: f"{today.year}-{m.group(1).zfill(2)}-{m.group(2).zfill(2)}"),
        ]
        
        for pattern, formatter in date_patterns:
            match = re.search(pattern, text)
            if match:
                return formatter(match)
        
        months = ['january', 'february', 'march', 'april', 'may', 'june',
                 'july', 'august', 'september', 'october', 'november', 'december']
        for i, month in enumerate(months, 1):
            pattern = rf'{month[:3]}\.?\s+(\d{{1,2}})'
            match = re.search(pattern, text_lower)
            if match:
                day = match.group(1)
                return f"{today.year}-{str(i).zfill(2)}-{day.zfill(2)}"
        
        return None

    def parse_time(self, text: str) -> Optional[str]:
        """Enhanced time parsing."""
        text_lower = text.lower()
        
        match = re.search(r'(\d{1,2})(?::(\d{2}))?\s*(am|pm)', text_lower)
        if match:
            hour = int(match.group(1))
            minute = match.group(2) or "00"
            period = match.group(3)
            
            if period == 'pm' and hour != 12:
                hour += 12
            elif period == 'am' and hour == 12:
                hour = 0
            
            return f"{hour:02d}:{minute}"
        
        match = re.search(r'(\d{1,2}):(\d{2})', text)
        if match:
            hour = int(match.group(1))
            minute = match.group(2)
            if 0 <= hour <= 23:
                return f"{hour:02d}:{minute}"
        
        time_mappings = {
            'noon': '12:00',
            'midnight': '00:00',
            'morning': '09:00',
            'afternoon': '14:00',
            'evening': '18:00',
            'night': '20:00'
        }
        for word, time in time_mappings.items():
            if word in text_lower:
                return time
        
        return None

    def extract_entities(self, text: str) -> Dict:
        """Enhanced entity extraction."""
        entities = {'event': None, 'date': None, 'time': None, 'duration': None}
        
        entities['date'] = self.parse_date(text)
        entities['time'] = self.parse_time(text)
        
        duration_match = re.search(r'for (\d+)\s*(hour|hr|minute|min)', text.lower())
        if duration_match:
            value = int(duration_match.group(1))
            unit = duration_match.group(2)
            if 'hour' in unit or 'hr' in unit:
                entities['duration'] = f"{value}h"
            else:
                entities['duration'] = f"{value}m"
        
        # Extract event name - simplified and robust
        patterns = [
            r'(?:schedule|add|book|setup|create|plan)\s+(?:a\s+|an\s+)?(.+?)(?:\s+(?:on|at|tomorrow|today|yesterday|next|this|for|in)\s+|\s+\d)',
            r'(?:schedule|add|book|setup|create|plan)\s+(?:a\s+|an\s+)?(.+?)$',
            r'^(.+?)\s+(?:on|at)\s+',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                event_text = match.group(1).strip()
                event_text = re.sub(r'\s+(on|at|in|for|with)$', '', event_text, flags=re.IGNORECASE)
                event_text = re.sub(r'^(the|a|an|my|our)\s+', '', event_text, flags=re.IGNORECASE).strip()
                
                if len(event_text) > 2 and event_text.lower() not in ['a', 'an', 'the']:
                    entities['event'] = event_text
                    break
        
        if not entities['event']:
            temp_text = text
            
            for word in ['schedule', 'add', 'book', 'please', 'can you', 'could you', 'setup', 'create', 'plan']:
                temp_text = re.sub(rf'\b{word}\b', '', temp_text, flags=re.IGNORECASE)
            
            temp_text = re.sub(r'\b(today|tomorrow|yesterday|next\s+\w+|this\s+\w+|\d{1,2}/\d{1,2}(/\d{4})?|\d{4}-\d{2}-\d{2})\b', '', temp_text, flags=re.IGNORECASE)
            temp_text = re.sub(r'\b(at\s+)?\d{1,2}(:\d{2})?\s*(am|pm)?\b', '', temp_text, flags=re.IGNORECASE)
            temp_text = re.sub(r'\b(on|at|in|for)\b', '', temp_text, flags=re.IGNORECASE)
            temp_text = ' '.join(temp_text.split()).strip()
            
            if len(temp_text) > 2:
                entities['event'] = temp_text
        


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
                entities['date'] = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')

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

    def add_event(self, date: str, event_details: str, time: Optional[str] = None, 
                  duration: Optional[str] = None) -> str:
        """Add event with conflict detection."""
        if not date or not event_details:
            return "❌ I need both a date and event description. Try: 'Schedule team meeting tomorrow at 2pm'"
        
        if date not in self.calendar:
            self.calendar[date] = []
        
        if time:
            conflicts = [e for e in self.calendar[date] if time in e]
            if conflicts:
                return f"⚠️ Warning: You already have an event at {time} on {date}:\n  • {conflicts[0]}\nScheduling anyway..."
        
        self.event_id_counter += 1
        event_str = f"[ID:{self.event_id_counter}] {event_details}"
        if time:
            event_str += f" at {time}"
        if duration:
            event_str += f" ({duration})"
        
        self.calendar[date].append(event_str)
        
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        formatted_date = date_obj.strftime('%A, %B %d, %Y')
        
        return f"✅ Event scheduled!\n📅 {formatted_date}\n⏰ {time or 'Time not specified'}\n📝 {event_details}"

    def get_schedule(self, date: Optional[str] = None, range_days: int = 1) -> str:
        """Get schedule with optional date range."""
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
        
        results = []
        current = datetime.strptime(date, '%Y-%m-%d')
        
        for i in range(range_days):
            check_date = (current + timedelta(days=i)).strftime('%Y-%m-%d')
            date_obj = datetime.strptime(check_date, '%Y-%m-%d')
            formatted_date = date_obj.strftime('%A, %B %d')
            
            if check_date in self.calendar and self.calendar[check_date]:
                events = '\n  • '.join(self.calendar[check_date])
                results.append(f"📅 {formatted_date}:\n  • {events}")
            else:
                results.append(f"📅 {formatted_date}: ✨ Free day!")
        
        if results:
            header = "🗓️  Your Schedule" if range_days == 1 else f"🗓️  Your {range_days}-Day Schedule"
            return f"{header}\n\n" + "\n\n".join(results)
        
        return "✨ Your calendar is completely clear!"

    def delete_event(self, text: str) -> str:
        """Delete events by ID."""
        id_match = re.search(r'id:?\s*(\d+)', text.lower())
        if id_match:
            event_id = int(id_match.group(1))
            for date, events in self.calendar.items():
                for event in events:
                    if f"[ID:{event_id}]" in event:
                        self.calendar[date].remove(event)
                        return f"✅ Deleted event: {event.split(']')[1].strip()}"
            return f"❌ No event found with ID {event_id}"
        
        return "❌ Please specify an event ID. Use 'show calendar' to see IDs."

    def make_suggestion(self) -> str:
        """Smart scheduling suggestions."""
        if not self.calendar:
            return "💡 Your calendar is empty! Great time to:\n  • Block focus time for deep work\n  • Schedule regular breaks\n  • Plan your week ahead"
        
        today = datetime.now()
        week_dates = [(today + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]
        
        day_counts = {date: len(self.calendar.get(date, [])) for date in week_dates}
        free_days = [date for date in week_dates if day_counts[date] == 0]
        busy_days = [date for date in week_dates if day_counts[date] >= 3]
        
        suggestions = ["💡 Smart Scheduling Suggestions:\n"]
        
        if free_days:
            free_date = datetime.strptime(free_days[0], '%Y-%m-%d')
            suggestions.append(f"  • {free_date.strftime('%A')} is completely free - perfect for focused work")
        
        if busy_days:
            busy_date = datetime.strptime(busy_days[0], '%Y-%m-%d')
            suggestions.append(f"  • {busy_date.strftime('%A')} is packed - consider buffering breaks")
        
        lightest_day = min(day_counts, key=day_counts.get)
        lightest_date = datetime.strptime(lightest_day, '%Y-%m-%d')
        suggestions.append(f"  • {lightest_date.strftime('%A')} has the most availability")
        
        return "\n".join(suggestions)

    def show_help(self) -> str:
        """Display help message."""
        return """
🤖 **Scheduling Chatbot - Command Guide**

📝 **Add Events:**
  • "Schedule team meeting tomorrow at 2pm"
  • "Add doctor appointment on Friday at 9:30am"
  • "Book project review next Monday afternoon"

📅 **Check Schedule:**
  • "What's on my calendar today?"
  • "Show me tomorrow's agenda"
  • "What do I have this week?"

🗑️ **Delete Events:**
  • "Delete event ID:5"

💡 **Get Suggestions:**
  • "When am I free this week?"
  • "Suggest a good time to focus"
"""

    def process_input(self, user_input: str) -> str:
        """Main processing pipeline."""
        intent = self.extract_intent(user_input)
        entities = self.extract_entities(user_input)
        
        print(f"\n[DEBUG] Input: '{user_input}'")
        print(f"[DEBUG] Intent: {intent}")
        print(f"[DEBUG] Entities: {entities}")
        
        if intent == 'help':
            return self.show_help()
        
        elif intent == 'add_event':
            event = entities.get('event')
            date = entities.get('date')
            time = entities.get('time')
            duration = entities.get('duration')
            
            if not event:
                return "🤔 What would you like to schedule? Try: 'Schedule team standup tomorrow at 10am'"
            if not date:
                return "🤔 When should I schedule this? Try adding 'tomorrow' or a specific date."
            
            return self.add_event(date, event, time, duration)
        
        elif intent == 'check_schedule':
            if any(word in user_input.lower() for word in ['week', 'next 7', 'coming days']):
                date = entities.get('date', datetime.now().strftime('%Y-%m-%d'))
                return self.get_schedule(date, range_days=7)
            else:
                date = entities.get('date')
                return self.get_schedule(date)
        
        elif intent == 'delete_event':
            return self.delete_event(user_input)
        
        elif intent == 'suggestion':
            return self.make_suggestion()
        
        else:
            return "🤔 I'm not sure what you'd like me to do. Type 'help' to see what I can do!"


if __name__ == '__main__':
    bot = SchedulingChatbot()
    
    print("\n" + "=" * 80)
    print("🎬 LIVE DEMO")
    print("=" * 80)
    
    demo_commands = [
        "Schedule team meeting tomorrow at 3pm",
        "Add doctor appointment on Friday at 9:30am",
        "Book lunch next Monday at noon",
        "What's on my calendar tomorrow?",
        "Show me this week",
        "When am I free this week?",
    ]
    
    for cmd in demo_commands:
        print(f"\n💬 User: {cmd}")
        response = bot.process_input(cmd)
        print(f"🤖 Bot: {response}")
        print("-" * 80)