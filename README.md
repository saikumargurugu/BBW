# API Documentation

## Authentication APIs

1. **Token Obtain Pair**
   - **Endpoint**: `/api/token/`
   - **Method**: `POST`
   - **Description**: Obtain a pair of access and refresh tokens.
   - **Request Body**:
     ```json
     {
       "username": "your_username",
       "password": "your_password"
     }
     ```
   - **Response**:
     ```json
     {
       "access": "access_token",
       "refresh": "refresh_token"
     }
     ```

2. **Token Refresh**
   - **Endpoint**: `/api/token/refresh/`
   - **Method**: `POST`
   - **Description**: Refresh the access token using the refresh token.
   - **Request Body**:
     ```json
     {
       "refresh": "refresh_token"
     }
     ```
   - **Response**:
     ```json
     {
       "access": "new_access_token"
     }
     ```

---

## User APIs

- **Base URL**: `/api/auth/`
- **Description**: Includes all user-related APIs (defined in `users.urls`).

---

## Shop APIs

- **Base URL**: `/api/shop/`
- **Description**: Includes all shop-related APIs (defined in `shop.urls`).

### Product APIs

1. **List Products**
   - **Endpoint**: `/api/shop/products/`
   - **Method**: `GET`
   - **Description**: Retrieve a list of all products.

2. **Create Product**
   - **Endpoint**: `/api/shop/products/`
   - **Method**: `POST`
   - **Description**: Create a new product.

3. **Retrieve Product Details**
   - **Endpoint**: `/api/shop/products/<id>/`
   - **Method**: `GET`
   - **Description**: Retrieve details of a specific product.

4. **Update Product**
   - **Endpoint**: `/api/shop/products/<id>/`
   - **Method**: `PUT`
   - **Description**: Update details of a specific product.

5. **Delete Product**
   - **Endpoint**: `/api/shop/products/<id>/`
   - **Method**: `DELETE`
   - **Description**: Delete a specific product.

---

### Brand APIs

1. **List Brands**
   - **Endpoint**: `/api/shop/brands/`
   - **Method**: `GET`
   - **Description**: Retrieve a list of all brands.

2. **Create Brand**
   - **Endpoint**: `/api/shop/brands/`
   - **Method**: `POST`
   - **Description**: Create a new brand.

3. **Retrieve Brand Details**
   - **Endpoint**: `/api/shop/brands/<id>/`
   - **Method**: `GET`
   - **Description**: Retrieve details of a specific brand.

4. **Update Brand**
   - **Endpoint**: `/api/shop/brands/<id>/`
   - **Method**: `PUT`
   - **Description**: Update details of a specific brand.

5. **Delete Brand**
   - **Endpoint**: `/api/shop/brands/<id>/`
   - **Method**: `DELETE`
   - **Description**: Delete a specific brand.

---

### Category APIs

1. **List Categories**
   - **Endpoint**: `/api/shop/categories/`
   - **Method**: `GET`
   - **Description**: Retrieve a list of all categories.

2. **Create Category**
   - **Endpoint**: `/api/shop/categories/`
   - **Method**: `POST`
   - **Description**: Create a new category.

3. **Retrieve Category Details**
   - **Endpoint**: `/api/shop/categories/<id>/`
   - **Method**: `GET`
   - **Description**: Retrieve details of a specific category.

4. **Update Category**
   - **Endpoint**: `/api/shop/categories/<id>/`
   - **Method**: `PUT`
   - **Description**: Update details of a specific category.

5. **Delete Category**
   - **Endpoint**: `/api/shop/categories/<id>/`
   - **Method**: `DELETE`
   - **Description**: Delete a specific category.

---

### Notes

- Replace `<id>` in the endpoints with the actual ID of the resource.
- Use tools like Postman or curl to test these APIs.
- Ensure proper authentication headers are included for protected endpoints.


