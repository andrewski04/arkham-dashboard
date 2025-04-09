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
    "threat_levels": ["low", "medium", "high", "critical"],
    "incidents": ["tampering with surveillance", "attempted escape", "assault on staff", "contraband possession"],
    "recommendations": ["increased surveillance", "access revocation", "isolation", "psych evaluation"],
    "comm_types": ["lockdown alert", "system update", "security breach", "routine check-in"],
    "messages": [
        "Zone 3 lockdown initiated due to intruder detection.",
        "All staff report to admin office.",
        "Routine system maintenance scheduled.",
        "Security breach detected in cell block B."
    ],
    "senders": ["automated-system", "warden", "security_team", "maintenance_bot"],
    "protocols": ["TCP", "UDP", "ICMP"],
    "actions": ["allowed", "blocked", "flagged"],
    "surveillance_levels": ["low", "medium", "high", "severe"],
    "activities": ["unauthorized person detected", "motion detected", "camera offline", "normal activity"]
}

def generate_server_log():
    return {
        "server": random.choice(arkham_data["servers"]),
        "event": random.choice(arkham_data["events"]),
        "attempts": random.randint(1, 10),
        "status": random.choice(arkham_data["statuses"]),
        "timestamp": random_timestamp()
    }

def generate_physical_security_log():
    return {
        "system": random.choice(arkham_data["systems"]),
        "location": random.choice(arkham_data["locations"]),
        "status": random.choice(["active", "inactive", "fault"]),
        "trigger_reason": random.choice(arkham_data["trigger_reasons"]),
        "timestamp": random_timestamp()
    }

def generate_biometric_access_log():
    return {
        "scanner_id": random.choice(arkham_data["scanner_ids"]),
        "user_id": random.choice(arkham_data["user_ids"]),
        "access_result": random.choice(arkham_data["access_results"]),
        "reason": random.choice(arkham_data["access_reasons"]),
        "location": random.choice(arkham_data["locations"]),
        "timestamp": random_timestamp()
    }

def generate_inmate_threat_log():
    return {
        "inmate_id": random.choice(arkham_data["inmate_ids"]),
        "name": random.choice(arkham_data["inmate_names"]),
        "threat_level": random.choice(arkham_data["threat_levels"]),
        "last_known_location": random.choice(arkham_data["locations"]),
        "incident_flag": random.choice(arkham_data["incidents"]),
        "recommendation": random.choice(arkham_data["recommendations"]),
        "timestamp": random_timestamp()
    }

def generate_internal_comms_log():
    return {
        "type": random.choice(arkham_data["comm_types"]),
        "recipients": random.sample(["security_team", "admin_office", "medical_staff", "maintenance"], k=random.randint(1,3)),
        "message": random.choice(arkham_data["messages"]),
        "sent_by": random.choice(arkham_data["senders"]),
        "timestamp": random_timestamp()
    }

def generate_network_log():
    return {
        "source_ip": random_ip(),
        "destination_ip": random_ip(),
        "protocol": random.choice(arkham_data["protocols"]),
        "port": random.choice([22, 80, 443, 8080, 3306]),
        "action": random.choice(arkham_data["actions"]),
        "threat_level": random.choice(arkham_data["threat_levels"]),
        "timestamp": random_timestamp()
    }

def generate_video_surveillance_log():
    return {
        "location": random.choice(arkham_data["locations"]),
        "level": random.choice(arkham_data["surveillance_levels"]),
        "activity": random.choice(arkham_data["activities"]),
        "timestamp": random_timestamp()
    }
