#!/usr/bin/env python3
"""Debug script to understand caldav event structure"""

import os
from caldav import DAVClient
import json

ICLOUD_EMAIL = os.getenv("ICLOUD_EMAIL", "ydagot@icloud.com")
ICLOUD_APP_PASSWORD = os.getenv("ICLOUD_APP_PASSWORD")

url = "https://caldav.icloud.com/"
client = DAVClient(url=url, username=ICLOUD_EMAIL, password=ICLOUD_APP_PASSWORD)
principal = client.principal()

print("✅ Connected!")
print("\n📅 Calendars:")

calendars = principal.calendars()
for cal in calendars:
    print(f"\n--- {cal.name} ---")
    try:
        events = cal.search()
        print(f"Found {len(events)} events")
        
        if events:
            event = events[0]
            print(f"Event type: {type(event)}")
            print(f"Event dir: {[x for x in dir(event) if not x.startswith('_')]}")
            print(f"\nFirst event data:")
            
            # Try different ways to access data
            if hasattr(event, "data"):
                print(f"Has .data: {type(event.data)}")
                print(f"Data sample: {str(event.data)[:200]}")
            
            if hasattr(event, "vobject"):
                print(f"Has .vobject: {type(event.vobject)}")
            
            if hasattr(event, "instance"):
                print(f"Has .instance: {type(event.instance)}")
                
            # Print raw attributes
            for attr in ["summary", "dtstart", "dtend", "description", "location"]:
                try:
                    val = getattr(event, attr, "NOT_FOUND")
                    print(f"  .{attr} = {val} ({type(val).__name__})")
                except:
                    print(f"  .{attr} = ERROR")
    except Exception as e:
        print(f"Error: {e}")
