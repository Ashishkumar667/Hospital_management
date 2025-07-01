# 🏥 Hospital Management API – Django + DRF

A secure backend API that allows doctors and admins to manage patients and their medical records, with token-based authentication and role-based access.

## 🔧 Tech Stack
- Python 3.x
- Django 5.x
- Django REST Framework
- Token Auth
- Swagger (drf-yasg)

---

## 📦 Features

### 👨‍⚕️ Doctor:
- Signup/Login via token
- Create patients
- View only own patients
- Add/view records only for own patients

### 🛡️ Admin:
- View all patients
- View records for any patient

---

## 🚀 API Endpoints

> Base URL: `/api/`

| Method | Endpoint                         | Access   | Description                          |
|--------|----------------------------------|----------|--------------------------------------|
| POST   | `/signup/`                       | Public   | Register doctor/admin                |
| POST   | `/login/`                        | Public   | Login and get token                  |
| GET    | `/patients/`                     | Doctor   | List own patients                    |
| POST   | `/patients/`                     | Doctor   | Create new patient                   |
| GET    | `/patients/`                     | Admin    | View all patients                    |
| POST   | `/patients/records/add`          | Doctor   | Add record to own patient            |
| GET    | `/patients/<id>/records/`        | Both     | View record (admin: all, doctor: own only) |

---

## 🧪 Tests

Run tests with:

```bash
python manage.py test core
