FROM public.ecr.aws/lambda/python:3.8

# Copy dependencies
COPY etl/src/lambda_transform/requirements_transform.txt requirements.txt
RUN pip install -r requirements.txt -t ${LAMBDA_TASK_ROOT}

# Copy lambda code and utils
COPY etl/src/lambda_transform ${LAMBDA_TASK_ROOT}/etl/src/lambda_transform
COPY etl/utils ${LAMBDA_TASK_ROOT}/etl/utils
COPY etl/src/__init__.py ${LAMBDA_TASK_ROOT}/etl/src/__init__.py
COPY etl/__init__.py ${LAMBDA_TASK_ROOT}/etl/__init__.py
COPY etl/utils/__init__.py ${LAMBDA_TASK_ROOT}/etl/utils/__init__.py

# Set Python path so top-level 'etl' is recognized
ENV PYTHONPATH="/var/task"

# Lambda handler
CMD ["etl.src.lambda_transform.lambda_transform.lambda_transform"]
