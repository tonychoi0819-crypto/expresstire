
# PART 2 - Continue from where we left off
# Paste this after the previous code

for pi,row_data in enumerate(proc2):
    for ci,val in enumerate(row_data,1): dat(ws3,r+pi,ci,val,alt=(pi%2==1))
sw(ws3,[10,32,14,12,12,12,16,12,14,22,8,20])
ws3.freeze_panes = "A4"
print("Sheet 3: Phase 2 DONE")

# ============================================================
# SHEET 4: PHASE 3 — INSTALLATION & INTEGRATION
# ============================================================
ws4 = wb.create_sheet("Phase 3 - Installation"); ws4.sheet_properties.tabColor = "B4C6E7"
ws4.merge_cells('A1:L1'); ws4['A1'] = "PHASE 3: SITE INSTALLATION & SYSTEM INTEGRATION"
ws4['A1'].font = Font(bold=True,size=14,color="000000",name="Calibri")
ws4['A1'].fill = PatternFill(start_color=phase_colors[2],fill_type="solid"); ws4['A1'].alignment = ctr
r = 3
hdr(ws4,r,1,"WORK BREAKDOWN STRUCTURE (WBS)",span=12); r+=1
for i,h in enumerate(wh,1): hdr(ws4,r,i,h,PatternFill(start_color=phase_colors[2],fill_type="solid"))
r+=1
wbs3 = [
    ["3.1","Site Preparation - Site A (Chek Lap Kok)","90","2027-01-15","2027-04-14","2.6","Civil Contractor","0%","Not Started","Site Ready","Grey",""],
    ["3.2","Site Preparation - Site B (Tai Mo Shan)","90","2027-01-15","2027-04-14","2.6","Civil Contractor","0%","Not Started","Site Ready","Grey",""],
    ["3.3","Site Preparation - Site C (MLS)","75","2027-02-01","2027-04-16","2.6","Civil Contractor","0%","Not Started","Site Ready","Grey",""],
    ["3.4","Install Primary Radar","120","2027-04-15","2027-08-12","3.1,PKG1","Vendor","0%","Not Started","Install Cert","Grey",""],
    ["3.5","Install SSR","90","2027-05-01","2027-07-29","3.2,PKG2","Vendor","0%","Not Started","Install Cert","Grey",""],
    ["3.6","Install MLAT Stations (x4)","150","2027-04-16","2027-09-12","3.3,PKG3","Vendor","0%","Not Started","Install Cert","Grey",""],
    ["3.7","Install Data Processing System","60","2027-06-01","2027-07-30","3.1,PKG4","Vendor","0%","Not Started","Install Cert","Grey",""],
    ["3.8","Network & Communications Install","75","2027-05-15","2027-07-28","3.1,PKG5","Vendor","0%","Not Started","Install Cert","Grey",""],
    ["3.9","System Integration","90","2027-08-13","2027-11-10","3.4-3.8","SI Lead","0%","Not Started","Integ. Report","Grey",""],
    ["3.10","CAD System Interface","60","2027-09-01","2027-10-30","3.7,3.8","SW Team","0%","Not Started","Interface Cert","Grey",""],
    ["3.11","Power Supply & Backup","45","2027-07-01","2027-08-14","3.1","Electrical","0%","Not Started","Power Cert","Grey",""],
    ["3.12","Earthing & Lightning Protection","30","2027-07-15","2027-08-13","3.1","Electrical","0%","Not Started","Safety Cert","Grey",""],
    ["3.13","Phase Gate Review","7","2027-11-20","2027-11-26","3.9-3.12","CAD/PM","0%","Not Started","Gate Approval","Grey",""],
]
for wi,row_data in enumerate(wbs3):
    for ci,val in enumerate(row_data,1): dat(ws4,r+wi,ci,val,alt=(wi%2==1))
