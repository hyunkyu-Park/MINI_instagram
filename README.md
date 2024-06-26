# Mini Instagram Project - Web Application

website: [minista.pro](https://minista.pro/)

old 1: https://www.youtube.com/watch?v=LGtg9R7kAVc

old 2: https://youtu.be/FPLNeisLifc

old 3: https://www.youtube.com/watch?v=myKAVkKYNxI

## Introduction
This project begins with server-side dynamic pages and refactored to transition into client-side dynamic pages.
This is single page application and it consists of a total of 11 webpages(in users view), each focusing on specific functionalities

## Features and Structure
   <pre>
1. Account Creation
  • Allows users to create a new account
2. Login
  • Allows users to log in
3. Main Feed
  • Presents the user's main feed with infinite scroll functionality
4. Account Deletion
  • Enables users to delete their accounts
5. Account Information Modification
  • Provides a page for users to modify their account information
6. New User Recommendations
  • Recommends new users to the current user
7. Followers
  • Shows the list of followers for a user
8. Following
  • Displays the list of users being followed by a user
9. Password Modification
  • Provides a page for users to modify their passwords
10. Post Detail
  • Shows detailed information about a specific post
11. User Page
  • Displays a page for a specific user
</pre>

## Technology Stack
<pre>
Server: Nginx
back-end: Python Flask
front-end: Javascript React
Database: SQLite3
Server Hosting: AWS EC2
   
Password Management: SHA-512 Algorithm
Infinite Scroll Implementation:
Utilizes pagination techniques and the React InfiniteScroll library
Deployed the project using AWS services such as EC2, Route 53, and Elastic Beanstalk
</pre>

## ER Diagram
![Minista_ERD](https://github.com/hyunkyu-Park/MINI_instagram/assets/68415173/b45194cc-41a8-44bb-97d0-0d61d5e7f4f0)

## Notes
The project started as server-side dynamic pages and refactored towards client-side dynamic pages.
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

Solution: Create random UUIDs using uuid.uuid4(.hex), change them to lowercase using pathlib.path(filename).suffix.lower() and save them (unifying by lowercase since not all environments are case sensitive)

## Page infinite loading issue
Situation: When user click a button depending on whether user follow or not, I wrote the code to change the status to Follow->Unfollow or Unfollow->Page. But Infinite Loading occured

Cause: Implemented function call not function reference <br>

Solution:  
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

Solution: 
I tried to check all the codes from the time when the server-side code was called to the time when it was terminated.
But I could not recognized that the return statement was wrong, so it took time to resolve the error. I learned that just because it's familiar to me, it's not the right code.  
When refactoring code, I should always observe that there is no conflict between the old code and the updated code, and the existing design. 
It would be more effective to check the pieces in advance that could cause conflicts when designing before writing the actual code.

## Query for create_like 

Situation: Error occurs when users cancel like and press like again

Cause: Wrong Query logic, my code check if the user likes the post in the javascript and it checks in the api endpoint.

Solution: Before writing the code in the future, let's distinguish between what JavaScript will solve and what will be solved using sql. Let's also think about which one would be more efficient!


## User experience improvement -- user feedback 1

Situation: Sometimes, the main page takes few seconds two render the page

Cause: When image files are large or the internet connection is not good, it takes time to fetch multiple post images, resulting in a poor user experience.

Solution: Applying loading="lazy". It optimizes performance by delaying the loading of elements until the user scrolls to the image or element, which can reduce the initial page loading time and reduce data usage, providing a better experience for the user.

++Additional update(03/25/2024)  
Display a mosaic-style background instead of showing loading text when the main page is loading for the first time.  

1. Create Placeholder Elements:  
Design placeholder elements that resemble the layout of posts, including images, titles, and other relevant information.
2. Render Placeholder Elements During Initial Loading:  
While the main page is loading for the first time, render these placeholder elements instead of actual post content.  
3. Replace Placeholder Elements with Actual Content:  
Once the actual post content is loaded, replace the placeholder elements with the real posts dynamically.

During the gif file conversion process, it changed slower than the actual speed (actual user experience is about 3 times faster)  
![Screen Recording 2024-03-25 at 9 43 51 PM](https://github.com/hyunkyu-Park/MINI_instagram/assets/68415173/b7eb537f-8532-41d0-bb31-ae34306cca45)


※ Studying transition and see if it can resolve this issue  

## User experience improvement -- user feedback 2

Situation: When creating an account for the first time, the main page feels empty, giving a dull impression.

Cause: There is no content to display on the main page when there are no users being followed or when there are no posts from the user and the users being followed.

Solution: In case there are no posts to display on the main page, redirect the user to the explore page to naturally encourage interaction with other users and improve user experience.

## User experience improvement -- user feedback 3

Situation: The password criteria for creating an account and for modifying the password afterward are different. It would be better if the password requirements are visible.

Solution: 
1. Modify Password Change Page:  
• Increase the font size for better readability.  
• Add text to indicate the password requirements.  
2. Update Error Handling:  
• Handle different types of errors returned from the API when changing the password.  
• Display corresponding error messages for each type of error.  

## User experience improvement -- user feedback 4

Situation:
Feedback has been received that the elements on the login and account creation screens are too small and uncomfortable.

Cause:
The elements are too small, making it difficult for users to perceive text or input fields.

Solution:
Increased the font size to make the elements appear larger and more visible.

## User experience improvement -- user feedback 5

Situation:
When the user posts a new post, the timestamp doesn't match.

Cause: sqlite3 server time is based on UTC, resulting in a created time that doesn't match the user's time zone.

Solution: Convert the user's time zone to UTC and then apply fromNow.

## User experience improvement -- user feedback 6

Situation:
It would be nice to have a button to show the entered password while entering it.

Solution: Create a toggle switch for showing password visibility using toggle password visibility.

## User experience improvement -- user feedback 7

Situation: Requirement for each post to be visually distinguished from one another.  

Solution: Added small spaces between each post to visually separate them.  

Situation: Each post's image had different sizes, causing them to not appear uniformly.  

Cause: The images were displayed at their own sizes without regard to the width and height of the parent container, .user_posts. This led to inconsistency in the aspect ratios of the images, resulting in an inconsistent appearance among the posts.  

Solution: Updated CSS to set the width and height of the .user_posts container, ensuring that the images are displayed uniformly. Additionally, I added small spaces between each post to visually separate them, meeting the requirement for visual distinction between posts.  

## No image file being called on server

Situation: When running the code on AWS EC2, the website was unable to find image files.

Cause: The issue occurred because the Nginx web server configuration file ('/etc/nginx/conf.d/minista.conf') was configured to check '/accounts/auth' when accessing the '/uploads' route. However, in the actual code, a different API name was used. As a result, with each GET request for an image file, an unspecified API was continuously called, leading to a 500 server error on the web page and a GET /accounts/auth 404 error in the Flask log.

Solution: Initially, I thought that the issue is my lack of experience with AWS because the code worked fine in my local environment. I spent the first three days searching through all AWS-related documentation but couldn't find any relevant information. Afterward, I started examining Flask server logs and discovered a different error being triggered than what was expected on the website. Even though my code does not have api called '/accounts/auth' but the server was trying to call it. I tracked where the relevant function was called and I was able to find it in the config file

This experience underscored the importance of comprehending the logic and functions employed in any code, irrespective of one's familiarity with it. I gleaned the lesson that it is imperative to document and understand the overall logic of a codebase before deploying it.


## User experience improvement -- user feedback 8

Situation: When the user name is long, it is displayed vertically in the post, affecting readability.  

Cause: The CSS styles were tested only in an environment with short English user IDs, leading to vertical display issues when longer names were displayed in different languages.  

Solution: After testing with expanded data, it was confirmed that the styles did not apply as expected. Additional scenarios were considered, and the styling was modified accordingly by dividing and addressing each section.  

## User experience improvement -- user feedback 9

Situation: Errors related to account creation are only displayed as 'existing username'.

Cause: I thought the only error that could occur was "duplicate record errors" but I unexpectedly encountered a 413 error.  
[nginx] 413 Request Entity Too Large Error: When using nginx as a reverse proxy, if user try to upload a large file, user may encounter a 413 Request Entity Too Large error message.  

Solution: I adjusted the client_max_body_size setting. client_max_body_size limits the size of requests that can be sent. The default value is 1MB. Requests cannot exceed the value set here in the Content-Length header. Although it can limit the size of requests such as POST or PUT, it is typically used to prevent malicious attempts to fill up the disk by uploading excessively large files.  

## Security vulnerabilities issue

Situation: need for security measures to prevent malicious code injection.

Solution:  
Using special character filtering and regular expressions to validate input data, and employing parameterized queries to protect against attacks such as SQL injection.  
Regularly utilize security check services to inspect website security.  

++Additional update(04/07/2024)  
Situation: Identified security vulnerabilities related to cookies using a website security verification service.

Solution:  
Use SESSION_COOKIE_SECURE = True, to enhance cookie security.  
Set SESSION_COOKIE_HTTPONLY = True, to protect against XSS attacks.  
Configure SESSION_COOKIE_SAMESITE = 'Strict', to prevent cookies from being sent to other sites.  

## User experience improvement -- user feedback 12

Situation:  
1. The font is unclear, making it difficult to read the code.  
2. When clicking on links, the font color changes, which is visually unappealing.  

Causes:  
1. The default font choice lacks attractiveness and does not engage the reader effectively. 
2. Clicking on links triggers a change in font color based on default settings, leading to an inconsistent and unappealing interface.

Solution:  
1. Use a clear and easy-to-read font when providing code to improve readability.  
2. Remove the feature that changes font color upon clicking links, maintaining a consistent interface with the default font color.  

## User experience improvement -- user feedback 13
applying crop function

## User experience improvement -- user feedback 14 (update: 04/14/2024)

Situation: requiring a photo input during signup is cumbersome.

Solution:  
Frontend Side (Client):  
1. If the user doesn't select a file, extract the username from the user input field.  
2. Send an HTTP request to the server with the extracted username data.  

Backend Side (Server):  
1. Receive the username data from the frontend.  
2. Generate a profile picture based on the received username using pillow library.  
3. Save the generated profile picture on the server.  

This approach streamlines the signup process by allowing users to proceed without uploading a photo, with a profile picture automatically generated based on their username.  

## Error handling update --  
update: 04/15/2024  
1. error handling update for create account && changePasswordPage  
2. Start creating an error handling function that deals with commonly occurring errors

update: 04/20/2024  
1. followers & followings get error handling  
2. user_account errors

## Update - Dark Mode : 05/18/2024
![Screen Recording 2024-05-18 at 7 43 27 PM](https://github.com/hyunkyu-Park/MINI_instagram/assets/68415173/69f27239-9a7c-4f31-8d90-6e4293f5fdac)

### add transition option: 05/19/2024
![Screen Recording 2024-05-19 at 3 20 43 PM](https://github.com/hyunkyu-Park/MINI_instagram/assets/68415173/8c6d5daa-aae6-4ca6-a2e8-064b618350d6)

## Update - User search based on ID: 05/20/2024
Situation: As the number of users increased, I anticipated the need for an ID-based search functionality and implemented it.  

Implementation: I used the filter and includes functions to filter and store search results based on user input.

Issues Encountered:  

   - Problem: Initially, I stored users who were not being followed in the notFollowing state. I attempted to update notFollowing with search results, but this led to the issue where applying further filters on the filtered results prevented maintaining the initial notFollowing data.  

   - Cause: The notFollowing array was being overwritten with search results, so the initial state could not be preserved.

   - Solution: To resolve this, I stored the filtered results in a separate state variable filteredPeople.

Changes Made:

   - The notFollowing array retains the initial data.
   - The filtered results are stored and used from the filteredPeople array.
   - This approach allowed us to preserve the initial data while rendering the filtered results.
   - 
![Screen Recording 2024-05-21 at 1 58 38 PM](https://github.com/hyunkyu-Park/MINI_instagram/assets/68415173/040168d5-8630-4fbc-be22-cdfb3337142e)

### Additional update: 05/21/2024

   - Adding User ID Search Functionality to the Followers Page
   - Adding User ID Search Functionality to the Following Page

## 
