from asyncio import tasks
import duckdb
import yaml
import asyncio

# from tinyflow import async_execute_query

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
        # self.file=file

    def yaml(self):
        with open(self.file, 'r') as file:
            recs = yaml.safe_load(file)
            dataset_path = recs['transforms']
        return dataset_path

    def yaml_tuple(self):
        yaml = self.yaml()
        tuple1 = [(item['insert_uuid'], item) for item in yaml]
        return tuple1
    



class Orchestrate(TransformYAML,TinyFlowYAML):

    def __init__(self, transforms):
        super().__init__(transforms)
        self.tranforms2=self.yaml_tuple()
        dict1 = {}
        for x in self.tranforms2:
            dict1[x[0]] = x[1]['query']
        self.dict1 = dict1
        self.tinyflow_steps = self.dataflows_yaml_stages()


    def trans(self):
        xx = self.dict1


    def lookup_task(self, task_uuid):
        return self.dict1[task_uuid]

    def execute_query(query):
        conn = duckdb.connect(database=':memory:', read_only=False)
        try:
            result = conn.execute(duckdb.query).fetchall()         
        except Exception as e:
            print(f"Error executing query: {e}")
        finally:
            conn.close()
        return result

    async def async_execute_query(self,query):
        conn = duckdb.connect(database=':memory:', read_only=False)
        try:
            result = conn.execute(query).fetchall()
            return result
        except Exception as e:
            print(f"Error executing query: {e}")
        finally:
            conn.close()

    async def run_async_task_group(self,task_list):
        tasks = []
        async with asyncio.TaskGroup() as tg:
            for task in task_list:
                print(task)
                print(f"Creating task for query {task}")
                task = tg.create_task(self.async_execute_query(task))
                tasks.append(task)
        results = [task.result() for task in tasks]
        # print(results)

    def async_execute_sql(self,query):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self.execute_query(query))
    

    # def execute_steps
    def execute_steps(self):
        steps = self.tinyflow_steps
        for stage in steps:
            print(stage)
            print(len(stage))
            if len(stage) > 1:
                list50 = []
                for task in stage:
                    print(task)
                    task_uuid = task['task_uuid']
                    query_string = self.lookup_task(task_uuid)
                    list50.append(query_string)
                    asyncio.run(self.run_async_task_group(list50))
                    #  result = execute_query(query_string)
                    #  print(result)
            elif len(stage) == 1:
                print('only one')
                task_uuid = stage[0]['task_uuid']
                query_string = self.lookup_task(task_uuid)
                print(query_string)
                result = self.execute_query(query_string)
                #  print(result)
            else:
                print('nothing there')
            return 'finish'
