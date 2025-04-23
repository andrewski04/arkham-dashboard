import random
import datetime
from datetime import timezone # Import timezone

def random_timestamp():
    # Use timezone-aware UTC time
    now = datetime.datetime.now(timezone.utc)
    # Generate timestamps within the last 10 seconds to avoid immediate purging
    delta = datetime.timedelta(seconds=random.randint(0, 10))
    ts = now - delta
    return ts.replace(microsecond=0).isoformat() + 'Z'

def random_ip():
    return ".".join(str(random.randint(1, 254)) for _ in range(4))

arkham_data = {
    "servers": ["auth-node-1", "auth-node-2", "auth-node-3", "db-core-1", "db-core-2", "proxy-gateway"],
    "events": ["Multiple failed SSH login attempts", "Unexpected server reboot", "Malware signature detected", "Configuration change detected", "Unusual outbound traffic"],
    "statuses": ["investigating", "resolved", "escalated", "monitoring"],
    "locations": ["cell block A", "cell block B", "cell block C", "cell block D", "lab wing", "armory", "restricted library", "admin office", "yard"],
    "systems": ["emergency_alarm", "lockdown_system", "power_grid", "lighting_control", "door_lock"],
    "trigger_reasons": ["manual override", "sensor activation", "scheduled test", "system fault"],
    "scanner_ids": ["biometric-1A", "biometric-2F", "biometric-3C", "biometric-4D"],
    "access_results": ["granted", "denied"],
    "access_reasons": ["fingerprint mismatch", "unauthorized user", "system error", "successful authentication"],
    "user_ids": ["unknown", "staff-001", "staff-002", "warden", "visitor-123"],
    "inmate_ids": ["ARK-001", "ARK-056", "ARK-099", "ARK-123", "ARK-200"],
    "inmate_names": ["Harleen Quinzel", "Edward Nigma", "Oswald Cobblepot", "Pamela Isley", "Waylon Jones"],
    "threat_levels": ["low"] * 10 + ["medium"] * 5 + ["high"] * 2 + ["critical"], # Weighted towards less severe
    "incidents": ["tampering with surveillance", "attempted escape", "assault on staff", "contraband possession"],
    "recommendations": ["increased surveillance", "access revocation", "isolation", "psych evaluation"],
    "comm_types": ["lockdown alert", "system update", "security breach", "routine check-in"],
    "messages": [
        "Zone 3 lockdown initiated due to intruder detection.",
        "All staff report to admin office.",
        "Routine system maintenance scheduled.",
        "Security breach detected in cell block B.",
        "Unauthorized access attempt detected at main gate.",
        "Anomalous network activity originating from internal server.",
        "Physical security breach reported in the East Wing.",
        "Inmate disturbance in Cell Block C.",
        "Biometric scanner failure at the armory entrance."
    ],
    "senders": ["automated-system", "warden", "security_team", "maintenance_bot"],
    "protocols": ["TCP", "UDP", "ICMP"],
    "actions": ["allowed"] * 10 + ["blocked"] * 3 + ["flagged"], # Weighted towards allowed
    "surveillance_levels": ["low"] * 10 + ["medium"] * 5 + ["high"] * 2 + ["severe"], # Weighted towards less severe
    "activities": ["normal activity"] * 10 + ["motion detected"] * 5 + ["unauthorized person detected"] * 2 + ["camera offline"] # Weighted towards normal activity
}

def generate_server_log():
    status = random.choice(arkham_data["statuses"] * 5 + ["escalated", "resolved"]) # Weighted towards less severe
    event = random.choice(arkham_data["events"])
    if status in ["escalated", "resolved"]:
        event = random.choice(["Critical system failure", "Security vulnerability patched", "Major service disruption", "Data breach contained"])

    return {
        "server": random.choice(arkham_data["servers"]),
        "event": event,
        "attempts": random.randint(1, 10),
        "status": status,
        "timestamp": random_timestamp()
    }

def generate_physical_security_log():
    status = random.choice(["active"] * 10 + ["inactive", "fault"]) # Weighted towards active
    trigger_reason = random.choice(arkham_data["trigger_reasons"])
    if status in ["inactive", "fault"]:
        trigger_reason = random.choice(["system malfunction", "power outage", "vandalism", "breach attempt detected"])

    return {
        "system": random.choice(arkham_data["systems"]),
        "location": random.choice(arkham_data["locations"]),
        "status": status,
        "trigger_reason": trigger_reason,
        "timestamp": random_timestamp()
    }

def generate_biometric_access_log():
    access_result = random.choice(arkham_data["access_results"] * 10 + ["denied"]) # Weighted towards granted
    reason = random.choice(arkham_data["access_reasons"])
    if access_result == "denied":
        reason = random.choice(["fingerprint mismatch", "unauthorized user", "system error", "access revoked", "security alert"])

    return {
        "scanner_id": random.choice(arkham_data["scanner_ids"]),
        "user_id": random.choice(arkham_data["user_ids"]),
        "access_result": access_result,
        "reason": reason,
        "location": random.choice(arkham_data["locations"]),
        "timestamp": random_timestamp()
    }

