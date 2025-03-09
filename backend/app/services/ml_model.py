from sklearn.ensemble import RandomForestClassifier
import numpy as np

class CreditRiskModel:
    """Predicts creditworthiness using a machine learning model."""

    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)

    def train_model(self, X_train, y_train):
        """Train the model on historical credit data."""
        self.model.fit(X_train, y_train)

    def predict_risk(self, features):
        """Predict credit risk level based on financial metrics."""
        features = np.array(features).reshape(1, -1)
        return self.model.predict(features)[0]
