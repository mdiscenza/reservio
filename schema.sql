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
  ('Mason', '18609162984','2','0'),
  ('Ryan', '18609162984','1','0'),
  ('Brian', '18609162984','5','0'),
  ('Dina', '18609162984','3','0'),
  ('Hans', '18609162984','4','0'),
  ('Justin', '18609162984','2','0'),
  ('Vivek', '18609162984','1','0'),
  ('Alex', '18609162984','1','0'),
  ('Calvin', '18609162984','4','0'),
  ('Justin', '18609162984','2','0'),
  ('Ann', '18609162984','3','1');