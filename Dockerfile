FROM python:3.13-slim AS build

RUN python -m venv /app
ENV PATH="/app/bin:$PATH"
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN pip install .


FROM python:3.13-slim
COPY --from=build /app /app
ENV PATH="/app/bin:$PATH"
ENTRYPOINT [ "zaphod-power" ]