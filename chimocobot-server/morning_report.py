#!/usr/bin/env python3
"""
Morning Report Generator
Pulls calendar data and generates beautiful Telegram summary
"""

from icloud_calendar import iCloudCalendar
from datetime import datetime, timedelta
import pytz

def generate_morning_report():
    """Generate complete morning report with calendar data"""
    
    tz = pytz.timezone("Europe/Lisbon")
    cal = iCloudCalendar()
    
    # Connect to iCloud
    if not cal.connect():
        return "❌ Erro a conectar ao calendário. Tenta mais tarde."
    
    # Get data
    today_events = cal.get_events_today()
    next_events = cal.get_events_next_days(3)
    
    # Build report
    report = []
    report.append("☀️ **Bom dia, Yuri!**\n")
    report.append(f"📅 **{datetime.now(tz).strftime('%A, %d de %B')}**\n")
    
    # Today's schedule
    if today_events:
        report.append("**📋 Hoje:**")
        for event in today_events:
            start = event["start"]
            if start:
                dt = datetime.fromisoformat(start.replace("Z", "+00:00"))
                time_str = dt.strftime("%H:%M")
                summary = event["summary"]
                location = event["location"]
                
                if location:
                    report.append(f"• {time_str} → {summary} @ {location}")
                else:
                    report.append(f"• {time_str} → {summary}")
    else:
        report.append("**📋 Hoje:** Sem eventos marcados")
    
    report.append("")
    
    # Next days
    report.append("**📆 Próximos 3 dias:**")
    if next_events:
        current_date = None
        for event in next_events:
            start = event["start"]
            if start:
                dt = datetime.fromisoformat(start.replace("Z", "+00:00"))
                event_date = dt.strftime("%d/%m")
                day_name = dt.strftime("%A").capitalize()
                
                # Group by date
                if event_date != current_date:
                    current_date = event_date
                    report.append(f"\n{day_name} ({event_date}):")
                
                time_str = dt.strftime("%H:%M")
                summary = event["summary"]
                report.append(f"  • {time_str} — {summary}")
    else:
        report.append("Sem eventos próximos")
    
    report.append("")
    report.append("---")
    report.append("Tens algo novo pra hoje? Quer reschedulizar algo? Estou aqui. 🔥")
    
    return "\n".join(report)

if __name__ == "__main__":
    print(generate_morning_report())
