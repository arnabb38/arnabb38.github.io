#!/usr/bin/env python3
"""Generates the case-study pages under work/ from one shared template."""
import sys, pathlib

ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent.parent)

DEFS = """<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false">
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="arrowhead"/></marker>
    <marker id="arrow-teal" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="arrowhead teal"/></marker>
  </defs>
</svg>"""

def page(slug, title, desc, client, body, prev, nxt):
    return f"""<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} · Arnab Basak</title>
  <meta name="description" content="{desc}">
  <meta property="og:title" content="{title} · Arnab Basak">
  <meta property="og:description" content="{desc}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="https://arnabb38.github.io/work/{slug}.html">
  <link rel="canonical" href="https://arnabb38.github.io/work/{slug}.html">
  <script>try{{var t=localStorage.getItem("theme")}}catch(e){{}}document.documentElement.setAttribute("data-theme",t||"dark");</script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans+Condensed:wght@600&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../assets/site.css?v=20261029">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{DEFS}
<div class="cs-top">
  <a class="home" href="../index.html#work">Arnab Basak</a>
  <button class="theme" type="button" data-theme-toggle aria-label="Switch to light theme" title="Switch to light theme"><svg class="i-sun" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4.5"/><path d="M12 2v2.5M12 19.5V22M2 12h2.5M19.5 12H22M4.9 4.9l1.8 1.8M17.3 17.3l1.8 1.8M4.9 19.1l1.8-1.8M17.3 6.7l1.8-1.8"/></svg><svg class="i-moon" viewBox="0 0 24 24" aria-hidden="true"><path d="M20.5 14.5A8.5 8.5 0 0 1 9.5 3.5a8.5 8.5 0 1 0 11 11z"/></svg></button>
</div>
<main class="cs" id="main">
{body}
  <nav class="next" aria-label="More case studies">
    <a href="{prev[0]}">Previous: {prev[1]}</a>
    <a href="{nxt[0]}">Next: {nxt[1]}</a>
  </nav>
</main>
<script src="../assets/site.js?v=20261029"></script>
</body>
</html>
"""

def task(x, y, w, h, lines, cls="task"):
    """A rounded BPMN task with centred, multi-line label."""
    cx = x + w / 2
    n = len(lines)
    top = y + h / 2 - (n - 1) * 8 + 4
    spans = "".join(f'<tspan x="{cx}" y="{top + i * 16}">{l}</tspan>' for i, l in enumerate(lines))
    return (f'<rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="8"/>'
            f'<text text-anchor="middle">{spans}</text>')

def gw(cx, cy, label=None, lx=None, ly=None):
    s = f'<path class="gw" d="M{cx},{cy-22} L{cx+22},{cy} L{cx},{cy+22} L{cx-22},{cy} z"/>'
    s += f'<text class="t-amber" x="{cx}" y="{cy+5}" text-anchor="middle">?</text>'
    if label:
        s += f'<text class="t-soft" x="{lx if lx is not None else cx}" y="{ly if ly is not None else cy-30}" text-anchor="middle">{label}</text>'
    return s

def ev(cx, cy, end=False, label=None):
    s = f'<circle class="ev{" end" if end else ""}" cx="{cx}" cy="{cy}" r="14"/>'
    if label:
        s += f'<text class="t-faint" x="{cx}" y="{cy+32}" text-anchor="middle">{label}</text>'
    return s

def lanes(names, x0, y0, w, lh, head=128):
    s = ""
    for i, n in enumerate(names):
        y = y0 + i * lh
        s += f'<rect class="lane" x="{x0}" y="{y}" width="{w}" height="{lh}"/>'
        s += f'<rect class="lane-head" x="{x0}" y="{y}" width="{head}" height="{lh}"/>'
        parts = n.split("|")
        top = y + lh / 2 - (len(parts) - 1) * 8 + 4
        s += '<text class="t-lane" text-anchor="middle">' + "".join(
            f'<tspan x="{x0 + head/2}" y="{top + k*16}">{p}</tspan>' for k, p in enumerate(parts)) + "</text>"
    return s

def fig(svg, vb, caption, label):
    return f"""<figure class="dia">
      <div class="dia__frame">
        <svg viewBox="{vb}" role="img" aria-label="{label}">{svg}</svg>
      </div>
      <figcaption>{caption}</figcaption>
    </figure>"""

def facts(items):
    return '<dl class="facts">' + "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in items) + "</dl>"

