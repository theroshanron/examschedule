from flask import Flask, request, send_file, render_template, redirect, url_for
from datetime import datetime
import pytz
import io
import os

app = Flask(__name__)

schedule = {
    "EFM-02": {"name": "Security Analysis and Portfolio Management", "date": "2025-04-06", "time": "17:30-20:30"},
    "EFM-01": {"name": "Advanced Management Accounting", "date": "2025-04-06", "time": "17:30-20:30"},
    "EOM-01": {"name": "Supply Chain Management", "date": "2025-04-12", "time": "17:30-20:30"},
    "EHL-01": {"name": "Advanced Corporate Communication", "date": "2025-04-12", "time": "17:30-20:30"},
    "EIT-02": {"name": "Cyber Security and Privacy", "date": "2025-04-13", "time": "13:30-16:30"},
    "EMM-03": {"name": "Product and Brand Management", "date": "2025-04-13", "time": "13:30-16:30"},
    "ESM-02": {"name": "Management of Technology and Innovation", "date": "2025-04-19", "time": "17:30-20:30"},
    "EEC-01": {"name": "Game Theory", "date": "2025-04-19", "time": "17:30-20:30"},
    "EHR-01": {"name": "Leading Self and Organization", "date": "2025-04-20", "time": "13:30-16:30"},
    "EFM-12": {"name": "Advance Corporate Finance", "date": "2025-04-20", "time": "13:30-16:30"},
    "EFM-03": {"name": "Project Finance", "date": "2025-04-20", "time": "13:30-16:30"},
    "EMM-14": {"name": "Marketing Meets Technology", "date": "2025-04-20", "time": "17:30-20:30"},
    "EMM-01": {"name": "Managing Business Markets", "date": "2025-04-20", "time": "17:30-20:30"},
    "EMM-16": {"name": "Understanding Our Social World", "date": "2025-04-20", "time": "17:30-20:30"},
    "EOM-02": {"name": "Lean Six Sigma", "date": "2025-04-26", "time": "13:30-16:30"},
    "EHL-06": {"name": "Democracy, Politics and Institutions", "date": "2025-04-26", "time": "13:30-16:30"},
    "EHL-02": {"name": "Cross Cultural Communication", "date": "2025-04-26", "time": "17:30-20:30"},
    "ESM-01": {"name": "Strategy Implementation", "date": "2025-04-26", "time": "17:30-20:30"},
    "ESM-03": {"name": "Mergers & Strategic Alliances", "date": "2025-04-26", "time": "17:30-20:30"},
    "EIT-01": {"name": "AI for Business", "date": "2025-04-27", "time": "13:30-16:30"},
    "EMM-02": {"name": "Strategic Marketing", "date": "2025-04-27", "time": "17:30-20:30"},
    "EEC-02": {"name": "Introduction to Public Policy", "date": "2025-04-27", "time": "17:30-20:30"},
    "EEC-03": {"name": "Agent-based Simulation", "date": "2025-04-27", "time": "17:30-20:30"},
    "WS-01": {"name": "Leadership and Corporate Accountability", "date": "2025-05-10", "time": "09:30-12:30"},
    "WS-02": {"name": "International Business", "date": "2025-05-10", "time": "14:00-17:00"}
}

bpp_schedule = {
    "BPP-Briefing": {"name": "Briefing on BPP (Time: 10:00 AM)", "date": "2025-01-05"},
    "BPP-Proposal": {"name": "BPP Proposal Submission (Time: 11:59 PM)", "date": "2025-03-25"},
    "BPP-Mentor-Intimation": {"name": "Mentor Allotment (Time: 11:59 PM)", "date": "2025-04-20"},
    "BPP-Interim-Report": {"name": "Interim Report to Mentor (Time: 11:59 PM)", "date": "2025-08-01"},
    "BPP-Interim-Feedback": {"name": "Interim Feedback from Mentor (Time: 11:59 PM)", "date": "2025-08-25"},
    "BPP-Final-Report-Submission": {"name": "Final Report + Pitch Video (Time: 11:59 PM)", "date": "2025-11-10"},
    "BPP-Softcopy-Final": {"name": "Final Soft Copy Upload (Time: 11:59 PM)", "date": "2025-11-30"},
    "BPP-Hardcopy-Final": {"name": "Final Hard Copy to LIVE (Time: 11:59 PM)", "date": "2025-12-16"},
    "BPP-Presentation": {"name": "BPP Presentation & Evaluation (Time: 09:00 AM)", "date": "2026-01-05"},
    "Session-Intro": {"name": "IIMK LIVE Intro (Time: 09:00 AM)", "date": "2025-01-04"},
    "BPP-GroupFormation": {"name": "Group Formation & Proposal (Time: 11:59 PM)", "date": "2025-03-01"},
    "BPP-FirstProgress": {"name": "1st Progress Report (Time: 11:59 PM)", "date": "2025-04-26"},
    "BPP-SecondProgress": {"name": "2nd Progress Report (Time: 11:59 PM)", "date": "2025-05-26"},
    "BPP-ThirdProgress": {"name": "3rd Progress Report (Time: 11:59 PM)", "date": "2025-06-26"},
    "BPP-FourthProgress": {"name": "4th Progress Report (Time: 11:59 PM)", "date": "2025-07-26"},
    "BPP-FifthProgress": {"name": "5th Progress Report (Time: 11:59 PM)", "date": "2025-09-25"}
}

