

-- generates and populates tables with dummy data




  -- users
  create table kaitest.dbo.tbl_users (
  
	user_id int IDENTITY(1,1) PRIMARY KEY,
	user_name varchar(255) NOT NULL,	
	)
	
  
  insert into kaitest.dbo.tbl_users (user_name) values 
  ('kai.aeberli')
  , ('farshad.dashti')






  -- properties
   create table kaitest.dbo.tbl_properties (
  
	property_id int IDENTITY(1,1) PRIMARY KEY,
	address varchar(255) NOT NULL,	
	)

insert into kaitest.dbo.tbl_properties (address) values 
  ('Flat 3, Colney Hatch Lane, N10 1EJ')
  , ('16B Regents Square, WC1H 8HZ')


  
  
  
--  -- property attributes
--  create table kaitest.dbo.tbl_property_attributes (
  
--	attribute_id int IDENTITY(1,1) PRIMARY KEY,
--	landlord_comment varchar(255) NOT NULL,	
--	facilities_comment varchar(255),	
--	area_comment varchar(255),	
--	rent int,
--	distance_to_tfl_km float,
--	property_rating int,
--	landlord_rating int
--	)

--insert into kaitest.dbo.tbl_property_attributes (landlord_comment, facilities_comment, area_comment, rent, distance_to_tfl_km, property_rating, landlord_rating) values 
  
  
--  ('great guy', 'stinks a bit', 'very leafy', 650, 3, 2, 1)
--  , ('not so good' , 'great smell', 'lots of mice', 790, 2.5, 5, 5)





  ---- show results
  --select * from kaitest.dbo.tbl_property_attributes


  -- type table


    create table kaitest.dbo.tbl_attribute_types (
  
	type_id int IDENTITY(1,1) PRIMARY KEY,
	type_descr varchar(255) NOT NULL,	
	value_type varchar(255) NOT NULL,	
	
	
	)


	insert into kaitest.dbo.tbl_attribute_types values

	('Property Description', 'text'), ('Landlord Description', 'text'), ('Rent', 'int'), ('Landlord Rating', 'int'), ('Property Rating', 'int')


	select * from kaitest.dbo.tbl_attribute_types






	-- create type contents
	 create table kaitest.dbo.tbl_attribute_values (
  
	value_id int IDENTITY(1,1) PRIMARY KEY, -- random number
	type_id int, -- 1
	value_content varchar(255) NOT NULL,	-- hello my friiend, 650, 3
	
	)



	insert into kaitest.dbo.tbl_attribute_values values 
		(1, 'great place'), (3, '650'), (4, '3')

	

	select * from kaitest.dbo.tbl_attribute_values




	
















  -- mapping property - users

    create table kaitest.dbo.tbl_mapping_user_property (
  
	mapping_id int IDENTITY(1,1) PRIMARY KEY,
	user_id int NOT NULL,	
	property_id int not null
	)

	insert into kaitest.dbo.tbl_mapping_user_property VALUES
	(1, 1)





  -- mapping users - attributes
     
   create table kaitest.dbo.tbl_mapping_user_attributes (
  
	mapping_id int IDENTITY(1,1) PRIMARY KEY,
	user_id int NOT NULL,	
	attribute_id int not null
	)


	insert into kaitest.dbo.tbl_mapping_user_attributes VALUES
	(1, 1)



	-- show connections


	select 
	
		properties.address
		, users.user_name
		
		, propertyAttributes.*

	from kaitest.dbo.tbl_properties properties

	join kaitest.dbo.tbl_mapping_user_property mappingUserProperty
	on properties.property_id = mappingUserProperty.property_id
	
	left join kaitest.dbo.tbl_users users
	on mappingUserProperty.user_id = users.user_id


	left join kaitest.dbo.tbl_mapping_user_attributes mappingUserAttributes
	on users.user_id = mappingUserAttributes.user_id

	left join kaitest.dbo.tbl_property_attributes propertyAttributes
	on mappingUserAttributes.attribute_id = propertyAttributes.attribute_id

	WHERE

		properties.property_id = 1
		and users.user_name = 'kai.aeberli'

