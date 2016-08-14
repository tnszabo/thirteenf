db.managers.find().forEach(function (m) {    
db.filings.update(
    {cik: m.cik},
    {$set: { manager_name: m.manager_name }},
    {multi: true}
    )
    } );