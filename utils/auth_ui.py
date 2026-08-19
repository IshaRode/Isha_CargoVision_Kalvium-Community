import streamlit as st
import os
import time
from utils.auth import (
    init_auth,
    is_authenticated,
    login_user,
    signup_user,
    reset_password
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
    st.markdown('<div style="height: 40px;"></div>', unsafe_allow_html=True)
    _, center_col, _ = st.columns([0.16, 0.68, 0.16])

    with center_col:
        col_left, col_right = st.columns([1, 1], gap="large")

        # ==========================================
        # LEFT COLUMN: Branding + Logistics Card
        # ==========================================
        with col_left:
            left_content_html = """<div>
<!-- Brand Header -->
<div style="margin-bottom: 20px;">
<div style="display: flex; align-items: center; gap: 10px; margin-bottom: 6px;">
<div style="width: 36px; height: 36px; background: linear-gradient(135deg, #0ea5e9, #0284c7); border-radius: 10px; display: flex; align-items: center; justify-content: center; color: white; font-weight: 800; font-size: 1.05rem; box-shadow: 0 4px 14px rgba(14, 165, 233, 0.4);">CV</div>
<span style="font-size: 1.7rem; font-weight: 800; letter-spacing: -0.5px; color: #ffffff;">CargoVision</span>
</div>
<div style="color: #38bdf8; font-size: 0.82rem; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 4px;">
PREDICT. PREVENT. DELIVER.
</div>
<p style="color: #94a3b8; font-size: 0.9rem; margin: 0; line-height: 1.4;">
Enterprise Logistics Intelligence Platform
</p>
</div>

<!-- Logistics Visualization Card -->
<div class="auth-card">
<div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px; border-bottom: 1px solid rgba(255,255,255,0.06); padding-bottom: 10px;">
<div style="display: flex; align-items: center; gap: 8px;">
<span style="display: inline-block; width: 8px; height: 8px; background: #22c55e; border-radius: 50%; box-shadow: 0 0 8px #22c55e;"></span>
<span style="color: #f8fafc; font-size: 0.8rem; font-weight: 600; letter-spacing: 0.5px;">LOGISTICS NETWORK: ONLINE</span>
</div>
<span style="background: rgba(14, 165, 233, 0.15); color: #38bdf8; border: 1px solid rgba(14, 165, 233, 0.3); padding: 3px 10px; border-radius: 12px; font-size: 0.72rem; font-weight: 700;">AI SHIELD ACTIVE</span>
</div>

<!-- Route Nodes Pipeline -->
<div style="margin-bottom: 16px; background: rgba(15, 23, 42, 0.6); border-radius: 14px; padding: 14px; border: 1px solid rgba(255,255,255,0.04);">
<div style="color: #94a3b8; font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px;">⚡ LIVE LOGISTICS NETWORK</div>
<div style="display: flex; align-items: center; justify-content: space-between; position: relative;">
<div style="text-align: center;">
<div style="width: 28px; height: 28px; background: rgba(34, 197, 94, 0.15); border: 1px solid #22c55e; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 4px; font-size: 0.75rem;">📦</div>
<div style="color: #f8fafc; font-size: 0.74rem; font-weight: 600;">Mumbai DC</div>
<div style="color: #22c55e; font-size: 0.68rem; font-weight: 600;">Healthy</div>
</div>
<div style="flex: 1; height: 2px; background: linear-gradient(90deg, #22c55e, #f59e0b); margin: 0 6px; position: relative;">
<div style="position: absolute; top: -9px; left: 40%; font-size: 0.7rem;">🚚</div>
</div>
<div style="text-align: center;">
<div style="width: 28px; height: 28px; background: rgba(245, 158, 11, 0.15); border: 1px solid #f59e0b; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 4px; font-size: 0.75rem;">🏭</div>
<div style="color: #f8fafc; font-size: 0.74rem; font-weight: 600;">Pune Hub</div>
<div style="color: #f59e0b; font-size: 0.68rem; font-weight: 600;">High Capacity</div>
</div>
<div style="flex: 1; height: 2px; background: linear-gradient(90deg, #f59e0b, #0ea5e9); margin: 0 6px; position: relative;">
<div style="position: absolute; top: -9px; left: 40%; font-size: 0.7rem;">⚡</div>
</div>
<div style="text-align: center;">
<div style="width: 28px; height: 28px; background: rgba(14, 165, 233, 0.15); border: 1px solid #0ea5e9; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 4px; font-size: 0.75rem;">🎯</div>
<div style="color: #f8fafc; font-size: 0.74rem; font-weight: 600;">Delhi Port</div>
<div style="color: #38bdf8; font-size: 0.68rem; font-weight: 600;">On Time</div>
</div>
</div>
</div>

<!-- Compact Stats Grid -->
<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 14px;">
<div style="background: rgba(15, 23, 42, 0.5); padding: 10px 12px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.04);">
<div style="color: #94a3b8; font-size: 0.7rem;">Tracked Deliveries</div>
<div style="color: #ffffff; font-size: 1.2rem; font-weight: 800;">8,341</div>
<div style="color: #22c55e; font-size: 0.68rem; font-weight: 600;">↑ Live Operational Feeds</div>
</div>
<div style="background: rgba(15, 23, 42, 0.5); padding: 10px 12px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.04);">
<div style="color: #94a3b8; font-size: 0.7rem;">SLA Reliability</div>
<div style="color: #ffffff; font-size: 1.2rem; font-weight: 800;">96.7%</div>
<div style="color: #38bdf8; font-size: 0.68rem; font-weight: 600;">AI Delay Mitigation</div>
</div>
</div>

<!-- Core Capabilities Footer -->
<div style="display: flex; gap: 8px; justify-content: space-around; color: #94a3b8; font-size: 0.72rem; font-weight: 600;">
<div>📦 Visibility</div>
<div>🛣️ Route AI</div>
<div>🧠 Delay Forecasts</div>
</div>
</div>
</div>"""
            if hasattr(st, "html"):
                st.html(left_content_html)
            else:
                st.markdown(left_content_html, unsafe_allow_html=True)

        # ==========================================
        # RIGHT COLUMN: Authentication Container Card
        # ==========================================
        with col_right:
            if not is_supabase_configured():
                st.warning("⚠️ **Supabase Setup**: Please set `SUPABASE_URL` and `SUPABASE_KEY` in `.env`.")

            # ------------------------------------------
            # LOGIN VIEW
            # ------------------------------------------
            if auth_mode == "login":
                with st.form("login_form", clear_on_submit=False):
                    login_header_html = """<div style="margin-bottom: 18px;">
<div style="color: #ffffff; font-size: 1.6rem; font-weight: 800; margin: 0 0 4px 0; letter-spacing: -0.5px;">Welcome back</div>
<div style="color: #94a3b8; font-size: 0.9rem; margin: 0;">Sign in to your CargoVision account.</div>
</div>"""
                    if hasattr(st, "html"):
                        st.html(login_header_html)
                    else:
                        st.markdown(login_header_html, unsafe_allow_html=True)

                    email_input = st.text_input("Email", placeholder="name@company.com", key="login_email")
                    pass_input = st.text_input("Password", type="password", placeholder="••••••••", key="login_pass")
                    submit_login = st.form_submit_button("Login", use_container_width=True, type="primary")

                    if submit_login:
                        with st.spinner("Authenticating..."):
                            success, msg = login_user(email_input, pass_input)
                        if success:
                            st.success("✅ Login successful! Redirecting to Home...")
                            time.sleep(0.5)
                            try:
                                st.switch_page("app.py")
                            except Exception:
                                st.rerun()
                        else:
                            st.error(f"❌ {msg}")

                if st.button("Forgot password?", key="btn_to_forgot", use_container_width=True):
                    st.session_state["auth_mode"] = "forgot"
                    st.rerun()

                st.markdown("<hr style='border: none; border-top: 1px solid rgba(255,255,255,0.08); margin: 14px 0 10px;'>", unsafe_allow_html=True)
                
                st.markdown("<div style='text-align: center; color: #94a3b8; font-size: 0.88rem; margin-bottom: 6px;'>Don't have an account?</div>", unsafe_allow_html=True)
                if st.button("Sign Up", key="btn_to_signup", use_container_width=True):
                    st.session_state["auth_mode"] = "signup"
                    st.rerun()

            # ------------------------------------------
            # SIGNUP VIEW
            # ------------------------------------------
            elif auth_mode == "signup":
                with st.form("signup_form", clear_on_submit=False):
                    signup_header_html = """<div style="margin-bottom: 18px;">
<div style="color: #ffffff; font-size: 1.6rem; font-weight: 800; margin: 0 0 4px 0; letter-spacing: -0.5px;">Create your CargoVision account</div>
<div style="color: #94a3b8; font-size: 0.9rem; margin: 0;">Start managing your logistics intelligence in one place.</div>
</div>"""
                    if hasattr(st, "html"):
                        st.html(signup_header_html)
                    else:
                        st.markdown(signup_header_html, unsafe_allow_html=True)

                    su_name = st.text_input("Full Name", placeholder="e.g. David Vance", key="su_name")
                    
                    col_c1, col_c2 = st.columns(2)
                    with col_c1:
                        su_company = st.text_input("Company Name", placeholder="e.g. Acme Freight", key="su_comp")
                    with col_c2:
                        su_role = st.selectbox(
                            "Role",
                            [
                                "Logistics Manager",
                                "Supply Chain Analyst",
                                "Warehouse Manager",
                                "Operations Executive"
                            ],
                            key="su_role"
                        )

                    su_email = st.text_input("Email", placeholder="david.v@company.com", key="su_email")
                    
                    col_p1, col_p2 = st.columns(2)
                    with col_p1:
                        su_pass = st.text_input("Password", type="password", placeholder="Min 6 characters", key="su_pass")
                    with col_p2:
                        su_confirm = st.text_input("Confirm Password", type="password", placeholder="Re-enter password", key="su_confirm")

                    submit_signup = st.form_submit_button("Create Account", use_container_width=True, type="primary")

                    if submit_signup:
                        with st.spinner("Creating account..."):
                            success, msg = signup_user(
                                name=su_name,
                                email=su_email,
                                password=su_pass,
                                confirm_password=su_confirm,
                                company=su_company,
                                role=su_role
                            )
                        if success:
                            st.success(f"🎉 {msg}")
                            time.sleep(0.6)
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

                st.markdown("<hr style='border: none; border-top: 1px solid rgba(255,255,255,0.08); margin: 14px 0 10px;'>", unsafe_allow_html=True)
                
                st.markdown("<div style='text-align: center; color: #94a3b8; font-size: 0.88rem; margin-bottom: 6px;'>Already have an account?</div>", unsafe_allow_html=True)
                if st.button("Login", key="btn_back_to_login", use_container_width=True):
                    st.session_state["auth_mode"] = "login"
                    st.rerun()

            # ------------------------------------------
            # FORGOT PASSWORD VIEW
            # ------------------------------------------
            elif auth_mode == "forgot":
                with st.form("forgot_form"):
                    forgot_header_html = """<div style="margin-bottom: 18px;">
<div style="color: #ffffff; font-size: 1.6rem; font-weight: 800; margin: 0 0 4px 0; letter-spacing: -0.5px;">Reset your password</div>
<div style="color: #94a3b8; font-size: 0.9rem; margin: 0;">Enter your registered work email to receive reset instructions.</div>
</div>"""
                    if hasattr(st, "html"):
                        st.html(forgot_header_html)
                    else:
                        st.markdown(forgot_header_html, unsafe_allow_html=True)

                    forgot_email = st.text_input("Registered Email", placeholder="name@company.com", key="forgot_email")
                    submit_forgot = st.form_submit_button("Send Reset Instructions →", use_container_width=True, type="primary")

                    if submit_forgot:
                        with st.spinner("Sending password reset instructions..."):
                            success, msg = reset_password(forgot_email)
                        if success:
                            st.success(f"📧 {msg}")
                        else:
                            st.error(f"❌ {msg}")

                st.markdown("<hr style='border: none; border-top: 1px solid rgba(255,255,255,0.08); margin: 14px 0 10px;'>", unsafe_allow_html=True)
                if st.button("← Back to Login", key="btn_forgot_back_login", use_container_width=True):
                    st.session_state["auth_mode"] = "login"
                    st.rerun()