def outcomes(items):
    return '<dl class="outcomes">' + "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in items) + "</dl>"


# ---------------------------------------------------------------- Internet banking
def ib():
    # context diagram
    s = '<text class="t-head" x="20" y="24">Channels</text>'
    s += '<text class="t-head" x="350" y="24">Platform</text>'
    s += '<text class="t-head" x="730" y="24">Connected systems</text>'
    chans = [("Retail web and app", "transfers, wallets, QR"),
             ("Corporate banking", "500+ customers, bulk payouts"),
             ("Branch and back office", "reconciliation, disputes"),
             ("EduPay", "university fee collection")]
    hub_in = [150, 200, 250, 300]
    for i, (a, b) in enumerate(chans):
        y = 40 + i * 95
        s += task(20, y, 210, 60, [a, f'<tspan class="t-faint">{b}</tspan>'])
        s += f'<path class="flow" d="M230,{y+30} L350,{hub_in[i]}"/>'
    s += '<rect class="hub" x="350" y="120" width="260" height="210" rx="10"/>'
    s += '<text class="t-head" x="480" y="152" text-anchor="middle">Digital banking platform</text>'
    for k, l in enumerate(["onboarding and eKYC", "transfers and payments", "wallets and QR",
                           "statements and alerts", "reconciliation, disputes"]):
        s += f'<text class="t-soft" x="480" y="{186 + k*28}" text-anchor="middle">{l}</text>'
    exts = ["Core banking system", "Bangla QR (national QR)", "BEFTN and NPSB rails",
            "bKash and Nagad wallets", "SSLCommerz, ShurjoPay", "Five mobile operators",
            "Election Commission (NID)"]
    hub_out = [135, 160, 185, 215, 245, 275, 305]
    for i, e in enumerate(exts):
        y = 40 + i * 54
        s += task(730, y, 210, 42, [e], "task ext")
        s += f'<path class="flow" style="marker-start:url(#arrow)" d="M610,{hub_out[i]} L730,{y+21}"/>'
    d1 = fig(s, "0 0 960 420",
             "Context: four channels on one platform, connected to the bank’s core and to the national payment, wallet, telecom and identity systems.",
             "Context diagram of the digital banking platform")

    # BPMN: interbank transfer and settlement
    s = lanes(["Customer", "Platform", "Core banking", "Back office", "Payment|network"], 10, 10, 1110, 84)
    L = lambda i: 10 + i * 84 + 42
    s += ev(170, L(0))
    s += task(210, L(0) - 25, 160, 50, ["Choose beneficiary,", "confirm with OTP"])
    s += '<path class="flow" d="M184,%d H210"/>' % L(0)
    s += task(400, L(1) - 25, 130, 50, ["Request debit"])
    s += '<path class="flow" d="M370,%d H465 V%d"/>' % (L(0), L(1) - 25)
    s += task(400, L(2) - 25, 130, 50, ["Post debit"])
    s += '<path class="flow" d="M465,%d V%d"/>' % (L(1) + 25, L(2) - 25)
    s += gw(600, L(1), "result clear?", 600, L(1) - 30)
    s += '<path class="flow" d="M530,%d H560 V%d H578"/>' % (L(2), L(1))
    s += task(540, L(3) - 25, 120, 50, ["Resolve", "pending"])
    s += '<path class="flow alt" d="M600,%d V%d"/>' % (L(1) + 22, L(3) - 25)
    s += '<text class="t-faint" x="608" y="%d">no</text>' % (L(2) + 4)
    s += task(650, L(4) - 25, 140, 50, ["Settle via", "BEFTN or NPSB"], "task hot")
    s += '<path class="flow hot" d="M622,%d H720 V%d"/>' % (L(1), L(4) - 25)
    s += '<text class="t-faint" x="640" y="%d">yes</text>' % (L(1) - 8)
    s += '<path class="flow alt" d="M660,%d H830"/>' % L(3)
    s += task(830, L(3) - 25, 130, 50, ["Reconcile", "settlement file"], "task hot")
    s += '<path class="flow hot" d="M790,%d H895 V%d"/>' % (L(4), L(3) + 25)
    s += gw(1010, L(3), "mismatch?", 1010, L(3) + 40)
    s += '<path class="flow" d="M960,%d H988"/>' % L(3)
    s += ev(1094, L(3), True)
    s += '<path class="flow" d="M1032,%d H1080"/>' % L(3)
    s += '<text class="t-faint" x="1040" y="%d">no</text>' % (L(3) - 8)
    s += task(955, L(2) - 25, 110, 50, ["Batch", "reversal"])
    s += '<path class="flow" d="M1010,%d V%d"/>' % (L(3) - 22, L(2) + 25)
    s += ev(1010, L(0), True)
    s += '<path class="flow" d="M1010,%d V%d"/>' % (L(2) - 25, L(0) + 14)
    s += '<text class="t-faint" x="988" y="%d" text-anchor="end">customer notified</text>' % (L(0) + 5)
    s += '<text class="t-faint" x="1018" y="%d">yes</text>' % (L(3) - 30)
    d2 = fig(s, "0 0 1130 440",
             "An interbank transfer as BPMN, from the customer’s confirmation through settlement and reconciliation. Customers can also raise an NPSB dispute, which the back office resolves.",
             "BPMN diagram of interbank transfer, settlement and reconciliation")

    body = f"""  <header>
    <p class="client">Agrani Bank PLC · 2024 to present</p>
    <h1>Digital banking platform</h1>
    <p class="lede">Retail, corporate, branch and education banking on one platform for one of Bangladesh’s largest state-owned banks. I lead its engineering and product.</p>
  </header>
  {facts([("Client", "Agrani Bank PLC"), ("My role", "Engineering and product lead"), ("Team", "16 engineers: backend, web, mobile, QA, support, data"), ("Stack", "Java 17, Spring Boot, Angular, Flutter, PostgreSQL, Redis")])}
  <div class="cs-body">
    <section>
      <h2>The problem</h2>
      <p>The bank needed digital channels that could keep up with national payment schemes, digital wallets and a growing list of institutional clients, without risking the trust of hundreds of thousands of retail customers. Every new capability had to meet central bank ICT guidelines and fit around the bank’s core banking system.</p>
    </section>
    <section class="wide">
      <h2>What we built</h2>
      <p>One platform with four channels on top. Around 35 backend services and 10 portals sit behind it, connected to the core banking system and the country’s payment, wallet, telecom and identity infrastructure.</p>
      {d1}
    </section>
    <section>
      <h2>What customers can do</h2>
      <ul>
        <li><strong>Move money:</strong> own-account and in-bank transfers, other banks over BEFTN and NPSB, bKash and Nagad wallets, and Bangla QR, including QR-to-QR transfer and QR cash withdrawal.</li>
        <li><strong>Pay:</strong> mobile recharge on all five operators, credit card bills, tuition and school fees, loan repayments, and online purchases with external merchants through the bank’s payment gateway.</li>
        <li><strong>Recurring:</strong> Standing Instructions for scheme instalments and fixed-amount transfers, for all of the bank’s customers.</li>
        <li><strong>Corporate:</strong> 500+ institutional customers on corporate banking, including bulk disbursement of payments from one instruction.</li>
        <li><strong>Manage:</strong> statements and downloads, beneficiaries, device changes, disputes, and a chatbot. Accounts open through self-service eKYC or with help from a branch.</li>
        <li><strong>EduPay:</strong> students register with their university, pay fees through ShurjoPay or the bank’s own gateway, and download receipts.</li>
      </ul>
    </section>
    <section>
      <h2>My part</h2>
      <ul>
        <li><strong>Product.</strong> I own the roadmap and a contracted scope of about 150 features, along with the requirements, PRDs and backlog, and the relationship with the bank.</li>
        <li><strong>Payments.</strong> I led the integration with Bangla QR, Bangladesh Bank’s national interoperable QR scheme, as well as the BEFTN and NPSB rails, the bKash and Nagad wallets and the SSLCommerz and ShurjoPay gateways. We also opened the bank’s own online payment to external parties, and SSLCommerz integrated it into its net banking section.</li>
        <li><strong>Standing Instructions.</strong> I led the requirements, design and on-time delivery of Standing Instructions for every customer of the bank, across all branches and not only internet banking users. Recurring deductions, such as scheme instalments and fixed-amount transfers, now run on their own.</li>
        <li><strong>Growth beyond retail.</strong> I led the extension into corporate banking, now live for 500+ institutional customers with bulk disbursement, and into institutional fee collection.</li>
        <li><strong>UK expansion.</strong> I led the platform’s UK expansion project, running meetings and requirement gathering with UK stakeholders to understand the market and its needs.</li>
        <li><strong>Reporting and budget.</strong> Stakeholders and our Managing Director get a daily update: what happened, the impact, what is being done, who owns the next action and when it will be resolved. On top of that there is an automated business-status email and a weekly project and product report. I control headcount and licences, and agree infrastructure spend with the teams involved.</li>
        <li><strong>Hands-on.</strong> I maintain the project’s cloud infrastructure and VMs, set up the Prometheus, Grafana and Alertmanager monitoring myself, so the team hears about unusual behaviour before customers do, and I tuned PostgreSQL: its configuration, the slowest queries and its security settings.</li>
        <li><strong>Team.</strong> 16 direct reports. I hired 10+ of them, and I own performance reviews and headcount.</li>
        <li><strong>How we work.</strong> Scrum with backlog refinement every two sprints, and an agentic SDLC I introduced for the team and my own PM work: AI coding agents for codebase analysis, code review and delivery documents, with human review before anything ships.</li>
      </ul>
    </section>
    <section class="wide">
      <h2>One process, end to end</h2>
      <p>An interbank transfer looks simple to the customer. Behind it are the core banking system, a national payment network and a back-office team that makes sure every transfer settles exactly once.</p>
      {d2}
    </section>
    <section>
      <h2>How we delivered</h2>
      <p>We run Scrum and plan sprints at an 80% velocity factor against roughly 85% realised capacity, leaving room for production support and regulatory change. The backlog uses feature IDs, a definition of ready, T-shirt sizing and a flag for whether test cases are written. Every feature moves through the same stages: sprint, QA, UAT, production. Compliance requirements, from Bangladesh Bank’s ICT security guidelines to the applicable PCI-DSS controls and PII protection, are written into each PRD’s definition of done and checked before release. Every feature shipped so far went live on time, within scope and within budget.</p>
      <p>Each service ships through a GitLab pipeline that builds, deploys, health-checks and rolls back automatically if the check fails, with SonarQube on the way. Web journeys are tested with Cypress and the mobile app with Appium and WebdriverIO; the app alone has hundreds of automated tests. Standard releases take fifteen minutes, down from an hour. Releases that need downtime are agreed with the bank in advance and announced to customers.</p>
    </section>
    <section class="wide">
      <h2>Outcomes</h2>
      {outcomes([("640k+", "retail customers"), ("17k+", "eKYC registrations a month"), ("15 min", "standard release, down from 1 hour"), ("90%", "automated test coverage"), ("500+", "corporate banking customers"), ("1,500+", "branch and back-office users")])}
    </section>
  </div>"""
    return page("internet-banking", "Digital banking platform",
                "Case study: retail, corporate, branch and education banking on one platform for Agrani Bank PLC, with Bangla QR, national payment rails and digital wallets.",
                "Agrani Bank PLC", body,
                ("universe-billing.html", "UniVerge ICX billing"), ("agent-licensing.html", "Agent Licensing Online"))


