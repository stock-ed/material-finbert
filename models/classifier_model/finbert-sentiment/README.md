---
language: "en"
tags:
- financial-sentiment-analysis
- sentiment-analysis
widget:
- text: "Stocks rallied and the British pound gained."
---

FinBERT is a pre-trained NLP model to analyze sentiment of financial text. It is built by further training the BERT language model in the finance domain, using a large financial corpus and thereby fine-tuning it for financial sentiment classification. [Financial PhraseBank](https://www.researchgate.net/publication/251231107_Good_Debt_or_Bad_Debt_Detecting_Semantic_Orientations_in_Economic_Texts) by Malo et al. (2014) is used for fine-tuning. For more details, please see [FinBERT: Financial Sentiment Analysis with Pre-trained Language Models](https://arxiv.org/abs/1908.10063).

The model will give softmax outputs for three labels: positive, negative or neutral.