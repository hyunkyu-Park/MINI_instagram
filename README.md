# Mini Instagram Project - Web Application

old: https://www.youtube.com/watch?v=LGtg9R7kAVc

current: https://youtu.be/FPLNeisLifc

## Introduction
This project begins with server-side dynamic pages and is currently undergoing refactoring to transition into client-side dynamic pages. 
It consists of a total of 11 webpages, each focusing on specific functionalities.

## Features and Structure
   <pre>
1. Account Creation
  • Allows users to create a new account.
2. Login
  • Allows users to log in.
3. Main Feed
  • Presents the user's main feed with infinite scroll functionality.
4. Account Deletion
  • Enables users to delete their accounts.
5. Account Information Modification
  • Provides a page for users to modify their account information.
6. New User Recommendations
  • Recommends new users to the current user.
7. Followers
  • Shows the list of followers for a user.
8. Following
  • Displays the list of users being followed by a user.
9. Password Modification
  • Provides a page for users to modify their passwords.
10. Post Detail
  • Shows detailed information about a specific post.
11. User Page
  • Displays a page for a specific user.
</pre>

## Technology Stack
<pre>
Server: Python Flask
Database: SQLite3
Server Hosting: AWS EC2
Password Management: SHA-512 Algorithm
Infinite Scroll Implementation:
Utilizes pagination techniques and the React InfiniteScroll library.
</pre>

## Notes
The project started as server-side dynamic pages and is currently undergoing refactoring towards client-side dynamic pages.
It enhances user experience through account management, social features, and the implementation of infinite scroll.

## My Project Notes

### Using only client side? Can I use the existing code?
Rather than discarding all existing codes and grinding the entire structure, modify existing codes and implement api endpoint for client side dynamic pages on top of them for code reuse.

### overlapped file name. 
Situation: I saved the image using raw name as it is and saved it in the database, and a query error occurred

Cause: The names of photos saved by users may overlap ex: dog.jpg

Resolution: Create random UUIDs using uuid.uuid4(.hex), change them to lowercase using pathlib.path(filename).suffix.lower() and save them (unifying by lowercase since not all environments are case sensitive)

### page infinite loading issue
Situation: When user click a button depending on whether user follow or not, I wrote the code to change the status to Follow->Unfollow or Unfollow->Page. But Infinite Loading occured

Cause: Implemented function call not function reference
<input type="submit" value="unfollow"  onClick={() => handleUnfollow(username) }/>
<input type="submit" value="unfollow" onClick={handleUnfollow(username)}/>

