class LLMModel:
    def __init__(self, model_path):
    # Loads model...
        pass

    # Trains model
    def train(self, data_path, epochs=3, batch_size=16):
        
        # Tallentaa loss, accuracy, jne.
        pass

    # Returns classification of work type
    def classifyWork(self, inputText):
        
        pass

    # Returns classification of urgency
    def classifyUrgency(self, inputText):
        pass

    # Creates summary
    def createSummary(self, inputText):
        pass
    
    # Creates answer (positive or negative)
    def createAnswer(self, positiveAnswer, inputText):
        pass