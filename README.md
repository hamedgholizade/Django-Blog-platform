# Django Blog Platform with Tagging System

[![Django Version](https://img.shields.io/badge/django-3.2%2B-green)](https://www.djangoproject.com/)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)

A full-featured blogging platform with advanced user roles, post management, tagging system, and comment moderation.

## Features

- **User Management System** with different roles (Admin, Writer, Viewer)
- **Blog Post Creation** with rich text content and images
- **Tagging System** for content organization
- **Post Moderation** with approval workflow (Pending/Confirmed/Refused/Hidden)
- **Comment System** with approval controls
- **Search Functionality** across posts
- **Soft Delete** functionality for all models
- **Pagination** for post lists
- **User Session Tracking** for recently viewed posts

## Models Overview

### Core Models
- **BaseModel**: Abstract model with common fields (`is_deleted`, `created_at`, `last_update`)
- **User**: Custom user model extending AbstractUser with role-based permissions
- **Post**: Blog posts with status management and tagging
- **Comment**: User comments with approval system
- **Tag**: Categorization system for posts

## Installation
### Prerequisites
- Python 3.8+
- Django 3.2+
- Virtual environment (recommended)


### setup Installation


1. Clone the repository:
```bash
git clone git@github.com:parsaz13/django-blog-platform.git

cd django-blog-platform
```

2. Create and Activate a Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```
4. Set up the database
```bash
python manage.py migrate
```
5. Create a superuser
```bash
python manage.py createsuperuser
```
6. Run the development server
```bash
python manage.py runserver
```
## Usage

### User roles

Admin: Full access to all features

Writer: Can create and manage their own posts

Viewer: Can view approved posts and comment

### Creating a Post

Log in as a Writer or Admin

Navigate to /blog/create_post/ # or click on blog and then on create a create a new post


Fill in the form (title, content, image, tags)

Submit for approval (Admin will need to approve)

### Managing Posts (Admin)
Approve posts at /blog/pending-posts/

View all posts at /blog/

### Managing Comments (Admin)
Moderate comments at /blog/pending-comments/

Approve or hide comments as needed

### Searching Posts
Use the search bar to find posts by content or title


## API Endpoints
Endpoint	Method	Description
/blog/	GET	List all approved posts
/blog/<slug>/	GET	View post details
/blog/create_post/	POST	Create new post
/blog/pending-posts/	GET	List pending posts (admin only)
/blog/approve-post/<id>/	POST	Approve a post (admin only)


## Configuration
#### Environment variables set in .env file
```bash
DEBUG=True
SECRET_KEY=your_secret_key_here
DB_NAME=your_database_name_in_postgres
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost,127.0.0.1
DB_PORT=5432
```

## Contributing

### Collaborators
github:
- hamedgholizade
- parsaz13
- dev-saman007
- MohammadJavid-Hosseini
#### We welcome contributions! Please follow these steps:

- Fork the repository

- Create your feature branch (git checkout -b feature/AmazingFeature)

- Commit your changes (git commit -m 'Add some AmazingFeature')

- Push to the branch (git push origin feature/AmazingFeature)

- Open a Pull Request

