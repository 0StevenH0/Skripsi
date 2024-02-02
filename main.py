import db_controller,fix_typo,rag_pipeline
import torch


if __name__ == "__main__":
    model = rag_pipeline.BERT_QA()
    question = "Who is te daughter of A?"
    answer = """B'S Father's C and her mother is A"""
    inputs = model.tokenizer(question, answer, return_tensors="pt")

    outputs = model.QA(**inputs)
    start_scores = outputs.start_logits
    end_scores = outputs.end_logits

    start_index = torch.argmax(start_scores)
    end_index = torch.argmax(end_scores)

    answer_tokens = inputs["input_ids"][0][start_index:end_index + 1]
    answer = model.tokenizer.decode(answer_tokens, skip_special_tokens=True)
    print(answer)