r += 15
hdr(ws4,r,1,"INSTALLATION MILESTONE TRACKER",span=12); r+=1
imh = ["Milestone","Planned Date","Forecast Date","Actual Date","Status","Days Variance"]
for i,h in enumerate(imh,1): hdr(ws4,r,i,h,PatternFill(start_color=phase_colors[2],fill_type="solid"))
r+=1
milestones3 = [
    ["Site A Ready","2027-04-14","2027-04-20","—","On Track","+6"],
    ["Site B Ready","2027-04-14","2027-04-18","—","On Track","+4"],
    ["Primary Radar Installed","2027-08-12","2027-08-12","—","On Track","0"],
    ["All Sites Integrated","2027-11-10","2027-11-15","—","On Track","+5"],
    ["Phase 3 Gate Approved","2027-11-26","2027-11-26","—","On Track","0"],
]
for mi,row_data in enumerate(milestones3):
    for ci,val in enumerate(row_data,1): dat(ws4,r+mi,ci,val,alt=(mi%2==1))
sw(ws4,[30,14,14,12,14,14])
ws4.freeze_panes = "A4"
print("Sheet 4: Phase 3 DONE")

# ============================================================
# SHEET 5: PHASE 4 — TESTING & COMMISSIONING
# ============================================================
ws5 = wb.create_sheet("Phase 4 - Testing"); ws5.sheet_properties.tabColor = "F4B084"
ws5.merge_cells('A1:L1'); ws5['A1'] = "PHASE 4: TESTING & COMMISSIONING"
ws5['A1'].font = Font(bold=True,size=14,color="000000",name="Calibri")
ws5['A1'].fill = PatternFill(start_color=phase_colors[3],fill_type="solid"); ws5['A1'].alignment = ctr
r = 3
hdr(ws5,r,1,"WORK BREAKDOWN STRUCTURE (WBS)",span=12); r+=1
for i,h in enumerate(wh,1): hdr(ws5,r,i,h,PatternFill(start_color=phase_colors[3],fill_type="solid"))
r+=1
wbs4 = [
    ["4.1","Factory Acceptance Test (FAT)","45","2028-01-15","2028-02-27","3.9","QA/Vendor","0%","Not Started","FAT Report","Grey","All subsystems"],
    ["4.2","Site Acceptance Test (SAT) - Site A","30","2028-03-01","2028-03-30","4.1","QA Team","0%","Not Started","SAT Report A","Grey",""],
    ["4.3","Site Acceptance Test (SAT) - Site B","30","2028-03-15","2028-04-13","4.1","QA Team","0%","Not Started","SAT Report B","Grey",""],
    ["4.4","Site Acceptance Test (SAT) - Site C","25","2028-04-01","2028-04-25","4.1","QA Team","0%","Not Started","SAT Report C","Grey",""],
    ["4.5","End-to-End System Test","30","2028-05-01","2028-05-30","4.2-4.4","QA/PM","0%","Not Started","E2E Report","Grey","Full radar chain"],
    ["4.6","Operational Acceptance Test (OAT)","45","2028-06-01","2028-07-15","4.5","CAD Ops","0%","Not Started","OAT Report","Grey","ATCO participation"],
    ["4.7","Safety Case Assessment","30","2028-07-01","2028-07-30","4.6","Safety Eng.","0%","Not Started","Safety Case","Grey",""],
    ["4.8","Regulatory Commissioning","30","2028-08-01","2028-08-30","4.7","CAD","0%","Not Started","Commission Cert","Grey","CAD approval"],
    ["4.9","Parallel Running (Old+New)","90","2028-09-01","2028-11-29","4.8","Ops Team","0%","Not Started","Parallel Report","Grey","3 months"],
    ["4.10","Performance Validation","30","2028-11-01","2028-11-30","4.9","QA/PM","0%","Not Started","Perf. Report","Grey","ICAO standards"],
    ["4.11","Phase Gate Review","7","2028-12-05","2028-12-11","4.10","Steering Comm.","0%","Not Started","Gate Approval","Grey",""],
]
for wi,row_data in enumerate(wbs4):
    for ci,val in enumerate(row_data,1): dat(ws5,r+wi,ci,val,alt=(wi%2==1))
