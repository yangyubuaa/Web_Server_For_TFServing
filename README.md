### TFServing前处理的Python Web部署代码
1. model_transfer模块将torch模型加载转为onnx模型再转为pb模型，转为onnx模型需要pytorch环境，转为pb模型需要tensorflow环境，环境在Dockfile给出
2. run_server.py为python web服务启动脚本
3. torch模型到pb模型的转换需要在docker环境中进行，运行转换脚本自动创建docker环境进行转换




### 服务的配置和启动

