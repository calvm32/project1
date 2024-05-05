from tkinter import *
from tkinter import messagebox
import csv
import sys
import os

class Gui:
    '''
    Class to represent Tkinter Graphical User Interface
    '''
    def __init__(self, window):
        '''
        Window constructor to initialize GUI
        :param window: initializes the window
        '''
        # Window
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

    def add_candidate(self):
        '''
        Adds candidate names entered by the user to a list for voting
        '''
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
        '''
        Sets up the screen for user to start voting by removing previous Tkinter elements and adding new Tkinter elements
        '''
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

        width = 300
        height = 260
        self.window.geometry('{}x{}'.format(width,height))

        # Vote buttons
        for candidate in self.candidates:
            self.button_candidate = Radiobutton(self.window, text="Vote for {}".format(candidate), variable=self.choice, value=candidate)
            self.button_candidate.pack(pady=10)
            self.button_candidate.select()
            width += 20
            height += 40
            self.window.geometry('{}x{}'.format(width,height))

        # Button to end voting display CSV contents
        self.button_end_voting = Button(self.window, text="End voting", command=self.end_voting)
        self.button_end_voting.pack(pady=10)
        
        # Creates a button for the user to restart the program with a new list of candidates
        self.button_restart_program = Button(self.window, text="Restart", command=self.restart_program)
        self.button_restart_program.pack(pady=10)

        # Removes previous Tkinter elements
        self.label_add_candidate.pack_forget()
        self.entry_candidate.pack_forget()
        self.button_add_candidate.pack_forget()
        self.button_start_voting.pack_forget()

        # Fill in total and individual votes label with each value is 0
        votetext = ""
        for i in self.candidates:
            votetext += "{} - 0, ".format(i)
        votetext += "Total - 0"
        self.label_total_votes.config(text=votetext)

    def update_votes(self):
        '''
        Updates a label to display the current individual and total vote counts
        '''
        # Check if user has chosen a value
        if self.choice is not None and len(self.choice.get()) != '':
            candidate = self.choice.get()
            voter_id = self.entry_id.get() 
            # Check if the length of voter ID is 4
            if len(voter_id) == 4:  
                # Check if the voter ID is not already in the dictionary
                if voter_id not in self.voter_ids:  
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

        # After updating votes, write to csv
        self.write_to_csv()

    def write_to_csv(self):
        '''
        Now write voter ID and candidate voted for to a csv file
        '''
        with open('votes.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Voter ID', 'Voted For'])
            for voter_id, candidate in self.voter_ids.items():
                writer.writerow([voter_id, candidate])

    def set_candidates(self, candidates):
        '''
        Sets the candidates list
        '''
        self.candidates = candidates

    def get_candidates(self):
        '''
        Returns the candidates list
        '''
        return self.candidates

    def end_voting(self):
        '''
        Displays the winning candidate in a messagebox
        '''
        # Finds the winning candidate(s)
        max_votes = max(self.candidates.values())
        winners = []
        for candidate in self.candidates():
            if self.candidates[candidate] == max_votes:
                winners.append(candidate)
        
        # Displays the winners in a messagebox
        if len(winners) == 1:
            winner_message = "The winner is: {}".format(winners[0])
        else:
            winner_message = "There is a tie between: {}".format(", ".join(winners))
        
        messagebox.showinfo("Winner", winner_message)

    def restart_program(self):
        '''
        Restarts the program for the user to start voting again with new candidates
        '''
        python = sys.executable
        os.execl(python, python, * sys.argv)