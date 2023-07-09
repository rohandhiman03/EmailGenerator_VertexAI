from flask import Flask, request, render_template
import vertexai
from vertexai.language_models import TextGenerationModel

vertexai.init(project="emailforge", location="us-central1")
parameters = {
    "temperature": 0.2,
    "max_output_tokens": 256,
    "top_p": 0.95,
    "top_k": 40
}
model = TextGenerationModel.from_pretrained("text-bison@001")

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/read-form', methods=['POST'])
def read_form():
    data = request.form
    receiver = data['receiver']
    email_type = data['emailtype']
    content = data['content']
    sender = data['sender']
    request_str = "Write me a "+email_type+" email . The receiver's name is "+receiver+". The email should be regarding "+content+". The name of the mail sender is "+sender
    response = model.predict(request_str,**parameters)
    # response_str = str(response)

    return render_template('index.html', generated_email=response.text)

if __name__ == '__main__':
    app.run()
