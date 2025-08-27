import tinyflow_config as config


str_uuid='5cd854ff-0036-4826-969c-1a61710d8d97'


trans1 = config.Orchestrate("ConfigYAML.yaml",str_uuid)


meh = trans1.execute_steps()





