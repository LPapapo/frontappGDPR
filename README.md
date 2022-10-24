## Intro


#### Problem to be solved/ User story

Typeform is a platform that is used to create forms. User responses are collected.
Many times, a user can request that his response be deleted in order to delete some personal information, such as his email address.(GDPR oriented)
A lot of manual work is required due to the lack of a global user search within Typeform.
All emails must be copied and pasted into each form one by one.
This manual process takes a long time.




#### How is it currently solved?

A Python script is written to solve this problem.
A Typeform API access token is generated, and all emails that have requested deletion are placed as input.
When you run the script, all forms are searched and a report is generated.





### How to use it ?

1. Make sure that you have the API access token placed in the config file . 
2. While in the config file, you can change the response.deletion setting to true or false. If true, when it finds a requeried entry, it will be deleted automatically.
If set to false, it will only return the find result.(save the changes)![tyform0](https://user-images.githubusercontent.com/97594496/186655086-389981bf-a2e7-432a-9efe-a5db5830192a.png)
3. The next step is to open input.txt and copy all of the emails that need to be deleted into the txt file line by line.(save the changes)![typeform2](https://user-images.githubusercontent.com/97594496/186651169-9671abd5-854e-43db-8bf7-6e0fdd8a78d5.jpg)
4. Start the search by opening the typeformGDPR forlder in terminal and typing 'python typeformGDPR.py'.![typeform4](https://user-images.githubusercontent.com/97594496/186651586-2a0dcf66-a3b4-45da-b31f-ae2e533bceea.jpg)![typeform5](https://user-images.githubusercontent.com/97594496/186652473-37434f89-4343-4442-9677-98464527640d.jpg)
5.  After the search is finished, you can review the errors, logs, and results by opening the .txt files .
![typeform3](https://user-images.githubusercontent.com/97594496/186652589-4d2d3a9c-2acb-45d7-b289-d0aeca5be557.jpg)




