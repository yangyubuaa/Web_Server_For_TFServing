import torch
from transformers import AlbertForSequenceClassification, BertTokenizer

def torchmodel2onnx():
    # 设置batchsize和输入的最大长度
    Batch_size = 1
    seg_length = 64

    # 读取训练好的模型
    model_path = "albert_tiny_pytorch"
    albert_model = AlbertForSequenceClassification.from_pretrained(model_path)

    # 将模型置于eval模式
    albert_model.eval()

    # 随机初始化模型输入
    dummy_input0 = torch.zeros(Batch_size, seg_length).long()
    dummy_input1 = torch.zeros(Batch_size, seg_length).long()
    dummy_input2 = torch.zeros(Batch_size, seg_length).long()

    # 将pytorch模型导出为onnx格式
    torch.onnx.export(albert_model,
                      (dummy_input0, dummy_input1, dummy_input2),
                      "output.onnx",
                      input_names=["input_ids", "token_type_ids", "attention_mask"],
                      output_names=["loss", "logits", "hidden_states", "attentions"],
                      opset_version=12)

if __name__ == '__main__':
    torchmodel2onnx()
    
