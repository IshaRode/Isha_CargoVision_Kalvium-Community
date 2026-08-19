from utils.auth import is_authenticated, get_current_user, get_auth_token

def get_top_nav_html(active_page='home'):
    # Determine which link should have the 'active' class
    pages = ['home', 'dashboard', 'shipments', 'routes', 'warehouses', 'ai_predictions', 'reports']
    active_classes = {p: 'active' if p == active_page else '' for p in pages}
    
    # Check authentication state
    auth = is_authenticated()
    user = get_current_user() if auth else None
    token = get_auth_token() if auth else ""
    q_str = f"?auth_token={token}" if token else ""
    
    if auth and user:
        user_name = user.get('name', 'User')
        role = user.get('role', 'Logistics Manager')
        initial = user_name[0] if user_name else 'U'
        first_name = user_name.split()[0]
        actions_html = f'<div class="nav-actions"><span class="top-nav-user-chip" title="{user_name} ({role})"><span class="user-avatar-initial">{initial}</span><span class="user-name-text">{first_name}</span></span><a href="/?action=logout" target="_self" class="btn-outline" style="padding: 6px 14px; font-size: 0.82rem; border-radius: 18px; border: 1px solid rgba(239, 68, 68, 0.35) !important; color: #fca5a5 !important;">Logout</a></div>'
    else:
        actions_html = ''
    
    return f"""<div class="top-nav-wrapper">
<div class="top-nav-container">
<div class="logo-section">
<div class="nav-logo-icon">CV</div>
<span style="font-size: 1.3rem; font-weight: 800; letter-spacing: -0.5px; color: white; white-space: nowrap;">CargoVision</span>
</div>
<div class="nav-links">
<a href="/{q_str}" target="_self" class="top-nav-link {active_classes['home']}">Home</a>
<a href="/dashboard{q_str}" target="_self" class="top-nav-link {active_classes['dashboard']}">Dashboard</a>
<a href="/shipment_tracking{q_str}" target="_self" class="top-nav-link {active_classes['shipments']}">Shipments</a>
<a href="/route_analytics{q_str}" target="_self" class="top-nav-link {active_classes['routes']}">Routes</a>
<a href="/warehouse_intelligence{q_str}" target="_self" class="top-nav-link {active_classes['warehouses']}">Warehouses</a>
<a href="/ai_predictions{q_str}" target="_self" class="top-nav-link {active_classes['ai_predictions']}">AI Predictions</a>
<a href="/reports{q_str}" target="_self" class="top-nav-link {active_classes['reports']}">Reports</a>
</div>
{actions_html}
</div>
</div>"""
