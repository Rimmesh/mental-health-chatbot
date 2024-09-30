import pickle
import nltk
import random
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer

# Ensure NLTK resources are downloaded
nltk.download('stopwords')
nltk.download('punkt')

# Load the SVM model and the TF-IDF vectorizer
with open('model/svm_model (1).pkl', 'rb') as model_file:
    svm_classifier = pickle.load(model_file)

with open('model/tfidf_vectorizer (1).pkl', 'rb') as vectorizer_file:
    tfidf_vectorizer = pickle.load(vectorizer_file)

def tokenizeWithoutPunctuation(text):
    # Tokenization without punctuation
    tokens = nltk.word_tokenize(text)
    words = [word for word in tokens if word.isalnum()]
    return words

def nlp_analysis(text):
    if isinstance(text, str):
        # Tokenization
        tkn_words = tokenizeWithoutPunctuation(text)
        
        # Remove stopwords
        stop_words = set(stopwords.words("english"))
        filtered_words = [word.lower() for word in tkn_words if word.lower() not in stop_words]
        
        processed_text = ' '.join(filtered_words)
        return processed_text
    else:
        return ' '  # Return an empty string

def predict_sentiment(text):
    processed_text = nlp_analysis(text)  # Preprocess the text
    new_text_vectorized = tfidf_vectorizer.transform([processed_text])  # Vectorize the new sentence
    predicted_label = svm_classifier.predict(new_text_vectorized)  # Predict with the trained SVM model
    return int(predicted_label[0])

responses = {
    1: [
        "Sorry to hear that you're feeling down. Would you like to talk more about it?",
        "It seems you're having a tough time. I'm here to listen.",
        "I'm sorry you're feeling stressed. Maybe some relaxing music would help: <a href='https://www.youtube.com/watch?v=2OEL4P1Rz04' target='_blank'>Relaxing Music</a>",
        "I understand it's hard. Would you like to play a game to distract yourself? Check out this: <a href='https://www.coolmathgames.com/' target='_blank'>Cool Math Games</a>",
        "It can be overwhelming sometimes. Taking a walk outside can help clear your mind. Nature can be very soothing.",
        "I hear you. Sometimes reading a book can be a great escape. Do you have a favorite book?",
        "You're not alone. If you feel comfortable, talking to a friend or family member can provide support.",
        "I know it's tough. Breathing exercises can help reduce stress: <a href='https://www.youtube.com/watch?v=inpok4MKVLM' target='_blank'>Guided Breathing Exercise</a>",
        "It's okay to feel this way. Try to write down your feelings. Journaling can be therapeutic.",
        "I understand it's challenging. Maybe some guided meditation could help: <a href='https://www.youtube.com/watch?v=inpok4MKVLM' target='_blank'>Guided Meditation</a>",
        "I'm here for you. Listening to calming nature sounds might help you relax: <a href='https://www.youtube.com/watch?v=eKFTSSKCzWA' target='_blank'>Nature Sounds</a>",
        "It can be difficult. How about trying some gentle yoga to relax your mind and body? <a href='https://www.youtube.com/watch?v=v7AYKMP6rOE' target='_blank'>Gentle Yoga</a>",
        "I understand. If you like puzzles, this site has some great options: <a href='https://www.jigsawplanet.com/' target='_blank'>Jigsaw Puzzles</a>",
        "It's not easy. Listening to a positive podcast might uplift your mood: <a href='https://www.happierpodcast.com/' target='_blank'>Happier Podcast</a>",
        "I'm sorry you're feeling this way. Drawing or coloring can be a calming activity. Do you enjoy any form of art?",
        "I know it's tough. Sometimes it helps to just sit and have a cup of tea. Maybe try some herbal tea?",
        "You're not alone in this. If you're into aromatherapy, lighting a scented candle or using essential oils might help."
    ],
    0: [
        "That's great to hear! Keep up the positive attitude!",
        "I'm glad you're feeling good. What made your day special?",
        "It's wonderful that you're in a good mood. Maybe some uplifting music would help you maintain it: <a href='https://www.youtube.com/watch?v=d-diB65scQU' target='_blank'>Uplifting Music</a>",
        "Keep spreading your positive vibes! How about sharing a smile with someone today?",
        "Feeling good is awesome! Maybe celebrate with a little dance: <a href='https://www.youtube.com/watch?v=6JCLY0Rlx6Q' target='_blank'>Happy Dance Music</a>",
        "A good mood is contagious. How about calling a friend and sharing your joy?",
        "It's great that you're feeling good. Enjoy your mood with a fun activity, like a favorite hobby or a new recipe.",
        "Enjoy your good mood! A walk in the park can enhance your mood even further. Nature is beautiful!",
        "It's fantastic that you're feeling good. How about some inspirational TED Talks to keep the positivity flowing? <a href='https://www.ted.com/talks' target='_blank'>TED Talks</a>",
        "It's lovely to hear you're feeling great. If you're in the mood for a good laugh, check out some comedy sketches: <a href='https://www.youtube.com/results?search_query=comedy+sketches' target='_blank'>Comedy Sketches</a>",
        "I'm glad to hear you're in high spirits. Maybe try learning something new today. Here's a great place to start: <a href='https://www.coursera.org/' target='_blank'>Coursera</a>",
        "It's wonderful that you're feeling positive. Reading some motivational quotes might keep you inspired: <a href='https://www.brainyquote.com/' target='_blank'>Motivational Quotes</a>",
        "It's great that you're feeling good. How about trying some upbeat workouts to keep your energy high? <a href='https://www.youtube.com/results?search_query=upbeat+workout' target='_blank'>Upbeat Workouts</a>",
        "It's lovely to hear that you're feeling positive. Listening to a positive podcast can keep the good vibes going: <a href='https://www.goodlifeproject.com/podcast/' target='_blank'>Good Life Project Podcast</a>",
        "I'm happy to hear you're doing well. How about a fun online quiz to keep you entertained? <a href='https://www.buzzfeed.com/quizzes' target='_blank'>BuzzFeed Quizzes</a>",
        "It's fantastic that you're feeling good. If you enjoy cooking, trying a new recipe could be a delightful experience: <a href='https://www.allrecipes.com/' target='_blank'>All Recipes</a>",
        "It's great that you're in a good mood. Exploring a virtual museum could be both fun and educational: <a href='https://artsandculture.google.com/partner' target='_blank'>Google Arts & Culture</a>"
    ]
}


def get_response(predicted_label):
    if predicted_label in responses:
        return random.choice(responses[predicted_label])
    else:
        return 'Sorry, I did not understand that.'
