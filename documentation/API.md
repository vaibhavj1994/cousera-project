# API Endpoints

## Restaurant Menu API

- **GET** `/api/menu/`
  - **Description**: Retrieve all available menu items.
  - **Access**: Any user.

- **POST** `/api/menu/`
  - **Description**: Add a new menu item.
  - **Access**: Restaurant owner (superuser) only.

- **PUT/DELETE** `/api/menu/<int:pk>/`
  - **Description**: Update or delete a specific menu item.
  - **Access**: Restaurant owner (superuser) only.

## Menu Cart API

- **POST** `/api/cart/menu-items/`
  - **Description**: Add items to the cart by specifying the item and quantity.
  - **Access**: Any user.

- **GET** `/api/cart/menu-items/`
  - **Description**: View the contents of the user's cart.
  - **Access**: Any user.

- **DELETE** `/api/cart/menu-items/`
  - **Description**: Empty the cart.
  - **Access**: Any user.

## Delivery Order API

- **GET** `/api/orders/`
  - **Description**: Retrieve all restaurant orders (for managers).
  - **Access**: Managers.

- **GET** `/api/orders/`
  - **Description**: Retrieve orders assigned to a specific delivery crew (for delivery crew members).
  - **Access**: Delivery crew members.

- **GET** `/api/orders/`
  - **Description**: Retrieve only the user's own orders (for customers).
  - **Access**: Customers.

- **POST** `/api/orders/`
  - **Description**: Place a new order and automatically clear the cart.
  - **Access**: Any user.

- **PUT** `/api/orders/<int:pk>/`
  - **Description**: Assign an order to a delivery crew member.
  - **Access**: Managers.

- **PUT** `/api/orders/<int:pk>/`
  - **Description**: Update the status of an order (completed, in progress).
  - **Access**: Managers or delivery crew responsible for the order.

- **DELETE** `/api/orders/<int:pk>/`
  - **Description**: Delete an order.
  - **Access**: Managers.

## Table Booking API

- **GET** `/api/booking/tables`
  - **Description**: View all table bookings in the restaurant.
  - **Access**: Managers.

## Delivery Crew Staffing API

- **POST** `/api/groups/delivery-crew/users/`
  - **Description**: Hire a new delivery crew member.
  - **Access**: Managers.

- **DELETE** `/api/groups/delivery-crew/users/<int:userId>/`
  - **Description**: Fire a delivery crew member.
  - **Access**: Managers.

## Manager Staffing API

- **POST** `/api/groups/manager/users/`
  - **Description**: Hire a new manager.
  - **Access**: Restaurant owner (superuser).

- **DELETE** `/api/groups/manager/users/<int:userId>/`
  - **Description**: Fire a manager.
  - **Access**: Restaurant owner (superuser).

<br>

**Note**: [User Roles](./Users.md) contains a list of users with different roles (Owner, Manager, Delivery Crew, Customer). Ensure that the roles are assigned correctly to access the respective endpoints.
