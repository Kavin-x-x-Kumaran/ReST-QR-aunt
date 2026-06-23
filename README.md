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

```
/
├── auth/
│   ├── token/                              POST        Obtain JWT token pair
│   ├── refresh/                            POST        Refresh JWT token
│   └── users/
│       ├──                                 GET         List users              (admin)
│       ├──                                 POST        Create user             (admin)
│       └── <pk>/
│           ├──                             GET         Retrieve user           (admin)
│           ├──                             PUT/PATCH   Update user             (admin)
│           └──                             DELETE      Delete user             (admin)
│
├── tables/
│   ├──                                     GET         List tables             (admin)
│   ├──                                     POST        Create table            (admin)
│   └── <pk>/
│       ├──                                 GET         Retrieve table          (admin)
│       ├──                                 PATCH       Update table            (authenticated)
│       ├──                                 DELETE      Delete table            (admin)
│       ├── bills/
│       │   ├──                             GET         Active bill             (non-admin)
│       │   ├──                             GET         All bills by table      (admin)
│       │   ├──                             POST        Create bill             (authenticated)
│       │   ├──                             PATCH       Update active bill      (non-admin)
│       │   └── <bill_id>
│       │       └──                         GET         Bill by ID+table        (admin)
│       └── orders/
│           ├──                             GET         List orders             (customer)
│           ├──                             POST        Create order            (customer)
│           └── <order_id>/
│               ├──                         PATCH       Update order            (customer)
│               └──                         DELETE      Delete order            (customer)
│
├── bills/
│   ├──                                     GET         List all bills          (admin)
│   └── <bill_id>/
│       ├──                                 GET         Retrieve bill           (admin)
│       ├──                                 PATCH       Update bill             (admin)
│       ├──                                 DELETE      Delete bill             (admin)
│       └── orders/
│           ├──                             GET         List orders in bill     (staff)
│           ├──                             POST        Create order in bill    (staff)
│           └── <order_id>/
│               ├──                         GET         Retrieve order          (staff)
│               ├──                         POST        Update order            (staff)
│               └──                         DELETE      Delete order            (staff)
│
├── categories/
│   ├──                                     GET         List categories         (all)
│   └── <pk>/
│       └──                                 GET         Retrieve category       (all)
│
├── items/
│   ├──                                     GET         List items              (all)
│   └── <pk>/
│       └──                                 GET         Retrieve item           (all)
│
├── kitchen/
│   └── items/<pk>/
│       └──                                 PATCH       Update availability     (staff)
│
├── orders/
│   ├──                                     GET         List all orders         (staff)
│   ├──                                     POST        Create order            (staff)
│   ├── status/<status>/
│   │   └──                                 GET         Filter by status        (staff)
│   └── <order_id>/
│       ├──                                 GET         Retrieve order          (staff)
│       ├──                                 PATCH       Update order            (staff)
│       └──                                 DELETE      Delete order            (staff)
│
└── admin/
    ├── categories/
    │   ├──                                 GET         List categories         (admin)
    │   ├──                                 POST        Create category         (admin)
    │   └── <pk>/
    │       ├──                             GET         Retrieve category       (admin)
    │       └──                             PUT/PATCH   Update category         (admin)
    └── items/
        ├──                                 GET         List items              (admin)
        ├──                                 POST        Create item             (admin)
        └── <pk>/
            ├──                             GET         Retrieve item           (admin)
            └──                             PUT/PATCH   Update item             (admin)
```

## Access Levels

|    Level      | Description              |
|---------------|--------------------------|
|     all       | Any user                 |
| authenticated | Any authenticated user   |
|   customer    | Customer (table-scoped)  |
|    staff      | Kitchen staff and Admin  |
|    admin      | Admin only               |