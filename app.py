"""
Umami Comms — Nori HR Policy Bot
Handles Slack events, slash commands, and DMs.
"""

import os
import re
import threading
from flask import Flask, request, jsonify
from slack_sdk import WebClient
from slack_sdk.signature import SignatureVerifier
import anthropic

app = Flask(__name__)

slack_client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])
signature_verifier = SignatureVerifier(os.environ["SLACK_SIGNING_SECRET"])
anthropic_client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

processed_events = set()

HANDBOOK = """
SECTION 1 - CULTURE & WORKPLACE EXPECTATIONS
Core values: Respect, Integrity, Innovation. Also: Competitive, Honest, Free-Spirited, Agile, Caring, Ambitious, Tolerant, Bold, Humble.
Professional Behaviour: Punctuality required. Business casual for office/video; business professional for client meetings. No gossip; solutions-focused.
Confidentiality: Always protect client info and company-sensitive data. Consult HR if unsure.
Inclusivity & Diversity: Equal opportunity employer. Zero tolerance for discrimination based on gender, age, race, religion, disability, or sexual orientation. Report harassment to HR immediately.
Company Resources & Technology: Equipment is company property. Used responsibly. Negligence may result in cost recovery. Prohibited: discriminatory content, pornographic material, unlicensed software, confidential sharing, illegal activities.
Social Media: Professional conduct expected. Company equipment may be monitored. Personal accounts linked to employee identity should reflect professionalism.

SECTION 2 - WORKPLACE CONDUCT, ETHICS & COMPLIANCE
Open Door Policy: Discuss concerns with Department Heads, Line Managers, or HR. Strictly confidential.
Sexual Harassment: Zero tolerance. Unwanted advances, propositions, derogatory comments all prohibited. Report to Line Manager, Department Head, or HR. Formal Grievance Form available from HR.
Business Ethics: Highest standards of integrity required. Consult CEO for difficult ethical situations.
Conflicts of Interest: Disclose to Managing Director if you have outside employment or relationships that could influence decisions.
Confidentiality & NDA: Client lists, financial info, strategies are confidential. Improper disclosure = disciplinary action or termination.
Non-Compete: During employment and up to 12 months after termination, no competing business within UAE in same type of work.
Non-Solicitation: 12 months after termination, cannot solicit Umami clients or employees.
Personal Relationships: Allowed but maintain professionalism. No public displays of affection during work hours.

SECTION 3 - EMPLOYMENT ESSENTIALS
Onboarding: Pre-boarding, Day 1, Week 1. Each new joiner gets an Agency Ally. HR check-ins at month 1, 3, and 6.
Probation: Standard 6 months. Performance, attendance, cultural fit evaluated. Not eligible for paid annual leave during probation (but accruing). 14 days notice to terminate during probation by either party.
Employment Classification: Full-Time (5-day hybrid), Part-Time (prorated benefits), Freelancers/Contractors (no employee benefits).
Immigration: HR manages visa/residency. Employee responsible for accurate documents, notifying HR of changes.
Ending Employment: Resignation requires 30 days written notice. Termination possible for performance, restructuring, misconduct. Exit interview conducted by HR. All company property must be returned.

SECTION 4 - WORKING HOURS, FLEXIBILITY & LEAVE
Standard Hours: 9:00 AM to 6:00 PM, Monday to Friday, 1-hour lunch break.
Attendance: Notify Line Manager of absence/lateness no later than 2 hours before start time.
Hybrid Schedule: In-office: Monday, Wednesday, Thursday. Remote: Tuesday, Friday.
Overtime & TOIL: Overtime not remunerated in cash. TOIL = 1 lieu day per authorized weekend worked. Must be used within 1 month. Submit via Bayzat (Lieu Days tab). Weekday overtime: flex hours next day.
Annual Leave: 22 working days per year. Accrual ~1.83 days/month. From 3 months of service, can use accrued leave. Only 50% of unused leave carries forward; remainder forfeited. Not encashed except upon termination after 1 year service (at basic pay rate). Requests via Bayzat.
Public Holidays: All official UAE public holidays. Working on a public holiday = compensatory leave or pay in lieu.
Sick Leave: After probation, up to 90 calendar days/year (first 15 days full pay, next 30 days half pay, remainder unpaid per UAE law). Notify Line Manager within 2 hours of start time. Doctor certificate required for absences over 2 days.
Maternity Leave: Less than 1 year = 45 days full pay. 1-3 years = 90 days full pay. 3+ years = 180 days full pay. Next 15 days at 50% pay. Return-to-work expected within 1 year. Nursing breaks: 1-2 daily (up to 1 hr total) for 6 months post-return.
Paternity Leave: 30 calendar days fully paid, taken intermittently or concurrently over 6 months after birth. Must continue employment for at least 1 year after.
Compassionate Leave: 10 days for spouse death; 5 days for parent, sibling, child, grandparent. Upload on Bayzat Compassionate Leave tab.
Hajj Leave: 30 days unpaid (once during employment).
Study Leave: 10 business days for state-approved education; requires 2+ years service.
Birthday Leave: Paid day off on birthday (weekday). If weekend, take preceding Friday. Cannot combine with other leave. Submit via Bayzat 2 weeks in advance.
Personal Leave: 5 days per calendar year for essential personal tasks (bank, doctor, moving). Cannot combine with other leave.
Remote Work Global: 1+ year of service, no disciplinary issues. Up to 5 consecutive days per year. Submit 1 month in advance. Must be available 9AM-6PM Dubai time. Data roaming charges deducted from salary.
Remote Work Local: Must be physically in UAE. Post-probation only. Must attend in-person if required.
Christmas Day: December 25 is a paid holiday. If already on annual leave, Christmas Day is part of that leave.
Unpaid Leave: First 3 months typically unpaid. Post-3-months, available when annual leave exhausted, subject to approval.
Handover Policy: Written handover document required before any leave. Handover meeting at least 1 working day before leave start. Debrief upon return.

SECTION 5 - COMPENSATION & BENEFITS
Salary: Paid monthly on 28th via UAE WPS in AED. Basic pay + allowances per contract. Salary details strictly confidential.
Salary Review: Annual, based on KPIs, performance, market benchmarks, company performance. Not automatic.
End-of-Service Gratuity: Requires 1 year continuous service. 1-5 years = 21 days basic pay/year. 5+ years = 30 days basic pay/year. Max = 2 years basic salary. Paid within 14 days of termination.
EOSB Beneficiary Nomination: Voluntary but recommended. HR provides Beneficiary Appointment Form.
Medical Insurance: Provided to Umami-sponsored employees. Details on Bayzat app. Must disclose pre-existing/chronic conditions before employment. Optional upgrades/dependents at employee expense.
Annual Ticket Allowance: After 1 year service. AED 3,500 cap. Options: book via Airlink, book independently for reimbursement, or cash-out. 4-month claim window from work anniversary. Submit via Bayzat.
Expense Reimbursement: Submit via Bayzat with receipts. Day-to-day: by 4th of following month. International travel: within 15 days of return. Pre-approval required for expenses over AED 500. Petrol to Abu Dhabi: AED 150 cap per round trip. Taxis: Hala/Bolt with digital invoice. Non-reimbursable: personal meals, alcohol unless pre-approved client event, personal entertainment, fines, premium vehicles without approval.

SECTION 6 - HEALTH, SAFETY & WELLBEING
Safety: Follow UAE & DMCC regulations. Report hazards to HR. Emergency evacuation routes are marked.
Smoking: Prohibited in workplace. E-cigarettes/vapes permitted on terrace only.
Wellness: Up to 2 wellness workshops per year. Health check-ups, mental wellbeing resources, financial literacy sessions may be offered.

SECTION 7 - PERFORMANCE & DEVELOPMENT
Goal Setting: SMART goals set at start of year with manager. Mid-year check-ins.
Performance Reviews: Quarterly formal reviews. Cover goals, values, collaboration, areas for improvement.
Written Warning: Active for 6 months. Employees on written warning generally ineligible for salary increase or promotion for 12 months.
Learning & Development: Train the Trainer, workshops, on-the-job learning, Individual Development Plans.

SECTION 8 - PROBLEM-SOLVING & RESOLUTION
Progressive Discipline: Verbal warning, Written warning, Final written warning, Termination.
Immediate Termination Grounds: Forged documents, material damage, safety violations, repeated duty failure despite 2 written warnings, confidential info disclosure, intoxication at work, workplace assault, 20+ non-consecutive or 7 consecutive unjustified absences, abuse of position, unauthorized employment elsewhere.
Grievance Procedure: Informal (talk to manager or HR), Formal (written to HR), Investigation (10 working days), Outcome in writing (5 working days), Appeal within 5 working days of outcome. No retaliation for good-faith grievances.

SECTION 9 - OFFBOARDING & EXIT
Resignation: Written notice to Line Manager, HOD, and HR. Minimum 30 days notice. Continue duties and complete handover.
Termination by Company: For performance, misconduct, or redundancy.
Garden Leave: Company may require employee to stay away from office during notice period while on full pay.
Final Settlement: Final salary, unused annual leave payment, gratuity. All within 14 days of termination.
Exit Procedures: Return all company property. Clear advances. Exit interview with HR. Activate Out-of-Office email. Reference letters: neutral employment certificate provided; additional reference at management discretion.

KEY CONTACTS:
HR (leaves, benefits, general): hr@umamicomms.com
Finance/Payroll: finance@umamicomms.com
COO: Sara El Choueiry | sara@umamicomms.com
Office: 103 Tamweel Tower, Cluster U, JLT, Dubai | +97145726990
"""

