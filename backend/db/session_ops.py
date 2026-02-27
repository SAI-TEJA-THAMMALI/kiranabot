from db.supabase_client import get_supabase

def create_session(period: str) -> dict:
    try:
        db = get_supabase()
        result = db.table("sessions").insert({
            "period": period
        }).execute()
        return result.data[0] if result.data else {}
    except Exception as e:
        print(f"Create session error: {e}")
        return {"id": "offline-session", "period": period}

def get_session(session_id: str) -> dict:
    try:
        db = get_supabase()
        result = db.table("sessions").select(
            "*, invoices(*)"
        ).eq("id", session_id).execute()
        return result.data[0] if result.data else {}
    except Exception as e:
        print(f"Get session error: {e}")
        return {}