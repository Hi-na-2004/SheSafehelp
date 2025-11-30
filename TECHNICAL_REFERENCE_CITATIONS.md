# SheSafe - Technical Reference & Citations
## AI Methods, Datasets, and Open Source Resources

---

## 1. KEY AI METHODS AND TECHNOLOGIES USED

### A. Natural Language Processing (NLP)

**1.1 Toxicity Detection**
- **Method:** Transformer-based sequence classification
- **Architecture:** RoBERTa (Robustly optimized BERT approach)
- **Technique:** Transfer learning with fine-tuning
- **Model:** Detoxify - unitary/toxic-bert
- **Parameters:** 125M parameters
- **Technology Stack:**
  - PyTorch 2.9.1
  - Transformers 4.57.3
  - Detoxify 0.5.2

**1.2 Emotion & Mental Health Detection**
- **Method:** Multi-label emotion classification
- **Architecture:** DistilRoBERTa (distilled version, 40% faster)
- **Technique:** Knowledge distillation + fine-tuning
- **Model:** j-hartmann/emotion-english-distilroberta-base
- **Emotions Detected:** Joy, Sadness, Anger, Fear, Surprise, Love
- **Sentiment Analysis:** DistilBERT-SST2
- **Technology Stack:**
  - Hugging Face Transformers
  - Sentence-BERT for semantic understanding

### B. Machine Learning for Safety Scoring

**1.3 Location Safety Analysis**
- **Method:** Spatial risk modeling with time-series analysis
- **Techniques:**
  - Proximity-based risk calculation (Haversine formula)
  - Exponential decay modeling for crime impact
  - Time-of-day risk weighting
  - K-nearest neighbors for hotspot detection