# ---------------------------------------------------------------- ALO
def alo():
    s = lanes(["Candidate|agent", "Insurance|company", "Training|institute", "IDRA"], 10, 10, 1280, 88)
    L = lambda i: 10 + i * 88 + 44
    s += ev(170, L(1))
    s += task(210, L(1) - 25, 130, 50, ["Issue access", "number"])
    s += '<path class="flow" d="M184,%d H210"/>' % L(1)
    s += task(380, L(0) - 25, 130, 50, ["Submit Form-1", "online"])
    s += '<path class="flow" d="M340,%d H445 V%d"/>' % (L(1), L(0) + 25)
    s += task(550, L(1) - 25, 130, 50, ["Review and", "appoint agent"])
    s += '<path class="flow" d="M510,%d H615 V%d"/>' % (L(0), L(1) - 25)
    s += task(550, L(2) - 25, 130, 50, ["Training and", "certificate"])
    s += '<path class="flow" d="M615,%d V%d"/>' % (L(1) + 25, L(2) - 25)
    s += task(730, L(1) - 25, 140, 50, ["Form-3 batch", "to IDRA"], "task hot")
    s += '<path class="flow" d="M680,%d H705 V%d H730"/>' % (L(2), L(1))
    s += task(860, L(3) - 25, 110, 50, ["Review"])
    s += '<path class="flow hot" d="M870,%d H915 V%d"/>' % (L(1), L(3) - 25)
    s += gw(1015, L(3), "accepted?", 1015, L(3) + 40)
    s += '<path class="flow" d="M970,%d H993"/>' % L(3)
    s += '<path class="flow alt" d="M1015,%d V%d H800 V%d"/>' % (L(3) - 22, L(2), L(1) + 25)
    s += '<text class="t-faint" x="815" y="%d">rejected: fix and resubmit</text>' % (L(2) - 8)
    s += task(1060, L(3) - 25, 90, 50, ["Verify"])
    s += '<path class="flow" d="M1037,%d H1060"/>' % L(3)
    s += task(1170, L(3) - 25, 110, 50, ["Approve,", "licence no."], "task hot")
    s += '<path class="flow" d="M1150,%d H1170"/>' % L(3)
    s += ev(1225, L(0), True)
    s += '<path class="flow hot" d="M1225,%d V%d"/>' % (L(3) - 25, L(0) + 14)
    s += '<text class="t-faint" x="1203" y="%d" text-anchor="end">licence issued</text>' % (L(0) + 5)
    d1 = fig(s, "0 0 1300 372",
             "A new agent licence as BPMN. IDRA works in batches: one officer reviews, another verifies, a third approves. Renewals (Form-5) follow the same IDRA path, with late fees calculated under the regulation.",
             "BPMN diagram of the insurance agent licence process")

    s = '<text class="t-head" x="20" y="30">Time to approve a licence</text>'
    s += '<text class="t-soft" x="20" y="72">Before</text>'
    s += '<rect class="bar-a" x="100" y="56" width="784" height="24" rx="3"/>'
    s += '<text x="894" y="74">14 days</text>'
    s += '<text class="t-soft" x="20" y="122">After</text>'
    s += '<rect class="bar-b" x="100" y="106" width="56" height="24" rx="3"/>'
    s += '<text x="166" y="124">24 hours</text>'
    d2 = fig(s, "0 0 960 150", "Bars are drawn to scale: 336 hours against 24.", "Bar chart: approval time fell from 14 days to 24 hours")

    body = f"""  <header>
    <p class="client">Insurance Development and Regulatory Authority · 2021 to 2026</p>
    <h1>Agent Licensing Online</h1>
    <p class="lede">The national platform that recruits, trains and licenses insurance agents in Bangladesh, built to the 2021 agent regulations and run until the contract completed in June 2026.</p>
  </header>
  {facts([("Client", "IDRA, the insurance regulator"), ("My role", "Requirements, architecture and delivery lead"), ("Scale", "800,000+ agents, 83 insurers, 8 training institutes"), ("Stack", "Node.js, Angular, PostgreSQL, Spring Batch, JasperReports")])}
  <div class="cs-body">
    <section>
      <h2>The problem</h2>
      <p>The Insurance Agent (Recruitment, Registration and Licence) Regulations 2021 set out how agents must be recruited, trained and licensed. In practice the work was slow and paper-heavy, split between the regulator, dozens of insurance companies and the training institutes. A licence took about two weeks.</p>
    </section>
    <section class="wide">
      <h2>The process we put online</h2>
      <p>Four parties, one flow, separate tracks for life and non-life insurers. Each step has a single owner and the platform enforces the regulation, so the regulator reviews complete batches instead of chasing missing papers.</p>
      {d1}
    </section>
    <section>
      <h2>What the platform covers</h2>
      <ul>
        <li><strong>Recruitment:</strong> insurers issue time-limited access numbers by SMS, candidates apply online, and approval generates the agent code and appointment letter.</li>
        <li><strong>Training:</strong> institutes run batches and issue certificates, which the licence application then picks up.</li>
        <li><strong>Licensing and renewal:</strong> Form-3 and Form-5 applications in batches, a three-step review at IDRA, generated licences, and a late-fee calculator that follows the regulation.</li>
        <li><strong>Agent register:</strong> the national licensed-agent register, agent history, release letters for agents moving between insurers, and NID verification with the Election Commission.</li>
        <li><strong>Reporting:</strong> summaries by company and training status, eKYC results, and policies sold per agent, shared with the regulator’s policy information system.</li>
      </ul>
    </section>
    <section>
      <h2>My part</h2>
      <ul>
        <li>Turned the regulation into requirements and acceptance criteria with IDRA, and owned that relationship from first build to completion.</li>
        <li>Led the architecture and delivery: a bilingual Bangla and English web app, an API, a report service for licences and certificates, and an SMS service with per-insurer sender names.</li>
        <li>Coordinated the rollout across insurance companies and training institutes, each with different levels of digital readiness.</li>
      </ul>
    </section>
    <section>
      <h2>How we delivered</h2>
      <p>Five years of steady releases, with nearly 4,000 commits across the web, API, report and SMS services. Releases moved through GitLab with manual promotion gates, rolling updates and automatic rollback. API and report services had integration test suites. In the final year we added Prometheus, Grafana and Loki monitoring with business-level alerts, such as a rising NID-verification rejection rate, sent to the team’s chat.</p>
    </section>
    <section class="wide">
      <h2>Outcomes</h2>
      {d2}
      {outcomes([("800k+", "agents managed"), ("3-step", "review, verify, approve at IDRA"), ("Best Innovation", "Project award")])}
    </section>
  </div>"""
    return page("agent-licensing", "Agent Licensing Online",
                "Case study: the national insurance agent recruitment, training and licensing platform for IDRA. Licence approval cut from 14 days to 24 hours.",
                "IDRA", body,
                ("internet-banking.html", "Digital banking platform"), ("customs-agents.html", "Customs Agent Management"))


