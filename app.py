from flask import Flask, request, send_file, render_template
from datetime import datetime
import pytz
import io

app = Flask(__name__)

schedule = {
    "EFM-01": {"name": "Security Analysis and Portfolio Management", "date": "2025-04-06", "time": "17:30-20:30"},
    "EFM-02": {"name": "Advanced Management Accounting", "date": "2025-04-06", "time": "17:30-20:30"},
    "EOM-01": {"name": "Supply Chain Management", "date": "2025-04-12", "time": "17:30-20:30"},
    "EHL-01": {"name": "Advanced Corporate Communication: The Practitioner’s Approach", "date": "2025-04-12", "time": "17:30-20:30"},
    "EIT-02": {"name": "Cyber Security and Privacy", "date": "2025-04-13", "time": "13:30-16:30"},
    "EMM-03": {"name": "Product and Brand Management", "date": "2025-04-13", "time": "13:30-16:30"},
    "ESM-02": {"name": "Management of Technology and Innovation", "date": "2025-04-19", "time": "17:30-20:30"},
    "EEC-01": {"name": "Game Theory", "date": "2025-04-19", "time": "17:30-20:30"},
    "EHR-01": {"name": "Leading Self and Organization", "date": "2025-04-20", "time": "13:30-16:30"},
    "EFM-12": {"name": "Advance Corporate Finance", "date": "2025-04-20", "time": "13:30-16:30"},
    "EFM-03": {"name": "Project Finance", "date": "2025-04-20", "time": "13:30-16:30"},
    "EMM-14": {"name": "Marketing Meets Technology", "date": "2025-04-20", "time": "17:30-20:30"},
    "EMM-01": {"name": "Managing Business Markets", "date": "2025-04-20", "time": "17:30-20:30"},
    "EMM-16": {"name": "Understanding Our Social World: Through Pierre Bourdieu", "date": "2025-04-20", "time": "17:30-20:30"},
    "EOM-02": {"name": "Lean Six Sigma", "date": "2025-04-26", "time": "13:30-16:30"},
    "EHL-06": {"name": "Democracy, Politics and Institutions", "date": "2025-04-26", "time": "13:30-16:30"},
    "EHL-01": {"name": "Cross Cultural Communication", "date": "2025-04-26", "time": "17:30-20:30"},
    "ESM-01": {"name": "Strategy Implementation", "date": "2025-04-26", "time": "17:30-20:30"},
    "ESM-03": {"name": "Mergers, Acquisitions and Strategic Alliances", "date": "2025-04-26", "time": "17:30-20:30"},
    "EIT-01": {"name": "Artificial Intelligence for Business", "date": "2025-04-27", "time": "13:30-16:30"},
    "EMM-02": {"name": "Strategic Marketing", "date": "2025-04-27", "time": "17:30-20:30"},
    "EEC-02": {"name": "Introduction to Public Policy", "date": "2025-04-27", "time": "17:30-20:30"},
    "EEC-03": {"name": "Agent-based Simulation for Business Analytics", "date": "2025-04-27", "time": "17:30-20:30"},
    "WS-01": {"name": "Leadership and Corporate Accountability", "date": "2025-05-10", "time": "09:30-12:30"},
    "WS-02": {"name": "International Business", "date": "2025-05-10", "time": "14:00-17:00"}
}

@app.route('/')
def index():
    return render_template('index.html', subjects=schedule)

@app.route('/generate-ics', methods=['POST'])
def generate_ics():
    selected_subjects = request.form.getlist('subjects')
    ics = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//IIMK Exam Calendar//EN",
        "CALSCALE:GREGORIAN"
    ]

    for code in selected_subjects:
        sub = schedule[code]
        name, date_str, time_str = sub["name"], sub["date"], sub["time"]
        start, end = time_str.split('-')
        start_dt = datetime.strptime(f"{date_str} {start}", "%Y-%m-%d %H:%M")
        end_dt = datetime.strptime(f"{date_str} {end}", "%Y-%m-%d %H:%M")

        ics += [
            "BEGIN:VEVENT",
            f"UID:{code}@iimk.exam",
            f"DTSTAMP:{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}",
            f"SUMMARY:{name}",
            f"DESCRIPTION:{name} - {code}",
            f"LOCATION:IIM Kozhikode",
            f"DTSTART;TZID=Asia/Kolkata:{start_dt.strftime('%Y%m%dT%H%M%S')}",
            f"DTEND;TZID=Asia/Kolkata:{end_dt.strftime('%Y%m%dT%H%M%S')}",
            "BEGIN:VALARM",
            "TRIGGER:-PT10080M",
            "ACTION:DISPLAY",
            "DESCRIPTION:Reminder 1 week before",
            "END:VALARM",
            "BEGIN:VALARM",
            "TRIGGER:-PT1440M",
            "ACTION:DISPLAY",
            "DESCRIPTION:Reminder 1 day before",
            "END:VALARM",
            "END:VEVENT"
        ]

    ics.append("END:VCALENDAR")
    ics_data = "\n".join(ics)

    return send_file(
        io.BytesIO(ics_data.encode("utf-8")),
        mimetype="text/calendar",
        as_attachment=True,
        download_name="exam_schedule.ics"
    )

if __name__ == '__main__':
    app.run(debug=True)
