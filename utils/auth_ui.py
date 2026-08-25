import streamlit as st
import os
import time
from utils.auth import (
    init_auth,
    is_authenticated,
    login_user,
    login_demo_user,
    signup_user,
    reset_password,
    ALLOWED_SIGNUP_ROLES,
    CARGOVISION_LOCATIONS
)
from utils.supabase_client import is_supabase_configured

def render_auth_page():
    """
    Renders the balanced, enterprise-grade CargoVision Login / Signup authentication page.
    Centered in the middle of the screen with matching frosted-glass container cards.
    """
    init_auth()

    # Load custom CSS
    css_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'styles.css')
    if os.path.exists(css_file):
        with open(css_file) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    auth_mode = st.session_state.get("auth_mode", "login")

    # Center the authentication card horizontally and vertically in the middle of the screen
    st.markdown('<div style="height: 30px;"></div>', unsafe_allow_html=True)
    _, center_col, _ = st.columns([0.14, 0.72, 0.14])

    with center_col:
        col_left, col_right = st.columns([0.9, 1.1], gap="large")

        # ==========================================
        # LEFT COLUMN: Branding + Logistics Card
        # ==========================================
        with col_left:
            left_content_html = """<div>
<!-- Brand Header -->
<div style="margin-bottom: 20px;">
<div style="display: flex; align-items: center; gap: 10px; margin-bottom: 6px;">
<div style="width: 38px; height: 38px; background: linear-gradient(135deg, #0ea5e9, #0284c7); border-radius: 10px; display: flex; align-items: center; justify-content: center; color: white; font-weight: 800; font-size: 1.1rem; box-shadow: 0 4px 14px rgba(14, 165, 233, 0.4);">CV</div>
<span style="font-size: 1.75rem; font-weight: 800; letter-spacing: -0.5px; color: #ffffff;">CargoVision</span>
</div>
<div style="color: #38bdf8; font-size: 0.8rem; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 4px;">
PREDICT. PREVENT. DELIVER.
</div>
<p style="color: #94a3b8; font-size: 0.88rem; margin: 0; line-height: 1.4;">
Enterprise Logistics Intelligence & Multi-Tier Control Tower
</p>
</div>

<!-- Logistics Visualization Card -->
<div class="tower-panel" style="padding: 20px;">
<div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px; border-bottom: 1px solid rgba(255,255,255,0.06); padding-bottom: 10px;">
<div style="display: flex; align-items: center; gap: 8px;">
<span style="display: inline-block; width: 8px; height: 8px; background: #22c55e; border-radius: 50%; box-shadow: 0 0 8px #22c55e;"></span>
<span style="color: #f8fafc; font-size: 0.78rem; font-weight: 600; letter-spacing: 0.5px;">LOGISTICS ACCESS GATE</span>
</div>
<span style="background: rgba(14, 165, 233, 0.15); color: #38bdf8; border: 1px solid rgba(14, 165, 233, 0.3); padding: 3px 10px; border-radius: 12px; font-size: 0.72rem; font-weight: 700;">LOCATION RBAC</span>
</div>

<!-- Route Nodes Pipeline -->
<div style="margin-bottom: 14px; background: rgba(15, 23, 42, 0.6); border-radius: 12px; padding: 12px; border: 1px solid rgba(255,255,255,0.04);">
<div style="color: #94a3b8; font-size: 0.7rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 8px;">NETWORK HUBS</div>
<div style="display: flex; align-items: center; justify-content: space-between; position: relative;">
<div style="text-align: center;">
<div style="width: 26px; height: 26px; background: rgba(34, 197, 94, 0.15); border: 1px solid #22c55e; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 3px; font-size: 0.7rem;">🏢</div>
<div style="color: #f8fafc; font-size: 0.72rem; font-weight: 600;">Mumbai Hub</div>
</div>
<div style="flex: 1; height: 2px; background: linear-gradient(90deg, #22c55e, #38bdf8); margin: 0 6px;"></div>
<div style="text-align: center;">
<div style="width: 26px; height: 26px; background: rgba(14, 165, 233, 0.15); border: 1px solid #0ea5e9; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 3px; font-size: 0.7rem;">🏭</div>
<div style="color: #f8fafc; font-size: 0.72rem; font-weight: 600;">Pune DC</div>
</div>
<div style="flex: 1; height: 2px; background: linear-gradient(90deg, #38bdf8, #f59e0b); margin: 0 6px;"></div>
<div style="text-align: center;">
<div style="width: 26px; height: 26px; background: rgba(245, 158, 11, 0.15); border: 1px solid #f59e0b; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 3px; font-size: 0.7rem;">🛣️</div>
<div style="color: #f8fafc; font-size: 0.72rem; font-weight: 600;">Gurgaon Toll</div>
</div>
</div>
</div>

<!-- Compact Stats Grid -->
<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-bottom: 14px;">
<div style="background: rgba(15, 23, 42, 0.5); padding: 10px 12px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.04);">
<div style="color: #94a3b8; font-size: 0.68rem; font-weight: 600; text-transform: uppercase;">Active Fleet</div>
<div style="color: #ffffff; font-size: 1.15rem; font-weight: 800;">8,341</div>
<div style="color: #22c55e; font-size: 0.68rem; font-weight: 600;">Live GPS Ingestion</div>
</div>
<div style="background: rgba(15, 23, 42, 0.5); padding: 10px 12px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.04);">
<div style="color: #94a3b8; font-size: 0.68rem; font-weight: 600; text-transform: uppercase;">Audit Reliability</div>
<div style="color: #ffffff; font-size: 1.15rem; font-weight: 800;">100%</div>
<div style="color: #38bdf8; font-size: 0.68rem; font-weight: 600;">Location Verification</div>
</div>
</div>

<div style="display: flex; gap: 8px; justify-content: space-around; color: #94a3b8; font-size: 0.72rem; font-weight: 600;">
<div>📦 Shipment Audits</div>
<div>🏢 Hub Access</div>
<div>⚡ Real-Time Logging</div>
</div>
</div>
</div>"""
            st.markdown(left_content_html, unsafe_allow_html=True)

        # ==========================================
        # RIGHT COLUMN: Authentication Container Card
        # ==========================================
        with col_right:
            # ------------------------------------------
            # AUTHENTICATION MODE SWITCHER PILL BAR
            # ------------------------------------------
            auth_mode_curr = st.session_state.get("auth_mode", "login")
            
            st.markdown(f"""
<div style="display: flex; background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 4px; margin-bottom: 20px;">
<div style="flex: 1; text-align: center;">
<a href="#" onclick="return false;" style="display: block; padding: 8px 12px; border-radius: 8px; font-weight: 700; font-size: 0.84rem; text-decoration: none; color: {'#ffffff' if auth_mode_curr=='login' else '#94a3b8'}; background: {'linear-gradient(135deg, rgba(14,165,233,0.3), rgba(2,132,199,0.3))' if auth_mode_curr=='login' else 'transparent'}; border: {'1px solid rgba(14,165,233,0.4)' if auth_mode_curr=='login' else 'none'};">
🔑 Sign In
</a>
</div>
<div style="flex: 1; text-align: center;">
<a href="#" onclick="return false;" style="display: block; padding: 8px 12px; border-radius: 8px; font-weight: 700; font-size: 0.84rem; text-decoration: none; color: {'#ffffff' if auth_mode_curr=='signup' else '#94a3b8'}; background: {'linear-gradient(135deg, rgba(34,197,94,0.3), rgba(16,185,129,0.3))' if auth_mode_curr=='signup' else 'transparent'}; border: {'1px solid rgba(34,197,94,0.4)' if auth_mode_curr=='signup' else 'none'};">
📝 Staff Registration
</a>
</div>
<div style="flex: 1; text-align: center;">
<a href="#" onclick="return false;" style="display: block; padding: 8px 12px; border-radius: 8px; font-weight: 700; font-size: 0.84rem; text-decoration: none; color: {'#ffffff' if auth_mode_curr=='forgot' else '#94a3b8'}; background: {'linear-gradient(135deg, rgba(245,158,11,0.3), rgba(217,119,6,0.3))' if auth_mode_curr=='forgot' else 'transparent'}; border: {'1px solid rgba(245,158,11,0.4)' if auth_mode_curr=='forgot' else 'none'};">
🛡️ Reset Access
</a>
</div>
</div>
""", unsafe_allow_html=True)

            btn_sw1, btn_sw2, btn_sw3 = st.columns(3)
            with btn_sw1:
                if st.button("🔑 Sign In", key="pill_mode_login", use_container_width=True, type="primary" if auth_mode_curr=="login" else "secondary"):
                    st.session_state["auth_mode"] = "login"
                    st.rerun()
            with btn_sw2:
                if st.button("📝 Sign Up", key="pill_mode_signup", use_container_width=True, type="primary" if auth_mode_curr=="signup" else "secondary"):
                    st.session_state["auth_mode"] = "signup"
                    st.rerun()
            with btn_sw3:
                if st.button("🛡️ Password Reset", key="pill_mode_forgot", use_container_width=True, type="primary" if auth_mode_curr=="forgot" else "secondary"):
                    st.session_state["auth_mode"] = "forgot"
                    st.rerun()

            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

            # Quick Demo Buttons (When local / demo mode or quick testing is useful)
            if not is_supabase_configured():
                st.info("💡 **Local / Demo Mode**: Click below to quickly test role and location authorization without manual signup:")
                demo_c1, demo_c2 = st.columns(2)
                with demo_c1:
                    if st.button("🏭 Warehouse Staff (Pune DC)", key="btn_demo_staff", type="primary", use_container_width=True):
                        login_demo_user(name="Rahul Sharma", role="Warehouse Staff", assigned_location="Pune DC")
                        st.success("✅ Logged in as Rahul (Warehouse Staff • Pune DC)!")
                        time.sleep(0.4)
                        st.rerun()
                with demo_c2:
                    if st.button("👑 Operations Manager", key="btn_demo_mgr", type="secondary", use_container_width=True):
                        login_demo_user(name="Isha Rode", role="Operations Manager", assigned_location="All Hubs")
                        st.success("✅ Logged in as Operations Manager (All Locations)!")
                        time.sleep(0.4)
                        st.rerun()
                st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

            # ------------------------------------------
            # LOGIN VIEW
            # ------------------------------------------
            if auth_mode == "login":
                with st.form("login_form", clear_on_submit=False):
                    st.markdown("""<div style="margin-bottom: 16px;">
<div style="color: #ffffff; font-size: 1.5rem; font-weight: 800; margin: 0 0 4px 0; letter-spacing: -0.5px;">Welcome Back</div>
<div style="color: #94a3b8; font-size: 0.88rem; margin: 0;">Sign in to load your assigned role, location profile, and operational tasks.</div>
</div>""", unsafe_allow_html=True)

                    email_input = st.text_input("Email", placeholder="name@company.com", key="login_email")
                    pass_input = st.text_input("Password", type="password", placeholder="••••••••", key="login_pass")
                    submit_login = st.form_submit_button("Sign In with Supabase", use_container_width=True, type="primary")

                    if submit_login:
                        with st.spinner("Authenticating with Supabase..."):
                            success, msg = login_user(email_input, pass_input)
                        if success:
                            st.success(f"✅ {msg}")
                            time.sleep(0.4)
                            try:
                                st.switch_page("pages/dashboard.py")
                            except Exception:
                                st.rerun()
                        else:
                            st.error(f"❌ {msg}")

                if is_supabase_configured():
                    if st.button("Forgot password?", key="btn_to_forgot", use_container_width=True):
                        st.session_state["auth_mode"] = "forgot"
                        st.rerun()

                st.markdown("<hr style='border: none; border-top: 1px solid rgba(255,255,255,0.08); margin: 12px 0 10px;'>", unsafe_allow_html=True)
                
                st.markdown("<div style='text-align: center; color: #94a3b8; font-size: 0.86rem; margin-bottom: 6px;'>Need an operational account?</div>", unsafe_allow_html=True)
                if st.button("Create Staff Account", key="btn_to_signup", use_container_width=True):
                    st.session_state["auth_mode"] = "signup"
                    st.rerun()

            # ------------------------------------------
            # SIGNUP VIEW
            # ------------------------------------------
            elif auth_mode == "signup":
                with st.form("signup_form", clear_on_submit=False):
                    st.markdown("""<div style="margin-bottom: 16px;">
<div style="color: #ffffff; font-size: 1.5rem; font-weight: 800; margin: 0 0 4px 0; letter-spacing: -0.5px;">Create Staff Account</div>
<div style="color: #94a3b8; font-size: 0.86rem; margin: 0 0 14px 0;">Register your operational profile with assigned location authorization.</div>

<!-- Registration Progress Steps Bar -->
<div style="display: flex; align-items: center; justify-content: space-between; background: rgba(15,23,42,0.6); padding: 8px 12px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.05); margin-bottom: 16px;">
<div style="display: flex; align-items: center; gap: 6px; font-size: 0.75rem; font-weight: 700; color: #38bdf8;">
<span style="width: 18px; height: 18px; background: #0ea5e9; color: white; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; font-size: 0.65rem;">1</span> Profile
</div>
<div style="width: 20px; height: 1px; background: rgba(255,255,255,0.2);"></div>
<div style="display: flex; align-items: center; gap: 6px; font-size: 0.75rem; font-weight: 700; color: #4ade80;">
<span style="width: 18px; height: 18px; background: #22c55e; color: white; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; font-size: 0.65rem;">2</span> Location
</div>
<div style="width: 20px; height: 1px; background: rgba(255,255,255,0.2);"></div>
<div style="display: flex; align-items: center; gap: 6px; font-size: 0.75rem; font-weight: 700; color: #fbbf24;">
<span style="width: 18px; height: 18px; background: #f59e0b; color: white; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; font-size: 0.65rem;">3</span> Security
</div>
</div>
</div>""", unsafe_allow_html=True)

                    su_name = st.text_input("Full Name *", placeholder="e.g. Rahul Sharma", key="su_name")
                    su_email = st.text_input("Work Email *", placeholder="rahul.s@cargovision.io", key="su_email")
                    su_company = st.text_input("Company *", placeholder="e.g. CargoVision Enterprise", key="su_comp")
                    
                    col_p1, col_p2 = st.columns(2)
                    with col_p1:
                        su_pass = st.text_input("Password *", type="password", placeholder="Min 6 characters", key="su_pass")
                    with col_p2:
                        su_confirm = st.text_input("Confirm Password *", type="password", placeholder="Re-enter password", key="su_confirm")

                    col_r1, col_r2 = st.columns(2)
                    with col_r1:
                        # Only allowed roles for public registration
                        su_role = st.selectbox(
                            "Role *",
                            options=ALLOWED_SIGNUP_ROLES,
                            index=0,
                            key="su_role",
                            help="Select your operational role. Admin and Operations Manager roles are provisioned by organization administrators."
                        )
                    with col_r2:
                        # Existing CargoVision hub locations
                        su_assigned_loc = st.selectbox(
                            "Assigned Location *",
                            options=CARGOVISION_LOCATIONS,
                            index=0,
                            key="su_assigned_loc",
                            help="You will be authorized to record operational events and updates at this location."
                        )

                    st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)
                    submit_signup = st.form_submit_button("Register Account & Profile", use_container_width=True, type="primary")

                    if submit_signup:
                        with st.spinner("Creating profile in Supabase..."):
                            success, msg = signup_user(
                                name=su_name,
                                email=su_email,
                                password=su_pass,
                                confirm_password=su_confirm,
                                company=su_company,
                                role=su_role,
                                assigned_location=su_assigned_loc
                            )
                        if success:
                            st.success(f"🎉 {msg}")
                            time.sleep(0.5)
                            if is_authenticated():
                                try:
                                    st.switch_page("app.py")
                                except Exception:
                                    st.rerun()
                            else:
                                st.session_state["auth_mode"] = "login"
                                st.rerun()
                        else:
                            st.error(f"❌ {msg}")

                st.markdown("<hr style='border: none; border-top: 1px solid rgba(255,255,255,0.08); margin: 12px 0 10px;'>", unsafe_allow_html=True)
                
                st.markdown("<div style='text-align: center; color: #94a3b8; font-size: 0.86rem; margin-bottom: 6px;'>Already registered?</div>", unsafe_allow_html=True)
                if st.button("← Back to Sign In", key="btn_back_to_login", use_container_width=True):
                    st.session_state["auth_mode"] = "login"
                    st.rerun()

            # ------------------------------------------
            # FORGOT PASSWORD VIEW
            # ------------------------------------------
            elif auth_mode == "forgot":
                with st.form("forgot_form"):
                    st.markdown("""<div style="margin-bottom: 16px;">
<div style="color: #ffffff; font-size: 1.5rem; font-weight: 800; margin: 0 0 4px 0; letter-spacing: -0.5px;">Reset Password</div>
<div style="color: #94a3b8; font-size: 0.86rem; margin: 0;">Enter your registered work email to receive reset instructions.</div>
</div>""", unsafe_allow_html=True)

                    forgot_email = st.text_input("Registered Email", placeholder="name@company.com", key="forgot_email")
                    submit_forgot = st.form_submit_button("Send Reset Instructions →", use_container_width=True, type="primary")

                    if submit_forgot:
                        with st.spinner("Sending password reset instructions..."):
                            success, msg = reset_password(forgot_email)
                        if success:
                            st.success(f"📧 {msg}")
                        else:
                            st.error(f"❌ {msg}")

                st.markdown("<hr style='border: none; border-top: 1px solid rgba(255,255,255,0.08); margin: 12px 0 10px;'>", unsafe_allow_html=True)
                if st.button("← Back to Sign In", key="btn_forgot_back_login", use_container_width=True):
                    st.session_state["auth_mode"] = "login"
                    st.rerun()
