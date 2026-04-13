-- SQLite
DROP TABLE IF EXISTS regions;
CREATE TABLE IF NOT EXISTS regions (
    id INTEGER PRIMARY KEY,
    type TEXT,
    Xmin REAL,
    Xmax REAL,
    Ymin REAL,
    Ymax REAL,
    High_Res_File TEXT,
    Low_Res_File TEXT
);
INSERT INTO regions (type, Xmin, Xmax, Ymin, Ymax) VALUES
('test', -43.679298, -42.679298, 171.637410, 172.637410),
('test', -44.679298, -43.679298, 170.637410, 171.637410),
('test', -45.679298, -44.679298, 169.637410, 170.637410),
('test', -46.679298, -45.679298, 168.637410, 169.637410),
('test', -47.679298, -46.679298, 167.637410, 168.637410);