SYSTEM_PROMPT = """You are Nori, Umami Comms' friendly HR Policy Assistant. You are warm, approachable, and knowledgeable.
Your ONLY knowledge source is the employee handbook content below. Never use outside knowledge.

PERSONALITY:
- Warm and approachable, never robotic
- Use a conversational tone while staying professional
- Occasionally use light friendly language like "Happy to help with that!"

RULES:
1. Answer ONLY from the handbook. If the answer is not there, say so clearly.
2. Every answer MUST end with: :books: *Source: [exact section name]*
3. For sensitive matters requiring human judgment such as active grievances, disciplinary cases, salary negotiations, visa problems, medical situations, or personal complaints about colleagues, respond with: "This is best handled directly by the HR team. Please reach out to hr@umamicomms.com for confidential support. I am always here for policy questions though! :handshake:"
4. Keep answers concise, warm, and employee-friendly. Use plain English.
5. If a question is unrelated to HR or the handbook, say: "That one is outside my expertise. I am Nori, Umami HR policy guide! Ask me anything about our policies."
6. Format responses for Slack: use *single asterisks* for bold, use - for bullet points, never use ## headers or **double asterisks**.
7. If someone asks who you are, say: "Hi! I am *Nori*, Umami's HR Policy Assistant. I am here to help you navigate our employee handbook. Ask me anything about leave, benefits, working hours, or any other policy."

HANDBOOK:
""" + HANDBOOK


