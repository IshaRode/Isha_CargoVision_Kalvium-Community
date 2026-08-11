def get_top_nav_html(active_page='home'):
    # Determine which link should have the 'active' class
    pages = ['home', 'dashboard', 'shipments', 'routes', 'warehouses', 'ai_predictions', 'reports']
    active_classes = {p: 'active' if p == active_page else '' for p in pages}
    
    return f"""
<div class="top-nav-wrapper">
<div class="top-nav-container">
<div class="logo-section">
<div class="nav-logo-icon">CV</div>
<h2 style="margin: 0; font-size: 1.3rem; letter-spacing: -0.5px; color: white;">CargoVision</h2>
</div>
<div class="nav-links">
<a href="/" target="_self" class="top-nav-link {active_classes['home']}">Home</a>
<a href="/dashboard" target="_self" class="top-nav-link {active_classes['dashboard']}">Dashboard</a>
<a href="/shipment_tracking" target="_self" class="top-nav-link {active_classes['shipments']}">Shipments</a>
<a href="/route_analytics" target="_self" class="top-nav-link {active_classes['routes']}">Routes</a>
<a href="/warehouse_intelligence" target="_self" class="top-nav-link {active_classes['warehouses']}">Warehouses</a>
<a href="/ai_predictions" target="_self" class="top-nav-link {active_classes['ai_predictions']}">AI Predictions</a>
<a href="/reports" target="_self" class="top-nav-link {active_classes['reports']}">Reports</a>
</div>
<div class="nav-actions">
<a href="#" class="btn-outline">Login</a>
<a href="#" class="btn-solid">Get Started</a>
</div>
</div>
</div>
"""
