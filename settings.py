class Settings():
    # IK should use ENV; but too lazy to set it
    def __init__(self):
        self.alias = "default"
        self.vector_db_name = "vector_db.db"
        self.mm_db_name = "multi_media_db.db"
        self.host = "127.0.0.1"
        self.user = "user"
        self.password = "Santa_Claus"
        self.port = 19530
        self.link = "temp link"
        self.vector_dims = 768
        self.vector_metrics_type = "L2"
        self.vector_index_type = "IVF_FLAT"
        self.params = {
            "nList": 768
        }
        self.model_path = "./model"
        self.qa_model_path = "./qa_model"
        self.tokenizer_path = "./tokenizer"
        self.typo_corrector_path = "./typo_corrector"
        self.source_model_path = "esakrissa/IndoBERT-SQuAD"
        self.source_tokenizer_path = "esakrissa/IndoBERT-SQuAD"
        self.source_qa_model_path = "esakrissa/IndoBERT-SQuAD"
        self.source_typo_corrector_path = "oliverguhr/spelling-correction-english-base"
        self.insert_batch_size = 20
        self.index_file_name = "vector_index.index"
        self.gemini_result_file_name = "gemini_result.csv"
        self.bert_result_file_name = "bert_result.csv"
        self.retrieval_result_file_name = "retrieval.csv"
        self.GOOGLE_API_KEY = "AIzaSyDasGPv1tjNi9YE48jgapws3vi5p6qm1n8"
        self.records_dir = "records/"
