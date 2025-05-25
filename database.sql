create table `user`(
	user_id integer PRIMARY KEY,
    name varchar(50),
    family varchar(50),
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
    FOREIGN KEY (category) REFERENCES `category`(`name`),
    user_id integer,
    FOREIGN KEY (`user_id`) REFERENCES `user`(`user_id`)
);
create table `budget`(
    budget_id integer primary key,
    amount float,
    category varchar(50),
    FOREIGN KEY (`category`) REFERENCES `category`(`name`),
    user_id integer,
    FOREIGN KEY (`user_id`) REFERENCES `user`(`user_id`)
);