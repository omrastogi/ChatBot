from transformers import BertForQuestionAnswering, AutoTokenizer, pipeline
import json


class QAModel():
    def __init__(self):
        modelname = 'deepset/bert-large-uncased-whole-word-masking-squad2'
        model = BertForQuestionAnswering.from_pretrained(modelname)
        tokenizer = AutoTokenizer.from_pretrained(modelname)
        self.nlp = pipeline('question-answering', model=model, tokenizer=tokenizer)
        self.context = None
        self.get_context()

    def inference(self, question):
        output = self.nlp({
            'question': question,
            'context': self.context
        })
        score, answer = output['score'], output['answer']
        return score, answer

    def get_context(self):
        with open("xlabs/context.json") as file:
            data = json.load(file)

        self.context = data['contexts']


if __name__ == "__main__":
    model = QAModel()
    # print(model.inference("define a chatbot"))
    while True:
        ques = input('You: ')

        if ques == quit:
            break

        score, reply = model.inference(ques)
        print('Machine:', reply)


