import re
import pickle
import emoji
import json
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from pyprojroot import here

# Inisialisasi stemmer dan stopword remover dari Sastrawi
stemmer_factory = StemmerFactory()
stemmer = stemmer_factory.create_stemmer()

stopword_factory = StopWordRemoverFactory()
stopword_remover = stopword_factory.create_stop_word_remover()

# Load slang words dari file JSON
slangword = {}
with open(here('assets/combined_slang_words.txt'), 'r') as f:
    slangword = json.load(f)

class TextPreprocessor:
    def __init__(self, text: str) -> None:
        """
        Inisialisasi TextPreprocessor dengan teks yang akan diproses.
        
        Parameters:
        text (str): Teks yang akan diproses.
        """
        self.text = text
        self.kata_tambahan = ["t", "n", " t", " n", " n ", "dengan", "yang", "dan", "user name", "username ", "username"]
        self.vectorizer = pickle.load(open(here('assets/vectorizer.pickle'), 'rb'))
        self.text_preprocess = self.text_preprocessing()

    def __clean_text(self, text: str):
        """
        Membersihkan teks dari berbagai karakter dan simbol yang tidak diinginkan.
        
        Parameters:
        text (str): Teks yang akan dibersihkan.
        
        Returns:
        str: Teks yang sudah dibersihkan.
        """
        emoticon_byte_regex = r"\s*(?:\\x[A-Fa-f0-9]{2})+"
        url_regex = r"((www\.[^\s]+)|(https?://[^\s]+)|(http?://[^\s]+)||(http\S+))"

        text = re.sub(emoticon_byte_regex, "", text)  # Menghapus emoticon bytes
        text = re.sub(url_regex, "", text)  # Menghapus setiap URL
        text = re.sub(r"<[^>]*>", "", text)  # Menghapus tag HTML
        text = re.sub(r"@[A-Za-z0-9]+", "", text)  # Menghapus username Twitter
        text = re.sub(r"\n", " ", text)  # Menghapus setiap new line '\n'
        text = re.sub("@[\w\-]+", "", text)  # Menghapus mentions
        text = re.sub("RT", "", text)  # Menghapus simbol retweet
        text = re.sub("USER", "", text)  # Menghapus kata 'USER'
        text = re.sub(" URL", " ", text)  # Menghapus kata 'URL'
        text = re.sub(" url", " ", text)  # Menghapus kata 'url'
        text = re.sub("\+", " ", text)  # Menghapus tanda tambah
        text = re.sub("\s+", " ", text)  # Menghapus karakter spesial
        text = re.sub("[^0-9a-zA-Z]", " ", text)  # Menghapus tanda baca
        text = re.sub("[^a-zA-Z]", " ", text)  # Menghapus angka
        text = re.sub(" +", " ", text)  # Menghapus spasi ekstra
        text = re.sub(r'http\S+', '', text)  # Menghapus URL atau tautan
        text = re.sub(r'#\w+', '', text)  # Menghapus hashtag (#)
        text = re.sub(r'@\w+', '', text)  # Menghapus username dan mentions (@)
        text = re.sub(r'RT', '', text)  # Menghapus retweet (RT)
        text = re.sub(r'[^\w\s]', '', text)  # Menghapus tanda baca, baris baru, angka, spasi kosong, dan emoji
        text = re.sub(r'\n', ' ', text)
        text = re.sub(r'\d+', '', text)
        text = emoji.demojize(text)  # Menghapus emoji
        text = ' '.join(text.split())  # Menghapus spasi ekstra dan spasi awal/akhir
        text = text.strip()
        
        return text

    def __replace_slang_words(self, text: str):
        """
        Mengganti kata-kata slang dengan padanan resmi.

        Parameters:
        text (str): Teks yang akan diproses.

        Returns:
        str: Teks dengan kata-kata slang yang sudah diganti.
        """
        text = text.lower()
        text = re.sub(r'\n', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        words = text.split()
        new_words = []
        for word in words:
            if word in slangword:
                new_words.append(slangword[word])
            else:
                new_words.append(word)
        new_text = ' '.join(new_words)
        return new_text
    
    def __remove_stopwords(self, text: str):
        """
        Menghapus stopwords dari teks.
        
        Parameters:
        text (str): Teks yang akan diproses.
        
        Returns:
        str: Teks yang sudah dihapus stopwords-nya.
        """
        text = stopword_remover.remove(text)
        words = text.split()
        words = [word for word in words if word not in self.kata_tambahan]
        return ' '.join(words)
    
    def text_preprocessing(self):
        """
        Melakukan keseluruhan proses praproses teks: mengganti kata slang, menghapus stopwords,
        membersihkan teks, dan stemming. Kemudian, teks diubah menjadi vektor fitur.
        
        Returns:
        sparse matrix: Hasil transformasi teks menjadi vektor fitur.
        """
        processed_text = self.__replace_slang_words(self.text)
        processed_text = self.__remove_stopwords(processed_text)
        processed_text = self.__clean_text(processed_text)
        processed_text = stemmer.stem(processed_text)
        vector = self.vectorizer.transform([processed_text])
        return vector

if __name__ == '__main__':
    text = "Ini adalah contoh text dengan slang gmn dan stopwords yang perlu dihilangkan."
    preprocessor = TextPreprocessor(text)
    clean = preprocessor.text_preprocess
    print(clean)