r += 13
# Defect Tracker
hdr(ws5,r,1,"DEFECT TRACKER",span=12); r+=1
dt_h = ["Defect ID","Description","Severity","Reported Date","Phase Found","Status","Assigned To","Resolution Date","Resolution"]
for i,h in enumerate(dt_h,1): hdr(ws5,r,i,h,PatternFill(start_color=phase_colors[3],fill_type="solid"))
r+=1
defects = [
    ["DEF-001","Radar display latency >2s","Major","2026-03-15","Phase 2 - Design","Resolved","SW Team","2026-04-01","Algorithm optimization"],
    ["DEF-002","SSR Mode S interrogation failure","Critical","2026-05-20","Phase 2 - Design","In Progress","Comms Eng.","—","Hardware replacement"],
    ["DEF-003","MLAT sync drift","Minor","2026-06-10","Phase 2 - Design","Open","Nav. Eng.","—","GPS clock sync fix"],
]
for di,row_data in enumerate(defects):
    for ci,val in enumerate(row_data,1): dat(ws5,r+di,ci,val,alt=(di%2==1))

# Test Metrics
r += 5
hdr(ws5,r,1,"TEST METRICS & KPIs",span=12); r+=1
tm_h = ["Metric","Target","Actual","Unit","Status"]
for i,h in enumerate(tm_h,1): hdr(ws5,r,i,h,PatternFill(start_color=phase_colors[3],fill_type="solid"))
r+=1
for ri,row in enumerate([["Test Cases Executed",">500","0","Cases","Not Started"],["Test Pass Rate",">98%","0%","%","Not Started"],["Critical Defects Open","0","0","Count","Not Started"],["Major Defects Open","<5","0","Count","Not Started"],["Test Environment READY","100%","0%","%","Not Started"]]):
    for ci,val in enumerate(row,1): dat(ws5,r+ri,ci,val,alt=(ri%2==1))
sw(ws5,[12,35,12,14,12,14,14,14,30])
ws5.freeze_panes = "A4"
print("Sheet 5: Phase 4 DONE")

# ============================================================
# SHEET 6: PHASE 5 — HANDOVER & CLOSEOUT
# ============================================================
ws6 = wb.create_sheet("Phase 5 - Handover"); ws6.sheet_properties.tabColor = "FF9999"
ws6.merge_cells('A1:L1'); ws6['A1'] = "PHASE 5: HANDOVER & PROJECT CLOSEOUT"
ws6['A1'].font = Font(bold=True,size=14,color="FFFFFF",name="Calibri")
ws6['A1'].fill = PatternFill(start_color=phase_colors[4],fill_type="solid"); ws6['A1'].alignment = ctr
r = 3
hdr(ws6,r,1,"WORK BREAKDOWN STRUCTURE (WBS)",span=12); r+=1
for i,h in enumerate(wh,1): hdr(ws6,r,i,h,PatternFill(start_color=phase_colors[4],fill_type="solid"))
r+=1
wbs5 = [
    ["5.1","System Handover to Operations","14","2029-01-01","2029-01-14","4.11","PM/Ops","0%","Not Started","Handover Cert","Grey",""],
    ["5.2","Documentation Handover","21","2029-01-08","2029-01-28","5.1","Tech Writer","0%","Not Started","Doc Register","Grey","O&M manuals"],
    ["5.3","Training - ATCO","30","2029-01-15","2029-02-13","5.1","Training Team","0%","Not Started","Training Cert","Grey","40 ATCOs"],
    ["5.4","Training - Maintenance Staff","21","2029-01-29","2029-02-18","5.1","Training Team","0%","Not Started","Training Cert","Grey","25 engineers"],
    ["5.5","Training - Engineering Staff","14","2029-02-19","2029-03-04","5.1","Vendor","0%","Not Started","Training Cert","Grey","15 engineers"],
    ["5.6","Warranty Period Start","182","2029-01-15","2029-07-15","5.1","PM","0%","Not Started","Warranty Cert","Grey","24 months"],
    ["5.7","Final Documentation Package","30","2029-02-01","2029-03-02","5.2","PM","0%","Not Started","Final Package","Grey","As-built docs"],
    ["5.8","Financial Closeout","21","2029-03-15","2029-04-04","5.7","Finance","0%","Not Started","Final Account","Grey","All payments"],
    ["5.9","Lessons Learned Workshop","7","2029-04-05","2029-04-11","5.8","PM","0%","Not Started","LL Report","Grey","All phases"],
    ["5.10","Final Audit","14","2029-04-12","2029-04-25","5.9","Auditor","0%","Not Started","Audit Report","Grey","Independent"],
    ["5.11","Project Closure","7","2029-06-24","2029-06-30","5.10","PM","0%","Not Started","Closure Report","Grey",""],
]
for wi,row_data in enumerate(wbs5):
    for ci,val in enumerate(row_data,1): dat(ws6,r+wi,ci,val,alt=(wi%2==1))
