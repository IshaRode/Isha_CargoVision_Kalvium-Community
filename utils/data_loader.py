import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')

def generate_mock_data():
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # 1. Generate Shipments (500+)
    num_shipments = 550
    statuses = ['Delivered', 'In Transit', 'Delayed', 'Pending']
    status_weights = [0.4, 0.4, 0.1, 0.1]
    
    locations = ['Mumbai Hub', 'Pune DC', 'Delhi Central', 'Bangalore Facility', 'Chennai Port', 'Hyderabad Station']
    
    shipments_data = {
        'shipment_id': [f'SHP-{1000+i}' for i in range(num_shipments)],
        'current_location': np.random.choice(locations, num_shipments),
        'destination': np.random.choice(locations, num_shipments),
        'status': np.random.choice(statuses, num_shipments, p=status_weights),
        'delay_risk': np.random.uniform(0, 100, num_shipments).round(1),
        'eta': [(datetime.now() + timedelta(days=np.random.randint(1, 14))).strftime('%Y-%m-%d') for _ in range(num_shipments)]
    }
    pd.DataFrame(shipments_data).to_csv(os.path.join(DATA_DIR, 'shipments.csv'), index=False)
    
    # 2. Generate Routes (50+)
    num_routes = 60
    routes_data = {
        'route_id': [f'RT-{100+i}' for i in range(num_routes)],
        'origin': np.random.choice(locations, num_routes),
        'destination': np.random.choice(locations, num_routes),
        'risk_score': np.random.uniform(10, 95, num_routes).round(1),
        'avg_delivery_time_days': np.random.uniform(1, 10, num_routes).round(1),
        'delay_frequency': np.random.randint(0, 50, num_routes)
    }
    pd.DataFrame(routes_data).to_csv(os.path.join(DATA_DIR, 'routes.csv'), index=False)
    
    # 3. Generate Warehouses (15+)
    num_warehouses = 18
    warehouses_data = {
        'warehouse_id': [f'WH-{10+i}' for i in range(num_warehouses)],
        'name': [f'Warehouse {chr(65+i)}' for i in range(num_warehouses)],
        'capacity_utilization': np.random.uniform(40, 98, num_warehouses).round(1),
        'status': np.where(np.random.rand(num_warehouses) > 0.8, 'Critical', 'Normal'),
        'processing_time_hours': np.random.uniform(2, 24, num_warehouses).round(1)
    }
    pd.DataFrame(warehouses_data).to_csv(os.path.join(DATA_DIR, 'warehouses.csv'), index=False)
    
    # 4. Generate Delays (1000+)
    num_delays = 1100
    delays_data = {
        'delay_id': [f'DLY-{5000+i}' for i in range(num_delays)],
        'shipment_id': np.random.choice(shipments_data['shipment_id'], num_delays),
        'duration_hours': np.random.uniform(1, 72, num_delays).round(1),
        'reason': np.random.choice(['Weather', 'Traffic', 'Customs', 'Vehicle Breakdown', 'Port Congestion'], num_delays),
        'date': [(datetime.now() - timedelta(days=np.random.randint(0, 90))).strftime('%Y-%m-%d') for _ in range(num_delays)]
    }
    pd.DataFrame(delays_data).to_csv(os.path.join(DATA_DIR, 'delays.csv'), index=False)

def load_data(filename):
    file_path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(file_path):
        generate_mock_data()
    return pd.read_csv(file_path)

if __name__ == '__main__':
    generate_mock_data()
    print("Mock data generated successfully in data/ directory.")
