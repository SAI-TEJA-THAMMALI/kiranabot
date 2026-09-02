-- ============================================================================
-- 001_auth.sql
-- Adds the users table, user_id columns on sessions/invoices, and RLS policies.
--
-- Apply order:
--   1. Drop existing demo data (sessions + invoices) — RLS will block reads on
--      rows that have no user_id, and the NOT NULL columns require backfill.
--   2. Run this script.
--   3. Re-run the demo seeder.
--
-- The backend uses the Supabase service-role key, which BYPASSES RLS.
-- RLS exists as a second line of defense in case the anon key is ever exposed
-- or someone connects directly with a non-service-role key.
-- ============================================================================

-- 0. Drop existing demo data (per migration plan: drop and re-seed)
TRUNCATE TABLE invoices RESTART IDENTITY CASCADE;
TRUNCATE TABLE sessions RESTART IDENTITY CASCADE;

-- 1. New users table
CREATE TABLE IF NOT EXISTS users (
    id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    email           text UNIQUE,
    phone           text UNIQUE,
    password_hash   text,
    created_at      timestamptz DEFAULT now(),
    updated_at      timestamptz DEFAULT now(),
    -- A user must have at least one contact method.
    -- Password_hash is required only for email users (phone OTP comes later).
    CONSTRAINT user_has_contact   CHECK (email IS NOT NULL OR phone IS NOT NULL),
    CONSTRAINT email_has_password CHECK (email IS NULL OR password_hash IS NOT NULL)
);

CREATE INDEX IF NOT EXISTS users_email_idx ON users (email) WHERE email IS NOT NULL;
CREATE INDEX IF NOT EXISTS users_phone_idx ON users (phone) WHERE phone IS NOT NULL;

-- 2. user_id on existing tables
ALTER TABLE sessions
    ADD COLUMN IF NOT EXISTS user_id uuid REFERENCES users(id) ON DELETE CASCADE;

ALTER TABLE invoices
    ADD COLUMN IF NOT EXISTS user_id uuid REFERENCES users(id) ON DELETE CASCADE;

-- user_id is nullable during this migration so the TRUNCATE above could happen
-- without a user row. After the migration, the backend always supplies it.
-- We deliberately do NOT make it NOT NULL here — the backend enforces presence
-- in the API layer, and a NOT NULL constraint would block the demo seeder
-- from running before any user exists. Revisit once seeders take a user_id.

CREATE INDEX IF NOT EXISTS sessions_user_id_idx ON sessions(user_id);
CREATE INDEX IF NOT EXISTS invoices_user_id_idx ON invoices(user_id);

-- 3. Row Level Security
ALTER TABLE users      ENABLE ROW LEVEL SECURITY;
ALTER TABLE sessions   ENABLE ROW LEVEL SECURITY;
ALTER TABLE invoices   ENABLE ROW LEVEL SECURITY;

-- Users can read/update their own row.
DROP POLICY IF EXISTS "users self read"   ON users;
DROP POLICY IF EXISTS "users self update" ON users;
CREATE POLICY "users self read" ON users
    FOR SELECT USING (id = auth.uid());
CREATE POLICY "users self update" ON users
    FOR UPDATE USING (id = auth.uid());

-- Sessions are scoped to a single user.
DROP POLICY IF EXISTS "sessions own" ON sessions;
CREATE POLICY "sessions own" ON sessions
    USING      (user_id = auth.uid())
    WITH CHECK (user_id = auth.uid());

-- Invoices are scoped directly to a user (denormalized for simpler RLS).
DROP POLICY IF EXISTS "invoices own" ON invoices;
CREATE POLICY "invoices own" ON invoices
    USING      (user_id = auth.uid())
    WITH CHECK (user_id = auth.uid());

-- updated_at trigger for users
CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS trigger AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS users_set_updated_at ON users;
CREATE TRIGGER users_set_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION set_updated_at();