def format_for_slack(text):
    text = re.sub(r'\*\*(.+?)\*\*', r'*\1*', text)
    text = re.sub(r'#{1,3}\s*(.+)', r'*\1*', text)
    text = re.sub(r'```[\w]*', '', text)
    return text.strip()


def ask_claude(question):
    try:
        message = anthropic_client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": question}]
        )
        return format_for_slack(message.content[0].text)
    except Exception as e:
        return "I am having trouble connecting right now. Please contact HR directly at hr@umamicomms.com"


def reply_in_thread(channel, thread_ts, text):
    slack_client.chat_postMessage(channel=channel, thread_ts=thread_ts, text=text)


def reply_dm(channel, text):
    slack_client.chat_postMessage(channel=channel, text=text)


def verify_slack_request(req):
    return signature_verifier.is_valid_request(req.get_data(), req.headers)


@app.route("/slack/command", methods=["POST"])
def slash_command():
    if not verify_slack_request(request):
        return jsonify({"error": "Unauthorized"}), 401

    question = request.form.get("text", "").strip()
    user_id = request.form.get("user_id", "")
    response_url = request.form.get("response_url", "")

    if not question:
        return jsonify({
            "response_type": "ephemeral",
            "text": "Hi! I am Nori. Ask me anything about Umami HR policies.\nUsage: /hrpolicy How many annual leave days do I get?"
        })

    def process_and_respond():
        answer = ask_claude(question)
        import urllib.request, json as json_lib
        payload = json_lib.dumps({
            "response_type": "in_channel",
            "text": "*<@" + user_id + "> asked:* " + question + "\n\n" + answer
        }).encode("utf-8")
        req = urllib.request.Request(
            response_url,
            data=payload,
            headers={"Content-Type": "application/json"}
        )
        urllib.request.urlopen(req)

    threading.Thread(target=process_and_respond).start()

    return jsonify({
        "response_type": "ephemeral",
        "text": "Looking that up for you..."
    })


@app.route("/slack/events", methods=["POST"])
def slack_events():
    if not verify_slack_request(request):
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json

    if data.get("type") == "url_verification":
        return jsonify({"challenge": data["challenge"]})

    event = data.get("event", {})
    event_id = data.get("event_id", "")
    event_type = event.get("type")

    if event_id in processed_events:
        return jsonify({"ok": True})
    processed_events.add(event_id)
    if len(processed_events) > 500:
        processed_events.clear()

    if event.get("bot_id") or event.get("subtype") == "bot_message":
        return jsonify({"ok": True})

    user_id = event.get("user", "")
    text = event.get("text", "").strip()
    channel = event.get("channel", "")
    ts = event.get("ts", "")
    channel_type = event.get("channel_type", "")

    text_clean = re.sub(r"<@[A-Z0-9]+>", "", text).strip()

    if not text_clean:
        return jsonify({"ok": True})

    if event_type == "message" and channel_type == "im":
        def handle_dm():
            answer = ask_claude(text_clean)
            reply_dm(channel, answer)
        threading.Thread(target=handle_dm).start()
        return jsonify({"ok": True})

    hr_channel_name = os.environ.get("HR_CHANNEL_NAME", "ask-nori")
    try:
        channel_info = slack_client.conversations_info(channel=channel)
        channel_name = channel_info["channel"]["name"]
    except Exception:
        channel_name = ""

    if event_type == "message" and channel_name == hr_channel_name:
        def handle_channel():
            answer = ask_claude(text_clean)
            reply_in_thread(channel, ts, answer)
        threading.Thread(target=handle_channel).start()
        return jsonify({"ok": True})

    return jsonify({"ok": True})


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "bot": "Nori - Umami HR Policy Assistant"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)
