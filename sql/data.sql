PRAGMA foreign_keys = ON;

INSERT INTO users(username, fullname, email, filename, password) 
VALUES ('hyunkp', 'Hyun Kyu Park ', 'hyunkp@umich.edu', 'hyunkp.jpg', 'sha512$a45ffdcc71884853a2cba9e6bc55e812$c739cef1aec45c6e345c8463136dc1ae2fe19963106cf748baf87c7102937aa96928aa1db7fe1d8da6bd343428ff3167f4500c8a61095fb771957b4367868fb8');

INSERT INTO users(username, fullname, email, filename, password) 
VALUES ('husky_leah', 'Leah Park', 'husky_leah@umich.edu', 'leah.jpg', 'sha512$a45ffdcc71884853a2cba9e6bc55e812$c739cef1aec45c6e345c8463136dc1ae2fe19963106cf748baf87c7102937aa96928aa1db7fe1d8da6bd343428ff3167f4500c8a61095fb771957b4367868fb8');

INSERT INTO users(username, fullname, email, filename, password)
VALUES ('michjc', 'Michael Cafarella', 'michjc@umich.edu', 'michjc.jpg', 'sha512$a45ffdcc71884853a2cba9e6bc55e812$c739cef1aec45c6e345c8463136dc1ae2fe19963106cf748baf87c7102937aa96928aa1db7fe1d8da6bd343428ff3167f4500c8a61095fb771957b4367868fb8');

INSERT INTO users(username, fullname, email, filename, password)
VALUES ('jag', 'H.V. Jagadish', 'jag@umich.edu', 'jag.jpg', 'sha512$a45ffdcc71884853a2cba9e6bc55e812$c739cef1aec45c6e345c8463136dc1ae2fe19963106cf748baf87c7102937aa96928aa1db7fe1d8da6bd343428ff3167f4500c8a61095fb771957b4367868fb8');

INSERT INTO posts(postid, filename, owner)
VALUES (1, '122a7d27ca1d7420a1072f695d9290fad4501a41.jpg', 'hyunkp');

INSERT INTO posts(postid, filename, owner)
VALUES (2, 'ad7790405c539894d25ab8dcf0b79eed3341e109.jpg', 'husky_leah');

INSERT INTO posts(postid, filename, owner)
VALUES (3, '9887e06812ef434d291e4936417d125cd594b38a.jpg', 'hyunkp');

INSERT INTO posts(postid, filename, owner)
VALUES (4, '2ec7cf8ae158b3b1f40065abfb33e81143707842.jpg', 'jag');

INSERT INTO posts(postid, filename, owner)
VALUES (5, 'leah0.jpg', 'husky_leah');

INSERT INTO posts(postid, filename, owner)
VALUES (6, 'leah1.jpg', 'husky_leah');

INSERT INTO likes(likeid, owner, postid)
VALUES (1, 'hyunkp', 1);

INSERT INTO likes(likeid, owner, postid)
VALUES (2, 'michjc', 1);

INSERT INTO likes(likeid, owner, postid)
VALUES (3, 'husky_leah', 1);

INSERT INTO likes(likeid, owner, postid)
VALUES (4, 'hyunkp', 2);

INSERT INTO likes(likeid, owner, postid)
VALUES (5, 'michjc', 2);

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
VALUES ('hyunkp', 'michjc');

INSERT INTO following(username1, username2)
VALUES ('husky_leah', 'hyunkp');

INSERT INTO following(username1, username2)
VALUES ('husky_leah', 'michjc');

INSERT INTO following(username1, username2)
VALUES ('michjc', 'jag');

INSERT INTO following(username1, username2)
VALUES ('jag', 'michjc');

INSERT INTO following(username1, username2)
VALUES ('michjc', 'hyunkp');

INSERT INTO comments(commentid, owner, postid, text)
VALUES (1, 'hyunkp', 3, '#chickensofinstagram');

INSERT INTO comments(commentid, owner, postid, text)
VALUES (2, 'husky_leah', 3, 'I <3 chickens');

INSERT INTO comments(commentid, owner, postid, text)
VALUES (3, 'michjc', 3, 'Cute overload!');

INSERT INTO comments(commentid, owner, postid, text)
VALUES (4, 'hyunkp', 2, 'Sick #crossword');

INSERT INTO comments(commentid, owner, postid, text)
VALUES (5, 'husky_leah', 1, 'Walking the plank #chickensofinstagram');

INSERT INTO comments(commentid, owner, postid, text)
VALUES (6, 'hyunkp', 1, 'This was after trying to teach them to do a #crossword');

INSERT INTO comments(commentid, owner, postid, text)
VALUES (7, 'jag', 4, 'Saw this on the diag yesterday!');