# ---------------------------------------------------------------- Customs
def cams():
    s = ""
    s += '<text class="t-head" x="30" y="30">Application</text>'
    s += '<text class="t-head" x="420" y="30">Licence</text>'
    s += task(30, 60, 120, 54, ["Draft"])
    s += task(200, 60, 140, 54, ["Submitted"])
    s += task(420, 60, 140, 54, ["Active"], "task hot")
    s += task(650, 60, 130, 54, ["Suspended"])
    s += task(860, 60, 130, 54, ["Cancelled"])
    s += '<path class="flow" d="M150,87 H200"/>'
    s += '<text class="t-faint" x="175" y="80" text-anchor="middle">submit</text>'
    s += '<path class="flow hot" d="M340,87 H420"/>'
    s += '<text class="t-faint" x="380" y="80" text-anchor="middle">approve</text>'
    s += '<path class="flow" d="M560,87 H650"/>'
    # revert / reject
    s += task(130, 200, 120, 46, ["Reverted"])
    s += task(300, 200, 120, 46, ["Rejected"])
    s += '<path class="flow" d="M240,114 L205,200"/>'
    s += '<path class="flow alt" d="M130,223 H90 V114"/>'
    s += '<text class="t-faint" x="84" y="160" text-anchor="end">edit and</text><text class="t-faint" x="84" y="176" text-anchor="end">resubmit</text>'
    s += '<path class="flow" d="M300,114 L350,200"/>'
    # amendment
    s += task(430, 200, 120, 46, ["Amendment"])
    s += '<path class="flow" d="M465,114 V200"/>'
    s += '<path class="flow alt" d="M515,200 V114"/>'
    s += '<text class="t-faint" x="490" y="268" text-anchor="middle">approved changes</text><text class="t-faint" x="490" y="284" text-anchor="middle">keep it active</text>'
    # suspend / cancel / reactivate
    s += '<path class="flow alt" d="M715,60 V36 H490 V60"/>'
    s += '<text class="t-faint" x="602" y="30" text-anchor="middle">reactivated</text>'
    s += '<path class="flow" d="M545,114 V160 H925 V114"/>'
    s += '<text class="t-faint" x="740" y="152" text-anchor="middle">cancelled</text>'
    s += '<path class="flow alt" d="M925,60 V14 H530 V60" />'
    s += '<text class="t-faint" x="760" y="10" text-anchor="middle">reactivated within licence validity</text>'
    s += '<text class="t-faint" x="925" y="190" text-anchor="middle">cascades to owners,</text>'
    s += '<text class="t-faint" x="925" y="206" text-anchor="middle">representatives and</text>'
    s += '<text class="t-faint" x="925" y="222" text-anchor="middle">reference licences</text>'
    d1 = fig(s, "0 0 1010 300",
             "The licence lifecycle as a state flow. An Initiator at a customs office drafts and submits; an Approver approves, sends it back or rejects it. Every status change records a reason and an effective date, and the agent is notified by SMS.",
             "State diagram of the customs agent licence lifecycle")

    body = f"""  <header>
    <p class="client">National Board of Revenue · 2023 to 2024</p>
    <h1>Customs Agent Management System</h1>
    <p class="lede">One national register for customs agent licences in Bangladesh: C&amp;F agents, freight forwarders and shipping agents, their owners and representatives, from application to cancellation.</p>
  </header>
  {facts([("Client", "National Board of Revenue"), ("My role", "End-to-end delivery lead"), ("Scale", "300,000+ customs agents, 19 customs offices"), ("Stack", "Node.js, Hapi, Angular, PostgreSQL, JasperReports; ASYCUDA World")])}
  <div class="cs-body">
    <section>
      <h2>The problem</h2>
      <p>Customs agent licences were handled separately by each custom house and commissionerate, largely on paper. Nobody had a single view of who held a valid licence, who the owners and representatives behind it were, or which cases were open against an agent, and the clearance system could not see licence status directly.</p>
    </section>
    <section class="wide">
      <h2>The licence lifecycle</h2>
      <p>We modelled every state a licence can be in, and who can move it from one state to the next, then built the system around that model.</p>
      {d1}
    </section>
    <section>
      <h2>What the system covers</h2>
      <ul>
        <li><strong>Licensing:</strong> applications with documents for three agent types and three licence types (general, reference and self-clearance), a two-level approval, amendments, and suspension, cancellation and reactivation.</li>
        <li><strong>People:</strong> owners and representatives (customs and jetty sarkars) linked to each licence, with their own status and printable ID cards.</li>
        <li><strong>Integration:</strong> connected to ASYCUDA World, the customs clearance system, and to an external SMS gateway that notifies agents as their applications and licences change status.</li>
        <li><strong>Verification:</strong> business identification numbers checked against the NBR VAT system, plus an agent portal for linking customs and VAT registrations, reviewed in three steps.</li>
        <li><strong>Enforcement:</strong> cases and show-cause notices tracked from the custom house through to the courts.</li>
        <li><strong>Oversight:</strong> dashboards for each office and across all 19 offices, and agent, owner, representative and verification reports.</li>
      </ul>
    </section>
    <section>
      <h2>My part</h2>
      <ul>
        <li>Led delivery end to end: requirements with the National Board of Revenue, design, build and rollout across custom houses and commissionerates.</li>
        <li>Designed the role model (initiator, approver, operations manager, office admin, super admin) so each office runs its own approvals while headquarters sees everything.</li>
        <li>Migrated the legacy C&amp;F agent records into the new register.</li>
      </ul>
    </section>
    <section>
      <h2>How we delivered</h2>
      <p>About 1,100 commits across the API and web app over nearly two years. GitLab CI deployed every change to a development environment automatically, and production releases were a deliberate, manual step. The web app is an installable progressive web app, and licences, ID cards and reports are generated from report templates in a separate service.</p>
    </section>
    <section class="wide">
      <h2>Outcomes</h2>
      {outcomes([("300k+", "customs agents on one register"), ("19", "custom houses and commissionerates"), ("90%", "less manual processing time")])}
    </section>
  </div>"""
    return page("customs-agents", "Customs Agent Management System",
                "Case study: a single licence register and lifecycle for customs agents across 19 customs offices, built for Bangladesh's National Board of Revenue.",
                "NBR", body,
                ("agent-licensing.html", "Agent Licensing Online"), ("universe-billing.html", "UniVerge ICX billing"))


