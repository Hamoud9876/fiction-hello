FROM public.ecr.aws/lambda/python:3.8

# Install dependencies
COPY etl/src/lambda_transform/requirements_transform.txt .
RUN pip install -r requirements_transform.txt -t ${LAMBDA_TASK_ROOT}

# Copy code
COPY etl/src/lambda_transform ${LAMBDA_TASK_ROOT}/etl/src/lambda_transform
COPY etl/utils ${LAMBDA_TASK_ROOT}/etl/utils

# Ensure __init__.py exists
COPY etl/src/__init__.py ${LAMBDA_TASK_ROOT}/etl/src/__init__.py
COPY etl/__init__.py ${LAMBDA_TASK_ROOT}/etl/__init__.py
COPY etl/utils/__init__.py ${LAMBDA_TASK_ROOT}/etl/utils/__init__.py

# Set Python path
ENV PYTHONPATH="/var/task"

# Lambda handler
CMD ["etl.src.lambda_transform.lambda_transform.lambda_transform"]
