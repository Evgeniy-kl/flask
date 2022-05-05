from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from service import get_questions_json

app = Flask(__name__)
db = SQLAlchemy(app)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:03072002@db:5432/flaskdb"


class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String())
    answer_text = db.Column(db.String())
    date_of_creation = db.Column(db.String())

    def __init__(self, id: int, question_text: str, answer_text: str, date_of_creation: str):
        self.id = id
        self.question_text = question_text
        self.answer_text = answer_text
        self.date_of_creation = date_of_creation

    def __repr__(self):
        return f"<Question {self.question_text}>"


class QuestionAPI(Resource):
    def get(self):
        """check"""
        return get_questions_json(2)

    def post(self):
        questions_num = int(request.form['questions_num'])
        data_from_service = get_questions_json(questions_num)

        for row in data_from_service:
            id = int(row['id'])
            question = row['question']
            answer = row['answer']
            created_at = row['created_at']

            existing = Question.query.get(id)
            if existing is not None:
                continue
            else:
                question_object = Question(
                    id=id,
                    question_text=question,
                    answer_text=answer,
                    date_of_creation=created_at
                )
                db.session.add(question_object)
        db.session.commit()

        return jsonify(data_from_service)


api.add_resource(QuestionAPI, '/')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5050)
