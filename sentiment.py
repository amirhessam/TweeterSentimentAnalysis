import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import MT5ForConditionalGeneration, MT5Tokenizer


class SentimentAnalyzer:
    ld_model_name = "papluca/xlm-roberta-base-language-detection"
    ps_model_name = "persiannlp/mt5-base-parsinlu-sentiment-analysis"
    es_model_name = "cardiffnlp/twitter-roberta-base-sentiment"
    ld_tokenizer = None
    ld_model = None
    ps_tokenizer = None
    ps_model = None
    es_tokenizer = None
    es_model = None

    def detect_language(self, in_list):
        if self.ld_model is None:
            self.ld_tokenizer = AutoTokenizer.from_pretrained(self.ld_model_name)
            self.ld_model = AutoModelForSequenceClassification.from_pretrained(self.ld_model_name)

        encoded_input = self.ld_tokenizer(in_list, return_tensors='pt', padding=True, truncation=True)
        output = self.ld_model(**encoded_input)
        scores = torch.nn.functional.softmax(output[0], dim=1)
        lang = list(torch.argmax(scores, dim=1).detach().numpy())
        return lang

    def persian_sentiment(self, in_list):
        if self.ps_model is None:
            self.ps_tokenizer = MT5Tokenizer.from_pretrained(self.ps_model_name)
            self.ps_model = MT5ForConditionalGeneration.from_pretrained(self.ps_model_name)
        chunks = [in_list[x:x + 100] for x in range(0, len(in_list), 100)]
        out_l = []
        for c in chunks:
            encoded_input = self.ps_tokenizer(c, return_tensors='pt', padding=True, truncation=True)
            output = self.ps_model.generate(**encoded_input)
            out_list = self.ps_tokenizer.batch_decode(output, skip_special_tokens=True)
            out_l += out_list
        return out_l

    def english_sentiment(self, in_list):
        if self.es_model is None:
            self.es_tokenizer = AutoTokenizer.from_pretrained(self.es_model_name)
            self.es_model = AutoModelForSequenceClassification.from_pretrained(self.es_model_name)
        chunks = [in_list[x:x + 100] for x in range(0, len(in_list), 100)]
        out_l = []
        for c in chunks:
            encoded_input = self.es_tokenizer(c, return_tensors='pt', padding=True, truncation=True)
            output = self.es_model(**encoded_input)
            scores = torch.nn.functional.softmax(output[0], dim=1)
            sentiment_l = list(torch.argmax(scores, dim=1).detach().numpy())

            for s in sentiment_l:
                if s == 0:
                    out_l.append('negative')
                elif s == 1:
                    out_l.append('no sentiment expressed')
                elif s == 2:
                    out_l.append('positive')
                else:
                    print('error in label assignment')
        return out_l
