## What is Apache Airflow?

Apache Airflow is an elegant Workflow Engine that can effortlessly manage, schedule, and monitor your workflows programmatically. It is a  popular Open-Source tool preferred by Data Engineers for orchestrating workflows or pipelines.

Airflow refers to Data pipelines as **Directed Acyclic Graphs (DAGs)**of operations where you can seamlessly identify your Data Pipelines’ dependencies, progress, logs, code, trigger tasks, and success status.

Airflow’s modular architecture is made to scale allowing you to enjoy its lightning-fast data processing speed. Defined in Python, you can  instantiate Data Pipelines dynamically, create workflows, build ML models, transfer data, etc. Its easy-to-use UI helps you keep a tab on the status and logs of completed and ongoing tasks.

With Robust Integrations like Airflow Databricks Integration, you can easily execute your tasks on various Cloud Platforms

### What is a DAG?

**DAG**  is a **D**irected **A**cyclic **G**raph, this means that is a graph composed by a set of edges *E_ab* with directions from one vertex *V_a* to a vertex *V_b,* E={*Va,Vb*}. A DAG is also acyclic meaning that there is no closed loop on the graph.

![https://image.slidesharecdn.com/etlmachinelearningslidesphpindonesia-160619044313/95/etl-machine-learning-13-638.jpg?cb=1466311915](https://image.slidesharecdn.com/etlmachinelearningslidesphpindonesia-160619044313/95/etl-machine-learning-13-638.jpg?cb=1466311915)

### What is a DAG in Airflow?

In an Airflow Python script a **DAG is just a configuration file** specifying the DAG’s structure as code. The actual tasks defined here will run in a different context from the context of this script. Different tasks run on different workers at different points in time, which means that this script cannot be used to cross communicate between tasks. 

To instantiate a DAG you need a DAG object to nest all the tasks, with:

- `dag_id`
- `schedule_interval`

**In Apache 2.0**  they introduced the decorator paradigm, this allows for the use of decorators to instantiate DAGs using `@dag` , with the Python function name acting as the DAG identifier. 

### Tasks

Tasks are generated when instantiating operator objects. An object instantiated from an operator is called a task. The first argument `task_id` acts as a unique identifier for the task.

The precedence rules for a task are as follows:

1. Explicitly passed arguments
2. Values that exist in the `default_args` dictionary
3. The operator’s default value, if one exists

A task must include or inherit the arguments `task_id` and `owner`, otherwise Airflow will raise an exception.

For each **Task** is possible to create templates based on [Jinja Templating](https://jinja.palletsprojects.com/en/2.11.x/), you can also define the use bash comands to run the pipeline files, moreover you can set your own macros following Jinja Documentation.

Each task can have its own documentation in Markdown, then this will appear in Airflow dashboard.

**In Apache 2.0**  they introduced the decorator paradigm, this allows for the use of decorators to instantiate Tasks using `@task` , with the Python function name acting as a unique identifier for the task.

 **Chain Operations** 

**In Airflow 1.0** you can set up dependencies by using:

- task1.set_upstream(task2)
- task2.set_downstream(task1)
- task1 >> task2 (bit shift operator )
- task2 << task1 (bit shift operator )

**In Airflow 2.0**  everything changed, since you can define the function name as the identifier for the Task you want to perform. Let’s imagine you have created a Extract, Transform, and Load tasks defined based on the Python functions. 

You can run a DAG pipeline as:

```python
order_data = extract() 
order_summary = transform(order_data) 
load(order_summary["total_order_value"])
```

Being the **extract, transform** and **load** the name of thee functions that define the tasks.

The dependencies between the tasks and the passing of data between these tasks which could be running on different workers on different nodes on the network is all handled by Airflow. 

Finally to run the script as a DAG we need to invoque the Python function that was set up using the `@dag`.

## **Running Airflow locally**

1- Lets create a python environment 

```bash
python -m venv airflow_env
source airflow_env/bin/activate
```

2- Install Apache Airflow in your environment using pip 

```bash
# Airflow needs a home. `~/airflow` is the default, but you can put it
# somewhere else if you prefer (optional)
export AIRFLOW_HOME=~/<absolute path to you working dir>

# Install Airflow using the constraints file
AIRFLOW_VERSION=2.3.4
PYTHON_VERSION="$(python --version | cut -d " " -f 2 | cut -d "." -f 1-2)"
# For example: 3.7
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
# For example: https://raw.githubusercontent.com/apache/airflow/constraints-2.3.4/constraints-3.7.txt
pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"

# The Standalone command will initialise the database, make a user,
# and start all components for you.
airflow standalone

# Visit localhost:8080 in the browser and use the admin account details
# shown on the terminal to login.
# Enable the example_bash_operator dag in the home page
```

3- Start a Airflow development environment

```bash
# Creat a SQL Lite database
airflow db init

# set up user credentials 
airflow users create \
    --username admin \
    --firstname Peter \
    --lastname Parker \
    --role Admin \
    --email spiderman@superhero.org
# Then enter your password 

# Finally start a webserver 
airflow webserver -p 8080
```

4- Create a folder inside the AIRFLOW_HOME directory for your dag files, and store the [tutorial.py](http://tutorial.py) inside. 

[tutorial.py](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/07726841-365c-498d-8079-78be9057acaa/tutorial.py)

```bash
cd AIRFLOW_HOME
mkdir dags
# save the tutorial.py file inside dags folder 
# run the python script to ensure that there are no erros
python dags/tutorial.py
```

5- **Metadata Validation**

```bash
# print the list of active DAGs
airflow dags list

# prints the list of tasks in the "tutorial" DAG
airflow tasks list first_taskflow_api_etl

# prints the hierarchy of tasks in the "tutorial" DAG
airflow tasks list first_taskflow_api_etl --tree
```

6 - **Testing**

```bash
airflow tasks test first_taskflow_api_etl extract  2015-06-01
```

7- **Backfill**

```bash
# start your backfill on a date range
airflow dags backfill first_taskflow_api_etl \
    --start-date 2015-06-01 \
    --end-date 2015-06-07
```

## **Using the TaskFlow API with Docker or Virtual Environments**

1- Make sure you have Docker installed 

2- Download the .yaml file

3- Run

```bash
mkdir -p ./dags ./logs ./plugins 
echo -e "AIRFLOW_UID=$(id -u)" > .env
docker-compose up airflow-init
```

### Importante Modules to bare in mind

datetime 

timedelta 

DAG

BashOperator

SEE WEBSITE

[https://medium.com/analytics-and-data/setting-up-airflow-on-azure-connecting-to-ms-sql-server-8c06784a7e2b](https://medium.com/analytics-and-data/setting-up-airflow-on-azure-connecting-to-ms-sql-server-8c06784a7e2b)

