Carnegie Mellon University
Web Apps Development
Assignment 6 - make new posts appear through AJAX/Jquery page refreshing and add commenting.

External Resrouces:
Utilized the example code from the ajax-example and the jquery-example. In some cases, copy and pasted. Credits to Dr. Eppinger and TA's for the code. Also used a number of online resources to help with AJAX/Jquery, styling and debugging; stackoverflow.com, w3school.com, jquery.com, and the django online docs.

Additional Notes:
This webapp meets all requirements. I added the ability to comment to all posts, minus the post that appears through the automatic page refreshing. The frontpage refreshes every 5 seconds and shows only appends new posts. I also improved aesthetics with the bootstrap panels, really like how that looks now. I also fixed the picture issue from last week. One caveat, I haven't give the user the ability to remove a profile picture once they upload one. They can either keep their pic or upload a new one.

BUG REPORT:
1 - When the frontpage refreshes and a new post appears, the comment button does not work. I looked into this and it looks like it's source is how I create it with Jquery. Since it's serialized HTML, it isn't active. I'll research a solution over the next week and have that fixed for hw7.
