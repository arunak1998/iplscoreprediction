FROM python:3.9-slim
# Declare build arguments
ARG GROQ_API_KEY
ARG LANGSMITH_API_KEY
ARG MONGO_DB
ARG LANGCHAIN_TRACING_v2

# Set environment variables using build arguments
ENV GROQ_API_KEY=$GROQ_API_KEY
ENV LANGSMITH_API_KEY=$LANGSMITH_API_KEY
ENV MONGO_DB=$MONGO_DB
ENV LANGCHAIN_TRACING_v2=$LANGCHAIN_TRACING_v2
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that the FastAPI app will run oEXPOSE 8000
EXPOSE 8000
# Define the command to run the FastAPI app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]