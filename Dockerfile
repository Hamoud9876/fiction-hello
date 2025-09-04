#image
FROM public.ecr.aws/lambda/python:3.12

# copy the dependencies
COPY etl/src/lambda_transform/requirements_transform.txt requirements.txt

#install the dependencies
RUN pip install -r requirements.txt -t ${LAMBDA_TASK_ROOT}

#copy the lambda and layers
COPY etl/src/lambda_transform ${LAMBDA_TASK_ROOT}/etl/src/lambda_transform
COPY etl/utils ${LAMBDA_TASK_ROOT}/etl/utils


#setting the lambda handler
CMD ["etl.src.lambda_transform.lambda_transform.lambda_transform"]

