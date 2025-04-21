# RAFT Status Tracker — README

A lightweight tool for GBLS staff to track RAFT application status, see missing documents, and generate a one-page `Case Summary` for court/opposing counsel. This tracker does not file RAFT; RAFT is already submitted in the state portal. We only read status and organize next actions.

---

## 1) Personas

- **Paralegal (primary):** needs to see live status, missing docs, next actions, and due dates.
- **Attorney (secondary):** needs a **printable Case Summary** proving RAFT is pending/under review.

---

## 2) User Stories

### Story A — Paralegal: View Live RAFT Status
**As a** paralegal,  
**I want** to click a client’s name and see their RAFT status,  
**so that** I can act quickly (re-apply or send missing documents).

**Acceptance Criteria**
- From **Client List**, clicking a client opens **Client Detail** showing:
  - Current **RAFT Status** (e.g., Submitted, Under Review, Expired, Closed, Paid)
  - **RAFT Case #**, **Submitted Date**
  - **Last Checked** (timestamp)
- A **Re-check Status** button refreshes status & updates **Last Checked**.
- If RAFT session/login fails, show a clear **Re-authenticate** prompt.

### Story B — Attorney: One-Page Case Summary
**As an** attorney,  
**I want** a one-page **Case Summary** view,  
**so that** I can show opposing counsel/judge that RAFT is pending.

**Acceptance Criteria**
- From **Client Detail**, **View Case Summary** shows:
  - Client Name
  - RAFT Case #, Current Status, **Last Checked**
  - **Notes/Contact Log** (last 3 entries)
- **Export PDF** outputs the same content with footer:  
  “Generated on <date/time> for verification purposes.”

---

## 3) Non-Functional Requirements

- Page loads in **< 2s** on office Wi-Fi.
- **Read-only** integration to RAFT portal (no edits).
- **Audit log** for who viewed/refreshed/exported.
- **Accessibility:** keyboard-navigable, meaningful labels, visible focus.
- **Privacy:** avoid unnecessary PII (no SSN, full DOB).

---

## 4) Status & Fields (MVP)

```json
{
  "status_enum": [
    "Not Submitted",
    "Submitted",
    "Under Review",
    "Expired",
    "Ready for Payment",
    "Payed",
    "Closed"
  ],
  "doc_flags": ["ID", "Case Number", "Rental Property"]
}

## 5) Wireframes
/Users/Marine/Desktop/raftStatusCheck/images/FoltawireFrames.jpeg