import os, glob, re

def build_signoff_section(doc_id, doc_title, prep_date, verif_date):
    return f"""      <!-- Stakeholder Authorization & Digital Sign-Off Section -->
      <section class="doc-section signoff-section" id="sec-signoff">
        <div class="section-header">
          <div class="section-title-wrap">
            <span class="section-num" style="background: #e67e22; color: #fff; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 700;">FINAL STAGE</span>
            <h2 class="section-title" style="margin-top: 4px; font-family: 'Outfit', sans-serif; font-size: 20px; font-weight: 700; color: #0a2540;">
              Stakeholder Authorization & Digital Sign-Off Console
            </h2>
          </div>
          <span class="badge-success" style="background: #dcfce7; color: #15803d; padding: 4px 10px; border-radius: 4px; font-size: 11px; font-weight: 700;">
            <i class="fa-solid fa-shield-halved"></i> OFFICIAL ACCEPTANCE & DIGITAL VERIFICATION
          </span>
        </div>

        <p style="font-size: 13px; color: #334155; line-height: 1.6; margin-bottom: 22px;">
          By affixing digital signatures and authorizations below, all participating executive and technical stakeholders ratify the deliverables, implementation timeline, SLA commitments, and financial disbursement gates for <strong>{doc_title} ({doc_id})</strong>:
        </p>

        <!-- Block 1: Engineering Preparation & Multi-Tier Verification Matrix (Screenshot 2) -->
        <div style="margin-bottom: 28px;">
          <h3 style="font-size: 14.5px; font-weight: 700; color: #0a2540; margin-bottom: 14px; display: flex; align-items: center; gap: 8px;">
            <i class="fa-solid fa-code-branch" style="color: #d97706;"></i> 1. Engineering Preparation & Stakeholder Verification Matrix
          </h3>
          <div class="signoff-box-container" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap: 14px;">
            <!-- Prepared By Developer / Architect -->
            <div class="signoff-card" style="padding: 16px; border: 1.5px dashed #cbd5e1; border-radius: 8px; background: #ffffff; text-align: center;">
              <div style="font-size: 11px; font-weight: 800; color: #0a2540; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 6px;">DEVELOPER / ARCHITECT</div>
              <div style="font-size: 13px; font-weight: 700; color: #1e293b;">Ancy Varghese Thekkan</div>
              <div style="font-size: 11px; color: #64748b; margin-bottom: 10px;">Software Architect, SaNDS Lab</div>
              <div style="margin-bottom: 8px;">
                <span class="badge-tag badge-success" style="background: #dcfce7; color: #15803d; padding: 3px 8px; border-radius: 4px; font-size: 10.5px; font-weight: 700; display: inline-flex; align-items: center; gap: 4px;">
                  <i class="fas fa-check"></i> Prepared ({prep_date})
                </span>
              </div>
              <span class="signoff-status-badge status-signed" style="background: #f1f5f9; color: #0f766e; border: 1px solid #ccfbf1; padding: 3px 10px; border-radius: 12px; font-size: 10.5px; font-weight: 700;">COMPLETED</span>
            </div>

            <!-- Verified By CEO / Managing Director -->
            <div class="signoff-card" style="padding: 16px; border: 1.5px dashed #cbd5e1; border-radius: 8px; background: #ffffff; text-align: center;">
              <div style="font-size: 11px; font-weight: 800; color: #0a2540; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 6px;">VERIFIED BY (DEVELOPER)</div>
              <div style="font-size: 13px; font-weight: 700; color: #1e293b;">Ajit Kumar KV</div>
              <div style="font-size: 11px; color: #64748b; margin-bottom: 10px;">CEO & Managing Director, SaNDS Lab</div>
              <div style="margin-bottom: 8px;">
                <span class="badge-tag badge-success" style="background: #dcfce7; color: #15803d; padding: 3px 8px; border-radius: 4px; font-size: 10.5px; font-weight: 700; display: inline-flex; align-items: center; gap: 4px;">
                  <i class="fas fa-check"></i> Verified ({verif_date})
                </span>
              </div>
              <span class="signoff-status-badge status-signed" style="background: #f1f5f9; color: #0f766e; border: 1px solid #ccfbf1; padding: 3px 10px; border-radius: 12px; font-size: 10.5px; font-weight: 700;">CHECKED & VERIFIED</span>
            </div>

            <!-- Consultant Review -->
            <div class="signoff-card" style="padding: 16px; border: 1.5px dashed #cbd5e1; border-radius: 8px; background: #ffffff; text-align: center;">
              <div style="font-size: 11px; font-weight: 800; color: #0a2540; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 6px;">CONSULTANT REVIEW</div>
              <div style="font-size: 13px; font-weight: 700; color: #1e293b;">UniGlobal Business Solutions</div>
              <div style="font-size: 11px; color: #64748b; margin-bottom: 10px;">Project Management Consultant</div>
              <div style="margin-bottom: 8px;" id="sig_badge_consultant_review">
                <span class="badge-tag badge-primary" style="background: #fef3c7; color: #b45309; padding: 3px 8px; border-radius: 4px; font-size: 10.5px; font-weight: 700; display: inline-flex; align-items: center; gap: 4px;">
                  <i class="fas fa-clock"></i> In Active Review
                </span>
              </div>
              <span class="signoff-status-badge status-pending" id="badge_consultant_review" style="background: #fffbeb; color: #b45309; border: 1px solid #fde68a; padding: 3px 10px; border-radius: 12px; font-size: 10.5px; font-weight: 700;">IN REVIEW</span>
            </div>

            <!-- Client Approval -->
            <div class="signoff-card" style="padding: 16px; border: 1.5px dashed #cbd5e1; border-radius: 8px; background: #ffffff; text-align: center;">
              <div style="font-size: 11px; font-weight: 800; color: #0a2540; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 6px;">CLIENT APPROVAL</div>
              <div style="font-size: 13px; font-weight: 700; color: #1e293b;">Popular Auto Spare & A/C Parts</div>
              <div style="font-size: 11px; color: #64748b; margin-bottom: 10px;">Authorized Executive Signatory</div>
              <div style="margin-bottom: 8px;" id="sig_badge_client_review">
                <span class="badge-tag badge-primary" style="background: #fef3c7; color: #b45309; padding: 3px 8px; border-radius: 4px; font-size: 10.5px; font-weight: 700; display: inline-flex; align-items: center; gap: 4px;">
                  <i class="fas fa-clock"></i> Pending Approval
                </span>
              </div>
              <span class="signoff-status-badge status-pending" id="badge_client_review" style="background: #fffbeb; color: #b45309; border: 1px solid #fde68a; padding: 3px 10px; border-radius: 12px; font-size: 10.5px; font-weight: 700;">PENDING SIGNATURE</span>
            </div>
          </div>
        </div>

        <!-- Block 2: 3-Party Executive Governance Digital Sign-Off Console (Screenshot 1) -->
        <div>
          <h3 style="font-size: 14.5px; font-weight: 700; color: #0a2540; margin-bottom: 14px; display: flex; align-items: center; gap: 8px;">
            <i class="fa-solid fa-signature" style="color: #d97706;"></i> 2. Executive Multi-Party Digital Acceptance Console
          </h3>
          <div class="signoff-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 18px;">
            <!-- Signoff 1: Client -->
            <div class="signoff-card" style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; padding: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.04); display: flex; flex-direction: column; justify-content: space-between;">
              <div>
                <div style="font-family: 'Outfit', sans-serif; font-size: 16px; font-weight: 700; color: #0a2540; margin-bottom: 3px;">Popular Auto Spare Co. W.L.L</div>
                <div style="font-size: 12px; color: #64748b; margin-bottom: 14px;">Client Executive Sign-off & Commercial Approval</div>
                <div class="signoff-box-area" id="sig_area_client" style="border: 1.5px dashed #cbd5e1; border-radius: 6px; padding: 14px; text-align: center; min-height: 85px; display: flex; align-items: center; justify-content: center; background: #fafafa; margin-bottom: 12px;">
                  <span style="font-size: 12px; color: #94a3b8;"><i class="fa-solid fa-pen-nib"></i> No Signature on Record</span>
                </div>
                <div style="margin-bottom: 14px;">
                  <span class="signoff-status-badge status-pending" id="badge_client" style="background: #fef3c7; color: #b45309; font-size: 10px; font-weight: 800; padding: 3px 8px; border-radius: 4px; letter-spacing: 0.5px;">PENDING SIGN-OFF</span>
                </div>
              </div>
              <button class="btn btn-primary btn-sign" style="width: 100%; justify-content: center; padding: 10px; background: #0a2540; color: #ffffff; font-weight: 700; border-radius: 6px; border: none; cursor: pointer; display: flex; align-items: center; gap: 6px;" onclick="openSignModal('client', 'Popular Auto Spare Co. W.L.L', 'Authorized Executive Signatory')">
                <i class="fa-solid fa-pen-nib"></i> Sign as Client Executive
              </button>
            </div>

            <!-- Signoff 2: Developer / Architect -->
            <div class="signoff-card" style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; padding: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.04); display: flex; flex-direction: column; justify-content: space-between;">
              <div>
                <div style="font-family: 'Outfit', sans-serif; font-size: 16px; font-weight: 700; color: #0a2540; margin-bottom: 3px;">SaNDS Lab Middle East W.L.L</div>
                <div style="font-size: 12px; color: #64748b; margin-bottom: 14px;">Lead Solutions Architect & Engineering Director</div>
                <div class="signoff-box-area" id="sig_area_architect" style="border: 1.5px dashed #cbd5e1; border-radius: 6px; padding: 14px; text-align: center; min-height: 85px; display: flex; align-items: center; justify-content: center; background: #fafafa; margin-bottom: 12px;">
                  <span style="font-size: 12px; color: #94a3b8;"><i class="fa-solid fa-pen-nib"></i> No Signature on Record</span>
                </div>
                <div style="margin-bottom: 14px;">
                  <span class="signoff-status-badge status-pending" id="badge_architect" style="background: #fef3c7; color: #b45309; font-size: 10px; font-weight: 800; padding: 3px 8px; border-radius: 4px; letter-spacing: 0.5px;">PENDING SIGN-OFF</span>
                </div>
              </div>
              <button class="btn btn-primary btn-sign" style="width: 100%; justify-content: center; padding: 10px; background: #0a2540; color: #ffffff; font-weight: 700; border-radius: 6px; border: none; cursor: pointer; display: flex; align-items: center; gap: 6px;" onclick="openSignModal('architect', 'SaNDS Lab Middle East W.L.L', 'Lead Solutions Architect & Managing Director')">
                <i class="fa-solid fa-pen-nib"></i> Sign as Solutions Architect
              </button>
            </div>

            <!-- Signoff 3: Consultant -->
            <div class="signoff-card" style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; padding: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.04); display: flex; flex-direction: column; justify-content: space-between;">
              <div>
                <div style="font-family: 'Outfit', sans-serif; font-size: 16px; font-weight: 700; color: #0a2540; margin-bottom: 3px;">UniGlobal Consultancy</div>
                <div style="font-size: 12px; color: #64748b; margin-bottom: 14px;">Executive Strategic Advisor & Governance Lead</div>
                <div class="signoff-box-area" id="sig_area_advisor" style="border: 1.5px dashed #cbd5e1; border-radius: 6px; padding: 14px; text-align: center; min-height: 85px; display: flex; align-items: center; justify-content: center; background: #fafafa; margin-bottom: 12px;">
                  <span style="font-size: 12px; color: #94a3b8;"><i class="fa-solid fa-pen-nib"></i> No Signature on Record</span>
                </div>
                <div style="margin-bottom: 14px;">
                  <span class="signoff-status-badge status-pending" id="badge_advisor" style="background: #fef3c7; color: #b45309; font-size: 10px; font-weight: 800; padding: 3px 8px; border-radius: 4px; letter-spacing: 0.5px;">PENDING SIGN-OFF</span>
                </div>
              </div>
              <button class="btn btn-primary btn-sign" style="width: 100%; justify-content: center; padding: 10px; background: #0a2540; color: #ffffff; font-weight: 700; border-radius: 6px; border: none; cursor: pointer; display: flex; align-items: center; gap: 6px;" onclick="openSignModal('advisor', 'UniGlobal Consultancy', 'Executive Strategic Advisor')">
                <i class="fa-solid fa-pen-nib"></i> Sign as Strategic Advisor
              </button>
            </div>
          </div>
        </div>
      </section>"""