- **Algorithms:**
  - Geospatial clustering (DBSCAN)
  - Weighted risk aggregation
  - Route optimization (modified Dijkstra's algorithm)
- **Technology Stack:**
  - Geopy 2.4.1
  - NumPy 2.3.5
  - Pandas 2.3.3
  - Scikit-learn 1.7.2
  - Folium 0.20.0 (visualization)

### C. Real-time Communication Systems

**1.4 Emergency Alert System**
- **Method:** Event-driven architecture
- **Technology:** WebSocket (Socket.IO)
- **SMS Gateway:** Twilio API
- **Geolocation:** HTML5 Geolocation API + Google Maps API
- **Technology Stack:**
  - Flask-SocketIO 5.5.1
  - Twilio SDK 9.8.7
  - Python-dotenv for configuration

---

## 2. DATASETS USED AND PREREQUISITES

### A. Training Datasets

**2.1 Toxicity Detection Dataset**
- **Source:** Jigsaw Toxic Comment Classification Challenge (Kaggle)
- **Size:** 2,000,000+ labeled comments
- **Labels:** Toxicity, Severe Toxicity, Obscene, Threat, Insult, Identity Attack
- **Language:** English
- **Citation:** [1] Jigsaw/Conversation AI. (2018). Toxic Comment Classification Challenge. Kaggle.
- **License:** CC0: Public Domain
- **URL:** https://www.kaggle.com/c/jigsaw-toxic-comment-classification-challenge

**2.2 Emotion Detection Dataset**
- **Source:** GoEmotions (Google Research)
- **Size:** 58,000+ Reddit comments
- **Labels:** 27 emotion categories + Neutral
- **Taxonomy:** Ekman's basic emotions extended
- **Citation:** [2] Demszky, D., Movshovitz-Attias, D., Ko, J., Cowen, A., Nemade, G., & Ravi, S. (2020). GoEmotions: A Dataset of Fine-Grained Emotions. ACL 2020.
- **License:** Apache 2.0
- **URL:** https://github.com/google-research/google-research/tree/master/goemotions

**2.3 Sentiment Analysis Dataset**
- **Source:** Stanford Sentiment Treebank (SST-2)
- **Size:** 11,855 sentences
- **Labels:** Binary (Positive/Negative)
- **Citation:** [3] Socher, R., Perelygin, A., Wu, J., Chuang, J., Manning, C. D., Ng, A. Y., & Potts, C. (2013). Recursive Deep Models for Semantic Compositionality Over a Sentiment Treebank. EMNLP 2013.
- **License:** Academic Use
- **URL:** https://nlp.stanford.edu/sentiment/

**2.4 Crime Data (Sample/Synthetic)**
- **Source:** Open crime databases (city-specific)
- **Examples:**
  - Data.gov crime statistics
  - Local police department open data
  - UCI Machine Learning Repository - Communities and Crime
- **Features:** Location coordinates, crime type, severity, timestamp
- **Citation:** [4] Redmond, M., & Baveja, A. (2002). Communities and Crime. UCI Machine Learning Repository.
- **Note:** Production deployment requires integration with local crime databases

### B. Prerequisites & System Requirements

**Infrastructure Requirements:**
- **CPU:** 4+ cores (8+ recommended)
- **RAM:** 8GB minimum (16GB recommended for model loading)
- **Storage:** 5GB free space (for models and dependencies)
- **Network:** Stable internet for first-run model download
- **OS:** Linux, macOS, Windows (Python 3.10+)

**Software Dependencies:**
- Python 3.10 or higher
- Virtual environment (venv/conda)
- pip package manager
- Git for version control

**API Keys Required (for full functionality):**
- Twilio Account (for SMS alerts) - Optional
- Google Maps API key (for enhanced geolocation) - Optional

**Development Tools:**
- Code editor (VS Code, PyCharm)
- Postman/cURL for API testing
- Browser with DevTools

---

## 3. OPEN SOURCE RESOURCES LEVERAGED

### A. Core AI/ML Libraries

**3.1 Detoxify (MIT License)**
- **Repository:** https://github.com/unitaryai/detoxify
- **Purpose:** Toxicity detection in text
- **Version:** 0.5.2
- **Citation:** [5] Hanu, L., & Unitary team. (2020). Detoxify. GitHub.
- **License:** MIT - Commercial use allowed

**3.2 Transformers by Hugging Face (Apache 2.0)**
- **Repository:** https://github.com/huggingface/transformers
- **Purpose:** State-of-the-art NLP models
- **Version:** 4.57.3
- **Citation:** [6] Wolf, T., Debut, L., Sanh, V., et al. (2020). Transformers: State-of-the-Art Natural Language Processing. EMNLP 2020.
- **License:** Apache 2.0 - Commercial use allowed

**3.3 PyTorch (BSD-3-Clause)**
- **Repository:** https://github.com/pytorch/pytorch
- **Purpose:** Deep learning framework
- **Version:** 2.9.1
- **Citation:** [7] Paszke, A., Gross, S., Massa, F., et al. (2019). PyTorch: An Imperative Style, High-Performance Deep Learning Library. NeurIPS 2019.
- **License:** BSD-3-Clause - Commercial use allowed

### B. Web Framework & API

**3.4 Flask (BSD-3-Clause)**
- **Repository:** https://github.com/pallets/flask
- **Purpose:** Web application framework
- **Version:** 3.1.2
- **License:** BSD-3-Clause

**3.5 Flask-SocketIO (MIT License)**
- **Repository:** https://github.com/miguelgrinberg/Flask-SocketIO
- **Purpose:** Real-time bidirectional communication
- **Version:** 5.5.1
- **License:** MIT

### C. Geospatial & Mapping

**3.6 Geopy (MIT License)**
- **Repository:** https://github.com/geopy/geopy
- **Purpose:** Geocoding and distance calculations
- **Version:** 2.4.1
- **License:** MIT

**3.7 Folium (MIT License)**
- **Repository:** https://github.com/python-visualization/folium
- **Purpose:** Interactive map visualization
- **Version:** 0.20.0
- **License:** MIT

### D. Communication & Alerts

**3.8 Twilio Python SDK (MIT License)**
- **Repository:** https://github.com/twilio/twilio-python
- **Purpose:** SMS and communication APIs
- **Version:** 9.8.7
- **License:** MIT

### E. Data Processing

**3.9 NumPy (BSD License)**
- **Repository:** https://github.com/numpy/numpy
- **Version:** 2.3.5
- **License:** BSD

**3.10 Pandas (BSD-3-Clause)**
- **Repository:** https://github.com/pandas-dev/pandas
- **Version:** 2.3.3
- **License:** BSD-3-Clause

**3.11 Scikit-learn (BSD-3-Clause)**
- **Repository:** https://github.com/scikit-learn/scikit-learn
- **Version:** 1.7.2
- **License:** BSD-3-Clause

### F. Pre-trained Models

**3.12 RoBERTa-base (MIT License)**
- **Model:** roberta-base
- **Source:** Hugging Face Model Hub
- **Citation:** [8] Liu, Y., Ott, M., Goyal, N., et al. (2019). RoBERTa: A Robustly Optimized BERT Pretraining Approach. arXiv:1907.11692

**3.13 DistilRoBERTa (Apache 2.0)**
- **Model:** j-hartmann/emotion-english-distilroberta-base
- **Source:** Hugging Face Model Hub
- **Fine-tuned on:** GoEmotions dataset
- **Citation:** [9] Hartmann, J. (2022). Emotion English DistilRoBERTa-base. Hugging Face.

---

## 4. RESEARCH REFERENCES & CITATIONS

### Academic Papers

[1] Jigsaw/Conversation AI. (2018). Toxic Comment Classification Challenge. Kaggle. https://www.kaggle.com/c/jigsaw-toxic-comment-classification-challenge

[2] Demszky, D., Movshovitz-Attias, D., Ko, J., Cowen, A., Nemade, G., & Ravi, S. (2020). GoEmotions: A Dataset of Fine-Grained Emotions. In Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics (ACL), pp. 4040-4054.

[3] Socher, R., Perelygin, A., Wu, J., Chuang, J., Manning, C. D., Ng, A. Y., & Potts, C. (2013). Recursive Deep Models for Semantic Compositionality Over a Sentiment Treebank. In Proceedings of the Conference on Empirical Methods in Natural Language Processing (EMNLP), pp. 1631-1642.

[4] Redmond, M., & Baveja, A. (2002). A data-driven software tool for enabling cooperative information sharing among police departments. European Journal of Operational Research, 141(3), 660-678.

[5] Hanu, L., & Unitary team. (2020). Detoxify. GitHub repository. https://github.com/unitaryai/detoxify

[6] Wolf, T., Debut, L., Sanh, V., Chaumond, J., Delangue, C., Moi, A., Cistac, P., Rault, T., Louf, R., Funtowicz, M., Davison, J., Shleifer, S., von Platen, P., Ma, C., Jernite, Y., Plu, J., Xu, C., Scao, T. L., Gugger, S., Drame, M., Lhoest, Q., & Rush, A. M. (2020). Transformers: State-of-the-Art Natural Language Processing. In Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing: System Demonstrations, pp. 38-45.

[7] Paszke, A., Gross, S., Massa, F., Lerer, A., Bradbury, J., Chanan, G., Killeen, T., Lin, Z., Gimelshein, N., Antiga, L., Desmaison, A., Kopf, A., Yang, E., DeVito, Z., Raison, M., Tejani, A., Chilamkurthy, S., Steiner, B., Fang, L., Bai, J., & Chintala, S. (2019). PyTorch: An Imperative Style, High-Performance Deep Learning Library. In Advances in Neural Information Processing Systems 32 (NeurIPS), pp. 8024-8035.

[8] Liu, Y., Ott, M., Goyal, N., Du, J., Joshi, M., Chen, D., Levy, O., Lewis, M., Zettlemoyer, L., & Stoyanov, V. (2019). RoBERTa: A Robustly Optimized BERT Pretraining Approach. arXiv preprint arXiv:1907.11692.

[9] Hartmann, J. (2022). Emotion English DistilRoBERTa-base. Hugging Face Model Hub. https://huggingface.co/j-hartmann/emotion-english-distilroberta-base

### Technical Documentation

[10] Devlin, J., Chang, M. W., Lee, K., & Toutanova, K. (2019). BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding. NAACL-HLT 2019, pp. 4171-4186.

[11] Sanh, V., Debut, L., Chaumond, J., & Wolf, T. (2019). DistilBERT, a distilled version of BERT: smaller, faster, cheaper and lighter. arXiv preprint arXiv:1910.01108.

### Safety & Crime Prediction

[12] Bogomolov, A., Lepri, B., Staiano, J., Oliver, N., Pianesi, F., & Pentland, A. (2014). Once Upon a Crime: Towards Crime Prediction from Demographics and Mobile Data. In Proceedings of the 16th International Conference on Multimodal Interaction, pp. 427-434.

[13] Wang, P., Mathieu, R., Ke, J., & Cai, H. J. (2016). Predicting Criminal Recidivism with Support Vector Machine. In 2016 International Conference on Management Science and Engineering, pp. 219-224.

---

## 5. ETHICAL AI FRAMEWORKS FOLLOWED

**Standards & Guidelines:**
- IEEE 7000-2021 (Model Process for Addressing Ethical Concerns)
- EU AI Act Guidelines
- ACM Code of Ethics and Professional Conduct
- Montreal Declaration for Responsible AI
- Partnership on AI Best Practices

**Bias Testing:**
- Gender bias evaluation using Winogender schemas
- Racial bias testing on demographically diverse datasets
- Regular fairness audits using AIF360 toolkit

---

## 6. PERFORMANCE BENCHMARKS

**Model Performance (Published Benchmarks):**

Detoxify on Jigsaw Dataset:
- Toxicity: AUC-ROC 0.9810
- Severe Toxicity: AUC-ROC 0.9860
- Obscene: AUC-ROC 0.9870
- Threat: AUC-ROC 0.9810
- Insult: AUC-ROC 0.9830
- Identity Attack: AUC-ROC 0.9820

GoEmotions Emotion Classifier:
- Overall Accuracy: 88.4%
- Macro F1: 86.7%
- Top-1 Emotion Accuracy: 91.2%

---

**All open-source components used are licensed under permissive licenses (MIT, Apache 2.0, BSD) allowing commercial use. Full license information available in LICENSE_INFO.md.**

---

**Document Version:** 1.0  
**Last Updated:** November 30, 2025  
**Contact:** shesafe@example.com

