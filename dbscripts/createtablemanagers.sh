sqlite3 ../database/thirteenf_db.sqlite 'CREATE TABLE "managers" (
  "cik" TEXT, manager_name text);

CREATE INDEX "ix_managers_index" ON "managers" ("cik");'