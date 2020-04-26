class config:
    protocol = {
        "PROTOCOL_VERSION": '1.0'
    }
    statusCode = {
        'SUCCESS': '200',
        'FAILED': '500',
    }
    taskStates = {
        'PENDING': 'PENDING',
        'IN_PROGRESS': 'IN_PROGRESS',
        'COMPLETED': 'COMPLETED'
    }
    taskStateEnums = {
        'PENDING': 1,
        'IN_PROGRESS': 2,
        'COMPLETED': 3
    }
    nodeStateEnums = {
        'AVAILABLE': 1,
        'BUSY': 2,
        'NOT_OPERATIONAL': 3
    }
    taskResultEnums = {
        'SUCCESS': 1,
        'FAILED': 2
    }
    taskOutcome = {
        'SUCCESS': 'SUCCESS',
        'FAILED': 'FAILED'
    }
    coordinator = {
        'COORDINATOR_EXECUTE_TASK': 'coordinator-executeTask'
    }
    task = {
        'TASK_NAME': 'taskName',
        'PARAMETERS': 'parameters'
    }
    error = {
        'CONNECTION_REFUSED' : 'Connection refused',
        'TIMED_OUT':'timed out'
    }
    server = {
        "NOT-OPERATIONAL": 'Server is not ready',
        "AVAILABLE": 'Server is ready to accept the request'
    }
