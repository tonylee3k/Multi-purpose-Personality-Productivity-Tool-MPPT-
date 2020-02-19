# Multipurpose Personal Productivity Tool (MPPT)

## Applicaiton built with Python using the following *main* libraries
1. **PyQt5** - for the app's GUI interface
2. **PyQtWebEngine** - for the app's built-in mini browser
3. **sqlite3** - for the built-in database management system to manage inputs from different users

## Application Description
The Multipurpose Personal Productivity Tool is an all-in-one mini-tools in a single computer
application that covers multiple common productivity enhancing computer programs. It allows
the user to employ this single application to accomplish several tasks encompassing ***note-
making***, ***events-planning*** and ***budget-tracking***.

## Objectives
1. Enhance individual’s productivity
2. Bridge several computer programs into a single application to avoid confusion while
using different programs
3. Enable better planning of events and decision making when dealing with time and
budget
4. Keep track of future and previous planning of events
5. Reduce paper wastage for productivity-oriented tasks

## Scope
**MPPT** will consists of several programs listed below, with each having separate purposes:

### Budget Tracker
> Budget Tracker will enable users to record their expenses and profits on a daily basic. Users
can access to their previous record and they are given an option to analyse their financial record
to calculate their ending balance for each month to check whether if they have the budget to
make certain purchases. The Budget Tracker may not be able to perform extensive analysis as
in-depth financial knowledge is not applied into the program.

### Alarm
> The built-in alarm program allows users to set multiple alarms. The Alarm will notify the users
with a sound when the time and date is met, with the details of the alarm being displayed in a
message box. The Alarm may not be able to sound when the users have their volume muted.

### Calendar
> The calendar program enables users to view the calendar with the option to insert details for
events planning. Hilighting of the selected dates with input details are included. The calendar’s user interface may fail to meet users’ preferences.

### Memo
> Users could use this Memo program to electronically jot down notes or messages for
themselves. The font style and fonts are fixed so users may find it uninteresting.

### Mini Browser
> A built-in browser that has identical functionalities as Google Chrome. Users can quickly surf
the web while using the application without the need to open the actual Google Chrome itself.
The only downside of this browser would be its dependencies on HTML5 which means it won’t
load some types of video format available on the internet.

### Other Features Included
1. CRUD implementation with sqlite3 embedded database.
2. Website-like appearances with local sign-up/login system.
3. Concurrent usage of all different programs allowed by default. 
4. Easy-access dashboard on the left pane to switch between programs.
5. Beautiful Home page that shows current datetime.

# Additional Features yet to be implemented
1. A **Setting** page that allow user to
    1.update/change his/her userID, userName and userPassword
    2.add, remove, change the wallpaper in login page and home page
2. Advance-budget analyzer
    1.provide visual representation of current month's expenses using matplotlib
    2.provide extimated maximum expense left for current month