r += 13
# Training Plan
hdr(ws6,r,1,"TRAINING PLAN",span=12); r+=1
tp_h = ["Course","Audience","Duration (Days)","Start","End","Trainer","Status"]
for i,h in enumerate(tp_h,1): hdr(ws6,r,i,h,PatternFill(start_color=phase_colors[4],fill_type="solid"))
r+=1
training = [
    ["Radar Familiarization","All ATC Staff","5","2029-01-15","2029-01-19","Vendor","Planned"],
    ["System Operations","ATCO (40 pax)","10","2029-01-22","2029-02-01","Vendor","Planned"],
    ["Maintenance - Primary Radar","Tech Staff (10)","5","2029-02-05","2029-02-09","Vendor","Planned"],
    ["Maintenance - SSR & Comms","Tech Staff (8)","5","2029-02-12","2029-02-16","Vendor","Planned"],
    ["SW & Data Processing","SW Engineers (7)","5","2029-02-19","2029-02-23","Vendor","Planned"],
    ["Emergency Procedures","All Staff","3","2029-03-01","2029-03-03","Safety Team","Planned"],
]
for ti,row_data in enumerate(training):
    for ci,val in enumerate(row_data,1): dat(ws6,r+ti,ci,val,alt=(ti%2==1))
sw(ws6,[28,22,14,12,12,20,12])
ws6.freeze_panes = "A4"
print("Sheet 6: Phase 5 DONE")

# ============================================================
# SHEET 7: KPI SUMMARY & PMP MEASUREMENTS
# ============================================================
ws7 = wb.create_sheet("KPI & PMP Summary")
ws7.merge_cells('A1:K1'); ws7['A1'] = "CONSOLIDATED KPI & PMP MEASUREMENTS"
ws7['A1'].font = Font(bold=True,size=14,color="FFFFFF",name="Calibri")
ws7['A1'].fill = hdr_fill; ws7['A1'].alignment = ctr

r = 3
# PMP Knowledge Areas
hdr(ws7,r,1,"PMP KNOWLEDGE AREA COMPLIANCE",span=11); r+=1
pmp_h = ["Knowledge Area","Process Group","Key Deliverable","Status","Compliance %","Auditor Notes"]
for i,h in enumerate(pmp_h,1): hdr(ws7,r,i,h,sub_fill)
r+=1
pmp_areas = [
    ["Integration Management","All Phases","Project Management Plan","On Track","95%","PMBOK 7 aligned"],
    ["Scope Management","Planning","WBS / Requirements Doc","On Track","98%","215 requirements baselined"],
    ["Schedule Management","Planning/Monitoring","Gantt Chart / Milestones","On Track","92%","12 milestones tracked"],
    ["Cost Management","Planning/Monitoring","Budget / EVM Reports","On Track","96%","CPI=1.05 favorable"],
    ["Quality Management","Executing","QA Plan / Defect Log","On Track","94%","ISO 9001 framework"],
    ["Resource Management","Executing","Resource Histogram","On Track","90%","52 FTEs allocated"],
    ["Communications Management","All Phaces","Comms Plan / Reports","On Track","95%","Weekly reports to CAD"],
    ["Risk Management","Planning/Monitoring","Risk Register","On Track","92%","68 risks, 12 high"],
    ["Procurement Management","Planning/Executing","Contracts / POs","On Track","88%","7 procurement packages"],
    ["Stakeholder Management","All Phases","Stakeholder Register","On Track","97%","47 stakeholders mapped"],
]
for pi,row_data in enumerate(pmp_areas):
    for ci,val in enumerate(row_data,1): dat(ws7,r+pi,ci,val,alt=(pi%2==1))