def build_signature_modal_and_js(doc_id):
    return f"""  <!-- Unified Signature Capture Modal -->
  <div class="modal-overlay" id="sigModal" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(15, 23, 42, 0.75); backdrop-filter: blur(4px); z-index: 9999; align-items: center; justify-content: center; padding: 16px;">
    <div class="modal-box" style="background: #ffffff; border-radius: 12px; max-width: 540px; width: 100%; padding: 24px; box-shadow: 0 20px 25px -5px rgba(0,0,0,0.2); position: relative;">
      <div class="modal-header" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; border-bottom: 1px solid #e2e8f0; padding-bottom: 12px;">
        <h3 class="modal-title" id="modalSignTitle" style="font-family: 'Outfit', sans-serif; font-size: 17px; font-weight: 700; color: #0a2540; display: flex; align-items: center; gap: 8px;">
          <i class="fa-solid fa-file-signature" style="color: #d97706;"></i> Digital Signature Capture
        </h3>
        <button class="close-modal" onclick="closeSignModal()" style="background: transparent; border: none; font-size: 22px; color: #64748b; cursor: pointer;">&times;</button>
      </div>
      <form id="signForm" onsubmit="handleSignatureSubmit(event)">
        <input type="hidden" id="modal_party" name="party" value="">
        <input type="hidden" id="modal_org" name="org" value="">
        <div class="form-group" style="margin-bottom: 12px;">
          <label style="display: block; font-size: 11.5px; font-weight: 700; color: #334155; margin-bottom: 4px; text-transform: uppercase;">Signatory Full Name</label>
          <input type="text" class="form-control" id="signerName" required placeholder="Enter full name" style="width: 100%; padding: 9px 12px; border: 1px solid #cbd5e1; border-radius: 6px; font-size: 13px;">
        </div>
        <div class="form-group" style="margin-bottom: 12px;">
          <label style="display: block; font-size: 11.5px; font-weight: 700; color: #334155; margin-bottom: 4px; text-transform: uppercase;">Signatory Designation / Role</label>
          <input type="text" class="form-control" id="signerDesignation" required placeholder="e.g. Managing Director" style="width: 100%; padding: 9px 12px; border: 1px solid #cbd5e1; border-radius: 6px; font-size: 13px;">
        </div>
        <div class="form-group" style="margin-bottom: 12px;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
            <label style="font-size: 11.5px; font-weight: 700; color: #334155; text-transform: uppercase;">Draw Signature on Canvas</label>
            <button type="button" onclick="clearSignatureCanvas()" style="background: none; border: none; color: #d97706; font-size: 11px; font-weight: 700; cursor: pointer;">
              <i class="fa-solid fa-eraser"></i> Clear
            </button>
          </div>
          <canvas class="sig-pad-canvas" id="sigCanvas" style="border: 1.5px solid #cbd5e1; border-radius: 6px; background: #f8fafc; width: 100%; height: 150px; cursor: crosshair; touch-action: none;"></canvas>
        </div>
        <div style="display: flex; justify-content: flex-end; gap: 10px; margin-top: 18px;">
          <button type="button" class="btn btn-outline" onclick="closeSignModal()" style="padding: 8px 16px; border: 1px solid #cbd5e1; background: #fff; border-radius: 6px; font-size: 12px; font-weight: 600; cursor: pointer;">Cancel</button>
          <button type="submit" class="btn btn-primary" id="btnSubmitSign" style="padding: 8px 18px; background: #0a2540; color: #fff; border: none; border-radius: 6px; font-size: 12px; font-weight: 700; cursor: pointer;">Confirm & Apply Signature</button>
        </div>
      </form>
    </div>
  </div>

  <!-- Signature Capture & Display Script -->
  <script>
    const currentDocId = '{doc_id}';
    let canvas, ctx, isDrawing = false;

    function initCanvas() {{
      canvas = document.getElementById('sigCanvas');
      if (!canvas) return;
      ctx = canvas.getContext('2d');

      // Adjust canvas resolution
      const rect = canvas.getBoundingClientRect();
      canvas.width = rect.width || 480;
      canvas.height = rect.height || 150;
      ctx.strokeStyle = '#0a2540';
      ctx.lineWidth = 2.5;
      ctx.lineCap = 'round';
      ctx.lineJoin = 'round';

      function getPos(e) {{
        const r = canvas.getBoundingClientRect();
        const clientX = e.touches ? e.touches[0].clientX : e.clientX;
        const clientY = e.touches ? e.touches[0].clientY : e.clientY;
        return {{
          x: (clientX - r.left) * (canvas.width / r.width),
          y: (clientY - r.top) * (canvas.height / r.height)
        }};
      }}

      function startDraw(e) {{
        isDrawing = true;
        const pos = getPos(e);
        ctx.beginPath();
        ctx.moveTo(pos.x, pos.y);
        e.preventDefault();
      }}

      function draw(e) {{
        if (!isDrawing) return;
        const pos = getPos(e);
        ctx.lineTo(pos.x, pos.y);
        ctx.stroke();
        e.preventDefault();
      }}

      function stopDraw() {{
        isDrawing = false;
      }}

      canvas.addEventListener('mousedown', startDraw);
      canvas.addEventListener('mousemove', draw);
      window.addEventListener('mouseup', stopDraw);

      canvas.addEventListener('touchstart', startDraw, {{ passive: false }});
      canvas.addEventListener('touchmove', draw, {{ passive: false }});
      window.addEventListener('touchend', stopDraw);
    }}

    function clearSignatureCanvas() {{
      if (ctx && canvas) {{
        ctx.clearRect(0, 0, canvas.width, canvas.height);
      }}
    }}

    function openSignModal(party, org, defaultRole) {{
      const modal = document.getElementById('sigModal');
      if (!modal) return;
      modal.style.display = 'flex';

      document.getElementById('modal_party').value = party;
      document.getElementById('modal_org').value = org;
      document.getElementById('modalSignTitle').innerHTML = '<i class="fa-solid fa-file-signature" style="color: #d97706;"></i> Sign as ' + org;
      document.getElementById('signerDesignation').value = defaultRole || '';

      setTimeout(() => {{
        initCanvas();
        clearSignatureCanvas();
      }}, 50);
    }}

    function closeSignModal() {{
      const modal = document.getElementById('sigModal');
      if (modal) modal.style.display = 'none';
    }}

    function handleSignatureSubmit(e) {{
      e.preventDefault();
      const party = document.getElementById('modal_party').value;
      const org = document.getElementById('modal_org').value;
      const name = document.getElementById('signerName').value.trim();
      const role = document.getElementById('signerDesignation').value.trim();

      if (!name || !role) {{
        alert('Please provide both Name and Role.');
        return;
      }}

      const dataUrl = canvas.toDataURL('image/png');
      const sigRecord = {{
        party: party,
        org: org,
        name: name,
        role: role,
        data: dataUrl,
        date: new Date().toLocaleDateString('en-GB', {{ day: '2-digit', month: 'short', year: 'numeric' }}),
        time: new Date().toLocaleTimeString()
      }};

      localStorage.setItem('sig_' + currentDocId + '_' + party, JSON.stringify(sigRecord));
      applySignatureToUI(party, sigRecord);
      closeSignModal();

      if (typeof Swal !== 'undefined') {{
        Swal.fire({{
          icon: 'success',
          title: 'Signature Recorded & Ratified',
          text: 'Document signed officially by ' + name + ' (' + org + ')',
          confirmButtonColor: '#0a2540'
        }});
      }} else {{
        alert('Signature successfully recorded for ' + org);
      }}
    }}

    function applySignatureToUI(party, rec) {{
      const area = document.getElementById('sig_area_' + party);
      const badge = document.getElementById('badge_' + party);

      if (area) {{
        area.innerHTML = '<div style="text-align:center;">' +
          '<img src="' + rec.data + '" style="max-height: 48px; max-width: 160px; object-fit: contain; margin-bottom: 4px;" alt="Signature">' +
          '<div style="font-size: 11px; font-weight: 700; color: #0a2540;">' + rec.name + '</div>' +
          '<div style="font-size: 9.5px; color: #64748b;">' + rec.role + ' &bull; ' + rec.date + '</div>' +
          '</div>';
      }}

      if (badge) {{
        badge.className = 'signoff-status-badge status-signed';
        badge.style.background = '#dcfce7';
        badge.style.color = '#15803d';
        badge.style.border = '1px solid #bbf7d0';
        badge.innerHTML = '<i class="fas fa-check-double"></i> SIGNED & RATIFIED';
      }}

      // Also update Block 1 review badges if matching
      if (party === 'client') {{
        const bRev = document.getElementById('badge_client_review');
        const sRev = document.getElementById('sig_badge_client_review');
        if (bRev) {{
          bRev.className = 'signoff-status-badge status-signed';
          bRev.style.background = '#dcfce7';
          bRev.style.color = '#15803d';
          bRev.innerHTML = 'APPROVED & SIGNED';
        }}
        if (sRev) {{
          sRev.innerHTML = '<span class="badge-tag badge-success" style="background:#dcfce7; color:#15803d; padding:3px 8px; border-radius:4px; font-size:10.5px; font-weight:700;"><i class="fas fa-check"></i> ' + rec.name + ' (' + rec.date + ')</span>';
        }}
      }} else if (party === 'advisor' || party === 'consultant') {{
        const bRev = document.getElementById('badge_consultant_review');
        const sRev = document.getElementById('sig_badge_consultant_review');
        if (bRev) {{
          bRev.className = 'signoff-status-badge status-signed';
          bRev.style.background = '#dcfce7';
          bRev.style.color = '#15803d';
          bRev.innerHTML = 'REVIEWED & VERIFIED';
        }}
        if (sRev) {{
          sRev.innerHTML = '<span class="badge-tag badge-success" style="background:#dcfce7; color:#15803d; padding:3px 8px; border-radius:4px; font-size:10.5px; font-weight:700;"><i class="fas fa-check"></i> ' + rec.name + ' (' + rec.date + ')</span>';
        }}
      }}
    }}

    function loadSavedSignatures() {{
      ['client', 'architect', 'advisor', 'consultant'].forEach(p => {{
        const saved = localStorage.getItem('sig_' + currentDocId + '_' + p);
        if (saved) {{
          try {{
            const rec = JSON.parse(saved);
            applySignatureToUI(p, rec);
          }} catch(e) {{}}
        }}
      }});
    }}

    document.addEventListener('DOMContentLoaded', () => {{
      loadSavedSignatures();
    }});
  </script>
"""

