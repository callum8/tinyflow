import yaml

class Config:  
    
    def __init__(self, file):
        self.file=file
        with open(self.file, 'r') as file:
            recs = yaml.safe_load(file)


class TinyFlowYAML(Config):
    def __init__(self, file, str_uuid=None):
        super().__init__(file)
        self.file=file
        self.str_uuid=str_uuid

    def dataflows_yaml(self):
            with open(self.file, 'r') as file:
                recs = yaml.safe_load(file)
                dataset_path = recs['dataflows']
            return dataset_path

    def dataflows_yaml_stages(self):
            yaml1 = self.dataflows_yaml()         
            yaml1 = yaml1[0]['Stages']
            
            key_value_pairs = list(yaml1.items())

            empty_list = []
            for x in key_value_pairs:
                try:
                    number = int(x[0])
                    empty_list.append(x[1]['StageTasks'])
                except ValueError:
                    continue
            return empty_list


class TransformYAML(Config):
    
    def __init__(self, file):
        super().__init__(file)
        self.file=file

    def yaml(self):
        with open(self.file, 'r') as file:
            recs = yaml.safe_load(file)
            dataset_path = recs['transforms']
        return dataset_path

    def yaml_tuple(self):
        yaml = self.yaml()
        tuple1 = [(item['insert_uuid'], item) for item in yaml]
        return tuple1