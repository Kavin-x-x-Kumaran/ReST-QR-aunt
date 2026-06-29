![Logo](docs/logo.png)
# ReST-QR-aunt
A Django REST-Framework API that streamlines restaurant order-giving process by delivering orders directly to the kitchen, reducing the workload on waiters.

# Problem statement
Most restaurants now-a-days rely on waiters to collect orders, deliver them to the kitchen, and deliver the food back to the tables. They must also keep track of the orders and bill the customers. Considering waiters' long working hours, and the number of tables they manage, the probability of human error skyrockets.

# The fix
An app that takes care of ordering and billing. 
- REST-QR-aunt allows users to place orders directly to the kitchen.
- Waiters can focus on delivering food to the right table. 
- The kitchen can update the availability of dishes **LIVE**. 
- Orders are tracked and added to the bill automatically.
- Admin staff can monitor bills, orders, add or delete new food items, menu categories, tables, etc.
    ```
    All in one app!
    ```
# Installation
## From GitHub
1. Open the terminal. Run the following commands.
2. Clone the repository onto your server: `git clone https://github.com/Kavin-x-x-Kumaran/ReST-QR-aunt`
3. Move into the project folder: `cd "ReST-QR-aunt"`
4. Install requirements in a virtual environment: 
    ```
    python -m venv .venv
    .venv/Scripts/activate
    pip install -r requirements.txt
    ```
5. Create a `.env` file in the project folder `REST-QR-AUNT`.
6. Open PgAdmin. (Install it if not done already from `https://www.postgresql.org/download/`)
7. Create a new database.
6. The app has been installed! Move to initialisation.

## Using Docker

# Initialisation
1. Run the following command to generate your secret key:
    ```
    python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
    ```
2. This is your django_secret_key. Copy it for the next step.
3. Copy the contents of `.env.sample` onto your newly created `.env` file.
4. In the terminal, run: `python manage.py runserver`
5. Your server is now running!

# API Endpoints Tree

# API Endpoints Tree

```
/
├── auth/
│   ├── token/                              POST        Obtain JWT token pair
│   ├── refresh/                            POST        Refresh JWT token
│   └── users/
│       ├──                                 GET         List users              (superuser)
│       ├──                                 POST        Create user             (superuser)
│       └── <public_id>/
│           ├──                             GET         Retrieve user           (superuser)
│           ├──                             PUT/PATCH   Update user             (superuser)
│           └──                             DELETE      Delete user             (superuser)
│
├── tables/
│   ├──                                     GET         List tables             (staff)
│   ├──                                     POST        Create table            (superuser)
│   └── <public_id>/
│       ├──                                 GET         Retrieve table          (authenticated)
│       ├──                                 PUT/PATCH   Update table            (authenticated)
│       ├──                                 DELETE      Delete table            (superuser)
│       ├── bills/
│       │   ├──                             GET         List bills              (authenticated; own table active only / superuser gets all)
│       │   ├──                             POST        Create bill             (authenticated; own table only / superuser any)
│       │   └── <public_id>/
│       │       ├──                         GET         Retrieve bill           (authenticated; own table only)
│       │       └──                         PUT/PATCH   Update bill             (superuser)
│       └── orders/
│           ├──                             GET         List orders             (authenticated)
│           ├──                             POST        Create order            (authenticated; not staff-only)
│           └── <public_id>/
│               ├──                         GET         Retrieve order          (authenticated)
│               ├──                         PUT/PATCH   Update order            (authenticated)
│               └──                         DELETE      Delete order            (authenticated)
│
├── bills/
│   ├──                                     GET         List all bills          (superuser)
│   ├──                                     POST        Create bill             (superuser)
│   └── <public_id>/
│       ├──                                 GET         Retrieve bill           (superuser)
│       ├──                                 PUT/PATCH   Update bill             (superuser)
│       ├──                                 DELETE      Delete bill             (superuser)
│       └── orders/
│           ├──                             GET         List orders in bill     (staff)
│           ├──                             POST        Create order in bill    (superuser)
│           └── <public_id>/
│               ├──                         GET         Retrieve order          (staff)
│               ├──                         PUT/PATCH   Update order            (staff)
│               └──                         DELETE      Delete order            (staff)
│
├── menu/
│   ├── categories/
│   │   ├──                                 GET         List categories         (all)
│   │   ├──                                 POST        Create category         (superuser)
│   │   └── <public_id>/
│   │       ├──                             GET         Retrieve category       (all)
│   │       ├──                             PUT/PATCH   Update category         (superuser)
│   │       └──                             DELETE      Delete category         (superuser)
│   └── items/
│       ├──                                 GET         List items              (all)
│       ├──                                 POST        Create item             (superuser)
│       └── <public_id>/
│           ├──                             GET         Retrieve item           (all)
│           ├──                             PATCH       Update availability     (staff)
│           ├──                             PUT         Full update item        (superuser)
│           └──                             DELETE      Delete item             (superuser)
│
└── orders/
    ├──                                     GET         List all orders         (staff)
    ├──                                     POST        Create order            (superuser)
    └── <public_id>/
        ├──                                 GET         Retrieve order          (staff)
        ├──                                 PUT/PATCH   Update order            (staff)
        └──                                 DELETE      Delete order            (staff)
```
## Note: 
`orders/` supports `?status=<status>` query param for filtering.

## Access Levels

|    Level      | Description                                         |
|---------------|-----------------------------------------------------|
|     all       | Any user, including unauthenticated                 |
| authenticated | Any authenticated user (IsAuthenticated)            |
|    staff      | is_staff=True — includes superusers (IsStaffUser)   |
|   superuser   | is_superuser=True (IsSuperUser)                     |