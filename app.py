import streamlit as st 
import joblib,os
import spacy
import pandas as pd
nlp = spacy.load("en_core_web_sm")
import matplotlib.pyplot as plt 
import matplotlib
matplotlib.use("Agg")
from wordcloud import WordCloud
from nltk.probability import FreqDist


# load Vectorizer 
news_vectorizer = open("models/final_news_cv_vectorizer.pkl","rb")
news_cv = joblib.load(news_vectorizer)

def load_prediction_models(model_file):

	loaded_model = joblib.load(open(os.path.join(model_file),"rb"))
	return loaded_model

# Get the Keys
def get_key(val,my_dict):
	for key,value in my_dict.items():
		if val == value:
			return key



def main():

	"""News Classifier"""
	st.title("News Classifier")
	
	# Layout Templates
	html_temp = """
	<div style="background-color:#464e5f;padding:10px;border-radius:10px;margin:10px;">
	<h1 style="color:white;text-align:center;"> Streamlit ML App - News Classifier </h1>
	<img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar" style="vertical-align: middle;width: 50px;height: 50px;border-radius: 50%;" >
	<p style="text-align:justify">{}</p>
	</div>
	"""
	title_temp ="""
	<div style="background-color:#464e5f;padding:10px;border-radius:10px;margin:10px;">
	<h4 style="color:white;text-align:center;">{}</h1>
	<img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar" style="vertical-align: middle;float:left;width: 50px;height: 50px;border-radius: 50%;" >
	<h6>Author:{}</h6>
	<br/>
	<br/> 
	<p style="text-align:justify">{}</p>
	</div>
	"""
	article_temp ="""
	<div style="background-color:#464e5f;padding:10px;border-radius:5px;margin:10px;">
	<h4 style="color:white;text-align:center;">{}</h1>
	<h6>Author:{}</h6> 
	<h6>Post Date: {}</h6>
	<img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar" style="vertical-align: middle;width: 50px;height: 50px;border-radius: 50%;" >
	<br/>
	<br/>
	<p style="text-align:justify">{}</p>
	</div>
	"""

	
	st.markdown(html_temp,unsafe_allow_html=True)

	activity = ['Prediction','NLP','About']
	choice = st.sidebar.selectbox("Select Activity",activity)


	if choice == 'Prediction':
		st.info("Prediction with ML")
		news_text = st.text_area("Enter News Here","Type Here")
		all_ml_models = ["Logistic Regression","Random Forest","Decision Tree"]
		model_choice = st.selectbox("Select Model",all_ml_models)

		prediction_labels = {'business': 0,'tech': 1,'sport': 2,'health': 3,'politics': 4,'entertainment': 5}
		if st.button("Classify"):
			st.text("Original Text:\n{}".format(news_text))
			vect_text = news_cv.transform([news_text]).toarray()
			if model_choice == 'Logistic Regression':
				predictor = load_prediction_models("models/newsclassifier_Logit_model.pkl")
				prediction = predictor.predict(vect_text)
				# st.write(prediction)
			elif model_choice == 'Random Forest':
				predictor = load_prediction_models("models/newsclassifier_RFOREST_model.pkl")
				prediction = predictor.predict(vect_text)
				# st.write(prediction)
			elif model_choice == 'Decision Tree':
				predictor = load_prediction_models("models/newsclassifier_CART_model.pkl")
				prediction = predictor.predict(vect_text)
				# st.write(prediction)

			final_result = get_key(prediction,prediction_labels)
			st.success("News Categorized as: {}".format(final_result))

	elif choice == 'NLP':
		st.info("Natural Language Processing of Text")
		raw_text = st.text_area("Enter News Here","Type Here")
		nlp_task = ["Tokenization","Lemmatization","Named Entity Recognition(NER)","Parts-of-Speech(POS) Tags"]
		task_choice = st.selectbox("Choose NLP Task",nlp_task)
		if st.button("Analyze"):
			st.info("Original Text:\n{}".format(raw_text))

			docx = nlp(raw_text)
			if task_choice == 'Tokenization':
				result = [token.text for token in docx ]
			elif task_choice == 'Lemmatization':
				result = ["'Token':{},'Lemma':{}".format(token.text,token.lemma_) for token in docx]
			elif task_choice == 'Named Entity Recognition(NER)':
				result = [(entity.text,entity.label_)for entity in docx.ents]
			elif task_choice == 'Parts-of-Speech(POS) Tags':
				result = ["'Token':{},'POS':{},'Dependency':{}".format(word.text,word.tag_,word.dep_) for word in docx]

			st.json(result)

		if st.button("Tabulize"):
			docx = nlp(raw_text)
			c_tokens = [token.text for token in docx ]
			c_lemma = [token.lemma_ for token in docx ]
			c_pos = [token.pos_ for token in docx ]

			new_df = pd.DataFrame(zip(c_tokens,c_lemma,c_pos),columns=['Tokens','Lemma','POS'])
			st.dataframe(new_df)


		if st.checkbox("WordCloud"):
			c_text = raw_text
			wordcloud = WordCloud().generate(c_text)
			plt.imshow(wordcloud,interpolation='bilinear')
			plt.axis("off")
			st.set_option('deprecation.showPyplotGlobalUse', False)
			st.pyplot()

		if st.checkbox("FrequencyDistribution"):
			c_text = raw_text
			fdist = FreqDist(c_text)
			print(fdist.most_common(10))

	else:
		st.write("")
		st.subheader("About")
		st.write("")
	
		st.markdown("""
        ### NLP News Classifier With Different Models (With Streamlit)
        Python Tools Used: spacy, pandas, matplotlib, wordcloud, Pillow(PIL), Joblib
        """)


if __name__ == '__main__':
	main()