r += 12
# Earned Value Details
hdr(ws7,r,1,"EARNED VALUE MANAGEMENT DETAIL",span=11); r+=1
ev_h = ["Month","PV (HK$)","EV (HK$)","AC (HK$)","SPI","CPI","SV (HK$)","CV (HK$)"]
for i,h in enumerate(ev_h,1): hdr(ws7,r,i,h,sub_fill)
r+=1
months = ["Jul-25","Aug-25","Sep-25","Oct-25","Nov-25","Dec-25","Jan-26","Feb-26","Mar-26","Apr-26","May-26","Jun-26"]
pv_cumulative = [3.5,7.1,12.8,18.5,25.0,32.5,42.5,54.0,66.5,80.0,95.0,110.0]
ev_cumulative = [3.3,6.8,12.2,17.8,24.0,31.0,40.5,51.5,63.5,76.5,91.0,105.5]
ac_cumulative = [3.2,6.5,11.5,16.8,22.8,29.5,38.5,49.0,60.5,73.0,86.5,101.0]
for mi,month in enumerate(months):
    pv = pv_cumulative[mi]
    ev = ev_cumulative[mi]
    ac = ac_cumulative[mi]
    spi = ev/pv if pv > 0 else 0
    cpi = ev/ac if ac > 0 else 0
    sv = ev - pv
    cv = ev - ac
    row_data = [month, pv*1e6, ev*1e6, ac*1e6, round(spi,3), round(cpi,3), round(sv*1e6), round(cv*1e6)]
    for ci,val in enumerate(row_data,1):
        cell = dat(ws7,r+mi,ci,val,alt=(mi%2==1))
        if ci in [2,3,4,7,8]: cell.number_format = 'HK$#,##0'
        if ci in [5,6]: cell.number_format = '0.000'
r += 14
# Budget Breakdown
hdr(ws7,r,1,"BUDGET BREAKDOWN BY PHASE",span=11); r+=1
bb_h = ["Phase","Budget (HK$)","Committed (HK$)","Spent (HK$)","Remaining (HK$)","% Spent","Forecast at Completion","Variance","Risk Reserve"]
for i,h in enumerate(bb_h,1): hdr(ws7,r,i,h,sub_fill)
r+=1
budget_data = [
    ["Phase 1 - Initiation","42,500,000","42,500,000","38,200,000","4,300,000","90%","40,500,000","+2,000,000","2,125,000"],
    ["Phase 2 - Design","170,000,000","110,000,000","95,000,000","75,000,000","56%","165,000,000","+5,000,000","8,500,000"],
    ["Phase 3 - Installation","340,000,000","0","0","340,000,000","0%","340,000,000","0","17,000,000"],
    ["Phase 4 - Testing","127,500,000","0","0","127,500,000","0%","125,000,000","+2,500,000","6,375,000"],
    ["Phase 5 - Handover","170,000,000","0","0","170,000,000","0%","170,000,000","0","8,500,000"],
    ["TOTAL","850,000,000","152,500,000","133,200,000","716,800,000","16%","840,500,000","+9,500,000","42,500,000"],
]
for bi,row_data in enumerate(budget_data):
    for ci,val in enumerate(row_data,1):
        cell = dat(ws7,r+bi,ci,val,alt=(bi%2==1),bold=(bi==5))
        if ci in [2,3,4,5,7,8]: cell.number_format = '#,##0'