def generate_inmate_threat_log():
    threat_level = random.choice(arkham_data["threat_levels"])
    incident_flag = random.choice(arkham_data["incidents"])
    recommendation = random.choice(arkham_data["recommendations"])
    inmate_id = random.choice(arkham_data["inmate_ids"])
    name = arkham_data["inmate_names"][arkham_data["inmate_ids"].index(inmate_id)] # Get corresponding name

    if threat_level in ["high", "critical"]:
        incident_flag = random.choice(["attempted escape from cell block", "hostage situation reported", "major contraband discovery", "violent outburst in common area"])
        recommendation = random.choice(["immediate lockdown of area", "security team intervention required", "transfer to high-security solitary", "emergency medical assessment"])

    return {
        "inmate_id": inmate_id,
        "name": name,
        "threat_level": threat_level,
        "last_known_location": random.choice(arkham_data["locations"]),
        "incident_flag": incident_flag,
        "recommendation": recommendation,
        "timestamp": random_timestamp()
    }

def generate_internal_comms_log():
    comm_type = random.choice(arkham_data["comm_types"])
    message = random.choice(arkham_data["messages"])
    recipients = random.sample(["security_team", "admin_office", "medical_staff", "maintenance"], k=random.randint(1,3))
    sent_by = random.choice(arkham_data["senders"])

    if comm_type == "security breach":
        message = random.choice([
            "Urgent: Security breach detected in perimeter fence, Sector 4.",
            "All units respond to Cell Block A, unauthorized movement detected.",
            "Code Red: Possible containment breach in the experimental wing."
        ])
        recipients = ["security_team", "warden"]
        sent_by = "automated-system"
    elif comm_type == "lockdown alert":
         message = random.choice([
             "Initiating full facility lockdown. All personnel follow protocol.",
             "Lockdown in effect for Cell Block B due to inmate disturbance.",
             "Perimeter lockdown activated. Standby for further instructions."
         ])
         recipients = ["security_team", "admin_office", "all_personnel"]
         sent_by = "automated-system"


    return {
        "type": comm_type,
        "recipients": recipients,
        "message": message,
        "sent_by": sent_by,
        "timestamp": random_timestamp()
    }

def generate_network_log():
    threat_level = random.choice(arkham_data["threat_levels"])
    action = random.choice(arkham_data["actions"])
    source_ip = random_ip()
    destination_ip = random_ip()
    protocol = random.choice(arkham_data["protocols"])
    port = random.choice([22, 80, 443, 8080, 3306])

    if threat_level in ["high", "critical"]:
        action = "blocked"
        destination_ip = random.choice(["192.168.1.1", "10.0.0.5", "172.16.0.10"]) # Internal critical servers
        if threat_level == "critical":
            protocol = random.choice(["TCP", "UDP"])
            port = random.choice([22, 443, 3306]) # Common attack ports
            if random.random() > 0.5: # Add specific attack types
                if protocol == "TCP" and port == 22:
                    # Simulate SSH brute force
                    return {
                        "source_ip": source_ip,
                        "destination_ip": destination_ip,
                        "protocol": protocol,
                        "port": port,
                        "action": action,
                        "threat_level": threat_level,
                        "details": "Multiple failed SSH login attempts detected.",
                        "timestamp": random_timestamp()
                    }
                elif protocol == "TCP" and port == 443:
                     # Simulate potential data exfiltration
                     return {
                        "source_ip": source_ip,
                        "destination_ip": destination_ip,
                        "protocol": protocol,
                        "port": port,
                        "action": action,
                        "threat_level": threat_level,
                        "details": "Unusual outbound data transfer detected on secure port.",
                        "timestamp": random_timestamp()
                    }


    return {
        "source_ip": source_ip,
        "destination_ip": destination_ip,
        "protocol": protocol,
        "port": port,
        "action": action,
        "threat_level": threat_level,
        "timestamp": random_timestamp()
    }

def generate_video_surveillance_log():
    level = random.choice(arkham_data["surveillance_levels"])
    activity = random.choice(arkham_data["activities"])
    location = random.choice(arkham_data["locations"])

    if level in ["high", "severe"]:
        activity = random.choice(["unauthorized person detected in restricted area", "multiple subjects in unauthorized zone", "camera tampered with", "abnormal behavior observed"])
        if level == "severe":
            activity = random.choice(["physical altercation in progress", "attempted breach of secure door", "unresponsive individual detected", "fire or smoke detected"])

    return {
        "location": location,
        "level": level,
        "activity": activity,
        "timestamp": random_timestamp()
    }
