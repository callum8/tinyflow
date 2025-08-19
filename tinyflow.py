import tinyflow_config as config
import duckdb
import asyncio

str_uuid='5cd854ff-0036-4826-969c-1a61710d8d97'
TinyFlowYAML = config.TinyFlowYAML("ConfigYAML.yaml",str_uuid)
TransformYAML = config.TransformYAML("ConfigYAML.yaml")

tinyflow= TinyFlowYAML.dataflows_yaml_stages()
transforms = TransformYAML.yaml_tuple()

print('transforms', transforms)


#we populate a dictionary with all of the transforms.
#this is so we can query this dictionary later to get the transform.
dict1 = {}

for x in transforms:
       dict1[x[0]] = x[1]['query']

print('dict1', dict1)


def lookup_task(task_uuid):
     return dict1[task_uuid]

def execute_query(query):
    conn = duckdb.connect(database=':memory:', read_only=False)
    try:
        result = conn.execute(query).fetchall()
        return result
    except Exception as e:
        print(f"Error executing query: {e}")
    finally:
        conn.close()

async def async_execute_query(query):
    conn = duckdb.connect(database=':memory:', read_only=False)
    try:
        result = conn.execute(query).fetchall()
        return result
    except Exception as e:
        print(f"Error executing query: {e}")
    finally:
        conn.close()

async def run_async_task_group(task_list):
    tasks = []
    async with asyncio.TaskGroup() as tg:
        for task in task_list:
            print(task)
            print(f"Creating task for query {task}")
            task = tg.create_task(async_execute_query(task))
            tasks.append(task)
    results = [task.result() for task in tasks]
    # print(results)

def async_execute_sql(query):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(execute_query(query))


## orchestrate
print('orchestrate')
for stage in tinyflow:
    print(stage)
    print(len(stage))
    if len(stage) > 1:
         list50 = []
         for task in stage:
             print(task)
             task_uuid = task['task_uuid']
             query_string = lookup_task(task_uuid)
             list50.append(query_string)
             asyncio.run(run_async_task_group(list50))
            #  result = execute_query(query_string)
            #  print(result)
    elif len(stage) == 1:
         print('only one')
         task_uuid = stage[0]['task_uuid']
         query_string = lookup_task(task_uuid)
         print(query_string)
         result = execute_query(query_string)
        #  print(result)
    else:
         print('nothing there')