from utils.auth import is_authenticated, get_current_user, get_auth_token

def get_top_nav_html(active_page='home'):
    # Determine which link should have the 'active' class
    pages = ['home', 'dashboard', 'shipments', 'scans', 'delay_reports', 'routes', 'warehouses', 'ai_predictions', 'reports']
    active_classes = {p: 'active' if p == active_page else '' for p in pages}
    
    # Check authentication state
    auth = is_authenticated()
    user = get_current_user() if auth else None
    token = get_auth_token() if auth else ""
    q_str = f"?auth_token={token}" if token else ""
    
    if auth and user:
        user_name = user.get('name', 'User')
        role = user.get('role', 'Warehouse Staff')
        location = user.get('assigned_location', 'Mumbai Hub')
        initial = user_name[0].upper() if user_name else 'U'
        first_name = user_name.split()[0]
        actions_html = f'<div class="nav-actions"><span class="top-nav-user-chip" title="{user_name} ({role} • {location})"><span class="user-avatar-initial">{initial}</span><span class="user-name-text">{first_name}</span><span style="font-size: 0.72rem; color: #38bdf8; margin-left: 2px;">📍 {location}</span></span><a href="/?action=logout" target="_self" class="btn-outline" style="padding: 6px 14px; font-size: 0.82rem; border-radius: 18px; border: 1px solid rgba(239, 68, 68, 0.35) !important; color: #fca5a5 !important;">Logout</a></div>'
    else:
        actions_html = f'<div class="nav-actions"><a href="/login" target="_self" class="btn-outline">Login</a><a href="/login" target="_self" class="btn-solid">Get Started</a></div>'
    
    return f"""<div class="top-nav-wrapper">
<div class="top-nav-container">
<div class="logo-section">
<div class="nav-logo-icon" style="background: linear-gradient(135deg, #0ea5e9, #6366f1); color: #ffffff; font-weight: 800; border-radius: 8px; width: 34px; height: 34px; display: flex; align-items: center; justify-content: center; box-shadow: 0 0 12px rgba(14, 165, 233, 0.4);">CV</div>
<span class="nav-logo-text" style="font-family: 'Outfit', sans-serif; font-weight: 800; font-size: 1.2rem; background: linear-gradient(90deg, #ffffff, #38bdf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">CargoVision</span>
<span class="badge-glow-green" style="font-size: 0.65rem; padding: 2px 7px; margin-left: 6px; display: inline-flex; align-items: center; gap: 4px;">
<span class="tower-live-dot" style="width: 5px; height: 5px;"></span> v2.4 Live
</span>
</div>
<div class="nav-links">
<a href="/{q_str}" target="_self" class="top-nav-link {active_classes['home']}">Home</a>
<a href="/dashboard{q_str}" target="_self" class="top-nav-link {active_classes['dashboard']}">Dashboard</a>
<a href="/shipment_tracking{q_str}" target="_self" class="top-nav-link {active_classes['shipments']}">Shipments</a>
<a href="/shipment_scans{q_str}" target="_self" class="top-nav-link {active_classes['scans']}">Scans</a>
<a href="/delay_reports{q_str}" target="_self" class="top-nav-link {active_classes['delay_reports']}">Delays</a>
<a href="/route_analytics{q_str}" target="_self" class="top-nav-link {active_classes['routes']}">Routes</a>
<a href="/warehouse_intelligence{q_str}" target="_self" class="top-nav-link {active_classes['warehouses']}">Warehouses</a>
<a href="/ai_predictions{q_str}" target="_self" class="top-nav-link {active_classes['ai_predictions']}">AI Predictions</a>
<a href="/reports{q_str}" target="_self" class="top-nav-link {active_classes['reports']}">Reports</a>
</div>
{actions_html}
</div>
</div>"""
