# CS Capstone Marketplace

## Synopsis

A marketplace for students/groups to find creative and challenging projects to work on. Projects will be provided by industry engineers.  

## CS390 Student Features

CS390 Students: Please refer to the [grading form](https://docs.google.com/document/d/1owkuHpkWHiZVTyX7PPE0SZMQ5wUxfQFdkWwn8CsJHo0/edit?usp=sharing) for most recent updates to these tasks.

- [x] Task 2 (10 pts): CommentsApp
  - [ ] Task 2 Bonus (5 pts): Add Nested Comments to CommentsApp
- [x] 3.1 (2 pts): Create “Teacher” model with profile (contact info, etc)
- [x] 3.2 (3 pts): Create “Engineer” model with profile (Alma Mater, About, Contact Info, etc)
- [x] 3.3 (8 pts): Complete “University” and “Class” models. All students should belong to 1 University, and can belong to multiple classes. Teachers should be able to manage who is enrolled in their class.
  - [x] 3.3.1 Allow teacher to add/remove students
- [x] 3.4 (5 pts): Groups: Students can create a group. Only group members may add additional members to the group. Only groups can be assigned to a project.
  - [x] 3.4.1 Only group members may add additional members to the group.
  - [x] 3.4.2 Only groups can be assigned to a project.
- [x] 3.5 (5 pts): Projects: Projects can be only created by engineer/corporate users. Projects have a list of qualifications, which are used for matching. Projects are visible to everyone.
  - [x] 3.5.1 Projects should be editable by users of the company which posted the project.
- [x] 3.6 (5 pts): Bookmarks: Create the “Bookmarks” model, which relates user_id and project_id.
  - [x] Add and implement a button on the project page to “Bookmark” a project.
  - [x] Add and implement a bookmark page or list.
- [ ] 3.7 (12 pts): Implement Matching System: Using group’s combined student properties, calculate suggested projects for the groups to choose.
- [x] 3.8 (15 pts): Group Profiles: Each group’s profile should include team member details and the project they opted for. Group members, their teachers, and the project corporate users may post comments on the group profile page, allowing discussion.
  - [ ] Group members, their teachers, and the project corporate users may post comments on the group profile page, allowing discussion.
- [x] 3.9 (10 pts): Deletion: Allow privileged users to delete groups, projects, classes, and comments.
  - [ ] Anyone can delete their own comments
  - [ ] Allow admin to delete any comments
  - [x] Allow admin to delete anything
- [x] 3.10 (10 pts): Use a WYSIWYG editor for any multi-line textarea (user profile about, group profile comments, etc). There are many WYSIWYG options available, just google “WYSIWYG editor”. One options is TinyMCE.
  - [x] Replace multi-line textarea with TinyMCE

- [ ] Robustness (5 pts): Did it crash?
- [ ] Easy To Use (5 pts): Could all tasks be performed with minimal steps?
- [ ] Presentation (5 pts)

# Extra Features

- [x] full-site search for University, Project, Company, Group and Course

## TA Features - Will not be provided

- [ ] Common Forms/Styling Across Site (Harris)
- [X] Alert Messages
  - [ ] Alert Messages for non-authentication modules (Harris)
- [ ] Authentication Module (Naman)
  - [ ] Change Password
  - [ ] Password Reset (sending email)
- [ ] Project Module (Harris)
  - [X] View Projects List
  - [ ] View Project
  - [ ] Create Project (Name, Description)
- [X] Company Module (Jacob)
- [X] University Model (Jacob)
- [X] Course Model (belongs to University)
- [ ] Groups Module
  - [ ] Advanced Group Profiles (Strengths, Weaknesses)
- [ ] Student model
  - [ ] Profile (Major, Year, Skills, Experience Resume, etc)

## Contributors

@harrischristiansen (http://www.harrischristiansen.com)  
@thenamanpat  
@dunbarj (http://www.jacobfdunbar.com)
