import aws


class Prediction:
    """
    Prediction service that communicates with the Amazon ML model.

    Public Methods:
        getTrashPrediction()
    """

    # CONSTANTS
    MODEL_ID = 'ml-il9BGcFLrzL'
    ENDPOINT = 'https://realtime.machinelearning.us-east-1.amazonaws.com'

    def __init__(self):
        self.ml = aws.getClient('machinelearning', 'us-east-1')

    def getTrashPrediction(self, recList):
        """
        Return a prediction of the ML model for the given list of identifiers.
        :param recList: list of string identifiers, e.g. ['fruit', 'flora']
        :return: Predicted category as a string
        """
        recText = self.formatQuery(recList)
        res = self.ml.predict(
            MLModelId=self.MODEL_ID,
            Record={
                'Text': recText,
            },
            PredictEndpoint=self.ENDPOINT
        )
        predict = res['Prediction']['predictedLabel']
        return predict

    def formatQuery(self, info):
        """
        Return a string the concatenated elements of the given list.
        :param info: List of strings, e.g., ['one', 'two', 'three']
        :return: String of the elements concatenated, e.g., "one, two, three"
        """
        txt = ''
        for label in info:
            txt += label + ', '
        return txt[:-2]
