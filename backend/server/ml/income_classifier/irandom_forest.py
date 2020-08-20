import joblib
import pandas as pd


class RFClassifier:

    def __init__(self):
        path = "../../research/"
        self.missing_values = joblib.load(path + "train_mode.joblib")
        self.encoders = joblib.load(path + "encoders.joblib")
        self.model = joblib.load(path + "rfi.joblib")

    def preprocessing(self, input_data):
        input_data = pd.DataFrame(input_data, index=[0])
        input_data = input_data.fillna(self.missing_values)
        for col in ["workclass", "education", "marital-status", "occupation",
                       "relationship", "race", "sex",  "native-country"]:
            le = self.encoders[col]
            input_data[col] = le.transform(input_data[col])
        return input_data

    def prediction(self, input_data):
        return self.model.predict_proba(input_data)

    def postprocessing(self, input_data):
        label = "<=50K"
        if input_data[1] > 0.5:
            label = ">50K"
        return {"probability": input_data[1], "label": label, "status": "OK"}

    def predict(self, input_data):

        try:
            input_data = self.preprocessing(input_data)
            prediction = self.prediction(input_data)[0]  # only one sample
            prediction = self.postprocessing(prediction)
        except Exception as e:
            return {"status": "Error", "message": str(e)}

        return prediction