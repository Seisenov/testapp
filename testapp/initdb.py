import postgresql

with postgresql.open('pq://user:passw@db:5432/test_db') as db:
	db.query("CREATE TABLE IF NOT EXISTS \"public\".\"cars\" (" +
	" \"car_id\" integer NOT NULL, " +
	" \"colour\" character varying(50) NOT NULL, " +
    " \"year\" integer NOT NULL," +
    " \"manufacturer\" character varying(255) NOT NULL );")
