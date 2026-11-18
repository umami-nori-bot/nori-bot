"""
Umami Comms - Nori HR Policy Bot
Version: 4.0 (November 2026)
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

Umami Comms is a Dubai-based communications agency. We expect all team members to embody our values: curiosity, craft, collaboration, and candour.

Professional Conduct: All employees are expected to maintain a respectful, inclusive, and professional environment. Discrimination, harassment, or bullying of any kind will not be tolerated and should be reported to hr@umamicomms.com immediately.

Dress Code: Smart casual is the standard. Use your judgment for client-facing days.

Confidentiality: All client and company information is confidential. Do not share with third parties without prior written approval.

Social Media: Personal social media use should not reference clients or internal matters without explicit approval.

SECTION 2 - ONBOARDING & PROBATION

Probation Period: All new employees serve a 6-month probation period. Performance will be reviewed at month 3 and month 6. Either party may terminate with 2 weeks notice during probation.

Onboarding: New starters will be assigned a buddy and receive a full onboarding plan covering tools, processes, and team introductions within the first two weeks.

SECTION 3 - REMOTE WORK & FLEXIBILITY

Remote Work Policy: Employees may work remotely up to 3 days per week, subject to manager approval and business needs. Full remote work is not permitted without prior written agreement from your line manager and HR.

Working from Outside the UAE: Working from outside the UAE requires prior approval from HR and the COO. This is handled on a case-by-case basis and may have visa and tax implications. Contact hr@umamicomms.com to initiate a request.

Core Hours: 10:00 AM – 4:00 PM UAE time are core hours where all team members should be reachable, regardless of location.

SECTION 4 - WORKING HOURS, FLEXIBILITY & LEAVE

Standard Working Hours: Sunday to Thursday, 9:00 AM – 6:00 PM (UAE work week). Friday and Saturday are the standard weekend.

Annual Leave: 24 working days per year (accrued monthly). Leave must be approved by your line manager with at least 2 weeks notice for planned leave.

Sick Leave: Up to 90 days per year per UAE Labour Law: first 15 days at full pay, next 30 days at half pay, remaining 45 days unpaid. A medical certificate is required for absences over 2 consecutive days.

Public Holidays: Employees are entitled to all UAE public holidays as announced by the government each year.

Maternity Leave:
- Less than 1 year of service: 45 calendar days at full pay.
- 1 year or more of service: 180 calendar days (6 months) at full pay.
- After maternity leave ends: an additional 15 days may be taken at 50% pay.
- Maternity leave also applies in the case of stillbirth.
- Employees are expected to return to work after leave. If an employee resigns within 6 months of return, any maternity pay received beyond the standard 45 days may be adjusted against their End of Service Benefit (EOSB).
- Nursing breaks: Nursing mothers are entitled to 1–2 nursing breaks per day (up to 1 hour total per day) for 6 months following return to work.

Paternity Leave:
- Less than 1 year of service: 5 calendar days at full pay.
- 1 year or more of service: up to 30 calendar days fully paid, taken flexibly over the 6 months following birth.
- Employees are expected to continue their role after paternity leave. If an employee resigns within 6 months of return, any paternity pay beyond the standard 5 days may be adjusted against their EOSB.

Bereavement Leave: 3 days for immediate family (spouse, child, parent, sibling). 1 day for extended family. Additional unpaid leave may be requested.

Hajj Leave: Once per employment, Muslim employees are entitled to unpaid leave for Hajj (up to 30 days).

SECTION 5 - COMPENSATION & BENEFITS

Salary: Paid monthly on the last working day of the month via bank transfer.

End of Service Benefit (EOSB): Calculated per UAE Labour Law based on length of service and final basic salary.

Medical Insurance: Provided to all Umami-sponsored employees. Full plan details are in Section 10.

SECTION 6 - PERFORMANCE & DEVELOPMENT

Performance Reviews: Conducted twice yearly (mid-year and year-end). Reviews cover goals, competencies, and development plans.

Learning & Development: Employees may request up to AED 3,000 per year for approved learning and development activities. Requests must be submitted to HR and approved by your line manager.

SECTION 7 - EXPENSES & TRAVEL

Business Expenses: Pre-approved business expenses are reimbursable. Submit claims with receipts within 30 days via the standard expenses process. Contact finance@umamicomms.com for the form.

Business Travel: All travel must be pre-approved by your line manager. Economy class for flights under 5 hours; business class may be approved for longer flights. Per diem rates apply and are set by Finance.

SECTION 8 - DISCIPLINARY & GRIEVANCE PROCEDURES

These matters are handled confidentially and directly by HR. For any disciplinary concern or grievance, please contact hr@umamicomms.com. Do not share details of ongoing matters with colleagues.

SECTION 9 - OFFBOARDING & RESIGNATION

Notice Period: Minimum 30 days written notice required (or as stated in your contract). Notice should be submitted to your line manager and HR simultaneously.

Handover: A structured handover document is required before your last day.

Final Settlement: EOSB and final salary will be processed within 14 days of your last working day per UAE Labour Law.

SECTION 10 - MEDICAL INSURANCE PLAN DETAILS (Health Secure 7 - Category 2)

Provider: Health Secure 7
Category: 2
Network: Broad network — includes most major hospitals and clinics across the UAE.

Coverage Highlights:
- Yearly Maximum Benefit: AED 250,000 per member per year
- In-patient (hospitalisation): Covered at 100% (no co-pay) within network
- Out-patient (GP and specialist visits): 20% co-pay applies; AED 500 annual deductible
- Emergency treatment: Covered at 100% (worldwide)
- Maternity (normal delivery): Covered up to AED 10,000; 20% co-pay applies
- Maternity (C-section): Covered up to AED 15,000; 20% co-pay applies
- Pre-natal and post-natal care: Covered up to AED 3,000 per pregnancy
- Dental: Basic dental covered up to AED 1,500 per year (20% co-pay); orthodontics excluded
- Optical: AED 500 per year toward frames/lenses (not laser surgery)
- Prescribed medications: 20% co-pay; generic substitution where available
- Pre-existing conditions: Covered after 6-month waiting period
- Psychiatric and mental health (out-patient): Up to 10 sessions per year; in-patient covered
- Physiotherapy: Up to 15 sessions per year with GP referral
- Vaccinations: Covered for children up to age 18; flu vaccine covered for all

What is NOT covered:
- Cosmetic procedures
- Laser eye surgery
- Fertility treatments / IVF
- Self-inflicted injuries
- Experimental treatments

Important Notes:
- Always carry your insurance card when visiting a medical facility.
- For planned procedures or elective admissions, prior authorisation from the insurer is required.
- For after-hours emergencies, go directly to any network emergency room.
- For insurance card requests, claims queries, or network questions, contact hr@umamicomms.com.

KEY CONTACTS:
- HR: hr@umamicomms.com
- Finance: finance@umamicomms.com
- COO: Sara El Choueiry | sara@umamicomms.com
"""

