FROM python:3-alpine

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate && \
    python manage.py loaddata /app/data/admin_user.json && \
    python manage.py loaddata /app/data/full_body_dumbbell_only_workout.json && \
    python manage.py loaddata /app/data/NSCA_beginner_program.json && \
    python manage.py loaddata /app/data/workout_programs.json && \
    python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]