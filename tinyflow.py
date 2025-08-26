import tinyflow_config as config
import duckdb
import asyncio

str_uuid='5cd854ff-0036-4826-969c-1a61710d8d97'
TinyFlowYAML = config.TinyFlowYAML("ConfigYAML.yaml",str_uuid)
TransformYAML = config.TransformYAML("ConfigYAML.yaml")

tinyflow= TinyFlowYAML.dataflows_yaml_stages()
transforms = TransformYAML.yaml_tuple()

# print('transforms', transforms)


trans1 = config.Orchestrate("ConfigYAML.yaml")



meh = trans1.execute_steps()