sw(ws7,[22,22,14,14,14])
ws7.freeze_panes = "A4"
print("Sheet 7: KPI & PMP Summary DONE")

# ============================================================
# SHEET 8: RISK REGISTER
# ============================================================
ws8 = wb.create_sheet("Risk Register")
ws8.merge_cells('A1:K1'); ws8['A1'] = "PROJECT RISK REGISTER"
ws8['A1'].font = Font(bold=True,size=14,color="FFFFFF",name="Calibri")
ws8['A1'].fill = PatternFill(start_color="C00000",fill_type="solid"); ws8['A1'].alignment = ctr
r = 3
rr_h = ["Risk ID","Description","Category","Probability (1-5)","Impact (1-5)","Risk Score","Mitigation Strategy","Owner","Status","Phase","Last Updated"]
for i,h in enumerate(rr_h,1): hdr(ws8,r,i,h,PatternFill(start_color="C00000",fill_type="solid"))
r+=1
risks = [
    ["R-001","Radar delivery delayed due to supply chain","Schedule","3","4","12","Dual-source procurement; advance ordering","Procurement Mgr","Active","Phase 2","2026-05-01"],
    ["R-002","Site access restrictions at airport","Schedule","2","5","10","Early coordination with Airport Authority","Site Mgr","Active","Phase 3","2026-04-15"],
    ["R-003","Currency fluctuation (USD/EUR procurement)","Financial","3","3","9","Forward contracts; HKD hedging","Finance Mgr","Active","Phase 2","2026-05-10"],
    ["R-004","Key personnel unavailability","Resource","2","4","8","Cross-training; documentation","HR/PM","Monitoring","All","2026-03-20"],
    ["R-005","Regulatory approval delays","Schedule","3","5","15","Early engagement with CAD; pre-submissions","PM","Active","Phase 2","2026-05-01"],
    ["R-006","Integration issues with legacy CAD system","Technical","4","4","16","Early prototyping; interface testing","SW Architect","Active","Phase 2-3","2026-04-01"],
    ["R-007","Undiscovered underground utilities at sites","Technical","2","4","8","Comprehensive GPR survey","Civil Eng.","Monitoring","Phase 3","2026-04-20"],
    ["R-008","Weather delays during installation","Schedule","3","3","9","Schedule buffer (20 working days)","Site Mgr","Monitoring","Phase 3","2026-03-15"],
    ["R-009","Cybersecurity certification delays","Technical","2","4","8","Early engagement with CERT team","IT Security","Monitoring","Phase 4","2026-05-05"],
    ["R-010","Stakeholder opposition to radar installation","Stakeholder","1","3","3","Public consultation; EIA compliance","PM/Comms","Closed","Phase 1","2025-09-10"],
]
for ri,row_data in enumerate(risks):
    for ci,val in enumerate(row_data,1):
        cell = dat(ws8,r+ri,ci,val,alt=(ri%2==1))
        # Color risk score
        if ci == 6:
            score = int(val) if str(val).isdigit() else 0
            if score >= 12: cell.font = Font(bold=True, color="C00000", size=10)
            elif score >= 8: cell.font = Font(color="ED7D31", size=10)
            elif score >= 4: cell.font = Font(color="FFC000", size=10)
            else: cell.font = Font(color="70AD47", size=10)
sw(ws8,[10,35,14,12,10,10,30,16,12,10,14])
ws8.freeze_panes = "A4"
print("Sheet 8: Risk Register DONE")

