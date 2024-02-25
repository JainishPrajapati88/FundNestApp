# FundNest

Welcome to FundNest - The All-in-One Platform for New Generation Startups!

## Overview

FundNest is a web platform that brings together startup founders, investors, and sellers, providing a comprehensive solution for the needs of new-generation startups. Whether you are seeking investments, mentorship, or looking to buy raw materials for your startup, FundNest has got you covered.

## Installation Setup
- **Installing dependencies:** pip install -r requirements.txt
- **To Run Project:** python app.py
## Features

- **Startup Registration:** Founders can easily register their startups on FundNest.

- **Investor Connection:** Connect with potential investors looking to support innovative startups.

- **Mentorship Opportunities:** Seek and provide mentorship to foster growth and success.

- **Seller Registration:** Register as a seller to offer products and raw materials to startups.

- **Product Marketplace:** Browse and buy products directly on the platform.

- **1:1 Meetings:** Schedule and conduct one-on-one meetings with investors or mentors.

## Problem it solves
- **Access to Funding:** FundNest connects startup founders with potential investors, addressing the common challenge of securing investment for innovative ideas and businesses.
- **Mentorship Opportunities:** Startups often require guidance and mentorship to navigate the complexities of the business world. FundNest facilitates the seeking and providing of mentorship, which is crucial for fostering growth and success.
- **Sourcing Raw Materials:** By allowing sellers to register and offer products and raw materials, FundNest helps startups in sourcing essential resources, which can be a significant challenge for new businesses.
- **Product Marketplace:** The platform also provides a marketplace for startups to browse and buy products directly, streamlining the procurement process.
- **Networking and Collaboration:** Through features such as 1:1 meetings, FundNest facilitates networking and collaboration opportunities, which are essential for the growth and development of startups.

## Technologies Used

- **Backend:** Python with Flask framework.

- **Database:** MongoDB.

- **Frontend:** Built with either Bootstrap or Tailwind for a modern and responsive user interface.

# DOCUMENTATION
## Overview:

This Flask application serves as a comprehensive web platform catering to startups, investors, and wholesale suppliers.
It offers various functionalities including user authentication, profile management, post management, product management, order management, and communication with users and admins.
The application utilizes MongoDB for data storage and includes email functionality for sending notifications and invitations.

## Responsive Designs:
The frontend of the application is designed using Bootstrap, ensuring a responsive layout that adapts well to different screen sizes and devices.

## Routes:
**1. Index Route ("/"):** 

Renders the index.html template. This page will be the main site which will be opened when you open the link to our website .
And when you scroll down you will get 4 options regarding login , signup , posts and contact-up page .  



**2. Signup Route ("/signup"):** 

Renders the signup.html template. once you go to the signup page you will be provided options for entering your first name, last name , email, username , password and lastly your occupation in which you are given 3 options and you need to choose between start up founder , investor and wholesale supplier .
And every time you sign in you need to have different email address and different usernames . You can not use same ones mutliple times 



**3. Startup Info Route ("/startup_info/<user_name>"):** 

Renders the startup_info.html template for providing additional startup information. Handles the form submission to update the database with startup information.



**4. Seller Info Route ("/seller_info/<user_name>"):** 

Renders the seller_info.html template for providing additional seller information. Handles the form submission to update the database with seller information.



**5. Investor Info Route ("/investor_info/<user_name>"):**

Renders the investor_info.html template for providing additional investor information. Handles the form submission to update the database with investor information.


**6. Home Route ("/home"):**

- Renders the home.html template with user-specific data and posts.
  
-Navigation Bar (Navbar):

The template includes a navigation bar that collapses into a toggle button on smaller screens.
It contains links to various sections of the application, such as Profile, LogOut, Add Post, YourPosts, Notifications, Add Products, Delete Products, Update Products, and Orders.
The visibility of certain links is conditionally rendered based on user roles (e.g., is_seller) and conditions (e.g., not investor).

-Welcome Message:

Displays a welcome message with the user's first and last name.

- Posts Container:

Iterates over a list of posts and displays each post in a container.

- Each post container includes:

The username of the post author . Title and description of the post . An image (display picture) associated with the post, encoded in base64 format.

- Dynamic Content Rendering:

The template uses Jinja templating syntax ({{ ... }}) to dynamically render content, such as URLs, usernames, post titles, descriptions, and images.


**7. Notifications Route ("/Notifications"):**

Renders the notifications.html template with notifications specific to the logged-in user. Requires user authentication.
Notification Display: Notifications are displayed inside a loop using {% for notification in Notifications %}. This loop iterates over the list of notifications passed to the template. Each notification is displayed in a separate <div>.


