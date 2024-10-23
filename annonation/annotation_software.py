import pandas as pd
import tkinter as tk
from tkinter import ttk
import os

def read_csv(file_path):
    return pd.read_csv(file_path)

def save_csv(file_path, data):
    data.to_csv(file_path, index=False, encoding='utf-8')

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

class LabelingApp:
    def __init__(self, root, data):
        self.root = root
        self.data = data
        self.current_index = 0

        # Questions and their corresponding options
        self.questions = [
            'Annotator', 'Not OK?', 'Political Influence',
            'Scientific Data Mentioned', 'Statistical Data Mentioned',
            'Source Mentioned', 'Authenticity', 'Stance Detection',
            'Location', 'Focus', 'Target', 'Authority Involvement'
        ]

        self.options = {
            'Annotator': ['Annotator 1','Annotator 2','Annotator 3'],
            'Not OK?': ['FALSE','TRUE'],
            'Political Influence': ['No','Yes'],
            'Scientific Data Mentioned': ['No','Yes'],
            'Statistical Data Mentioned': ['No','Yes', ],
            'Source Mentioned': ['No','Yes', ],
            'Authenticity': ['Real','Maybe Real','Maybe Fake','Fake','Problematic'],
            'Stance Detection': ['Positive','Neutral','Negative','Problematic'],
            'Location': ['Bangladesh','India','Global','China','USA','Others'],
            'Focus': ["Climate Change", "Environmental Pollution", "Air Pollution", "Water Pollution", "Soil Pollution", "Sound Pollution", "Global Warming", "Rain", "Water Resource Pollution", "Forestry and Tree Plantation", "Heavy Metal", "Wildlife", "Plastic Pollution", "Light Pollution", "E-Waste", "Natural Disaster", "Ozone Layer", "Sea Level Rising", "Environmental Protection"],
            'Target': ["N/A","Government", "General People", "Industries",  "All", "Dishonest people", "Authority", "World power"],
            'Authority Involvement':["N/A","Legal/Court", "Crime/Police", "Other Authority",  "Environmental/Forestry Authority", "Scientists & Researcher", "NGO", "Government", "General people", "UN"]
        }

        self.answers = {q: tk.StringVar() for q in self.questions}

        self.create_widgets()

    def create_widgets(self):
        self.title_label = tk.Label(self.root, text="", font=("Helvetica", 16, "bold"))
        self.title_label.pack(pady=10)
        
        self.rem_text = tk.Label(self.root, text="", font=("Helvetica", 12, "bold"))
        self.rem_text.pack(pady=5)

        self.body_text = tk.Text(self.root, wrap='word',spacing2=25, height=20,width=80,font=("Helvetica", 12, ))
        self.body_text.pack(pady=10)

        self.questions_frame = tk.Frame(self.root)
        self.questions_frame.pack(pady=10)

        self.question_labels = []
        self.option_menus = []
        for i, question in enumerate(self.questions):
            frame = tk.Frame(self.questions_frame)
            frame.grid(row=i // 4, column=i % 4, padx=10, pady=5, sticky='w')
            question_label = tk.Label(frame, text=question)
            question_label.pack()
            self.question_labels.append(question_label)

            option_menu = ttk.Combobox(frame, textvariable=self.answers[question])
            option_menu['values'] = self.options[question]
            option_menu.pack(pady=5)
            self.option_menus.append(option_menu)

        self.next_button = tk.Button(self.root, text="Submit", command=self.next)
        self.next_button.pack(pady=10)

        self.load_data()

    def load_data(self):
        while self.current_index < len(self.data):
            item = self.data.iloc[self.current_index]
            if item['Done'] == 'No':
                not_ok_count = (self.data['Not OK?'] == True).sum()
                print(not_ok_count)
                self.title_label.config(text=str(item['Title']))
                self.rem_text.config(text="Done: "+ str( self.current_index )+f" | Not Okay: {not_ok_count} "+f" | Okay: {self.current_index- not_ok_count} "+ " | Remaining: "+ str( len(self.data)-self.current_index) +" | Total "+ str( len(self.data)))
                file_path = os.path.join('../dataset_files', item['Files'])
                file_content = read_file(file_path)
                self.body_text.delete(1.0, tk.END)
                self.body_text.insert(tk.END, file_content)

                for question in self.questions:
                    self.answers[question].set(self.options[question][0])  # Set to first option by default
                break
            self.current_index += 1

    def next(self):
        if self.current_index < len(self.data):
            for question in self.questions:
                self.data.at[self.current_index, question] = self.answers[question].get()
            self.data.at[self.current_index, 'Done'] = 'Yes'

            save_csv('data.csv', self.data)
            
            self.current_index += 1
            if self.current_index < len(self.data):
                self.load_data()
            else:
                self.title_label.config(text="All items processed.")
                self.body_text.delete(1.0, tk.END)

if __name__ == "__main__":
    csv_file_path = 'data.csv'
    data = read_csv(csv_file_path)

    root = tk.Tk()
    root.title("ধরণী - Labelling Software")

    app = LabelingApp(root, data)
    root.mainloop()
