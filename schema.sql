drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  name string not null,
  cellnumber string not null,
  partyof integer not null,
  priority integer not null
);
INSERT INTO 'entries' ('name', 'cellnumber', 'partyof','priority') VALUES
  ('Mike', '18609162984','2','1'),
  ('Dan', '18609162984','5','0'),
  ('Julia', '18609162984','3','0'),
  ('Ann', '18609162984','3','1');