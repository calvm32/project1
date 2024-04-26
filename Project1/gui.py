from tkinter import *
from tkinter import messagebox

class Gui:
    def __init__(self, window):
        self.window = window
        self.candidates = {}
        self.voter_ids = {}
        self.choice = StringVar()

        # Label and button to add candidate for voting
        self.label_add_candidate = Label(self.window, text="Add Candidate:")
        self.label_add_candidate.pack(pady=10)
        self.entry_candidate = Entry(self.window)
        self.entry_candidate.pack(pady=10)
        self.button_add_candidate = Button(self.window, text="Add", command=self.add_candidate)
        self.button_add_candidate.pack(pady=10)

        # Start voting button
        self.button_start_voting = Button(self.window, text="Start Voting", command=self.start_voting, state=DISABLED)
        self.button_start_voting.pack(pady=10)

    # Function to add candidates
    def add_candidate(self):
        candidate = self.entry_candidate.get()
        if candidate and candidate not in self.candidates.keys() and candidate.isalpha():
            self.candidates.update({candidate: 0})
            self.entry_candidate.delete(0, END)
            self.button_start_voting.config(state=NORMAL)
        elif candidate in self.candidates.keys():
            messagebox.showwarning(title="Candidate already entered.", message= "Candidate already entered. Please enter a different candidate or start voting.")
        elif not candidate:
            messagebox.showwarning(title="Enter a candidate.", message= "Start typing the candidate's name and click Add.")
        elif not candidate.isalpha():
            messagebox.showwarning(title="Enter a candidate.", message= "Your candidate's name should only contain letters.")

    def start_voting(self):
        # Create a frame for ID entry
        self.id_frame = Frame(self.window)
        self.id_frame.pack(pady=10)

        # ID Label and Entry
        self.label_id = Label(self.id_frame, text='Enter 4-Digit ID:')
        self.label_id.pack(side=LEFT)
        self.entry_id = Entry(self.id_frame,width="8")
        self.entry_id.pack(side=LEFT, padx=10)

        # Total and individual votes label
        self.label_total_votes = Label(self.window, text="")
        self.label_total_votes.pack(pady=10)

        # Submit vote button
        self.button_submit_vote = Button(self.window, text="Submit Vote", command=self.update_votes)
        self.button_submit_vote.pack(pady=10)

        self.window.geometry('300x140')
        width = 300
        height = 140

        # Vote buttons
        for candidate in self.candidates:
            self.button_candidate = Radiobutton(self.window, text="Vote for {}".format(candidate), variable=self.choice, value=candidate)
            self.button_candidate.pack(pady=10)
            self.button_candidate.select()
            width += 20
            height += 40
            self.window.geometry('{}x{}'.format(width,height))

        self.label_add_candidate.pack_forget()
        self.entry_candidate.pack_forget()
        self.button_add_candidate.pack_forget()
        self.button_start_voting.pack_forget()


    def update_votes(self):
        if self.choice is not None and len(self.choice.get()) != '':
            candidate = self.choice.get()
            voter_id = self.entry_id.get()  # Get the entered voter ID
            
            if len(voter_id) == 4:  # Check if the length of voter ID is 4
                if voter_id not in self.voter_ids:  # Check if the voter ID is not already in the dictionary
                    self.voter_ids[voter_id] = candidate
                    if candidate:
                        self.candidates[candidate] += 1
                        votetext = ""
                        total = 0
                        for i in self.candidates:
                            votetext += "{} - {}, ".format(i, self.candidates[i])
                            total += self.candidates[i]
                        votetext += "Total - {}".format(total)
                        self.label_total_votes.config(text=votetext)
                    else:
                        messagebox.showwarning(title="No candidate selected.", message="Please select a candidate before submitting your vote.")
                else:
                    messagebox.showwarning(title="Already Voted", message="You have already voted.")
            else:
                messagebox.showwarning(title="Invalid ID", message="Please enter a 4-digit ID.")
        else:
            messagebox.showwarning(title="No candidate selected", message="Please select a candidate before submitting your vote.")
