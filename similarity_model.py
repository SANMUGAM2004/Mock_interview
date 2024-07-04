# import spacy
# import json

# # Load spaCy model
# nlp = spacy.load("en_core_web_lg")

# def model_fn(model_dir):
#     return nlp

# def input_fn(request_body, request_content_type):
#     if request_content_type == 'application/json':
#         request = json.loads(request_body)
#         return request['text1'], request['text2']
#     raise ValueError(f"Unsupported content type: {request_content_type}")

# def predict_fn(input_data, model):
#     text1, text2 = input_data
#     doc1 = model(text1)
#     doc2 = model(text2)
#     similarity_score = doc1.similarity(doc2)
#     return similarity_score

# def output_fn(prediction, response_content_type):
#     return json.dumps({'similarity': prediction})

