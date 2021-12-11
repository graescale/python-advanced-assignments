# ANSWER the following questions:


## a) Why should you use git instead of Google Drive for your (teams) code?

While both programs allow for version control and collaboration, git has several advantages. Git allows users to create multiple branches to build new features while simultaneously modifying the main branch and then merging branches back into the main branch.

Although  Google Drive does have an offline mode, using it - I believe - can result in a fork that cannot be merged back into the online version if other collaborators have modified it. Git users can work offline, to a degree, without affecting their ability to later merge their updates into the main branch. Git also allows solo developers to work entirely offline, using a local repository.

Many editors also support plugins and extensions that provide git functionality


## b) What does "git add" and "git commit" do? What is the difference?

Git add stages files to be committed and git commit saves changes in the staged files to the repository.


## c) What is the difference between "git pull" and "git push"?

Git pull downloads changes from a remote repository and git push uploads changes to a remote repository


## d) What does the command "git checkout" do?
### What can you do if you cannot checkout because you have untracked files?

Git checkout changes the current branch.

If you have untracked files you could:
git add [files]
add the files to .gitignore
git clean [files] to remove them
git stash to record the current state of the messy directory with untracked files and return to a clean directory.


## e) When do you need branches?

Branches can be used to add and test features or to make major modifications to the existing code. I would imagine anything that isn’t a bug fix or an aesthetic change should be a branch