bpp_sessions = {
    "Session-01": {"name": "Session 1: Introduction to IIMK LIVE - A to F", "date": "2025-01-04"},
    "Session-02": {"name": "Session 2: Customer Validation and Product Market Fit - A", "date": "2025-03-15", "time": "12:15-01:15"},
    "Session-03": {"name": "Session 3: Customer Validation and Product Market Fit - B", "date": "2025-03-15", "time": "01:30-02:30"},
    "Session-04": {"name": "Session 4: Customer Validation and Product Market Fit - D", "date": "2025-03-29", "time": "09:30-10:30"},
    "Session-05": {"name": "Session 5: Customer Validation and Product Market Fit - C", "date": "2025-03-29", "time": "12:15-01:15"},
    "Session-06": {"name": "Session 6: Digital Marketing Strategies and Tools - A", "date": "2025-04-05", "time": "09:00-10:00"},
    "Session-07": {"name": "Session 7: Startup Scale-up and Growth - A", "date": "2025-04-05", "time": "10:05-11:15"},
    "Session-08": {"name": "Session 8: Digital Marketing Strategies and Tools - B", "date": "2025-04-05", "time": "10:15-11:15"},
    "Session-09": {"name": "Session 9: Startup Scale-up and Growth - B", "date": "2025-04-05", "time": "12:15-01:15"},
    "Session-10": {"name": "Session 10: Digital Marketing Strategies and Tools - C", "date": "2025-04-05", "time": "12:15-01:15"},
    "Session-11": {"name": "Session 11: How to Make an Effective Pitch - A", "date": "2025-04-05", "time": "01:30-02:30"},
    "Session-12": {"name": "Session 12: Startup Scale-up and Growth - C", "date": "2025-04-05", "time": "01:30-02:30"},
    "Session-13": {"name": "Session 13: Customer Validation and Product Market Fit - E", "date": "2025-04-05", "time": "01:30-02:30"},
    "Session-14": {"name": "Session 14: Digital Marketing Strategies and Tools - D", "date": "2025-05-03", "time": "09:00-10:00"},
    "Session-15": {"name": "Session 15: Startup Scale-up and Growth - D", "date": "2025-05-03", "time": "09:00-10:00"},
    "Session-16": {"name": "Session 16: Digital Marketing Strategies and Tools - E", "date": "2025-05-03", "time": "10:15-11:15"},
    "Session-17": {"name": "Session 17: Startup Scale-up and Growth - E", "date": "2025-05-03", "time": "10:15-11:15"},
    "Session-18": {"name": "Session 18: Digital Marketing Strategies and Tools - F", "date": "2025-05-03", "time": "12:15-01:15"},
    "Session-19": {"name": "Session 19: Art of Fund Raising - E", "date": "2025-05-03", "time": "01:30-02:30"},
    "Session-20": {"name": "Session 20: Customer Validation and Product Market Fit - F", "date": "2025-05-03", "time": "01:30-02:30"},
    "Session-21": {"name": "Session 21: How to Make an Effective Pitch - C", "date": "2025-05-17", "time": "09:00-10:00"},
    "Session-22": {"name": "Session 22: How to Make an Effective Pitch - D", "date": "2025-05-17", "time": "10:15-11:15"},
    "Session-23": {"name": "Session 23: How to Make an Effective Pitch - E", "date": "2025-05-17", "time": "12:15-01:15"},
    "Session-24": {"name": "Session 24: How to Make an Effective Pitch - F", "date": "2025-05-17", "time": "01:30-02:30"},
    "Session-25": {"name": "Session 25: Art of Fund Raising - A", "date": "2025-05-31", "time": "09:00-10:00"},
    "Session-26": {"name": "Session 26: Art of Fund Raising - B", "date": "2025-05-31", "time": "10:15-11:15"},
    "Session-27": {"name": "Session 27: Art of Fund Raising - C", "date": "2025-05-31", "time": "12:15-01:15"},
    "Session-28": {"name": "Session 28: Art of Fund Raising - D", "date": "2025-05-31", "time": "01:30-02:30"},
    "Session-29": {"name": "Session 29: Declaration of Final Score", "date": "2026-03-01"},
    "Session-30": {"name": "Session 30: Final Evaluation and Feedback", "date": "2026-03-02"},
    "Session-31": {"name": "Session 31: BPP Wrap-up and Acknowledgement", "date": "2026-03-03"},
    "Session-32": {"name": "Session 32: Guest Talk - Innovation in Startups", "date": "2026-03-04"},
    "Session-33": {"name": "Session 33: Mock Pitch Evaluation", "date": "2026-03-05"},
    "Session-34": {"name": "Session 34: Elevator Pitch Day", "date": "2026-03-06"},
    "Session-35": {"name": "Session 35: Final Pitch Recording", "date": "2026-03-07"},
    "Session-36": {"name": "Session 36: Report Review Session", "date": "2026-03-08"},
    "Session-37": {"name": "Session 37: Mentor Feedback Roundtable", "date": "2026-03-09"},
    "Session-38": {"name": "Session 38: Team Collaboration Techniques", "date": "2026-03-10"},
    "Session-39": {"name": "Session 39: Business Model Canvas Deep Dive", "date": "2026-03-11"},
    "Session-40": {"name": "Session 40: Funding & Financial Planning", "date": "2026-03-12"},
    "Session-41": {"name": "Session 41: Peer Feedback & Refinement", "date": "2026-03-13"},
    "Session-42": {"name": "Session 42: Mock Investor Meeting", "date": "2026-03-14"},
    "Session-43": {"name": "Session 43: Capstone Evaluation", "date": "2026-03-15"},
    "Session-44": {"name": "Session 44: Final Submission Celebration", "date": "2026-03-16"}
}

