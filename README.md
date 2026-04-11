# GRIM COMMANDS

**make**

Create a new note. Opens the system editor, unless another editor is set by seted.

**edit**

Edit an existing note's content by Name or ID.


**ls**

List all notes. Supports filtering by tags and sorting.

Options:

 -t list by tag

 -n sort by newest

 -o works with option -t or both -t and -n 
    displays only notes with the tag(s) provided


**show**

Display a note's content rendered as Markdown.


**rm**

Remove a note from the database permanently.


**retag**

Update the tags of a note without changing its content.


**rename**

Change the title of an existing note.


**cfg**

Display current configuration


**find**

Search notes using Full-Text Search (FTS5)


**export**

Export a note as a standalone .md file to the export path.


**seted**

set editor from a selection of supported editors

- vscode
- sublime
- nano
- vim
- default

# INSTALLATION

## 1.Requirements

- Python 3.8+
-**IMPORTANT**: During installation, make sure to check the box "Add Python to PATH".

## SETUP

-Download the source code (ZIP) and extract it to your preferred location
-Open your terminal and navigate to that folder (cd "path to your extracted folder")

## INSTALL GRIM

I recommend using pipx to install it as  global standalone command
Type these commands in that order
- pip install pipx
- pipx ensurepath
- pipx install .

## VERIFICATION
grim --help
