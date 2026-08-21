-- ==============================================================================
-- CargoVision Supabase Database Schema
-- Run this SQL in your Supabase Dashboard -> SQL Editor -> New Query
-- ==============================================================================

-- 1. Create User Profiles Table (Linked to Supabase Auth user_id)
CREATE TABLE IF NOT EXISTS public.user_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    company TEXT DEFAULT 'Logistics Enterprise',
    role TEXT NOT NULL CHECK (role IN (
        'Admin',
        'Operations Manager',
        'Warehouse Staff',
        'Checkpoint Staff',
        'Operations Staff'
    )),
    assigned_location TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 2. Create Shipments Table
CREATE TABLE IF NOT EXISTS public.shipments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    shipment_id TEXT UNIQUE NOT NULL,
    origin TEXT NOT NULL,
    destination TEXT NOT NULL,
    current_location TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('Pending', 'In Transit', 'Delayed', 'Delivered')),
    expected_delivery TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 3. Create Shipment Scans Table (With User Audit Trail)
CREATE TABLE IF NOT EXISTS public.shipment_scans (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    shipment_id TEXT NOT NULL REFERENCES public.shipments(shipment_id) ON DELETE CASCADE,
    location TEXT NOT NULL,
    scan_time TIMESTAMPTZ DEFAULT timezone('utc'::text, now()) NOT NULL,
    scan_status TEXT NOT NULL CHECK (scan_status IN ('Departed', 'Arrived', 'In Transit', 'Delayed')),
    recorded_by_user_id TEXT,
    recorded_by_name TEXT,
    created_at TIMESTAMPTZ DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 4. Create Delay Reports Table
CREATE TABLE IF NOT EXISTS public.delay_reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    shipment_id TEXT NOT NULL REFERENCES public.shipments(shipment_id) ON DELETE CASCADE,
    route TEXT NOT NULL,
    delay_duration_hours NUMERIC NOT NULL,
    delay_reason TEXT NOT NULL CHECK (delay_reason IN (
        'Traffic Congestion',
        'Weather',
        'Vehicle Breakdown',
        'Warehouse Congestion',
        'Operational Issue',
        'Other'
    )),
    severity TEXT NOT NULL CHECK (severity IN ('Low', 'Medium', 'High', 'Critical')),
    description TEXT,
    reported_at TIMESTAMPTZ DEFAULT timezone('utc'::text, now()) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 5. Enable Row Level Security (RLS) & Policies
ALTER TABLE public.user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.shipments ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.shipment_scans ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.delay_reports ENABLE ROW LEVEL SECURITY;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE tablename = 'user_profiles' AND policyname = 'Enable read/write for all users') THEN
        CREATE POLICY "Enable read/write for all users" ON public.user_profiles FOR ALL USING (true) WITH CHECK (true);
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE tablename = 'shipments' AND policyname = 'Enable read/write for all users') THEN
        CREATE POLICY "Enable read/write for all users" ON public.shipments FOR ALL USING (true) WITH CHECK (true);
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE tablename = 'shipment_scans' AND policyname = 'Enable read/write for all users') THEN
        CREATE POLICY "Enable read/write for all users" ON public.shipment_scans FOR ALL USING (true) WITH CHECK (true);
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE tablename = 'delay_reports' AND policyname = 'Enable read/write for all users') THEN
        CREATE POLICY "Enable read/write for all users" ON public.delay_reports FOR ALL USING (true) WITH CHECK (true);
    END IF;
END $$;

-- 6. Seed Preloaded Sample Logistics Data
INSERT INTO public.shipments (shipment_id, origin, destination, current_location, status, expected_delivery)
VALUES 
('SH-1001', 'Mumbai Hub', 'Pune DC', 'NH-48 Expressway Toll 3', 'In Transit', NOW() + INTERVAL '4 hours'),
('SH-1002', 'Delhi Central', 'Jaipur Hub', 'Gurgaon NH-48 Checkpoint', 'Delayed', NOW() + INTERVAL '10 hours'),
('SH-1003', 'Chennai Port', 'Bangalore Facility', 'Sriperumbudur Transit Hub', 'In Transit', NOW() + INTERVAL '7 hours'),
('SH-1004', 'Mumbai Hub', 'Nashik Transit Hub', 'Kasara Ghat Waypoint', 'In Transit', NOW() + INTERVAL '5 hours'),
('SH-1005', 'Pune DC', 'Delhi Central', 'Pune DC Outbound Gate 2', 'Pending', NOW() + INTERVAL '28 hours'),
('SH-1006', 'Kolkata Port', 'Patna DC', 'NH-19 Asansol Waypoint', 'In Transit', NOW() + INTERVAL '14 hours'),
('SH-1007', 'Hyderabad Station', 'Bangalore Hub', 'Bangalore DC Inbound Dock', 'Delivered', NOW() - INTERVAL '1 hours'),
('SH-1008', 'Ahmedabad Hub', 'Mumbai Hub', 'Surat Express Checkpoint', 'In Transit', NOW() + INTERVAL '6 hours')
ON CONFLICT (shipment_id) DO NOTHING;

INSERT INTO public.shipment_scans (shipment_id, location, scan_status, scan_time, recorded_by_name)
VALUES
('SH-1001', 'Mumbai Hub Loading Dock 3', 'Departed', NOW() - INTERVAL '4 hours', 'Operations Lead'),
('SH-1001', 'NH-48 Expressway Toll 3', 'In Transit', NOW() - INTERVAL '45 minutes', 'Checkpoint Staff'),
('SH-1002', 'Delhi Central Sorting Facility', 'Departed', NOW() - INTERVAL '6 hours', 'Warehouse Staff'),
('SH-1002', 'Gurgaon NH-48 Checkpoint', 'Delayed', NOW() - INTERVAL '90 minutes', 'Checkpoint Staff'),
('SH-1003', 'Chennai Port Container Gate 2', 'Departed', NOW() - INTERVAL '5 hours', 'Operations Staff'),
('SH-1003', 'Sriperumbudur Transit Hub', 'In Transit', NOW() - INTERVAL '2 hours', 'Checkpoint Staff'),
('SH-1004', 'Bhiwandi Central Depot', 'Departed', NOW() - INTERVAL '3 hours', 'Warehouse Staff'),
('SH-1004', 'Kasara Ghat Waypoint', 'In Transit', NOW() - INTERVAL '50 minutes', 'Checkpoint Staff'),
('SH-1007', 'Bangalore DC Inbound Dock', 'Arrived', NOW() - INTERVAL '1 hours', 'Warehouse Staff')
ON CONFLICT DO NOTHING;

INSERT INTO public.delay_reports (shipment_id, route, delay_duration_hours, delay_reason, severity, description)
VALUES
('SH-1002', 'Delhi → Jaipur', 4.8, 'Traffic Congestion', 'High', 'Heavy congestion near Gurgaon NH-48 toll plaza due to road repairs.')
ON CONFLICT DO NOTHING;
