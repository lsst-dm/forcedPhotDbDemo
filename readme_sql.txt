
----------------------------- create schema -----------------------------
CREATE TABLE Source (
  sourceId INT PRIMARY KEY,
  ra DOUBLE, 
  decl DOUBLE,
  htmId20 BIGINT
) ENGINE='MyISAM';

CREATE TABLE Field (
  uniqueId INT PRIMARY KEY AUTO_INCREMENT,
  runId INT,
  fieldId INT,
  ra0 DOUBLE,
  decl0 DOUBLE,
  ra1 DOUBLE,
  decl1 DOUBLE,
  ra2 DOUBLE,
  decl2 DOUBLE,
  ra3 DOUBLE,
  decl3 DOUBLE
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

LOAD DATA LOCAL INFILE '/nfs/lsst/home/becla/forcedPhotDbDemo/fields.csv'
  INTO TABLE Field
  FIELDS TERMINATED BY ','
  OPTIONALLY ENCLOSED BY '"'
  IGNORE 1 LINES
  (runId, fieldId, ra0, decl0, ra1, decl1, ra2, decl2, ra3, decl3);

-- Query OK, 197472 rows affected (0.94 sec)
-- Records: 197472  Deleted: 0  Skipped: 0  Warnings: 0

-- -rw-rw---- 1 mysql mysql  15M Apr  9 20:53 Field.MYD
-- -rw-rw---- 1 mysql mysql 2.0M Apr  9 20:53 Field.MYI

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

-- run this as mysql user on lsst10

-- get the keys
/usr/local/mysql/bin/myisamchk -dvv /usr/data/mysql/mysql_data/jacek_forcedPhoto/Source.MYI

-- sort the table
time /usr/local/mysql/bin/myisamchk /usr/data/mysql/mysql_data/jacek_forcedPhoto/Source.MYI --sort-record=2

real 36m17.940s
user 14m2.192s
sys  19m36.862s

--------------------------------- query ---------------------------------

SELECT scisql_s2CPolyToBin(ra0, decl0, ra1, decl1, ra2, decl2, ra3, decl3) INTO @poly
FROM Field 
WHERE uniqueId = <xxx>;

CALL scisql.scisql_s2CPolyRegion(@poly, 20);

SELECT sourceId, ra, decl, htmId20 
FROM   Source AS s 
       INNER JOIN scisql.Region AS r ON (s.htmId20 BETWEEN r.htmMin AND r.htmMax) 
WHERE  scisql_s2PtInCPoly(ra, decl, @poly) = 1;