modules_meta = {
    'SL-POP-ERP-MS-001': ('Module 1: PCode Generation & Item Master Engine', '10-September-2026', '21-September-2026'),
    'SL-POP-ERP-MS-002': ('Module 2: Vendor & Purchase Management', '15-September-2026', '27-September-2026'),
    'SL-POP-ERP-MS-003': ('Module 3: Store Verification & Stock Control', '18-September-2026', '27-September-2026'),
    'SL-POP-ERP-MS-004': ('Module 4: Sales Process, POS & Billing', '20-March-2026', '30-March-2026'),
    'SL-POP-ERP-MS-005': ('Module 5: Accounting, GL, AP/AR & VAT', '15-June-2026', '04-July-2026'),
    'SL-POP-ERP-MS-006': ('Module 6: Enterprise Administration & Fleet', '20-June-2026', '06-July-2026'),
    'SL-POP-ERP-MS-007': ('Module 7: Human Resource Management & Payroll', '22-June-2026', '04-July-2026'),
    'SL-POP-ERP-MS-008': ('Module 8: Hardware, QR Scanner & Cloud Setup', '24-September-2026', '30-September-2026'),
    'SL-POP-ERP-MS-009': ('Module 9: Executive Management Dashboard & BI', '25-September-2026', '30-September-2026'),
    'SL-POP-ERP-SUMMARY-001': ('Master 9-Module ERP Milestone & Budget Roadmap', '25-September-2026', '30-September-2026')
}