# ---------------------------------------------------------------- UniVerge
def uv():
    s = ""
    steps = [["Switch session", "records (FTP)"], ["Pull and", "stage files"], ["Validate,", "find gaps"],
             ["Parse and rate", "by traffic type"], ["Oracle store", "and CSV"], ["Invoices and", "reports"]]
    notes = ["", "", "name, size, sequence", "ICX, IGW, ANS, IOS", "", "3 invoice types"]
    for i, st in enumerate(steps):
        x = 20 + i * 162
        s += task(x, 70, 140, 56, st, "task hot" if i in (2, 3) else ("task ext" if i == 0 else "task"))
        if notes[i]:
            s += f'<text class="t-amber" x="{x+70}" y="54" text-anchor="middle">{notes[i]}</text>'
        if i:
            s += f'<path class="flow{" hot" if i in (3,4) else ""}" d="M{x-22},98 H{x}"/>'
    s += task(182, 180, 140, 46, ["Regulator feed"], "task ext")
    s += '<path class="flow" d="M252,126 V180"/>'
    s += task(506, 180, 140, 46, ["Re-rating"])
    s += '<path class="flow" style="marker-start:url(#arrow)" d="M576,126 V180"/>'
    s += '<rect class="task ext" x="182" y="262" width="300" height="48" rx="8"/>'
    s += '<text x="332" y="291" text-anchor="middle">Coordination: ZooKeeper</text>'
    s += '<rect class="task ext" x="506" y="262" width="464" height="48" rx="8"/>'
    s += '<text x="738" y="291" text-anchor="middle">Live statistics and control (JMX), watchdog restarts</text>'
    d1 = fig(s, "0 0 1000 330",
             "The billing pipeline. Session records arrive from the switch, are validated for gaps in the file sequence, rated by traffic type and turned into invoices and regulator reports. Operators can watch, pause and re-rate from the web app.",
             "Pipeline diagram of the ICX billing system")

    body = f"""  <header>
    <p class="client">Telecom interconnect exchange · 2023 to present</p>
    <h1>UniVerge ICX billing</h1>
    <p class="lede">Rebuilding a telecom interconnect billing system: the call-record pipeline on a legacy Java River framework, plus a new web application and API, now kept running 24/7 under an annual maintenance contract with a team I lead.</p>
  </header>
  {facts([("Domain", "Telecom interconnect billing"), ("My role", "Rebuild lead, now sustain lead"), ("Scale", "985 files a cycle, 3.5 GB of records a day"), ("Stack", "Java, River framework, Node.js, Angular 16, Oracle, ZooKeeper")])}
  <div class="cs-body">
    <section>
      <h2>The problem</h2>
      <p>Interconnect billing settles what operators owe each other for calls that cross their networks, so a lost or double-counted record turns directly into a billing dispute. The pipeline ran on a legacy Java River framework, and the application around it was an ageing Struts and JSP web app on Tomcat 7: hard to change, hard to see into, and tied to old switch formats.</p>
    </section>
    <section class="wide">
      <h2>The pipeline</h2>
      {d1}
    </section>
    <section>
      <h2>What we changed</h2>
      <ul>
        <li><strong>A new application layer:</strong> an Angular 16 web app on a reusable component library and a Node.js API, replacing the legacy web app.</li>
        <li><strong>Billing operations:</strong> domestic, international incoming and international outgoing invoices with an approval step, scheduling and regeneration, plus re-rating for disputed or failed records.</li>
        <li><strong>Reporting:</strong> regulator reports, call volume by partner and route, completion ratios and dashboards for incoming and outgoing traffic.</li>
        <li><strong>Operability:</strong> live statistics and pause, resume and reload controls from the browser, and a watchdog that restarts the engine on known failure patterns.</li>
        <li><strong>The pipeline:</strong> rebuilt call-record processing on the River framework to parse 985 files a cycle, each carrying 30,000+ session records of 390 fields, about 3.5 GB a day, including a new switch’s record format and country-wise pulse rating.</li>
        <li><strong>The hardware:</strong> specified and configured the high-availability servers it runs on: 96 cores, 256 GB of RAM and 18 TB of SSD storage.</li>
        <li><strong>One codebase, two operators:</strong> client profiles let the same build serve two interconnect operators.</li>
      </ul>
    </section>
    <section>
      <h2>What running it taught me</h2>
      <p>A sustain contract is a product with a different shape: fewer features, more attention to database growth, capacity and the next change request. A small team that clearly owns the system keeps it boring, which is the goal for billing.</p>
    </section>
    <section class="wide">
      <h2>Outcomes</h2>
      {outcomes([("985", "files parsed per cycle"), ("3.5 GB", "of call records a day"), ("30k+", "session records per file"), ("3", "invoice types with approval"), ("2", "operators on one codebase"), ("24/7", "operation, now under AMC")])}
    </section>
  </div>"""
    return page("universe-billing", "UniVerge ICX billing",
                "Case study: rebuilding a telecom interconnect billing system, its call-record pipeline and a new web app and API, invoicing, re-rating and regulator reporting, and running it under a maintenance contract.",
                "Telecom", body,
                ("customs-agents.html", "Customs Agent Management"), ("internet-banking.html", "Digital banking platform"))


out = ROOT / "work"
out.mkdir(exist_ok=True)
for name, fn in [("internet-banking", ib), ("agent-licensing", alo), ("customs-agents", cams), ("universe-billing", uv)]:
    (out / f"{name}.html").write_text(fn())
    print("wrote", name)
