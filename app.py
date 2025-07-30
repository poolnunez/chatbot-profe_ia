from flask import Flask, request, render_template
from openai import AzureOpenAI
import os

app = Flask(__name__)

# CONFIGURA TUS DATOS DE AZURE
AZURE_OPENAI_ENDPOINT = ""
AZURE_OPENAI_API_KEY = ""  # Sustituye con tu clave real
AZURE_OPENAI_DEPLOYMENT = "gpt-4o-mini"
AZURE_OPENAI_VERSION = "2024-12-01-preview"

client = AzureOpenAI(
    api_version=AZURE_OPENAI_VERSION,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_API_KEY,
)

@app.route('/', methods=['GET', 'POST'])
def index():
    respuesta = ""
    if request.method == 'POST':
        pregunta = request.form['pregunta']

        chat_history = [
            {"role": "system", "content": "Eres un profesor experto en ecuaciones diferenciales. Responde de forma clara y con pasos."},
            {"role": "user", "content": pregunta}
        ]

        try:
            completion = client.chat.completions.create(
                model=AZURE_OPENAI_DEPLOYMENT,
                messages=chat_history,
                max_tokens=500,
                temperature=0.5
            )
            respuesta = completion.choices[0].message.content
        except Exception as e:
            respuesta = f"Error: {str(e)}"

    return render_template("index.html", respuesta=respuesta)

if __name__ == "__main__":
    app.run(debug=True)
