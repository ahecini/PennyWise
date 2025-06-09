                    create table `user`( 
                        username varchar(50) PRIMARY KEY,
                        pin varchar(50),
                        balance float
                    );
                    create table `category`(
                        name varchar(50) PRIMARY KEY
                    );
                    create table `transaction`(
                        trans_id integer PRIMARY KEY,
                        description varchar(50),
                        amount float,
                        income boolean,
                        tdate date,
                        category varchar(50),
                        username varchar(50),
                        FOREIGN KEY (category) REFERENCES `category`(`name`),
                        FOREIGN KEY (`username`) REFERENCES `user`(`username`)
                    );
                    create table `budget`(
                        budget_id integer primary key,
                        amount float,
                        category varchar(50),
                        username varchar(50),
                        FOREIGN KEY (`category`) REFERENCES `category`(`name`),
                        FOREIGN KEY (`username`) REFERENCES `user`(`username`)
                    );