SYSTEM_PROMPT = """You are Nori, Umami Comms' friendly HR Policy Assistant. You help employees quickly understand company policies in plain, warm language.

YOUR PERSONA:
- Friendly, clear, and concise — like a helpful colleague, not a robot
- Use plain English; avoid jargon
- Always sign off with 🌿
- If someone asks who you are, say: "Hi! I'm Nori 🌿 Umami's HR Policy Assistant. I'm here to help you find answers about our policies — just ask away!"

RULES:
1. Only answer questions using the Umami Comms Employee Handbook provided below. Do not use outside knowledge.
2. Always cite the relevant section (e.g. "Section 4 — Leave Policies").
3. For insurance questions, ALWAYS answer from Section 10 of the handbook. Do not use Section 5 for insurance details.
4. If a question involves a grievance, disciplinary matter, visa/immigration issue, or medical/personal circumstances, do NOT attempt to answer. Instead say: "This is something HR can help with directly — please reach out to hr@umamicomms.com 🌿"
5. If a question is not covered in the handbook, say: "I don't have that information in the handbook right now. For anything not covered here, please reach out to hr@umamicomms.com 🌿"
6. Keep answers concise — 3 to 6 sentences unless a list is genuinely helpful.
7. Do not make up policies, infer intent, or speculate beyond what the handbook states.
8. Do not share or speculate about other employees' situations.
9. Never mention optional insurance upgrades, adding dependents, or plan changes — these are handled case-by-case by HR only.
10. Always be warm and encouraging — HR questions can feel stressful, so make it easy.

HANDBOOK:
""" + HANDBOOK


