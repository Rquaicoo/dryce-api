

# API reference for Dryce

Dryce is a mobile application that allows its users to send laundry request through a vendor.
A vendor can be registered through our web application.




## Installation

Clone the project with git

```bash
  git clone https://github.com/Rquaicoo/dryce-api.git
```

## Run locally
to start the project, go to the project directory

```bash
cd dryce
```
Install dependencies

```bash
pip install -r requirements.txt
```
Start the server
```bash
pyhton manage.py runserver

```

The app starts by default at port 8000
to run at a custom port, run:
```cmd
python manage.py runserver [specify port number]
```









## API Reference

#### Get all items in cart

```http
  GET /api/cart
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `token` | `string` | **Required**. Your auth token |


#### Create a cart
```http
  POST /api/cart
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `token` | `string` | **Required**. Your auth token |
| `shirts `| `int` | **Required**. Number of shirts |
| `dresses `| `int` | **Required**. Number of dresses |
| `trousers `| `int` | **Required**. Number of trousers |
| `cardigans `| `int` | **Required**. Number of cardigans |
| `jeans `| `int` | **Required**. Number of jeans |
| `blouses `| `int` | **Required**. Number of blouses |

#### Update a cart
```http
  PUT /api/cart
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `token` | `string` | **Required**. Your auth token |
| `shirts `| `int` | **Required**. Number of shirts |
| `dresses `| `int` | **Required**. Number of dresses |
| `trousers `| `int` | **Required**. Number of trousers |
| `cardigans `| `int` | **Required**. Number of cardigans |
| `jeans `| `int` | **Required**. Number of jeans |
| `blouses `| `int` | **Required**. Number of blouses |
#### Get order

```http
  GET /api/items/${id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of item to fetch |
|`token`    | `string` | **Required**. Your authentication token|

#### Create user

```http
  POST /api/auth/register/
```

#### Login user

```http
  POST /api/auth/login/
```

#### Validate email

```http
  POST /api/auth/Validate_email/
```

#### Validate username

```http
  POST /api/auth/Validate_username/
```

#### Logout user

```http
  POST /api/auth/logout/
```

#### Reset password

```http
  GET /api/cart
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `token` | `string` | **Required**. Your auth token |
| `otp`   | `string` | **Required**. An otp send to the email |




