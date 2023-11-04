## Functional Requirements
1. Create Account (User should be able to create an acocunt)
2. Sign up (Users should have the option to sign up for an account)
3. Create Notes (User should be able to create a new note)
4. Attach Files/images (User should be able to add images/files to their notes)
5. Search Notes (Users should be able to search for specific notes)
6. Delete Notes (The user should be able to delete notes from their account)
7. Edit Notes (Users should have the ability to make changes or updates to their existing notes)
8. *Connect with any external API (The app should allow to integrate external APIs to provide additional functionality or data)
9. Log Out (Users should be able to sign out of their accounts)
10. Share Notes (Users should be able to share their notes with other users)
11. Edit User Profiles (Users should be able to modify and update their user profiles)
12. *Advance search items with regular expressions (User should be able to perform advanced searches on their notes)
13. *Visualize note connections (Users should be able to visualize how their notes are related to each other)

## Non-functional Requirements
1. Multilingual Support (Support contents in multiple languages)
2. Account Verification (The system should implement secure and efficient account verification processes)

## Use Cases
### 1. Create Account
- **Author:** Rodrigo (@Rodarkhen)
- **Pre-condition:** 
  - User is not registered on the platform.
- **Trigger:** 
  - Users clicks on the "Sign Up" button.
- **Primary Sequence:** 
  1. User clicks "Sign Up"
  2. User is prompted to a new page
  3. User enters necessary personal information
  4. System validate information entered
  5. The system creates the account if it passes validation
  6. User can now access the platform
- **Primary Postconditions:**
  - User has now a registered account and can access the app.
- **Alternate Sequence:** 
  1. User enters invalid information (e.g., email format is incorrect).
  2. The system displays an error message.
  3. User fixs the information.
  4. User clicks the "Create Account" button again.
   
### 2. Sign up
- **Author:** Nikola
- **Pre-condition:**
  - ...
- **Trigger:**
  - ...
- **Primary Sequence:** 
  1. ...
  2. ...
- **Primary Postconditions:**
  - ...
- **Alternate Sequence:** 
  1. ...
  2. ...
 
### 3. **Create Notes**
- **Author:** Anik (@AnikBudhathoki)
- **Pre-condition:** 
  - The user must be logged into their personal account.
- **Trigger:**
  - The user clicks the create new note option.
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
  
### 4. Attach Files/Images
- **Author:** Anik (@AnikBudhathoki)
- **Pre-condition:** 
  - The user must be logged into their personal account and on an existing note they want to edit.
- **Trigger:**
  - The clicks the "Attachments" option.
- **Primary Sequence:**
  1. The user clicks attach files option
  2. The system prompts the user with a file-picking dialogue
  3. User selects the files/images they want and clicks submit
  4. The system validates and uploads files onto notes
  5. The system prompts the user with a message validating if the upload was successful
- **Primary Postconditions:**
  - The user's notes are saved under their account
- **Alternate Sequence:**
  1. System prompts the user with an error message relating to image/file upload
  2. User presented the option to select another file for uploading
  3. The user selects files again and step v of the primary sequence is repeated

### 5. Search Notes
- **Author:** Rodrigo (@Rodarkhen)
- **Pre-condition:**
  - The user is logged into their account.
- **Trigger:**
  - The user initiates a search action from the search bar.
- **Primary Sequence:** 
  1. User enters search keywords or criteria in the search bar.
  2. The system looks for notes that match the search terms in the database.
  3. The system displays a list of matching notes in the search results.
  4. User can click on a search result to view the full note.
- **Primary Postconditions:**
  - The user is presented with a list of notes that match the search criteria.
- **Alternate Sequence:** 
  1. User enters search keywords, but no matching words are found.
  2. The system displays a not-found message.
   
### 6. Delete Notes
- **Author:** Anik (@AnikBudhathoki)
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
- **Alternate Sequence 1:**
  1. User decides not to proceed with their deletion and presses the "Cancel" option
  2. The system returns the user back to the note viewing page
- **Alternate Sequence 2:**
  1. System prompts an error during deletion(ex. server, database error) to the user
  2. A message is displayed to the user to try again later

### 7. Edit Notes
- **Author:** Nikola
- **Pre-condition:**
  - ...
- **Trigger:**
  - ...
- **Primary Sequence:** 
  1. ...
  2. ...
- **Primary Postconditions:**
  - ...
- **Alternate Sequence:** 
  1. ...
  2. ...

### 8. 
- **Author:** Nikola
- **Pre-condition:**
  - ...
- **Trigger:**
  - ...
- **Primary Sequence:** 
  1. ...
  2. ...
- **Primary Postconditions:**
  - ...
- **Alternate Sequence:** 
  1. ...
  2. ...

### 9. 
- **Author:** Nikola
- **Pre-condition:**
  - ...
- **Trigger:**
  - ...
- **Primary Sequence:** 
  1. ...
  2. ...
- **Primary Postconditions:**
  - ...
- **Alternate Sequence:** 
  1. ...
  2. ...
  
### 10. Share Notes
- **Author:** Rodrigo (@Rodarkhen)
- **Pre-condition:**
  - The user must be logged into their account.
- **Trigger:**
  - User clicks the "Share" button.
- **Primary Sequence:** 
  1. User selects a note they want to share
  2. User clicks the "Share" button
  3. The system generates a shareable link for the selected note
  4. User can copy and share the link with others through email or messaging apps
  5. Anyone with the link can view the shared note without needing an account
- **Primary Postconditions:**
  - The selected note is successfully shared with the recipient.
- **Alternate Sequence:** 
  - User enters an invalid or non-existent recipient email or username
  - An error message about the recipient's information is displayed
  - User must changes the correct recipient information to proceed with sharing

### 11. Edit User Profiles
- **Author:** Rodrigo (@Rodarkhen)
- **Pre-condition:**
  - The user is logged into their account.
- **Trigger:**
  - The user clicks "Account" to initiate profile edit action
- **Primary Sequence:** 
  1. User clicks on the "Account" or "Settings" option.
  2. User can modify personal information such as name, email, profile picture
  3. User saves the changes
  4. A confirmation message is shown that their profile has been updated.
  5. The system saves the new profile information on the database
- **Primary Postconditions:**
  - The user's profile is updated.
- **Alternate Sequence:** 
  1. User makes changes to their profile but decides to cancel.
  2. User clicks the "Cancel" or "Discard Changes" button.
  3. No changes is made.

### 12. Advanced search items with regular expressions
- **Author:** Rodrigo (@Rodarkhen)
- **Pre-condition:**
  - User is logged into their account.
- **Trigger:**
  - User clicks on "advanced search" bar.
- **Primary Sequence:** 
  1. User clicks the advanced search option.
  2. User enters a regular expression or search for a term in the search bar.
  3. A search using the regular expression or term is performed.
  4. A list of items that match the search criteria is displayed.
- **Primary Postconditions:**
  - The user is presented with a list of matched items.
- **Alternate Sequence:** 
  1. No matching items are found.
  2. A message is displayed indicating no results were found.

![Title](images/testImage.png)