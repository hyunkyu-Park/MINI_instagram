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

<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>

# My Project Notes

## Using only client side? Can I use the existing code?
Rather than discarding all existing codes and grinding the entire structure, modify existing codes and implement api endpoint for client side dynamic pages on top of them for code reuse.

## Overlapped file name. 
Situation: I saved the image using raw name as it is and saved it in the database, and a query error occurred

Cause: The names of photos saved by users may overlap ex: dog.jpg

Resolution: Create random UUIDs using uuid.uuid4(.hex), change them to lowercase using pathlib.path(filename).suffix.lower() and save them (unifying by lowercase since not all environments are case sensitive)

## Page infinite loading issue
Situation: When user click a button depending on whether user follow or not, I wrote the code to change the status to Follow->Unfollow or Unfollow->Page. But Infinite Loading occured

Cause: Implemented function call not function reference <br>

Resolution:  
<input type="submit" value="unfollow" onClick={() => handleUnfollow(username) }/> vs <input type="submit" value="unfollow" onClick={handleUnfollow(username)}/

Method 1 (Function Reference):
This method involves passing a reference to the handleUnfollow(username) function to the onClick event handler.
The function handleUnfollow(username) will be called only when the button is clicked.
This approach ensures that the function is invoked only at the time of the button click.

Method 2 (Function Call):
This method involves directly calling the handleUnfollow(username) function and passing its result to the onClick event handler.
In this case, the handleUnfollow(username) function is executed immediately when the page is rendered, and its result is passed to the onClick event.
Since the function is executed as soon as the page loads, caution is required as it may lead to unintended behavior.

In summary, while Method 1 ensures that the function is called only when the button is clicked (function reference), Method 2 executes the function immediately upon page load, potentially leading to undesired consequences (function call).

## Calling server side code instead of client side code

Situation: The first time user call the Followers page, the page is using proper client side api endpoint, but when I refresh, it uses server side code(old one)

Cause: return flakes.render_template was set to old version html when calling serverside ->index.html

Resolution: 
I tried to check all the codes from the time when the server-side code was called to the time when it was terminated.
But I could not recognized that the return statement was wrong, so it took time to resolve the error. I learned that just because it's familiar to me, it's not the right code.  
When refactoring code, I should always observe that there is no conflict between the old code and the updated code, and the existing design. 
It would be more effective to check the pieces in advance that could cause conflicts when designing before writing the actual code.

## Query for create_like 

Situation: Error occurs when users cancel like and press like again

Cause: Wrong Query logic, my code check if the user likes the post in the javascript and it checks in the api endpoint.

Resolution: Before writing the code in the future, let's distinguish between what JavaScript will solve and what will be solved using sql. Let's also think about which one would be more efficient!


## User experience improvement

Situation: if the size of the image files are big, it takes few seconds two render the page

Studying transition andd see if it can resolve this issue

