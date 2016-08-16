db.managers.find().forEach(function (m) {    
db.filings.update(
    {cik: m.cik},
    {$set: { manager: m.manager_name }},
    {multi: true}
    )
    } );