Notification Details: Inside each notification <div>, the following details are displayed:
	- MailID: This displays the email ID associated with the notification.
	
 - Date: This displays the date of the meeting request.
	
 - Time: This displays the time of the meeting request.
Overall, this template provides a simple and clean interface for users to view their notifications, with each notification displayed prominently along with its details. The styling ensures that the notifications are presented in an organized and visually appealing manner


**8. RequestingForMeeting Route ("/RequestingForMeeting"):**

Handles the request for a meeting by sending an email invitation to both the users.
github link : https://github.com/Nakshishah31/Fundnest-_video-call-web-rtc
A Flask application with a chatroom functionality using Flask-SocketIO for real-time communication between clients. 
Flask Application Setup:
You've initialized a Flask application and set a secret key for session management.
Initialized Flask-SocketIO and set it up with the Flask application.

- Routes:

/: Renders the home page where users can enter a custom room name to join.
/room/<string:room_id>/: Renders the chatroom page where users can chat. Users need to specify a room ID to join the chatroom.
/room/<string:room_id>/checkpoint/: Renders a page where users can enter their display name and choose to mute/unmute their audio and video before joining the chatroom.

- SocketIO Events:

connect: Triggered when a new socket connection is established.
join-room: Triggered when a user joins a specific room. Handles joining a room, registering the user's SID to the room, broadcasting the new user's connection to others in the room, and updating the user list.
disconnect: Triggered when a socket disconnects. Handles removing the user from the room and updating the user list.
data: Triggered when data is received from a client. This is likely used for passing chat messages or other data between clients.

- HTML Templates:

home.html: The home page template with a form for entering a room name to join.
chatroom.html: The chatroom page template with video chat functionality, including buttons for muting audio/video and ending the call.
chatroom_checkpoint.html: The template for entering display name and choosing audio/video options before joining the chatroom.

- JavaScript Files:

chatroom_ui.js: Contains client-side JavaScript code for the chatroom UI.
chatroom_networking.js: Contains client-side JavaScript code for handling networking and communication with the server.

- CSS Files:

style.css: Custom CSS styles for styling the HTML templates.
chatroom.css: Custom CSS styles specific to the chatroom functionality.
chatroom_checkpoint.js: Contains client-side JavaScript code for handling display name input and audio/video options before joining the chatroom.
Your application provides a basic video chat functionality where users can join specific chat rooms, communicate in real-time, and customize their audio/video settings before joining the chatroom. The use of Flask-SocketIO allows for seamless real-time communication between clients. If you have any specific questions or need further clarification on any part of the code or functionality, feel free to ask!


**9. Profile Route ("/profile/<user_name>"):**

Renders the profile.html template with user-specific information. Allows users to view and update their profiles. Requires user authentication.

- User Information Display:

Users can see their profile information such as first name, last name, and occupation.
If the profile is not in read-only mode, users can edit their profile information.

- Profile Picture:

Users can upload or change their profile picture.

- Additional Information:

Depending on the user's occupation (startup founder, investor, or seller), additional specific information fields are displayed. Users can update these additional information fields if the profile is editable.

- Request for Meeting:

If the user is an investor, they can request a meeting to startup by selecting a date and time.

- File Upload:

Users can upload images for their profile picture or other relevant images.



**10. UpdatingProfile Route ("/updatingProfile"):**

Handles the form submission to update user profiles. Requires user authentication. 



**11. AddPost Route ("/AddPost"):**

Renders the AddPost.html template for adding new posts.

- Title Field: Users can input the title of their post.

- Description Field: Users can input the description of their post.

- Image Field: Users can upload an image to accompany their post.


**12. AddIngPost Route ("/AddIngPost"):**

Handles the form submission to add new posts to the database.


**13. Posts Route ("/YourPosts"):**

Renders the posts.html template with posts specific to the logged-in user. Requires user authentication.
Here you can view all the post you uploaded . 


**14. DeletingPost Route ("/deletingPost"):**

Handles the deletion of posts.

- List of Products: Users can see a list of products displayed on the page. Each product is presented with details like name, description, product ID, price, seller, and field.

- Delete Button: For each product, there is a "Delete" button. Users can click this button to delete the corresponding product from the system
Overall, users can easily navigate through the list of products and delete them as needed, with clear feedback provided in case of any errors. The page maintains a clean and user-friendly interface for managing product deletions within the application.


**15. Login Route ("/login"):**

Renders the login.html template for user login.

It creates your session every time you login with correct email and password .


**16. Logout Route ("/logout"):**

Logs out the user and redirects to the login page.
This will destroy your session .


**17. Add Product Route ("/add_products"):**

Renders the add_products.html template for adding new products.

