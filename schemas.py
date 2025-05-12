from pydantic import BaseModel

# Model for creating a note (Input)
class NoteIn(BaseModel):
    content: str  # The content of the note

# Model for returning a note (Output) with ID
class Note(NoteIn):
    id: int  # The ID of the note, inherited from NoteIn and added to the model

# Model for processing text request (Input for prediction)
class TextRequest(BaseModel):
    text: str  # The text that needs to be processed or predicted
