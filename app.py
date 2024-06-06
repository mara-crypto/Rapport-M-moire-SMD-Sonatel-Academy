from flask import Flask, request, jsonify
import joblib
import pandas as pd

# Créer une instance de l'application Flask
app = Flask(__name__)

# Charger le modèle Random Forest
model = joblib.load('gradient_boosting_model.pkl')

# Charger le scaler et l'encoder
scaler = joblib.load('scaler.pkl')

encoder = joblib.load('encoder.pkl')



x_test = joblib.load('x_test.pkl')

# Créer une route pour les prédictions
@app.route('/predict', methods=['POST'])
def predict():
    # Obtenir les données à partir de la requête POST
    data = request.json
    df = pd.DataFrame([data])


    # Encoder les variables catégorielles
    # df_encoded = pd.get_dummies(df)
    # Encoder les variables catégorielles
    categorical_cols = ['metier', 'situation_matrimoniale', 'education', 'defaut_credit', 'logement', 'pret', 'contact', 'mois', 'jour_de_semaine', 'resultat_campagne_precendente']
    df_encoded = pd.get_dummies(df, dtype=int)

    # Vérifier et ajouter les colonnes manquantes
    missing_cols = set(encoder.columns) - set(df_encoded.columns)
    for col in missing_cols:
        df_encoded[col] = 0

    
    # Réorganiser les colonnes selon l'ordre de l'encoder
    df_encoded = df_encoded[encoder.columns]
                    
   
    # Normaliser les données numériques
    numerical_cols = ['age', 'campagne', 'nombre_de_jour_ecoule', 'nombre_contact_precedent', 'duree_appel']
    df_normalized = scaler.transform(df_encoded[numerical_cols])

    # Remplacer les données numériques par les données normalisées
    df_encoded[numerical_cols] = df_normalized

    if df_encoded.shape[1] != encoder.shape[1]:
        return jsonify({'error': 'Some columns are missing'})

    if not all(col in df_encoded.columns for col in numerical_cols):
        return jsonify({'error': 'Some numerical columns are missing'})
    
    # Faire la prédiction
    prediction = model.predict(df_encoded)


    # Renvoyer la prédiction sous forme de JSON
    return jsonify({'prediction': prediction.tolist()})

# Lancer l'application Flask
if __name__ == '__main__':
    app.run(port=5000)

