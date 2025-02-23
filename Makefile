init:
	myenv\Scripts\activate.bat
install:
	pip install -r requirements.txt
run:
	python -m streamlit run directory.py