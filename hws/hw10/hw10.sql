CREATE TABLE parents AS
  SELECT "ace" AS parent, "bella" AS child UNION
  SELECT "ace"          , "charlie"        UNION
  SELECT "daisy"        , "hank"           UNION
  SELECT "finn"         , "ace"            UNION
  SELECT "finn"         , "daisy"          UNION
  SELECT "finn"         , "ginger"         UNION
  SELECT "ellie"        , "finn";

CREATE TABLE dogs AS
  SELECT "ace" AS name, "long" AS fur, 26 AS height UNION
  SELECT "bella"      , "short"      , 52           UNION
  SELECT "charlie"    , "long"       , 47           UNION
  SELECT "daisy"      , "long"       , 46           UNION
  SELECT "ellie"      , "short"      , 35           UNION
  SELECT "finn"       , "curly"      , 32           UNION
  SELECT "ginger"     , "short"      , 28           UNION
  SELECT "hank"       , "curly"      , 31;

CREATE TABLE sizes AS
  SELECT "toy" AS size, 24 AS min, 28 AS max UNION
  SELECT "mini"       , 28       , 35        UNION
  SELECT "medium"     , 35       , 45        UNION
  SELECT "standard"   , 45       , 60;


-- All dogs with parents ordered by decreasing height of their parent
CREATE TABLE by_parent_height AS
  SELECT a.child as child
  FROM parents as a, dogs as b
  where a.parent=b.name
  order by b.height desc;

-- The size of each dog
CREATE TABLE size_of_dogs AS
  SELECT a.name as name, b.size AS size
  from dogs as a,sizes as b
  where a.height <= b.max and a.height > b.min;


-- [Optional] Filling out this helper table is recommended
-- column fitst second
-- resource parents
-- link parents is equal
-- limit a<b
CREATE TABLE siblings AS
  SELECT a.child as FIRST,b.child as second
  from parents as a,parents as b
  where a.parent = b.parent and a.child < b.child;

-- Sentences about siblings that are the same size
-- column pair
-- resource siblings to get the siblings ;size of dogs to get their size
-- link their size is equal
-- limit the structure of pair must be --- The two siblings, bella and charlie, have the same size: standard
CREATE TABLE sentences AS
  SELECT 'The two siblings, '||a.FIRST||' and '||a.second||', have the same size: '||b.size
  from siblings as a,size_of_dogs as b,size_of_dogs as c
  where a.FIRST=b.name and 
        a.second=c.name and 
        b.size=c.size;
-- fur average
CREATE TABLE average AS
  SELECT fur , avg(a.height) as age from dogs as a GROUP by fur; 
-- fur height 
CREATE TABLE FILTER AS
  WITH vaild_fur AS(
    SELECT a.fur
    from dogs as a
    JOIN average as b on a.fur=b.fur
    GROUP by a.fur,b.age 
    HAVING max(a.height) < b.age*1.3 AND
           min(a.height) >= b.age*0.7
  )
  SELECT a.fur as fur,b.height as height 
  FROM vaild_fur as a,dogs as b
  WHERE a.fur=b.fur;
-- Height range for each fur type where all of the heights differ by no more than 30% from the average height
-- column fur height_range
-- resource dogs to get fur and height
-- link fur is equal and height must between 0.7*average and 1.3*average 
-- limit height_range=the max sub the min

CREATE TABLE low_variance AS
  SELECT a.fur as fur , max(a.height)-min(a.height) as height_range 
  FROM FILTER as a GROUP by fur;

