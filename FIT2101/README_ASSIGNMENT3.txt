Links for time tracking:
Trello: https://trello.com/invite/b/pWNL1t7B/bad59e6cc33b15f1f73075ccb43765f8/user-stories
GitLab: https://git.infotech.monash.edu/fit2101-malaysia-projects-2021/jkin0011/commits/master

We again built on the foundations that we created during our project inception for our time tracking by using Trello and Git. Each members are required to complete their assigned tasks for before the deadline
set in the Trello page. They must then move it to done once the tasks are done and it fulfills our definition of done as stated in the first assignment report. If you have any issues with access our files 
or Trello during marking feel free to email me (Product Owner) at : dyee0005@student.monash.edu or my personal email at darrenyee25@gmail.com. 

Steps to open the web application built by Flask using visual studio code.

1. Install python from the link: https://www.python.org/downloads/
2. At visual studio code, go to manage(wheel icon at the left most corner)-> Settings -> type "Edit in settings" at the searching bar -> Select "Edit in settings.json"
3. Replace the original code with the following piece of code of :
{
    "terminal.integrated.profiles.windows": {
        "PowerShell": {
          "source": "PowerShell",
          "icon": "terminal-powershell",
          "args": ["-ExecutionPolicy", "Bypass"]
        }
      },
      "terminal.integrated.defaultProfile.windows": "PowerShell",
    "emmet.excludeLanguages": [
        

        "markdown"
    ],
    "liveServer.settings.donotShowInfoMsg": true,
    "tabnine.experimentalAutoImports": true,
    "liveServer.settings.AdvanceCustomBrowserCmdLine": "",
    "mssql.connections": [
      {
        "server": "{{put-server-name-here}}",
        "database": "{{put-database-name-here}}",
        "user": "{{put-username-here}}",
        "password": "{{put-password-here}}"
      }
    ],
    "python.analysis.extraPaths": [
      "./sources"
    ],
    "notebook.editorOptionsCustomizations": null
    
}
4. Save and reopen the visual studio code.
5. Open the project folder with visual studio code. Make sure the directory path is currently on the correct folder of the project. 
6. Create new terminal and type the following command :"python -m venv env". Your project directory should now have one new folder call "env".
7. Press "Ctrl + Shift + ~" to create a new terminal. You should now see "(env)" in your terminal. "Ctrl + Shift + P" to select the Python interpreter(select the python in the env) if you are not able to use python command at the terminal. 
8. In the new terminal, install Flask by typing following command :"pip install flask". (Make sure you have downloaded your pip! It should come with installation of you python)
9. Now, try and install the pyrebase using command :"pip install pyrebase4" (Remember, should be pyrebase4 instead of pyrebase!)
10. After the installation, check whether you are in the web_app layer or not. If not you can cd until web_app with command of "cd .../.../web_app".
11. You need to run the last command of "python -m flask run" in your terminal.
12. There will be a link generated at the terminal. Follow the link and you will now open and reach our web application using web browser!
