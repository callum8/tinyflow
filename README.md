
# TinyFlow

TinyFlow is a lightweight Python framework for orchestrating and executing data transformation workflows using DuckDB and YAML configuration files. It supports synchronous and asynchronous query execution, and is designed for easy extensibility and automation.

## Features
- Define dataflows, feeds, and transforms in a YAML config file
- Execute SQL queries and export results to Parquet files using DuckDB
- Run multiple tasks in parallel using Python's asyncio
- Modular OOP design with main classes: `Config`, `TinyFlowYAML`, `TransformYAML`, and `Orchestrate`

## YAML Configuration
The main configuration file is `ConfigYAML.yaml`, which contains:
- `dataflows`: Defines the stages and tasks for each workflow
- `feeds`: Lists input data sources
- `transforms`: Contains SQL queries to be executed

Example transform:
```yaml
transforms:
- query: |
		copy (
			select a.name, count(*) 
			from 'admin_testing\\test2.parquet' a
			inner join 'admin_testing\\test2.parquet' b
			on a.name = b.name
			group by all
		)
		TO 'C:\\envs\\tinyflow\\outputok.parquet'
		(FORMAT parquet);
	insert_uuid: ...
	name: Feed1
```

## Main Classes
- `Config`: Base class for loading YAML files
- `TinyFlowYAML`: Loads and parses dataflow stages from YAML
- `TransformYAML`: Loads and parses transform queries from YAML
- `Orchestrate`: Inherits from both, builds task dictionary, and executes workflow steps

## Async Execution
TinyFlow uses Python's `asyncio` to run multiple queries in parallel. See `Orchestrate.run_async_task_group` for details.

## Example Usage
```python
import tinyflow_config as config
import duckdb

str_uuid = '5cd854ff-0036-4826-969c-1a61710d8d97'
trans1 = config.Orchestrate('ConfigYAML.yaml', str_uuid)
trans1.execute_steps()
```

## Requirements
- Python 3.11+
- duckdb
- PyYAML

Install dependencies:
```bash
pip install -r requirements.txt
```

## License
MIT License
