PRAGMA foreign_keys = ON;

INSERT INTO users(username, fullname, email, filename, password) 
VALUES ('hyunkp', 'Hyun Kyu Park ', 'hyunkp@umich.edu', 'hyunkp.jpg', 'sha512$a45ffdcc71884853a2cba9e6bc55e812$c739cef1aec45c6e345c8463136dc1ae2fe19963106cf748baf87c7102937aa96928aa1db7fe1d8da6bd343428ff3167f4500c8a61095fb771957b4367868fb8');

INSERT INTO users(username, fullname, email, filename, password) 
VALUES ('husky_leah', 'Leah Park', 'husky_leah@umich.edu', 'leah.jpg', 'sha512$a45ffdcc71884853a2cba9e6bc55e812$c739cef1aec45c6e345c8463136dc1ae2fe19963106cf748baf87c7102937aa96928aa1db7fe1d8da6bd343428ff3167f4500c8a61095fb771957b4367868fb8');

INSERT INTO users(username, fullname, email, filename, password)
VALUES ('bram', 'brave mone', 'bram@umich.edu', 'bram.jpeg', 'sha512$a45ffdcc71884853a2cba9e6bc55e812$c739cef1aec45c6e345c8463136dc1ae2fe19963106cf748baf87c7102937aa96928aa1db7fe1d8da6bd343428ff3167f4500c8a61095fb771957b4367868fb8');

INSERT INTO users(username, fullname, email, filename, password)
VALUES ('alice', 'H. alice', 'alice@umich.edu', 'alice.jpeg', 'sha512$a45ffdcc71884853a2cba9e6bc55e812$c739cef1aec45c6e345c8463136dc1ae2fe19963106cf748baf87c7102937aa96928aa1db7fe1d8da6bd343428ff3167f4500c8a61095fb771957b4367868fb8');

INSERT INTO posts(postid, filename, owner)
VALUES (1, 'house.jpeg', 'hyunkp');

INSERT INTO posts(postid, filename, owner)
VALUES (2, 'f_Photo.jpeg', 'husky_leah');

INSERT INTO posts(postid, filename, owner)
VALUES (3, 'choco.png', 'hyunkp');

INSERT INTO posts(postid, filename, owner)
VALUES (4, 'fire.jpeg', 'alice');

INSERT INTO posts(postid, filename, owner)
VALUES (5, 'leah0.jpg', 'bram');

INSERT INTO posts(postid, filename, owner)
VALUES (6, 'leah1.jpg', 'bram');

INSERT INTO posts(filename, owner)
VALUES ('p1.jpeg', 'husky_leah');

INSERT INTO posts(filename, owner)
VALUES ('p2.jpeg', 'husky_leah');

INSERT INTO posts(filename, owner)
VALUES ('p3.jpeg', 'hyunkp');

INSERT INTO posts(filename, owner)
VALUES ('p4.jpeg', 'hyunkp');

INSERT INTO likes(likeid, owner, postid)
VALUES (1, 'hyunkp', 1);

INSERT INTO likes(likeid, owner, postid)
VALUES (2, 'bram', 1);

INSERT INTO likes(likeid, owner, postid)
VALUES (3, 'husky_leah', 1);

INSERT INTO likes(likeid, owner, postid)
VALUES (4, 'hyunkp', 2);

INSERT INTO likes(likeid, owner, postid)
VALUES (5, 'bram', 2);

INSERT INTO likes(likeid, owner, postid)
VALUES (6, 'hyunkp', 3);

INSERT INTO likes(likeid, owner, postid)
VALUES (7, 'hyunkp', 5);

INSERT INTO likes(likeid, owner, postid)
VALUES (8, 'hyunkp', 6);

INSERT INTO likes(likeid, owner, postid)
VALUES (9, 'husky_leah', 5);

INSERT INTO likes(likeid, owner, postid)
VALUES (10, 'husky_leah', 6);

INSERT INTO following(username1, username2)
VALUES ('hyunkp', 'husky_leah');

INSERT INTO following(username1, username2)
VALUES ('hyunkp', 'bram');

INSERT INTO following(username1, username2)
VALUES ('husky_leah', 'hyunkp');

INSERT INTO following(username1, username2)
VALUES ('husky_leah', 'bram');

INSERT INTO following(username1, username2)
VALUES ('bram', 'alice');

INSERT INTO following(username1, username2)
VALUES ('alice', 'bram');

INSERT INTO following(username1, username2)
VALUES ('bram', 'hyunkp');

INSERT INTO comments(commentid, owner, postid, text)
VALUES (1, 'hyunkp', 3, '#home sweet home');

INSERT INTO comments(commentid, owner, postid, text)
VALUES (2, 'husky_leah', 3, 'Hi guys~ you are so cuteeeee');

INSERT INTO comments(commentid, owner, postid, text)
VALUES (3, 'bram', 3, 'Cute overload!');

INSERT INTO comments(commentid, owner, postid, text)
VALUES (4, 'hyunkp', 2, 'awesome cake');

INSERT INTO comments(commentid, owner, postid, text)
VALUES (5, 'husky_leah', 1, 'Nice weather, March');

INSERT INTO comments(commentid, owner, postid, text)
VALUES (6, 'hyunkp', 1, 'Nice weather');

INSERT INTO comments(commentid, owner, postid, text)
VALUES (7, 'alice', 4, 'My yesterday!');