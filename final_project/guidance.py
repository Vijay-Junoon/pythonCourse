from groq import Groq

GROQ_API_KEY = 'YOUR_API_KEYA'

client = Groq(
  api_key = GROQ_API_KEY
)

def getGuidance(age,bmi,glucose,bp,prediction):
  
  prompt = f"""
    You are an expert in diabetes diagnosis. The following data includes age, BMI, glucose, blood pressure and a machine learning prediction of a patient. Your job is to analyze these parameters, and then give suitable suggestions inorder to maintain a better lifestyle.
    Data: Age: {age},BMI: {bmi}, Glucose: {glucose},Blood Pressure: {bp}, Prediction: {prediction}
    """

  response = client.chat.completions.create(
    model = 'llama-3.3-70b-versatile',
    messages = [
      {
        'role': 'user',
        'content': prompt
      }
    ]
  )

  return response.choices[0].message.content