sqlite3 ../database/thirteenf_db.sqlite 'CREATE TABLE "filings" (
"index" INTEGER,
  "ccc" TEXT,
  "cik" TEXT,
  "city" TEXT,
  "confirmingcopyflag" TEXT,
  "cusip" TEXT,
  "form13ffilenumber" TEXT,
  "infotable" TEXT,
  "investmentdiscretion" TEXT,
  "isamendment" TEXT,
  "isconfidentialomitted" TEXT,
  "livetestflag" TEXT,
  "manager_name" TEXT,
  "name" TEXT,
  "nameofissuer" TEXT,
  "none" INTEGER,
  "otherincludedmanagerscount" INTEGER,
  "othermanager" TEXT,
  "overrideinternetflag" TEXT,
  "periodofreport" TEXT,
  "phone" TEXT,
  "provideinfoforinstruction5" TEXT,
  "putcall" TEXT,
  "reportcalendarorquarter" TEXT,
  "reporttype" TEXT,
  "returncopyflag" TEXT,
  "sequencenumber" REAL,
  "shared" INTEGER,
  "shrsorprnamt" TEXT,
  "signature" TEXT,
  "signaturedate" TEXT,
  "sole" INTEGER,
  "sshprnamt" INTEGER,
  "sshprnamttype" TEXT,
  "stateorcountry" TEXT,
  "street1" TEXT,
  "street2" TEXT,
  "submissiontype" TEXT,
  "tableentrytotal" INTEGER,
  "tablevaluetotal" INTEGER,
  "title" TEXT,
  "titleofclass" TEXT,
  "value" INTEGER,
  "votingauthority" TEXT,
  "zipcode" TEXT
, amendmentno TEXT, additionalinformation TEXT, amendmenttype TEXT, datereported TEXT, confdeniedexpired TEXT, datedeniedexpired TEXT, reasonfornonconfidentiality TEXT);
CREATE INDEX "ix_filings_index" ON "filings" ("index");'

'CREATE INDEX "ix_filings_cik" ON "filings" ("cik");'

'CREATE INDEX "ix_filings_period" ON "filings" ("periodofreport");'