This HTML template provides a user-friendly form for adding a product. Here are the main things included from a user's perspective:

- Title: The page title "Add Product" clearly indicates the purpose of the page.

- Form Fields:\
  
	-Product Name: Allows users to enter the name of the product.
  
	-Description: Provides a textarea for users to describe the product.

  -Product ID: Allows users to specify a unique identifier for the product.

  -Price: Enables users to input the price of the product.

  -No Code Payment Link: Allows users to input a link for a no-code payment solution.

  -Filter by Field: Presents a dropdown menu for users to select the category or field the product belongs to.

  -Error Message Display: If there's an error during the form submission (e.g., duplicate product ID), an error message will be 	 displayed to inform the user about the issue.

  -Submit Button: A visually prominent "Submit" button allows users to submit the form once they've filled in the necessary details.
  
Overall, this template simplifies the process of adding a product by providing clear labels, input fields, and a straightforward submission mechanism, enhancing the user experience.


**18. Update Products Page Route ("/update_products"):**

Renders the update_products.html template for updating existing products.

This HTML template is for the "Update Products" page of a web application. Here's a brief overview of what users experience and care about when interacting with 
this page:

- Title and Styling: The page has a title "Update Products" and includes a CSS file ("add_products.css") for styling.

- Product List: It displays a list of products retrieved from the server.

- Error Message: If there's an error message (e.g., product not found or unauthorized access), it's displayed to the user.

- Product Details: For each product, it shows details such as name, product ID, price, supplier, and field.

- Update Button: A button is provided for each product to initiate the update process.

- Interactivity: Users can click on the "Update" button to navigate to the update form for the corresponding product.

Overall, users can easily view a list of products and initiate the update process for any specific product they choose, facilitating efficient management of product data within the application.


**19. Delete Product Page Route ("/delete_product"):**

Renders the delete_products.html template for deleting existing products.
This HTML template is designed to display a list of products and provide the functionality to delete them. Here are the main things included in this template from a user's perspective:

- Title: The title "Delete Products" indicates the purpose of the page.

- Product List: The template displays a list of products. Each product is represented as a list item with its name, description, product ID, price, seller, and field.

- Delete Button: For each product, there is a "Delete" button. Clicking this button triggers a form submission to delete the corresponding product.

- Error Message: If there's any error message passed from the server-side, it will be displayed above the product list.

Overall, this template provides a user-friendly interface for viewing and deleting products, making it easy for users to manage their product inventory.


**20. Products Route ("/products"):**

Renders the products.html template with all products or filtered by a specific field.
This HTML template is for displaying a list of products with an option to filter them by field. Here are the main things included that users experience and care about:

- Product Listing: Users can see a list of products with details such as name, description, product ID, price, and seller.
- Filtering: Users can filter the products based on their field/category using a dropdown menu.
- Ordering: Users can order a product by specifying the quantity and clicking the "Order" button. This action submits a form to 	 the server.
Overall, this template provides users with a simple and intuitive interface to browse and order products based on their preferences.


**21. Submit Order Route ("/submit_order"):**

Handles the submission of orders.
It lets you enter the quantity you want .
When you will order any product it will redirect you to the payment gateway link which the supplier has provided .


**22. Privacy Policy Route ("/privacy_policy"):** Renders the privacy_policy.html template.


**23. Contact Route ("/info"):**

Renders the contact_us.html template for users to send messages to the admin.
This Flask application includes a "Contact Us" feature where users can submit their queries or issues to the admin. Here's a breakdown of what this feature offers to users:

- Submission Form: Users can fill out a form with the following fields:
  
	-Email address
	-Name
	-Phone number
	-Subject
	-Description

- Submission Handling: Upon submitting the form, the application captures the form data and sends it to the backend for processing.

- Feedback Confirmation: After successful submission, users receive feedback confirming that their message has been sent to the admin.

- Email Notification: The application sends an email notification to the admin containing the user's submitted information, including email address, name, phone number, subject, and description of the issue.

- Error Handling: The application may include error handling to ensure that all required fields are filled out before submission.
Overall, this "Contact Us" feature provides users with a straightforward way to communicate with the admin, report issues, or ask questions, enhancing their experience by offering a direct channel for feedback and support.


**24. About Us Route ("/AboutUs"):**

Renders the About.html template providing information about the application.
This page gives you details of all 4 admins who are the developers of this website and the one who got this idea and wanted to implement it for the betterment of all the young struggling startup owners 


### Each route handles specific functionalities related to user authentication, profile management, post management, product management, order management, and communication with users and admins. The application also utilizes MongoDB for data storage and includes email functionality for sending notifications and invitations.
