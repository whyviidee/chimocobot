#!/usr/bin/env python3
"""
iCloud Calendar Integration via CalDAV
Pulls events from Yuri's iCloud calendar
"""

import os
from datetime import datetime, timedelta
from caldav import DAVClient
from icalendar import Calendar as iCal
import pytz

# Load credentials from .env
ICLOUD_EMAIL = os.getenv("ICLOUD_EMAIL", "ydagot@icloud.com")
ICLOUD_APP_PASSWORD = os.getenv("ICLOUD_APP_PASSWORD")
TIMEZONE = os.getenv("TIMEZONE", "WET")

class iCloudCalendar:
    def __init__(self):
        self.email = ICLOUD_EMAIL
        self.password = ICLOUD_APP_PASSWORD
        self.timezone = pytz.timezone("Europe/Lisbon")  # WET = Lisboa
        self.client = None
        self.principal = None
        
    def connect(self):
        """Establish connection to iCloud CalDAV"""
        try:
            url = "https://caldav.icloud.com/"
            self.client = DAVClient(url=url, username=self.email, password=self.password)
            self.principal = self.client.principal()
            print("✅ Connected to iCloud CalDAV")
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def get_calendars(self):
        """List all available calendars"""
        try:
            calendars = self.principal.calendars()
            calendar_list = []
            for cal in calendars:
                calendar_list.append({
                    "name": cal.name,
                    "url": str(cal.url),
                    "description": getattr(cal, "description", "N/A")
                })
            return calendar_list
        except Exception as e:
            print(f"❌ Error fetching calendars: {e}")
            return []
    
    def get_events_today(self):
        """Get events for today"""
        return self.get_events_for_dates(
            start=datetime.now(self.timezone),
            end=datetime.now(self.timezone) + timedelta(days=1)
        )
    
    def get_events_next_days(self, days=3):
        """Get events for next N days"""
        return self.get_events_for_dates(
            start=datetime.now(self.timezone),
            end=datetime.now(self.timezone) + timedelta(days=days)
        )
    
    def get_events_for_dates(self, start, end):
        """Get events between two dates"""
        try:
            events = []
            calendars = self.principal.calendars()
            
            for cal in calendars:
                try:
                    # Search for events in date range
                    cal_events = cal.search(
                        start=start,
                        end=end,
                        expand=True
                    )
                    
                    for event in cal_events:
                        event_data = self._parse_event(event)
                        if event_data:
                            events.append(event_data)
                except Exception as e:
                    print(f"⚠️ Error reading calendar {cal.name}: {e}")
                    continue
            
            # Sort by start time
            events.sort(key=lambda x: x.get("start", ""))
            return events
        except Exception as e:
            print(f"❌ Error fetching events: {e}")
            return []
    
    def _parse_event(self, event):
        """Parse iCalendar event into dict"""
        try:
            # Use icalendar_component for caldav 2.0
            ical = event.icalendar_component
            
            if not ical:
                return None
            
            # Extract key fields from component
            summary = str(ical.get("summary", "Untitled"))
            start = ical.get("dtstart")
            end = ical.get("dtend")
            description = str(ical.get("description", ""))
            location = str(ical.get("location", ""))
            
            # Convert datetime objects
            if start:
                if hasattr(start, "dt"):
                    start_dt = start.dt
                else:
                    start_dt = start
            else:
                start_dt = None
            
            if end:
                if hasattr(end, "dt"):
                    end_dt = end.dt
                else:
                    end_dt = end
            else:
                end_dt = None
            
            return {
                "summary": summary,
                "description": description,
                "location": location,
                "start": start_dt.isoformat() if start_dt else None,
                "end": end_dt.isoformat() if end_dt else None,
            }
        except Exception as e:
            print(f"⚠️ Error parsing event: {e}")
            return None
    
    def format_events_for_display(self, events):
        """Format events nicely for Telegram"""
        if not events:
            return "Sem eventos encontrados."
        
        formatted = []
        current_date = None
        
        for event in events:
            try:
                start_str = event.get("start", "")
                start_dt = datetime.fromisoformat(start_str.replace("Z", "+00:00"))
                
                # Group by date
                event_date = start_dt.strftime("%d/%m/%Y")
                if event_date != current_date:
                    current_date = event_date
                    formatted.append(f"\n**{event_date}**")
                
                # Format time
                time_str = start_dt.strftime("%H:%M")
                summary = event.get("summary", "Untitled")
                location = event.get("location", "")
                
                location_str = f" @ {location}" if location else ""
                formatted.append(f"• {time_str} → {summary}{location_str}")
            except Exception as e:
                print(f"⚠️ Error formatting event: {e}")
                continue
        
        return "\n".join(formatted)

# Test function
if __name__ == "__main__":
    cal = iCloudCalendar()
    
    print("🔐 Connecting to iCloud...")
    if cal.connect():
        print("\n📅 Available calendars:")
        for calendar in cal.get_calendars():
            print(f"  • {calendar['name']}")
        
        print("\n📅 Events today:")
        today_events = cal.get_events_today()
        print(cal.format_events_for_display(today_events))
        
        print("\n📅 Events (next 3 days):")
        next_events = cal.get_events_next_days(3)
        print(cal.format_events_for_display(next_events))
    else:
        print("❌ Failed to connect to iCloud")
