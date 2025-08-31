import os
import re
import json
import google.generativeai as genai
from dotenv import load_dotenv

class DeterministicClassifier:
    def __init__(self, rules_filepath="regras.json"):
        try:
            with open(rules_filepath, 'r', encoding='utf-8') as f:
                self.rules = json.load(f)
            print("✅ Regras do classificador determinístico carregadas.")
        except FileNotFoundError:
            self.rules = {}
            print("⚠️ Arquivo de regras não encontrado. Classificador determinístico inativo.")

    def classify(self, filename):
        for category, patterns in self.rules.items():
            for pattern in patterns:
                if re.search(pattern, filename, re.IGNORECASE):
                    return category
        return None

class IACore:
    def __init__(self):
        print("🧠 Inicializando novo motor de IA otimizado...")
        self.deterministic_classifier = DeterministicClassifier()
        load_dotenv()
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        if gemini_api_key:
            try:
                genai.configure(api_key=gemini_api_key)
                self.gemini_model = genai.GenerativeModel('gemini-1.5-pro-latest')
                print("🤖 Motor Gemini Pro (Fallback) conectado.")
            except Exception as e:
                self.gemini_model = None
                print(f"⚠️ Erro ao configurar Gemini: {e}.")
        else:
            self.gemini_model = None
            print("💡 Chave da API do Gemini não encontrada.")

    def classify(self, filename, categories):
        category = self.deterministic_classifier.classify(filename)
        if category:
            print(f"⚡ Classificação Rápida: '{filename}' -> '{category}'")
            return category
        if self.gemini_model:
            print(f"☁️ Usando IA em Nuvem para '{filename}'...")
            try:
                prompt = f"Categorias Válidas: {categories}. Analise o nome do arquivo '{filename}' e retorne apenas a categoria mais apropriada."
                response = self.gemini_model.generate_content(prompt)
                return response.text.strip()
            except Exception as e:
                print(f"⚠️ Erro na API Gemini: {e}")
                return "Para Revisão Manual"
        return "Para Revisão Manual"
