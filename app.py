"""
Umami Comms - Nori HR Policy Bot
Version: 4.1 (November 2026) — Full handbook sync
"""
import os
import re
import threading
from flask import Flask, request, jsonify
from slack_sdk import WebClient
import anthropic

app = Flask(__name__)
slack_client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])
anthropic_client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
processed_events = set()

HANDBOOK = """
SECTION 1 - OUR CULTURE & WORKPLACE EXPECTATIONS

Umami Comms is a Dubai-based full-service creative communications agency, founded in 2016 by Colin Hutton. Services include PR, Social Media, Branding & Design, Advertising, and Content Production.

Core Values: Respect, Integrity, Innovation — anchored by being Competitive, Honest, Free-Spirited, Agile, Caring, Ambitious, Tolerant, Bold, and Humble.

Professional Conduct:
- Punctuality: Be on time for meetings and respect deadlines.
- Communication: Use respectful language in person, over email, and on digital platforms.
- Dress Code: Business casual for regular office days and video calls with clients. Business professional (smart attire) for client meetings or after-hours client functions and events.
- Team Spirit: Support colleagues, avoid gossip, maintain a positive, solutions-focused mindset.

Confidentiality: Always protect client information and company-sensitive data. Do not share materials, documents, or strategies outside the agency without authorisation. If in doubt, consult HR or your manager.

Inclusivity & Diversity: Umami is an equal-opportunity employer. Zero tolerance for discrimination based on gender, age, race, religion, disability, or sexual orientation. Report any harassment to HR immediately — reports are handled confidentially.

Company Equipment: Employees must protect company equipment from physical and operational damage. Keep software updated, use strong passwords, lock devices when unattended, and avoid unauthorised apps. Excessive personal phone charges may need to be reimbursed. Negligence resulting in damage may result in cost recovery.

Computers, Email & Internet: Business use only. Prohibited: discriminatory or harassing content, pornographic material, unlicensed software, sharing confidential data without authorisation, illegal activities, gambling, or personal profit through company systems.

Phishing: Always verify sender email addresses. Be cautious of urgent/threatening language. Never click suspicious links or download attachments unless 100% certain of legitimacy. Forward suspicious emails to HR before acting.

Social Media: Content shared publicly should reflect professionalism, integrity, and truthfulness. Personal accounts linked to your identity should align with Umami's professional image — make accounts private or use alternative handles if this cannot be maintained.

KEY CONTACTS:
- HR (general enquiries, leaves, benefits): hr@umamicomms.com
- Finance/Payroll: finance@umamicomms.com
- COO: Sara El Choueiry | sara@umamicomms.com

SECTION 2 - WORKPLACE CONDUCT, ETHICS & COMPLIANCE

Open Door Policy: Employees who feel treated unfairly are encouraged to discuss concerns with Department Heads, Line Managers, or HR. All communication is treated strictly confidential.

Equal Employment Opportunity: Employment decisions are based on merit, qualifications, and abilities. No discrimination based on race, colour, religion, gender, age, nationality, or orientation.

Sexual & Unlawful Harassment: Zero tolerance. This includes unwanted advances, derogatory comments, intimidating or hostile behaviour, or anything targeting a protected characteristic. Report to Line Manager, Department Head, or HR immediately. Retaliation against anyone raising a concern in good faith is strictly prohibited.

Business Ethics: Employees must act in the best interests of the agency and avoid situations where personal interests conflict with business decisions.

Conflicts of Interest: Disclose to the Managing Director or an officer any situation where personal relationships or outside employment could influence your professional judgment — including ownership in firms that do business with Umami, accepting substantial gifts, or securing personal advantages using your role.

Non-Compete: During employment and for up to 12 months after termination, employees may not engage in a business that competes directly with Umami in the UAE.

Non-Solicitation: During employment and for 12 months after termination, employees must not solicit Umami's clients or employees.

Confidentiality & Non-Disclosure: Confidential information includes client lists, financial information, marketing strategies, pending proposals, and costing information. Improper use or disclosure may result in disciplinary action, up to and including termination and legal action.

Personal Relationships at Work: Umami does not prohibit personal relationships but employees must maintain professionalism at all times. Public displays of affection or excessive personal conversation during working hours are inappropriate.

SECTION 3 - EMPLOYMENT ESSENTIALS

Onboarding: Structured journey covering pre-boarding, Day 1, Week 1, and first 6 months. Each new joiner is assigned a Line Manager and an Agency Ally. HR conducts check-ins at approximately month 1, month 3, and month 6.

Employment Contracts: All employees receive a formal employment contract per UAE Labour Law, covering job title, compensation, probation, notice periods, and leave entitlements. In any discrepancy between this handbook and the contract, the contract and UAE Labour Law take precedence.

Probation Period: Standard 6-month probation. During probation:
- Performance, attendance, and cultural fit are evaluated.
- Employees are not eligible to use annual leave during probation, but leave accrues throughout. Employees with more than 6 but less than 12 months' service accrue 2 days per month.
- Either party may terminate with 14 days' written notice.
Upon successful completion, employees are confirmed in their role and become eligible for full benefits. HR issues a formal confirmation letter.

Employment Classification:
- Full-Time: Standard 5-day work week (hybrid model applies). Eligible for all benefits.
- Part-Time: Reduced hours; benefits and leave entitlements are prorated.
- Freelancers/Contractors: Engaged for specific projects; not entitled to employee benefits.

Immigration & Work Permits: All expatriate employees must hold a valid work visa and residency permit sponsored by Umami Comms (unless otherwise arranged). HR manages the application, renewal, and cancellation process.

Ending Employment: Resignation requires minimum 30 days' written notice. Termination may occur due to performance, restructuring, or valid reasons under UAE Labour Law.

Employee Records: HR maintains a confidential personnel file for each employee. Notify HR promptly of changes to personal address, emergency contacts, banking details, marital status, or dependents.

SECTION 4 - WORKING HOURS, FLEXIBILITY & LEAVE TYPES

Standard Working Hours: Monday to Friday, 9:00 AM – 6:00 PM, with a 1-hour lunch break. Employees must notify their Line Manager if arrival or departure times deviate significantly. Unexpected absence must be reported no later than 2 hours before usual start time.

Hybrid Work Model:
- In-office days: Monday, Wednesday, Thursday
- Remote days: Tuesday, Friday
Employees are expected to attend in-person meetings, client sessions, and team activities when required, regardless of the hybrid schedule.

Annual Leave:
- Entitlement: 22 working days per year for full-time employees.
- Accrual: Approximately 1.83 days per completed month of service. Accrual continues during probation but leave cannot be used during probation.
- From 3 months of service: Employees may use accrued leave, subject to approval.
- Before 3 months: Leave will typically be treated as unpaid.
- Advance Leave: In certain circumstances, Umami may approve leave in excess of accrued balance. If employment ends before the anniversary and more leave was taken than accrued, the value of excess days is deducted from final settlement.
- Carry Forward: Only 50% of unused annual leave may be carried to the next leave cycle. Unused leave exceeding this limit is forfeited. Unused annual leave is not encashed during employment.
- Final Settlement: Upon termination after completing 1 year of service, employees are entitled to payment for unused accrued annual leave, calculated at basic pay rate.
- All leave must be approved via Bayzat before making travel arrangements. Leave is not approved until it has completed the full Bayzat workflow.

Public Holidays: Employees are entitled to all UAE public holidays as announced by the government. If work is required on a public holiday, compensatory leave or payment in lieu is provided per UAE Labour Law.

Sick Leave: Up to 90 calendar days per year per UAE Labour Law:
- First 15 days: full pay
- Next 30 days: half pay
- Remaining 45 days: unpaid
- A medical certificate is required for absences over 2 consecutive days.
- Sick leave is not paid if illness is due to misconduct (e.g., alcohol consumption).
- If an employee cannot return after exhausting sick leave, Umami may terminate the employment contract.

Maternity Leave:
- Less than 1 year of service: 45 calendar days at full pay (as per UAE Labour Law).
- 1 year or more of service: 180 calendar days (6 months) at full pay.
- After maternity leave ends: an additional 15 days at 50% pay.
- If a medical condition prevents return to work, additional days are unpaid leave.
- Maternity leave also applies in the case of stillbirth.
- Employees are expected to continue employment for at least 1 year after childbirth. If employment ends earlier, any paid maternity leave in excess of the statutory 45 days will be adjusted against end-of-service benefits.
- Nursing breaks: Upon returning, employees are entitled to 1–2 nursing breaks per day (up to 1 hour total) for 6 months.
- Notify Line Manager and HR no later than 3 weeks before the expected due date.

Paternity Leave:
- Less than 1 year of service: 5 calendar days at full pay (as per UAE Labour Law).
- 1 year or more of service: up to 30 calendar days fully paid, taken intermittently or concurrently over a 6-month period after childbirth.
- Employees are expected to continue employment for at least 1 year after paternity leave. If employment ends earlier, paid paternity leave in excess of the statutory 5 days will be adjusted against end-of-service benefits.

Bereavement (Compassionate) Leave:
- 10 paid days for the death of a spouse.
- 5 paid days for the death of a parent, sibling, child, or grandparent.
- Request via Bayzat (Compassionate Leave tab). Notify Line Manager or HR as soon as practicable.

Hajj Leave: Once per employment, employees are entitled to 30 days unpaid leave for Hajj pilgrimage.

Study Leave: Employees studying in state-approved educational facilities are entitled to 10 business days of study leave, provided they have more than 2 years of service.

Birthday Leave: Umami provides a paid birthday leave day.
- If your birthday falls on a weekday, you are entitled to a paid day off on that date.
- If it falls on a weekend (Saturday or Sunday), you may take the preceding Friday or the following Monday as your Birthday Leave.
- Birthday Leave cannot be combined with any other type of leave, except annual leave — it may be tagged onto an approved annual leave period.
- If you are already on approved leave (other than annual leave) on your birthday, Birthday Leave is forfeited (cannot be carried forward or encashed).
- Requests must be submitted at least 2 weeks in advance via Bayzat, with Line Manager approval.

Personal Leave: 5 days per calendar year, regardless of tenure.
- Intended for essential life tasks: bank or doctor appointments, moving house, RTA driving tests.
- Personal Leave cannot be combined with any other type of leave.
- Submit via Bayzat with Line Manager approval.

Overtime & Time Off In Lieu (TOIL):
- Overtime must be pre-authorised by your Line Manager. Overtime hours are not paid in cash.
- Authorised weekend (Saturday or Sunday) work: 1 lieu day, regardless of hours worked. TOIL must be used within 1 month and may not be taken on consecutive days. Submit via Bayzat (Lieu Days tab) before taking the day.
- Weekday overtime (Monday–Thursday): With Line Manager approval, employees may start later (e.g. 11:00 AM) or leave earlier (e.g. 4:00 PM) the following working day.
- Friday overtime: With Line Manager approval, employees may adjust hours the following Monday (arrive at usual time and leave earlier, or arrive later for a shortened day).
- Client events, activations, photoshoots, or similar weekday functions: Employees are NOT eligible for TOIL. With Line Manager approval, they may adjust working hours the following business day.
- Working overtime without authorisation may result in disciplinary action up to and including termination.

Unpaid Leave: May be requested when annual leave is exhausted. Must be approved by Department Head and HR. Prolonged unpaid leave may affect gratuity and other benefits calculations.

Handover Policy: Before any form of leave, employees must:
1. Prepare a written handover document using the approved department template (covering key responsibilities, project deadlines, client updates, and pending actions).
2. Conduct a handover meeting with relevant colleagues at least 1 working day before leave starts (especially for leave longer than 1 week).
3. Upon return, schedule a debrief with Line Manager to review completed tasks and follow-up actions.

Remote Work — Local (Within UAE):
- Standard hybrid remote days are Tuesday and Friday.
- Remote work outside these days requires completion of probation (unless approved in advance by Head of Department and HR for an emergency).
- Employees must be physically present in the UAE, remain available for in-person meetings/client engagements if required, and accurately declare their working location.

Remote Work — Global (Outside UAE):
- Eligibility: At least 1 year of service and no recent disciplinary issues. Roles must be effectively performable outside the office.
- Entitlement: One block of up to 5 consecutive global remote working days per calendar year.
- May be tagged onto annual leave, provided the total combined duration does not exceed 2 consecutive weeks.
- For content creators: global remote work is only permitted within the UAE.
- Request: Submit to Department Head at least 1 month in advance. Upload approved days via Bayzat (Remote tab, Time Off section). Department Heads respond within 5 working days. Approval is discretionary.
- Rules: Available during UAE working hours (9:00 AM – 6:00 PM), attend all calls with camera on (unless agreed otherwise), use reliable technology, respond promptly.
- Any day outside the UAE during working hours without approved global remote work is treated as annual or unpaid leave.
- Data roaming charges, if incurred, will be deducted from salary.

Christmas Day: Umami recognises Christmas Day (25 December) as a paid holiday. Dubai employees receive a paid day off if it falls on a regular working day. If an employee's approved annual leave period already includes Christmas Day, they will not receive an additional paid day — they may opt to deduct it from their annual leave entitlement.

SECTION 5 - COMPENSATION & BENEFITS

Salary & Payment:
- Monthly salary paid in AED via bank transfer on the 28th of each month via the UAE Wages Protection System (WPS).
- Salaries consist of Basic Pay and Allowances (e.g. housing, transportation) as stated in the employment contract.
- If payday falls on a Sunday or public holiday, salary is paid on the preceding Saturday or last working day.
- Pro-rata payments apply if start/end date does not align with the beginning or end of a calendar month.
- Salary details are strictly confidential — do not disclose to colleagues.
- For payroll errors, contact HR or Finance (finance@umamicomms.com) immediately.

Annual Salary Review: Conducted annually, typically aligned with approved KPIs. Adjustments are based on individual and team performance, market benchmarks, and company performance/budget. Salary increases are discretionary and not automatic.

End of Service Benefit (EOSB) / Gratuity:
- Eligibility: Employees who have completed at least 1 year of continuous service.
- Calculation: 1–5 years: 21 days' basic pay per year. 5+ years: 30 days' basic pay per year.
- Total gratuity shall not exceed the equivalent of 2 years' basic salary.
- Calculated on last drawn basic salary.
- Unpaid absences are not counted toward service length.
- Unused annual leave is compensated at basic salary rate.
- Final settlement paid within 14 days of termination date.
- Umami may deduct outstanding amounts owed by the employee.

EOSB Beneficiary Nomination: Employees are encouraged to nominate a beneficiary for their EOSB. HR provides a Beneficiary Appointment Form. All records are kept strictly confidential by HR. Employees may update their nomination at any time by contacting HR.

Annual Flight Ticket Allowance:
- Eligibility: Employees who have completed 1 year of service.
- Allowance: AED 3,500 per year.
- Options: Book through Airlink (preferred travel agency partner), book independently and claim reimbursement up to AED 3,500, or cash-out equivalent.
- Cash-out: Based on cost of return flight from Dubai to home country, capped at AED 3,500. Submit written request to HR at least 1 month before work anniversary.
- Claim window: 4 months from work anniversary. Unclaimed benefits are forfeited.
- All requests must be uploaded to Bayzat for record-keeping.

Medical Insurance: All Umami-sponsored employees receive medical insurance. Full plan details are covered in the insurance section below.

SECTION 6 - HEALTH, SAFETY & WELLBEING

Workplace Safety: Umami follows all UAE health and safety regulations including DMCC Free Zone requirements. Maintain a tidy, hazard-free workspace. Report any hazards or unsafe conditions to HR immediately.

Emergency Procedures: Fire exits and evacuation routes are clearly marked. Follow instructions from designated safety marshals. First aid kits are available in the office.

Smoking: Strictly prohibited throughout the workplace. E-cigarettes and vapes are permitted only on the terrace. Smoking is prohibited during meetings, in client-facing settings, or on video calls.

Wellness: Umami conducts up to 2 wellness workshops per year on topics such as workload sustainability, preventive health, and financial confidence. We may host annual health check-up camps and share wellbeing resources. All wellbeing-related discussions with HR are strictly confidential.

SECTION 7 - PERFORMANCE & DEVELOPMENT

Performance Reviews: Formal review discussions take place during scheduled quarterly feedback sessions. Reviews cover achievement of goals, demonstration of Umami's values, collaboration, creativity, leadership, and areas for improvement. Outcomes may influence salary reviews, promotions, or development plans.

Goal Setting: At the start of each year (or upon joining), employees and managers set SMART goals aligned with individual role expectations, team objectives, and agency-wide vision. Mid-year check-ins allow recalibration.

Learning & Development: Includes Train the Trainer program, workshops and masterclasses with external speakers, cross-functional project learning, and Individual Development Plans (IDPs) created jointly by employees and managers.

Disciplinary Note: Employees issued a written warning are generally not eligible for salary increases or promotion for 12 months from the date of the warning (unless management approves an exception).

SECTION 8 - BUSINESS EXPENSES & TRAVEL

Business Expense Reimbursement:
- All expense claims submitted through Bayzat with supporting receipts.
- Local expenses: submitted by the 4th of the following month. International travel expenses: within 15 days of returning.
- Original receipts or digital invoices required (must show date, total cost, and TRN where applicable). Bank approval copies or screenshots alone are not accepted.
- Pre-approval required for expenses exceeding AED 500 (written approval from Department Head).
- Expenses are reimbursed via the next available payroll cycle after approval.
- Carpooling is strongly expected when multiple employees travel to the same destination.

Local Transport:
- Petrol for Abu Dhabi client meetings: AED 150 per round trip (requires valid petrol receipt). Only the driver may claim per trip when carpooling.
- Taxis within Dubai/UAE: Use Hala Taxi (via Careem app) or Bolt. Digital invoice required. Premium or business-class options not reimbursable without prior written approval.
- Parking: Reimbursable with valid receipt or RTA screenshot. Office parking full day: Zone 393K (14-hour pass). Partial day: Zone 393J (4-hour pass). Fines and penalties are the employee's personal responsibility.

International Business Travel:
- All trips require prior approval from Department Head and COO.
- Umami covers: return flights (economy class), accommodation, visa fees, airport taxes, and airport transfers.
- Per diem allowance covers meals and reasonable incidental expenses. Separate meal receipts are not submitted on days when per diem has been paid.
- For trips exceeding 7 consecutive days, continuation of per diem beyond day 7 requires additional written approval from COO or CEO.
- Car rental: compact or mid-sized only. Premium, SUV, or luxury class not reimbursable without prior written approval.
- Laundry and valet: reimbursable on trips of 5 or more days only.
- Travel expense report must be submitted via Bayzat within 15 days of returning.
- Falsifying expense reports may result in termination.

Non-Reimbursable Expenses: Personal meals, groceries, beverages not associated with an approved business event; alcohol unless pre-approved for a client entertainment event; personal entertainment, clothing, accessories; traffic fines; premium transport without prior approval; receipts submitted more than the deadline; expenses without valid documentation.

SECTION 9 - PROBLEM-SOLVING & RESOLUTION (Disciplinary & Grievance)

Discipline is intended to support improvement rather than create fear. Progressive discipline steps:
a. Verbal Warning — manager addresses concern directly; documented internally but not permanently filed unless repeated.
b. Written Warning — formal document with issue details, previous steps, expected improvements, timeline, and consequences. Active for 6 months. Employee signs to acknowledge receipt.
c. Final Written Warning — HR directly involved; further violations may result in termination.
d. Termination — if corrective measures fail, or for serious misconduct (harassment, theft, violence, gross negligence).

Immediate Termination (without notice) may occur for: forged documents/false identity, significant financial loss through negligence, safety rule breaches, repeated failure to perform duties after 2 written warnings, unauthorised disclosure of confidential information, alcohol/drug intoxication during work, workplace assault, absent without valid reason for 20+ non-consecutive or 7+ consecutive days in a year, abuse of position, working for another firm without approval.

Grievance Procedure:
- Informal: Raise with direct manager or HR. HR provides a safe, confidential forum.
- Formal: Submit written grievance to HR (email or Formal Grievance Form). HR acknowledges within 2 working days.
- Investigation: HR gathers information, speaks to involved parties. Completed within 10 working days (extendable for complex cases).
- Outcome: HR communicates decision in writing within 5 working days of investigation completion.
- Appeal: If not satisfied, submit written appeal to HR within 5 working days for escalation to senior leadership.
- Retaliation against employees who raise grievances in good faith is strictly prohibited.

For any grievance or disciplinary concern: hr@umamicomms.com

SECTION 10 - OFFBOARDING & EXIT PROCESS

Voluntary Resignation:
- Submit written resignation letter to Line Manager, Head of Department, and HR.
- Notice periods per employment contract and UAE Labour Law (usually 30 days).
- During notice period: continue fulfilling duties, complete handover of work/documents/client relations, participate in exit interview.

Termination by Umami:
- May occur due to performance issues, misconduct, or redundancy/restructuring.
- Notice per UAE Labour Law and employee's contract. Immediate termination (no notice) for gross misconduct.
- Umami may require garden leave during notice period (employee remains away from office but on full pay and benefits).

Final Settlement includes: final salary, payment for unused annual leave (if applicable), end-of-service gratuity per UAE Labour Law. Paid within 14 days of last working day.

Exit Procedures: Return all company property (laptops, access cards, credit cards, files). Clear outstanding advances, loans, or obligations. Complete structured handover. Participate in exit interview with HR. Activate Out-of-Office email before last working day.

Post-Employment Obligations: Respect any non-disclosure or non-compete clauses. Confidential information must not be shared or misused after departure.

Reference Letters: Upon request, Umami provides a neutral employment certificate confirming dates and role. Additional references at management's discretion.

SECTION 11 - MEDICAL INSURANCE PLAN DETAILS (Health Secure 7 - Category 2)

Provider: Health Secure 7 | Category: 2
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
- Cosmetic procedures | Laser eye surgery | Fertility treatments / IVF
- Self-inflicted injuries | Experimental treatments

Important Notes:
- Always carry your insurance card when visiting a medical facility.
- For planned procedures or elective admissions, prior authorisation from the insurer is required.
- For after-hours emergencies, go directly to any network emergency room.
- For insurance card requests, claims queries, or network questions: hr@umamicomms.com
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
3. For insurance questions, ALWAYS answer from Section 11 of the handbook. Do not use Section 5 for insurance details.
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
    data = request.json

    # URL verification challenge
    if data and data.get("type") == "url_verification":
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
    return jsonify({"status": "ok", "bot": "Nori - Umami HR Policy Assistant", "version": "4.1"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)
