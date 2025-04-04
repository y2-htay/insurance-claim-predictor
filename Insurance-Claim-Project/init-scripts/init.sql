-- init-scripts/init.sql
-- CREATE TABLE users (
--     id SERIAL PRIMARY KEY,
--     name VARCHAR(100) NOT NULL,
--     email VARCHAR(100) UNIQUE NOT NULL
-- );

-- INSERT INTO users (name, email) VALUES
-- ('Alice', 'alice@example.com'),
-- ('Bob', 'bob@example.com');

-- Insert data into accounts_userprofile table




INSERT INTO auth_user (username, password, permission_level)
VALUES ('user', 'needsHash', 0);


-- DO $$ BEGIN
--     IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'auth_user') THEN
--         RAISE NOTICE 'auth_user table not found, skipping user insertion.';
--     ELSE
--         INSERT INTO auth_user (username, password, permission_level) 
--         VALUES ('user', 'needsHash', 0);
--     END IF;
-- END $$;

