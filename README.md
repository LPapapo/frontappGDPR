## Intro


#### Problem to be solved/ User story

Frontapp is a email client service . All emails from different email addresses are gathered in the Team inboxes.
Many times, a user requests that his personal data and all of his personal information, such as his email address, Github handle, and so on, be removed (GDPR oriented)
A lot of manual work required.
All emails must be copied and pasted one by one to search the Team inboxes, and then copied and pasted again to search the trash inboxes.
This manual method is time-consuming.




#### How is it currently solved?

A Python script is written to solve this problem.
A Frontapp API access token is generated, and all emails that have requested deletion are placed as input.
When you run the script, all team inboxes and trash inboxes are searched and a report is generated.





### How to use it ?
(Make sure you have 'Python' and 'requests' module installed (run in cmd 'pip install requests')
1. Make sure that you have the API access token placed in the config file . 
2. The next step is to open input.txt and copy all of the emails that need to be deleted into the txt file line by line.(save the changes)
3. Start the search by opening the frontappGDPR forlder in terminal(cmd) and typing 'python frontappGDPR.py'.
4. After the search is finished, you can review the errors, logs, and results by opening the .txt files .
5. All search results are tagged in Frontapp as marked-for-deletion and placed in Trash inbox
6. Select all and choose permantly delete .

Because the Front API does not support the state 'destroyed' in order to automatically permanent delete the results, you must manually permanent delete them at the end.