@app.route('/bpp-sessions')
def bpp_sessions_page():
    return render_template('bpp_sessions.html', subjects=bpp_sessions)

@app.route('/generate-bpp-sessions', methods=['POST'])
def generate_bpp_sessions():
    selected = request.form.getlist('subjects')
    ics = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//IIMK BPP Sessions Calendar//EN",
        "CALSCALE:GREGORIAN"
    ]

    for code in selected:
        sub = bpp_sessions[code]
        name, date_str, time_str = sub["name"], sub["date"], sub["time"]
        start, end = time_str.split('-')
        start_dt = datetime.strptime(f"{date_str} {start}", "%Y-%m-%d %H:%M")
        end_dt = datetime.strptime(f"{date_str} {end}", "%Y-%m-%d %H:%M")

        ics += [
            "BEGIN:VEVENT",
            f"UID:{code}@iimk.bpp.session",
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
    with open("bpp_sessions.ics", "w", encoding="utf-8") as f:
        f.write("\n".join(ics))
    return redirect(url_for('download_bpp_sessions'))

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

    with open("schedule.ics", "w", encoding="utf-8") as f:
        f.write(ics_data)

    return redirect(url_for('download_ics'))

@app.route('/bpp')
def bpp():
    return render_template('bpp.html', subjects=bpp_schedule)

@app.route('/generate-bpp', methods=['POST'])
def generate_bpp():
    selected = request.form.getlist('subjects')
    ics = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//IIMK BPP Calendar//EN",
        "CALSCALE:GREGORIAN"
    ]
    for code in selected:
        item = bpp_schedule[code]
        date_str = item['date']
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        ics += [
            "BEGIN:VEVENT",
            f"UID:{code}@iimk.bpp",
            f"DTSTAMP:{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}",
            f"SUMMARY:{item['name']}",
            f"DTSTART;VALUE=DATE:{dt.strftime('%Y%m%d')}",
            f"DTEND;VALUE=DATE:{(dt.replace(day=dt.day+1)).strftime('%Y%m%d')}",
            "TRANSP:TRANSPARENT",
            "END:VEVENT"
        ]
    ics.append("END:VCALENDAR")
    with open("bpp_schedule.ics", "w", encoding="utf-8") as f:
        f.write("\n".join(ics))
    return redirect(url_for('download_bpp'))

@app.route('/handbook')
def handbook():
    return render_template("handbook.html")


@app.route('/download')
def download_ics():
    return send_file("schedule.ics", mimetype="text/calendar", as_attachment=True, download_name="exam_schedule.ics")

@app.route('/download-bpp')
def download_bpp():
    return send_file("bpp_schedule.ics", mimetype="text/calendar", as_attachment=True, download_name="bpp_schedule.ics")

@app.route('/download-bpp-sessions')
def download_bpp_sessions():
    return send_file("bpp_sessions.ics", mimetype="text/calendar", as_attachment=True, download_name="bpp_sessions.ics")

if __name__ == '__main__':
    app.run(debug=True)
