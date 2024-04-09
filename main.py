from random import choice
from PIL import Image
from base_db import DataBase
import customtkinter as ctk


class Menu(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("🎲 Викторина 🎲")
        self.geometry("600x700")
        self.db = DataBase('db.db')
        ctk.set_appearance_mode("Dark")
        ctk.set_widget_scaling(1.5)

    def start_app(self):

        self.db.execute_query("UPDATE points SET point = 0 WHERE id = 1")

        if hasattr(self, 'asked_questions'):
            self.asked_questions.clear()

        for widget in app.winfo_children():
            widget.destroy()

        greetings = self.db.fetch_one('SELECT greetings FROM alls')[0]
        label = ctk.CTkLabel(
            app,
            text=greetings
        , font=("Arial", 14), wraplength=400)
        label.pack(pady=20, padx=10)

        button_start = ctk.CTkButton(self, text="Играть", command=self.start_quiz, fg_color="green")
        button_start.place(relx=0.5, rely=0.4, anchor='center')

        button_rules = ctk.CTkButton(self, text="Правила", command=self.show_rules, fg_color="purple")
        button_rules.place(relx=0.5, rely=0.5, anchor='center')

    def show_rules(self):
        for widget in app.winfo_children():
            widget.destroy()
        rules_label = ctk.CTkLabel(app, text="Правила игры:", font=("Arial", 18))
        rules_label.pack(pady=10, padx=10)

        rules_text = self.db.fetch_one('SELECT rules FROM alls')[0]
        rules_text_label = ctk.CTkLabel(app, text=rules_text, font=("Arial", 14), wraplength=300)
        rules_text_label.pack(pady=10, padx=10)

        button_back = ctk.CTkButton(self, text="Назад", command=self.start_app, fg_color="purple")
        button_back.place(relx=0.5, rely=0.5, anchor='center')

    def display_questions_answers(self):
        if not hasattr(self, 'asked_questions'):
            self.asked_questions = []

        questions_answers = self.db.fetch_all("""
            SELECT question_text, choice1, choice2, choice3, choice4 
            FROM questions_answers
        """)

        if questions_answers:
            remaining_questions = [qa for qa in questions_answers if qa not in self.asked_questions]
            if remaining_questions:
                random_answers = choice(remaining_questions)
                self.asked_questions.append(random_answers)
                return random_answers
            else:
                self.asked_questions.clear()
                self.notify_user_question_end()
            return None
        else:
            return None

    def notify_user_question_end(self):
        end = ctk.CTkLabel(app,
                           text="Поздравляем игра окончена",
                           font=("Arial", 18, "bold"),
                           padx=20, pady=20, fg_color="purple")
        end.pack()

        my_image = ctk.CTkImage(light_image=Image.open("1.jpg"),
                                size=(398, 307))

        image_label = ctk.CTkLabel(app, image=my_image, text="")
        image_label.pack()

        app.after(1500, self.start_app)

    def start_quiz(self):
        for widget in app.winfo_children():
            widget.destroy()

        random_answers = self.display_questions_answers()

        if random_answers:
            question_label = ctk.CTkLabel(app, text=random_answers[0], font=("Arial", 17),
                                          padx=20, pady=70, wraplength=400)

            question_label.pack(fill='both')

            answer_choice1 = ctk.CTkButton(self, text=random_answers[1],
                                           command=lambda: self.check_answer(random_answers[1]), fg_color="Brown")
            answer_choice1.place(relx=0.3, rely=0.5, anchor='center')

            answer_choice2 = ctk.CTkButton(self, text=random_answers[2],
                                           command=lambda: self.check_answer(random_answers[2]), fg_color="Brown")
            answer_choice2.place(relx=0.7, rely=0.5, anchor='center')

            answer_choice3 = ctk.CTkButton(self, text=random_answers[3],
                                           command=lambda: self.check_answer(random_answers[3]), fg_color="Brown")
            answer_choice3.place(relx=0.3, rely=0.6, anchor='center')

            answer_choice4 = ctk.CTkButton(self, text=random_answers[4],
                                           command=lambda: self.check_answer(random_answers[4]), fg_color="Brown")
            answer_choice4.place(relx=0.7, rely=0.6, anchor='center')
        button_back = ctk.CTkButton(self, text="Назад", command=self.start_app, fg_color="gray")
        button_back.place(relx=0.5, rely=0.8, anchor='center')

    def check_answer(self, selected_answer):
        self.points = 0

        correct_answer = self.db.fetch_one("""
            SELECT correct_choice FROM questions_answers 
            WHERE correct_choice = ?
        """, (selected_answer,))

        if correct_answer:
            self.points += 1
            self.db.execute_query("UPDATE points SET point = point + :point WHERE id = 1",
                                  {"point": 1})
            notification = self.db.fetch_one('SELECT point FROM points')[0]
            alert_1 = ctk.CTkLabel(app,
                                   text=f"Ответ верный.\nОбщее количество баллов: {notification}",
                                   font=("Arial", 18, "bold"),
                                   padx=20, pady=20)
            alert_1.pack()
            app.after(1000, alert_1.destroy)
        else:
            self.points -= 1
            self.db.execute_query("UPDATE points SET point = point - :point WHERE id = 1",
                                  {"point": 1})
            notification = self.db.fetch_one('SELECT point FROM points')[0]
            alert_2 = ctk.CTkLabel(app,
                                   text=f"Ответ неверный.\nОбщее количество баллов: {notification}",
                                   font=("Arial", 18, "bold"),
                                   padx=20, pady=20)
            alert_2.pack()
            app.after(1000, alert_2.destroy)

        app.after(1400, self.start_quiz)


if __name__ == "__main__":
    app = Menu()
    app.start_app()
    app.mainloop()
