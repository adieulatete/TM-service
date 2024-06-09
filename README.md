## Task manager

### General information about the project
Service for managing tasks within the company.

#### Functional

Endpoints:  
• Endpoint for receiving tokens - /api/token/; api/token/refresh/  
• Endpoint for obtaining information about the current user - /api/users/; /api/users/me  
• Endpoints for working with tasks - /api/tasks/; /api/tasks/create_task/; /api/tasks/take_task/; /api/tasks/close_task/; /api/tasks/edit_task/  
• Endpoints for working with employees and customers - /register

#### Technologies used

`Python`, `Sqlite3`, `Git`, `Docker`

#### Libraries used

[`Django`](https://github.com/django/django),
[`Django REST framework`](https://github.com/encode/django-rest-framework),
[`Simple JWT`](https://github.com/jazzband/djangorestframework-simplejwt)

### Deploy 

```bash
cd ~
git clone https://github.com/adieulatete/TM_service.git
cd ~/TM_service
docker-compose up --build -d
```

### Tests

```bash
docker exec -it container_id /bin/bash
cd task_manager
python manage.py test
```