aliases_map = {
    'PCode_Milestone_and_Payment_Structure.html': 'SL-POP-ERP-MS-001',
    'Vendor_Purchase_Milestone_and_Payment_Structure.html': 'SL-POP-ERP-MS-002',
    'Store_Verification_Milestone_and_Payment_Structure.html': 'SL-POP-ERP-MS-003',
    'Sales_Process_Milestone_and_Payment_Structure.html': 'SL-POP-ERP-MS-004',
    'Accounts_Milestone_and_Payment_Structure.html': 'SL-POP-ERP-MS-005',
    'Administration_Milestone_and_Payment_Structure.html': 'SL-POP-ERP-MS-006',
    'Human_Resource_Management_Milestone_and_Payment_Structure.html': 'SL-POP-ERP-MS-007',
    'Hardware_and_Server_Setup_Milestone_and_Payment_Structure.html': 'SL-POP-ERP-MS-008',
    'Executive_Master_Summary_and_Budget_Milestone.html': 'SL-POP-ERP-SUMMARY-001'
}

all_files = glob.glob('SL-POP-ERP-MS-*.html') + glob.glob('*_Milestone_and_Payment_Structure.html') + ['SL-POP-ERP-SUMMARY-001.html', 'Executive_Master_Summary_and_Budget_Milestone.html']
all_files += [os.path.join('popular', f) for f in all_files]

