from flask import Flask, request, jsonify
from googletrans import Translator

app = Flask(__name__)
translator = Translator()

# Fonction pour obtenir les informations sur la langue
def get_language_info(language_code):
    lang_info = {
        "fr": {"name": "French", "flag": "🇫🇷"},
        "en": {"name": "English", "flag": "🇬🇧"},
        "es": {"name": "Spanish", "flag": "🇪🇸"},
        "mg": {"name": "Malagasy", "flag": "🇲🇬"},
        "de": {"name": "German", "flag": "🇩🇪"},
        "ja": {"name": "Japanese", "flag": "🇯🇵"},
        "ko": {"name": "Korean", "flag": "🇰🇷"},
        # Ajouter d'autres langues avec leurs noms complets et drapeaux emoji ici
    }

    lang = lang_info.get(language_code.lower())
    if lang:
        return f"{lang['flag']} {lang['name']}"
    else:
        return f"Unknown Language ({language_code})"

# Endpoint pour la traduction
@app.route('/translate', methods=['POST'])
def translate_text():
    try:
        data = request.json
        text_to_translate = data['text_to_translate']
        dest = data['dest']

        translated_text = translator.translate(text_to_translate, dest=dest)

        # Obtenir les informations sur les langues source et cible
        source_lang = get_language_info(translated_text.src)
        dest_lang = get_language_info(dest)

        translation_result = f"{source_lang} ➜ {dest_lang}"

        return jsonify({"translation": translated_text.text, "translation_info": translation_result})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/ping', methods=['GET'])
def healthcheck():
    return jsonify({"status": "API is running smoothly"})
