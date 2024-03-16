import re

def cleanText(text):
    try:
        text = re.sub('http\S+\s*', ' ', text)
        text = re.sub('RT|cc', ' ', text)
        text = re.sub('#\S+', '', text)
        text = re.sub('@\S+', '  ', text)
        text = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', text)
        text = re.sub(r'[^\x00-\x7f]',r' ', text)
        text = re.sub('\s+', ' ', text)
        return text
    except Exception as error:
        return error