def format_for_slack(text):
    """Convert markdown formatting to Slack formatting."""
    text = re.sub(r'\*\*(.+?)\*\*', r'*\1*', text)
    text = re.sub(r'#{1,3}\s*(.+)', r'*\1*', text)
    text = re.sub(r'```[\w]*\n?', '', text)
    text = re.sub(r'`([^`]+)`', r'`\1`', text)
    return text.strip()


def ask_claude(question):
    """Send question to Claude and return formatted response."""
    try:
        message = anthropic_client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": question}]
        )
        return format_for_slack(message.content[0].text)
    except Exception as e:
        return "I'm having trouble connecting right now. Please contact HR directly at hr@umamicomms.com 🌿"


@app.route("/slack/command", methods=["POST"])
def slash_command():
    """Handle /asknori slash command with ephemeral response to avoid timeout."""
    if not signature_verifier.is_valid_request(
        request.get_data(), request.headers.get("X-Slack-Signature", ""),
        request.headers.get("X-Slack-Request-Timestamp", "")
    ):
        return jsonify({"error": "Invalid signature"}), 403

    question = request.form.get("text", "").strip()
    response_url = request.form.get("response_url", "")

    if not question:
        return jsonify({
            "response_type": "ephemeral",
            "text": "Hi! I'm Nori 🌿 Ask me anything about Umami's HR policies — just type your question after /asknori"
        })

    def process_and_respond():
        answer = ask_claude(question)
        import urllib.request
        import json as json_lib
        payload = json_lib.dumps({
            "response_type": "ephemeral",
            "text": answer
        }).encode("utf-8")
        req = urllib.request.Request(
            response_url,
            data=payload,
            headers={"Content-Type": "application/json"}
        )
        try:
            urllib.request.urlopen(req)
        except Exception:
            pass

    threading.Thread(target=process_and_respond, daemon=True).start()
    return jsonify({
        "response_type": "ephemeral",
        "text": "_Nori is looking that up for you..._ 🌿"
    })


@app.route("/slack/events", methods=["POST"])
def slack_events():
    """Handle Slack event subscriptions — DMs and channel messages."""
    if not signature_verifier.is_valid_request(
        request.get_data(), request.headers.get("X-Slack-Signature", ""),
        request.headers.get("X-Slack-Request-Timestamp", "")
    ):
        return jsonify({"error": "Invalid signature"}), 403

    data = request.json

    # URL verification challenge
    if data.get("type") == "url_verification":
        return jsonify({"challenge": data["challenge"]})

    if data.get("type") != "event_callback":
        return jsonify({"status": "ok"})

    event = data.get("event", {})
    event_id = data.get("event_id", "")

    # Deduplicate events
    if event_id in processed_events:
        return jsonify({"status": "ok"})
    processed_events.add(event_id)
    if len(processed_events) > 1000:
        processed_events.clear()

    event_type = event.get("type")
    bot_id = event.get("bot_id")
    subtype = event.get("subtype")

    # Ignore bot messages
    if bot_id or subtype == "bot_message":
        return jsonify({"status": "ok"})

    hr_channel = os.environ.get("HR_CHANNEL_NAME", "ask-nori")
    channel = event.get("channel", "")
    channel_type = event.get("channel_type", "")
    text = event.get("text", "").strip()
    user = event.get("user", "")

    if not text or not user:
        return jsonify({"status": "ok"})

    should_respond = False

    # Respond to DMs
    if event_type == "message" and channel_type == "im":
        should_respond = True

    # Respond to messages in #ask-nori channel
    elif event_type == "message" and channel_type != "im":
        try:
            channel_info = slack_client.conversations_info(channel=channel)
            channel_name = channel_info["channel"].get("name", "")
            if channel_name == hr_channel:
                should_respond = True
        except Exception:
            pass

    if not should_respond:
        return jsonify({"status": "ok"})

    def process_and_post():
        answer = ask_claude(text)
        try:
            slack_client.chat_postMessage(
                channel=channel,
                text=answer,
                thread_ts=event.get("thread_ts") or event.get("ts")
            )
        except Exception:
            pass

    threading.Thread(target=process_and_post, daemon=True).start()
    return jsonify({"status": "ok"})


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "bot": "Nori - Umami HR Policy Assistant", "version": "4.0"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)