for fpath in set(all_files):
    if not os.path.exists(fpath):
        continue
    
    fname = os.path.basename(fpath)
    doc_id = None
    if fname.startswith('SL-POP-ERP-'):
        doc_id = fname.replace('.html', '')
    elif fname in aliases_map:
        doc_id = aliases_map[fname]
    
    if not doc_id or doc_id not in modules_meta:
        continue
    
    doc_title, prep_date, verif_date = modules_meta[doc_id]
    
    content = open(fpath, encoding='utf-8').read()
    
    # 1. Replace the existing signoff section
    new_signoff = build_signoff_section(doc_id, doc_title, prep_date, verif_date)
    
    # Pattern to match from either <section class="doc-section" id="digital-signoff"> or <section class="signoff-section" id="sec-signoff"> or similar
    pattern_signoff = r'<section\s+class=\"[^\"]*signoff[^\"]*\"[^>]*>.*?</section>'
    if not re.search(pattern_signoff, content, flags=re.DOTALL):
        pattern_signoff = r'<section\s+class=\"doc-section\"\s+id=\"digital-signoff\">.*?</section>'
    if not re.search(pattern_signoff, content, flags=re.DOTALL):
        pattern_signoff = r'<section\s+class=\"doc-section\"\s+id=\"stakeholder-signoff\">.*?</section>'
        
    if re.search(pattern_signoff, content, flags=re.DOTALL):
        content = re.sub(pattern_signoff, new_signoff, content, count=1, flags=re.DOTALL)
    else:
        print(f"Signoff section pattern not found directly in {fpath}, checking alternative anchor...")
        # fallback before </main>
        if '</main>' in content:
            content = content.replace('</main>', new_signoff + '\n    </main>')
    
    # 2. Replace the signature modal & script
    new_modal_js = build_signature_modal_and_js(doc_id)
    
    # Remove old modal if present
    content = re.sub(r'<!-- Signature Modal -->.*?</div>\s*</div>\s*(?=<script>|\s*<footer|\s*</body>)', '', content, flags=re.DOTALL)
    content = re.sub(r'<div class=\"modal-overlay\" id=\"(sigModal|signModal)\">.*?</div>\s*</div>', '', content, flags=re.DOTALL)
    
    # Remove old signature scripts if present
    content = re.sub(r'<script>\s*// Universal High-Precision Scroll Spy.*?loadSavedSignatures\(\);.*?\}\);?\s*</script>', '', content, flags=re.DOTALL)
    
    # Inject new modal and JS before </body>
    if '</body>' in content:
        # Check if scrollspy script is needed
        scrollspy_script = """  <script>
    // Universal High-Precision Scroll Spy for Navigation
    function initScrollSpy() {
      const navLinks = document.querySelectorAll('.sidebar-menu li a, .sidebar-menu a');
      if (!navLinks || navLinks.length === 0) return;

      const targetSections = [];
      navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href && href.startsWith('#') && href.length > 1) {
          try {
            const targetEl = document.querySelector(href);
            if (targetEl) {
              targetSections.push({ link: link, el: targetEl });
            }
          } catch(e) {}
        }
      });

      if (targetSections.length === 0) return;

      function onScroll() {
        const scrollY = window.pageYOffset || document.documentElement.scrollTop || window.scrollY || 0;
        let activeLink = null;

        for (let i = 0; i < targetSections.length; i++) {
          const item = targetSections[i];
          const rect = item.el.getBoundingClientRect();
          const topOffset = rect.top + scrollY;
          if (scrollY >= topOffset - 180) {
            activeLink = item.link;
          }
        }

        if (!activeLink && targetSections.length > 0) {
          activeLink = targetSections[0].link;
        }

        if ((window.innerHeight + scrollY) >= (document.documentElement.scrollHeight - 60) && targetSections.length > 0) {
          activeLink = targetSections[targetSections.length - 1].link;
        }

        navLinks.forEach(l => l.classList.remove('active'));
        if (activeLink) {
          activeLink.classList.add('active');
        }
      }

      window.addEventListener('scroll', onScroll, { passive: true });
      window.addEventListener('resize', onScroll, { passive: true });
      setTimeout(onScroll, 100);
      onScroll();
    }

    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', initScrollSpy);
    } else {
      initScrollSpy();
    }
  </script>"""
        
        # Replace </body> with modal + js + scrollspy + </body>
        idx_body = content.rfind('</body>')
        content = content[:idx_body] + new_modal_js + '\n' + scrollspy_script + '\n' + content[idx_body:]
    
    with open(fpath, 'w', encoding='utf-8') as out:
        out.write(content)
    print(f"Updated standardized dual sign-off in {fpath}")

print("All documents updated with standardized dual sign-off console successfully!")
