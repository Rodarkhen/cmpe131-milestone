## Functional Requirements
1. requirement <should be 1 sentence that describes requirement>
2. requirement
3. Create Notes (The user should be able to create a new note)
4. Attach Files/Images (The user should be able to add images/files to their notes)
5. requirement
6. Delete Notes (The user should be able to delete notes from their account)
7. requirement
8. requirement
9. requirement

<using the syntax [](images/ui1.png) add images in a folder called images/ and place sketches of your webpages>

## Non-functional Requirements
1. non-functional
2. non-functional

<each of the 14 requirements will have a use case associated with it>
## Use Cases <Add name of who will write (this specific requirement) and implement (in subsequent milestones) the use case below>
3. **Create Notes**
- **Pre-condition:** 
    - The user must be logged into their personal account.
- **Trigger:**
    - The user clicks the create new note option
- **Primary Sequence:**
  1. User clicks the "New Notes" option in the webpage
  2. User is presented with a blank note-taking template 
  3. User enters information in the title field and the contents field
  4. User clicks the "Save" button
  5. User enters name of the save
  6. System validates the notes to make sure all fields are entered (ie. Make sure title field is not missing)
  7. System prompts message stating the save was successful

- **Primary Postconditions:**
    - The user's notes are saved under their account
- **Alternate Sequence:** <you can have more than one alternate sequence to
describe multiple issues that may arise and their outcomes>
  1. System presents an error message prompting user to fill out missing information (ie. Title name)
  2. User presented option to type in missing fields
  3. System validates notes again to make sure all fields are entered properly
  
4. **Attach Files/Images**
- **Pre-condition:** 
    - The user must be logged into their personal account and on an existing note they want to edit
- **Trigger:**
    - The clicks the "Attachments" option
- **Primary Sequence:**
  1. The user clicks attach files option
  2. The system prompts the user with a file-picking dialogue
  3. User selects the files/images they want and clicks submit
  4. The system validates and uploads files onto notes
  5. The system prompts the user with a message validating if the upload was successful


- **Primary Postconditions:**
    - The user's notes are saved under their account
- **Alternate Sequence:** <you can have more than one alternate sequence to
describe multiple issues that may arise and their outcomes>
  1. (5a) System prompts the user with an error message relating to image/file upload
  2. (5b) User presented the option to select another file for uploading
  3. (5c) The user selects files again and step v of the primary sequence is repeated

5. **Delete Notes**
- **Pre-condition:** 
    - The user must be logged into their personal account and on an existing note they want to edit
- **Trigger:**
    - The clicks the "Delete" option
- **Primary Sequence:**
  1. The user selects the note they wish to delete from their collection of notes
  2. The user clicks on the "Delete" button
  3. The system prompts a message asking user to confirm their deletion action
  4. The user confirms their selection
  5. The system deletes the note from user's registered account
  6. System confirms that the note has been successfully deleted and provides a message to the user


- **Primary Postconditions:**
    - The note is deleted from the users account
    - The note no longer shows up in the users collection of notes
- **Alternate Sequence:** <you can have more than one alternate sequence to
describe multiple issues that may arise and their outcomes>
  1. (4a) User decides not to proceed with their deletion and presses the "Cancel" option
  2. (4b) The system returns the user back to the note viewing page

- **Alternate Sequence:** <you can have more than one alternate sequence to
describe multiple issues that may arise and their outcomes>
  1. (6a) System prompts an error during deletion(ex. server, database error) to the user
  2. (6b) A message is displayed to the user to try again later
