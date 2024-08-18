import milvus
import db_controller
# import fix_typo
# import rag_pipeline
# import torch


class Settings():
    # IK should use ENV; but too lazy to set it
    def __init__(self):
        self.vector_db_name = "vector_db"
        self.mm_db_name = "multi_media_db"
        self.host = "127.0.0.1"
        self.user = "user"
        self.password = "Santa_Claus"
        self.port = 19530
        self.link = "temp link"

if __name__ == "__main__":
    settings = Settings()
    connection = db_controller.Connector(
        settings.link,
        settings.vector_db_name,
        settings.host,
        settings.user,
        settings.port,
        settings.password
    )
    connection.create_db(settings.vector_db_name)
    # model = rag_pipeline.BERT_QA()
    # question = "Who is te daughter of A?"
    # answer = """B'S Father's C and her mother is A"""
    # inputs = model.tokenizer(question, answer, return_tensors="pt")
    #
    # outputs = model.QA(**inputs)
    # start_scores = outputs.start_logits
    # end_scores = outputs.end_logits
    #
    # start_index = torch.argmax(start_scores)
    # end_index = torch.argmax(end_scores)
    #
    # answer_tokens = inputs["input_ids"][0][start_index:end_index + 1]
    # answer = model.tokenizer.decode(answer_tokens, skip_special_tokens=True)
    # print(answer)