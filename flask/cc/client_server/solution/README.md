# Models

 - Server
    - **id**   Integer (primary key)
    - **name** String (unique, not null)
 - Message
    - **id**        Integer (primary key)
    - **content**   String (not null)
    - **server_id** Integer (not null)
    - **client_id** Integer (not null)
 - Client
    - **id**   (primary key)
    - **name** (unique, not null)
# Validation

  - Server
    - names must be all upper case letters
  - Message
    - content must not be an empty string
# Routes

  - GET /clients
  - POST /messages
  - POST /servers
  - PATCH /messages/<int:id>
  - DELETE /messages/<int:id>
    

# Response Formats

- GET /clients
    ```json
    [
        {
            id
            name
            servers: [
                {
                    id
                    name
                }
            ]
        }
    ]
    ```
- POST /messages
    ```json
        {
            id
            content
            server: {
                id
                name
            }
            client: {
                id
                name
            }
        }
    ```
- POST /servers
    ```json
        {
            id
            name
    ```
- PATCH /messages/<int:id>
    ```json
        {
            id
            content
        }
    ```