# ============================================================
# SHEET 9: ISSUE LOG
# ============================================================
ws9 = wb.create_sheet("Issue Log")
ws9.merge_cells('A1:J1'); ws9['A1'] = "PROJECT ISSUE LOG"
ws9['A1'].font = Font(bold=True,size=14,color="FFFFFF",name="Calibri")
ws9['A1'].fill = PatternFill(start_color="7030A0",fill_type="solid"); ws9['A1'].alignment = ctr
r = 3
il_h = ["Issue ID","Description","Raised Date","Raised By","Priority","Status","Assigned To","Due Date","Resolution","Phase"]
for i,h in enumerate(il_h,1): hdr(ws9,r,i,h,PatternFill(start_color="7030A0",fill_type="solid"))
r+=1
issues = [
    ["ISS-001","SSR vendor selection criteria disputed by tender board","2026-04-10","PM","High","In Progress","Procurement","2026-05-30","Clarification meeting scheduled","Phase 2"],
    ["ISS-002","Site B (Tai Mo Shan) access road inadequate for heavy transport","2026-03-25","Site Eng.","Medium","Open","Civil Works","2026-06-15","Road upgrade quote obtained","Phase 2"],
    ["ISS-003","Conflict between radar frequency and existing comms","2026-05-01","Comms Eng.","High","In Progress","Tech Lead","2026-05-20","Frequency coordination with OFCA","Phase 2"],
    ["ISS-004","CAD operations team not available for OAT planning","2026-04-20","QA Lead","Medium","Open","PM","2026-06-30","Schedule coordination meeting","Phase 4"],
    ["ISS-005","Budget overrun risk on PKG-001 (Primary Radar)","2026-05-15","Cost Eng.","High","Under Review","Finance/PM","2026-06-15","Value engineering options being assessed","Phase 2"],
]
for ii,row_data in enumerate(issues):
    for ci,val in enumerate(row_data,1):
        cell = dat(ws9,r+ii,ci,val,alt=(ii%2==1))
        if ci == 5:
            if val == "High": cell.font = Font(bold=True, color="C00000", size=10)
            elif val == "Medium": cell.font = Font(color="ED7D31", size=10)
sw(ws9,[12,40,12,14,10,14,14,12,30,10])
ws9.freeze_panes = "A4"
print("Sheet 9: Issue Log DONE")

# ============================================================
# SHEET 10: CHANGE REQUEST LOG
# ============================================================
ws10 = wb.create_sheet("Change Requests")
ws10.merge_cells('A1:J1'); ws10['A1'] = "CHANGE REQUEST LOG"
ws10['A1'].font = Font(bold=True,size=14,color="FFFFFF",name="Calibri")
ws10['A1'].fill = PatternFill(start_color="375623",fill_type="solid"); ws10['A1'].alignment = ctr
r = 3
cr_h = ["CR ID","Description","Requestor","Date Submitted","Impact (Cost)","Impact (Schedule)","Priority","Status","Decision Date","Approved By"]
for i,h in enumerate(cr_h,1): hdr(ws10,r,i,h,PatternFill(start_color="375623",fill_type="solid"))
r+=1
changes = [
    ["CR-001","Add 5th MLAT station for better coverage","CAD Ops","2026-04-01","+HK$12,000,000","+45 days","Medium","Approved","2026-05-10","Steering Committee"],
    ["CR-002","Upgrade display resolution to 4K","ATCO Union","2026-03-15","+HK$3,500,000","+14 days","Low","Approved","2026-04-20","PM"],
    ["CR-003","Additional cybersecurity requirements (CERT)","IT Security","2026-05-05","+HK$8,000,000","+30 days","High","Under Review","—","—"],
    ["CR-004","Extend parallel running period to 6 months","CAD Ops","2026-04-20","+HK$5,000,000","+90 days","Medium","Pending","—","—"],
]
for ci,row_data in enumerate(changes):
    for cii,val in enumerate(row_data,1):
        dat(ws10,r+ci,cii,val,alt=(ci%2==1),fmt='HK$#,##0' if 'HK$' in str(val) else None)
sw(ws10,[10,40,14,14,16,16,10,14,14,20])
ws10.freeze_panes = "A4"
print("Sheet 10: Change Requests DONE")

# Save
wb.save(r"C:\Users\TonyChoi\Projects\RIM CAP\ExpressTire\HK_CAD_Radar_Project_Monitoring.xlsx")
print("\n✅✅✅ EXCEL WORKBOOK COMPLETE ✅✅✅")
print("Saved to: HK_CAD_Radar_Project_Monitoring.xlsx")
