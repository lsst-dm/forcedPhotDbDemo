
----------------------------- create schema -----------------------------
CREATE TABLE Source (
  sourceId INT PRIMARY KEY,
  ra DOUBLE, 
  decl DOUBLE,
  htmId20 BIGINT
) ENGINE='MyISAM';

--------------------------- load the data -------------------------------

LOAD DATA LOCAL INFILE '/nfs/lsst/home/becla/forcedPhotDbDemo/sources.csv' 
  INTO TABLE Source
  FIELDS TERMINATED BY ',' 
  OPTIONALLY ENCLOSED BY '"'
  IGNORE 1 LINES
  (sourceId, ra, decl)
  SET htmId20 = scisql_s2HtmId(ra, decl, 20);
-- Query OK, 208800000 rows affected (19 min 52.16 sec)
-- Records: 208800000  Deleted: 0  Skipped: 0  Warnings: 0

-- -rw-rw---- 1 mysql mysql 5.7G Apr  6 14:37 Source.MYD
-- -rw-rw---- 1 mysql mysql 2.0G Apr  6 14:37 Source.MYI

------------------------- add htmId20 index ----------------------------

ALTER TABLE Source ADD INDEX IDX_htmId20(htmId20);
-- Query OK, 208800000 rows affected (22 min 15.85 sec)
-- Records: 208800000  Duplicates: 0  Warnings: 0

-- -rw-rw---- 1 mysql mysql 5.7G Apr  6 14:49 Source.MYD
-- -rw-rw---- 1 mysql mysql 5.0G Apr  6 15:03 Source.MYI

------------ make a copy to have sorted and non sorted version ---------

create table SourceNotSorted like Source;
insert into SourceNotSorted select * from Source;
-- Query OK, 208800000 rows affected (24 min 24.91 sec)
-- Records: 208800000  Duplicates: 0  Warnings: 0

------------------------ sort by htmId20 -------------------------------

-- get the keys
/usr/local/mysql/bin/myisamchk -dvv /usr/data/mysql/mysql_data/jacek_forcedPhoto/Source.MYI

-- sort the table
time /usr/local/mysql/bin/myisamchk /usr/data/mysql/mysql_data/jacek_forcedPhoto/Source.MYI --sort-record=2

real 36m17.940s
user 14m2.192s
sys  19m36.862s

------------------------- load exposure -----------------

