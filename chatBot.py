import re
from datetime import datetime, timedelta
from typing import Optional, Dict
import random


class SchedulingChatbot:
    """
    An enhanced AI Chatbot with natural conversation and advanced scheduling.
    """
    
    def __init__(self):
        self.calendar = {}
        self.event_id_counter = 0
        self.user_name = None
        self.conversation_context = []
        self.last_intent = None
        self.pending_event = {}
        
        print("🤖 Enhanced Scheduling Chatbot initialized and ready!")
        print("💬 I'm your personal scheduling assistant. What's your name?\n")

    def set_context(self, intent: str, entities: Dict):
        """Track conversation context for follow-ups."""
        self.last_intent = intent
        self.conversation_context.append({
            'intent': intent,
            'entities': entities,
            'timestamp': datetime.now()
        })
        # Keep only last 5 interactions
        if len(self.conversation_context) > 5:
            self.conversation_context.pop(0)

    def extract_intent(self, text: str) -> str:
        """Advanced intent classification with conversational context."""
        text_lower = text.lower()
        
        # Greetings
        if any(kw in text_lower for kw in ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"]):
            return 'greeting'
        
        # Gratitude
        if any(kw in text_lower for kw in ["thank", "thanks", "appreciate", "awesome", "perfect", "great"]):
            return 'gratitude'
        
        # Confirmation (yes/no responses)
        if text_lower.strip() in ["yes", "yeah", "yep", "sure", "ok", "okay", "yup", "correct", "right"]:
            return 'confirm'
        if text_lower.strip() in ["no", "nope", "nah", "not really", "cancel"]:
            return 'deny'
        
        # Name introduction
        if any(kw in text_lower for kw in ["my name is", "i'm", "i am", "call me"]):
            return 'introduce_name'
        
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
        
        # Small talk
        if any(kw in text_lower for kw in ["how are you", "what's up", "wassup", "sup"]):
            return 'smalltalk'
        
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
        
        # Next week
        if 'next week' in text_lower:
            return (today + timedelta(days=7)).strftime('%Y-%m-%d')
        
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
        entities = {'event': None, 'date': None, 'time': None, 'duration': None, 'name': None}
        
        # Extract name
        name_patterns = [
            r"(?:my name is|i'm|i am|call me)\s+(\w+)",
            r"^(\w+)$"  # Single word as name
        ]
        for pattern in name_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                entities['name'] = match.group(1).capitalize()
                break
        
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
        
        # Extract event name
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
        
        return entities

    def add_event(self, date: str, event_details: str, time: Optional[str] = None, 
                  duration: Optional[str] = None) -> str:
        """Add event with conflict detection."""
        if not date or not event_details:
            return "🤔 I'd love to help! Could you tell me what you'd like to schedule and when?"
        
        if date not in self.calendar:
            self.calendar[date] = []
        
        if time:
            conflicts = [e for e in self.calendar[date] if time in e]
            if conflicts:
                return f"⚠️ Heads up! You already have something at {time} on that day:\n  • {conflicts[0]}\n\nShould I still add this event? (yes/no)"
        
        self.event_id_counter += 1
        event_str = f"[ID:{self.event_id_counter}] {event_details}"
        if time:
            event_str += f" at {time}"
        if duration:
            event_str += f" ({duration})"
        
        self.calendar[date].append(event_str)
        
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        formatted_date = date_obj.strftime('%A, %B %d, %Y')
        
        responses = [
            f"✅ Perfect! I've added '{event_details}' to your calendar.",
            f"✅ All set! '{event_details}' is now scheduled.",
            f"✅ Done! I've booked '{event_details}' for you.",
        ]
        
        response = random.choice(responses)
        return f"{response}\n📅 {formatted_date}\n⏰ {time or 'No specific time set'}"

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
                results.append(f"📅 {formatted_date}: ✨ Nothing scheduled - free day!")
        
        if results:
            if range_days == 1:
                header = "🗓️  Here's what you have coming up:"
            else:
                header = f"🗓️  Your schedule for the next {range_days} days:"
            return f"{header}\n\n" + "\n\n".join(results)
        
        return "✨ Your calendar is completely clear! Time to relax or plan something fun!"

    def delete_event(self, text: str) -> str:
        """Delete events by ID."""
        id_match = re.search(r'id:?\s*(\d+)', text.lower())
        if id_match:
            event_id = int(id_match.group(1))
            for date, events in self.calendar.items():
                for event in events:
                    if f"[ID:{event_id}]" in event:
                        self.calendar[date].remove(event)
                        return f"✅ Got it! I've removed that event: {event.split(']')[1].strip()}"
            return f"🤔 Hmm, I couldn't find an event with ID {event_id}. Try 'show my calendar' to see all events."
        
        return "🤔 Could you tell me which event to delete? You can say 'delete event ID:5' for example."

    def make_suggestion(self) -> str:
        """Smart scheduling suggestions."""
        if not self.calendar:
            return "💡 Your calendar is completely open! Here are some ideas:\n  • Block time for focused work or creative projects\n  • Schedule regular breaks to recharge\n  • Plan out your week to stay organized"
        
        today = datetime.now()
        week_dates = [(today + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]
        
        day_counts = {date: len(self.calendar.get(date, [])) for date in week_dates}
        free_days = [date for date in week_dates if day_counts[date] == 0]
        busy_days = [date for date in week_dates if day_counts[date] >= 3]
        
        suggestions = ["💡 Here's what I'm thinking:\n"]
        
        if free_days:
            free_date = datetime.strptime(free_days[0], '%Y-%m-%d')
            suggestions.append(f"  • {free_date.strftime('%A')} looks wide open - perfect for deep work or personal time!")
        
        if busy_days:
            busy_date = datetime.strptime(busy_days[0], '%Y-%m-%d')
            suggestions.append(f"  • {busy_date.strftime('%A')} is pretty packed - maybe add some buffer time?")
        
        lightest_day = min(day_counts, key=day_counts.get)
        lightest_date = datetime.strptime(lightest_day, '%Y-%m-%d')
        suggestions.append(f"  • {lightest_date.strftime('%A')} has the most availability if you need to schedule something")
        
        return "\n".join(suggestions)

    def show_help(self) -> str:
        """Display help message."""
        name_part = f" {self.user_name}" if self.user_name else ""
        return f"""
🤖 **Hey{name_part}! Here's what I can help you with:**

💬 **Just talk to me naturally! For example:**
  • "Schedule a team meeting tomorrow at 2pm"
  • "What do I have on Friday?"
  • "Can you add lunch with Sarah next Monday at noon?"
  • "Show me my week"
  • "When am I free?"
  • "Delete event ID:5"

🎯 **I understand casual language like:**
  • "tomorrow afternoon" → I'll use 2pm
  • "next Monday" → I'll find the right date
  • "morning" → I'll set it for 9am

💡 **Pro tip:** You can also ask me for scheduling suggestions or just chat!
"""

    def handle_greeting(self) -> str:
        """Handle greetings naturally."""
        greetings = [
            "Hey there! 👋 How can I help you today?",
            "Hi! 😊 What can I do for you?",
            "Hello! Ready to help with your schedule!",
            "Hey! What's on your mind?"
        ]
        
        if self.user_name:
            greetings = [
                f"Hey {self.user_name}! 👋 What can I help with?",
                f"Hi {self.user_name}! 😊 How's it going?",
                f"Hello {self.user_name}! Ready to help!",
            ]
        
        return random.choice(greetings)

    def handle_gratitude(self) -> str:
        """Handle thank you messages."""
        responses = [
            "You're very welcome! 😊 Anything else I can help with?",
            "Happy to help! Let me know if you need anything else!",
            "My pleasure! 🎉 Feel free to ask if you need more help!",
            "Glad I could assist! Is there anything else?",
        ]
        return random.choice(responses)

    def handle_smalltalk(self) -> str:
        """Handle small talk."""
        responses = [
            "I'm doing great, thanks for asking! 😊 How about you? Need help with anything?",
            "All good here! Ready to help with your schedule. What's up?",
            "I'm here and ready to help! What can I do for you today?",
        ]
        return random.choice(responses)

    def process_input(self, user_input: str) -> str:
        """Main processing pipeline with natural conversation."""
        intent = self.extract_intent(user_input)
        entities = self.extract_entities(user_input)
        
        print(f"\n[DEBUG] Intent: {intent} | Entities: {entities}")
        
        # Handle name introduction
        if intent == 'introduce_name' or (not self.user_name and entities.get('name')):
            self.user_name = entities.get('name')
            return f"Nice to meet you, {self.user_name}! 😊 I'm here to help manage your schedule. Try saying something like 'schedule a meeting tomorrow at 2pm'!"
        
        # Conversational intents
        if intent == 'greeting':
            return self.handle_greeting()
        
        if intent == 'gratitude':
            return self.handle_gratitude()
        
        if intent == 'smalltalk':
            return self.handle_smalltalk()
        
        if intent == 'help':
            return self.show_help()
        
        # Handle confirmations for pending actions
        if intent == 'confirm' and self.pending_event:
            result = self.add_event(
                self.pending_event.get('date'),
                self.pending_event.get('event'),
                self.pending_event.get('time'),
                self.pending_event.get('duration')
            )
            self.pending_event = {}
            return result
        
        if intent == 'deny' and self.pending_event:
            self.pending_event = {}
            return "No problem! The event wasn't added. What else can I help with?"
        
        # Main functionality
        if intent == 'add_event':
            event = entities.get('event')
            date = entities.get('date')
            time = entities.get('time')
            duration = entities.get('duration')
            
            if not event:
                return "🤔 Sure! What would you like me to schedule?"
            if not date:
                return f"📅 Got it - '{event}'. When should I schedule this?"
            
            result = self.add_event(date, event, time, duration)
            
            # Check if there's a conflict and store pending event
            if "⚠️" in result:
                self.pending_event = {'date': date, 'event': event, 'time': time, 'duration': duration}
            
            return result
        
        elif intent == 'check_schedule':
            if any(word in user_input.lower() for word in ['week', 'next 7', 'coming days', 'next few']):
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
            helpful_suggestions = [
                "🤔 I'm not quite sure what you mean. Try something like:\n  • 'Schedule a meeting tomorrow at 3pm'\n  • 'What's on my calendar?'\n  • 'Show me this week'",
                "🤔 Hmm, I didn't catch that. You can say things like:\n  • 'Add lunch with Alex on Friday'\n  • 'When am I free?'\n  • Type 'help' to see more!",
            ]
            return random.choice(helpful_suggestions)

        self.set_context(intent, entities)


if __name__ == '__main__':
    bot = SchedulingChatbot()
    
    print("\n" + "=" * 80)
    print("🎬 CONVERSATIONAL DEMO")
    print("=" * 80)
    
    demo_commands = [
        "Hi there!",
        "My name is Alex",
        "Schedule team meeting tomorrow at 3pm",
        "Can you add doctor appointment on Friday at 9:30am?",
        "Book lunch next Monday at noon",
        "What's on my calendar tomorrow?",
        "Show me this week",
        "When am I free this week?",
        "Thanks!",
        "What can you do?"
    ]
    
    for cmd in demo_commands:
        print(f"\n💬 User: {cmd}")
        response = bot.process_input(cmd)
        print(f"🤖 Bot: {response}")
        print("-" * 80)